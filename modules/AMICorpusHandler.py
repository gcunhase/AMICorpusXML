
from xml.dom import minidom
from modules import utils
import os
import urllib.request
import zipfile
from collections import defaultdict

__author__ = "Gwena Cunha"

"""

"""


class AMICorpusHandler:
    def __init__(self, args, in_file_ext='xml'):
        self.args = args
        self.in_file_ext = in_file_ext

        self.ami_dir = self.args.ami_xml_dir + 'ami_public_manual_1.6.2/'
        self.download_corpus()

    def download_corpus(self):
        """ Check if AMI Corpus exists and only download it if it doesn't

        :return: directory where AMI Corpus is located
        """
        download_link = 'http://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip'
        directory = os.path.dirname(self.ami_dir)
        if not os.path.exists(directory):
            print("Downloading AMI Corpus to: {}".format(self.ami_dir))
            zipped_ami_filename = self.ami_dir + '.zip'
            urllib.request.urlretrieve(download_link, zipped_ami_filename)
            # Unzip zip file
            zip_ref = zipfile.ZipFile(zipped_ami_filename, 'r')
            zip_ref.extractall(self.ami_dir)
            zip_ref.close()
            # Delete zip file
            os.remove(zipped_ami_filename)
        else:
            print("AMI Corpus has already been downloaded in: {}".format(self.ami_dir))

    def get_corpus_directory(self):
        return self.ami_dir

    def extract_transcript(self, do_transcripts_speaker=True):
        """ Extracts transcript for each speaker and also for the entire meeting, where each transcript is a line in a
        new text file
        """
        print("\nSaving transcripts in: {}".format(self.args.results_transcripts_dir))

        if do_transcripts_speaker:
            self.extract_transcript_speaker()

        # Get every file
        transcript_speaker_dir = self.args.results_transcripts_speaker_dir
        transcript_speaker_files = [f for f in os.listdir(transcript_speaker_dir) if f.endswith('.txt')]

        # Group speaker files by meeting
        group_speaker_files = defaultdict(list)
        for t in transcript_speaker_files:
            meeting = t.split('.')[0]
            if bool(group_speaker_files[meeting]):
                group_speaker_files[meeting].append(t)
            else:
                group_speaker_files[meeting] = [t]

        # print(group_speaker_files)

        # Directory to save meetings transcripts
        transcript_dir = self.args.results_transcripts_dir
        utils.ensure_dir(transcript_dir)

        # Group transcripts by meeting
        for key in group_speaker_files.keys():
            # print(group_speaker_files[key])
            transcript_filename = '{}.transcript.txt'.format(key)
            all_transcripts_file = open(transcript_dir + transcript_filename, 'w')

            transcript_speakers_filename = group_speaker_files[key]
            for transcript_filename in transcript_speakers_filename:
                file_content = open(transcript_speaker_dir + transcript_filename, 'r').read()
                all_transcripts_file.write(file_content + '\n')

            all_transcripts_file.close()

    def extract_transcript_speaker(self):
        """ Extracts transcript from each speaker (A, B, C, D, and sometimes E)
        """
        print("Extracting speaker transcripts to: {}".format(self.args.results_transcripts_speaker_dir))

        words_dir = self.ami_dir + 'words/'
        utils.ensure_dir(self.args.results_transcripts_speaker_dir)
        words_files = [f for f in os.listdir(words_dir) if f.endswith('.{}'.format(self.in_file_ext))]
        for words_filename in words_files:
            # print("Extracting transcript from {}".format(words_filename))
            self.extract_transcript_single_file(words_dir, words_filename)
        print("Transcripts: {}".format(len(words_files)))

    def extract_transcript_single_file(self, words_dir, filename):
        # parse an xml file by name
        mydoc = minidom.parse(words_dir + filename)

        items = mydoc.getElementsByTagName('w')

        transcript = ""
        count = 0
        for elem in items:
            elem_text = elem.firstChild.data
            if count > 0 and not elem.hasAttribute('punc'):
                transcript += " "
            transcript += elem_text

            count += 1
        # transcript += '\n'

        # Save transcript
        results_filename = filename.split('.words.{}'.format(self.in_file_ext))[0] + '.transcript.txt'
        self.save_file(transcript, self.args.results_transcripts_speaker_dir, results_filename)
        return transcript

    def extract_summary(self):
        print("\nExtracting summaries to: {}".format(self.args.results_summary_dir))
        sum_dir = self.ami_dir + 'abstractive/'
        utils.ensure_dir(self.args.results_summary_dir)
        sum_files = [f for f in os.listdir(sum_dir) if f.endswith('.{}'.format(self.in_file_ext))]
        for sum_filename in sum_files:
            # print("Extracting summary from {}".format(sum_filename))
            self.extract_summary_single_file(sum_dir, sum_filename)
        print("Summaries: {}".format(len(sum_files)))

    def extract_summary_single_file(self, summary_dir, summary_filename):
        # parse an xml file by name
        mydoc = minidom.parse(summary_dir + summary_filename)
        items = mydoc.getElementsByTagName('abstract')
        summary = items[0].firstChild.nextSibling.firstChild.data

        # Save summary
        results_dir = self.args.results_summary_dir
        results_filename = summary_filename.replace('.{}'.format(self.in_file_ext), '.txt')
        #  summary_filename.split('.{}'.format(self.in_file_ext))[0] + '.summary.txt'  # '.summary.txt'
        self.save_file(summary, results_dir, results_filename)

        return summary

    def save_file(self, text, dir, filename):
        utils.ensure_dir(dir)
        file = open(dir + filename, 'w')
        file.write(text)
        file.close()

