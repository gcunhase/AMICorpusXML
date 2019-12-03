
from xml.dom import minidom
import utils
import os
import urllib.request
import zipfile
from collections import defaultdict
import nltk.data

__author__ = "Gwena Cunha"

"""
    Handler for AMI Corpus
    
    Functions:
        1. Extract transcripts
        2. Abstractive summary
        3. Extractive summary
        4. (Optional) Formatting: .TXT file to .STORY file
        
    Parses XML in Python using minidom
"""


class AMICorpusHandler:
    def __init__(self, args, in_file_ext='xml', out_file_ext='txt'):
        self.args = args
        self.in_file_ext = in_file_ext
        self.out_file_ext = out_file_ext

        self.ami_dir = self.args.ami_xml_dir + 'ami_public_manual_1.6.2'
        self.download_corpus()
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    def download_corpus(self):
        """ Check if AMI Corpus exists and only download it if it doesn't

        :return: directory where AMI Corpus is located
        """
        download_link = 'http://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip'
        # directory = os.path.dirname(self.ami_dir)
        if not os.path.exists(self.ami_dir):
            # 1. Ensure data directory exists
            utils.ensure_dir(self.args.ami_xml_dir)
            # 2. Download AMI Corpus
            print("Downloading AMI Corpus to: {}".format(self.ami_dir))
            zipped_ami_filename = self.ami_dir + '.zip'
            urllib.request.urlretrieve(download_link, zipped_ami_filename)
            # 3. Unzip zip file
            zip_ref = zipfile.ZipFile(zipped_ami_filename, 'r')
            zip_ref.extractall(self.ami_dir)
            zip_ref.close()
            # 4. Delete zip file
            os.remove(zipped_ami_filename)
        else:
            print("AMI Corpus has already been downloaded in: {}".format(self.ami_dir))

    def get_corpus_directory(self):
        return self.ami_dir

    """ Begin 1/4: EXTRACT TRANSCRIPT     """
    def extract_transcript(self, do_transcripts_speaker=True):
        """ Extracts transcript for each speaker (if boolean var is True) and also for the entire meeting,
        where each transcript is a line in a new text file.

            Summaries are originally saved in `data/ami_public_manual_1.6.2/words/`:
              * Example: `EN2001a.A.words.xml`
              * Meeting name: `EN2001`
              * Meetings are divided into 1 hour parts: `a` (each hour is a consecutive lowercase letter)
              * Speaker: `A` (usually there are four speakers named A, B, C and D, but E is sometimes also present)
            Each `.xml` file has a number of tags with the words and their respective times in the audio/video file.
             In order for us to extract the summaries, we have to put those words back together in sentences and paragraphs.
             Thus xml parsing is required.

            Output: 2 folders with corresponding .txt files
              * `data/ami-transcripts-speaker/`: meeting transcripts for each speaker
              * `data/ami-transcripts/`: complete meeting transcripts (all speakers together)

        :param do_transcripts_speaker: boolean to indicate if speaker transcription is needed
        :return:
        """
        if do_transcripts_speaker:
            self.extract_transcript_speaker()

        print("\nSaving transcripts in: {}".format(self.args.results_transcripts_dir))
        # Get every file
        transcript_speaker_dir = self.args.results_transcripts_speaker_dir
        transcript_speaker_files = [f for f in os.listdir(transcript_speaker_dir) if f.endswith('.{}'.format(self.out_file_ext))]

        # Group speaker files by meeting
        group_speaker_files = defaultdict(list)
        for t in transcript_speaker_files:
            meeting = t.split('.')[0]
            if bool(group_speaker_files[meeting]):
                group_speaker_files[meeting].append(t)
            else:
                group_speaker_files[meeting] = [t]

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
        print("Number of meetings: {}".format(len(group_speaker_files.keys())))

    def extract_transcript_speaker(self):
        """ Extracts transcript from each speaker (A, B, C, D, and sometimes E)
        """
        print("Extracting speaker transcripts to: {}".format(self.args.results_transcripts_speaker_dir))

        words_dir = self.ami_dir + '/words/'
        utils.ensure_dir(self.args.results_transcripts_speaker_dir)
        words_files = [f for f in os.listdir(words_dir) if f.endswith('.{}'.format(self.in_file_ext))]
        for words_filename in words_files:
            # print("Extracting transcript from {}".format(words_filename))
            self.extract_transcript_single_file(words_dir, words_filename)
        print("Transcripts: {}".format(len(words_files)))

    def extract_transcript_single_file(self, words_dir, filename):
        """ Extract transcript for a single .xml file

        :param words_dir: directory containing .xml files with meeting transcription
        :param filename: name of each .xml meeting file
        :return:
        """
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
        results_filename = filename.split('.words.{}'.format(self.in_file_ext))[0] + '.transcript.{}'.format(self.out_file_ext)
        self.save_file(transcript, self.args.results_transcripts_speaker_dir, results_filename)
        return transcript
    """ End: EXTRACT TRANSCRIPT     """

    """ Begin 2/4: ABSTRACTIVE SUMMARY     """
    def extract_abstractive_summary(self):
        """ Obtain abstractive summary from each meeting
              * Located in `data/ami_public_manual_1.6.2/abstractive/*.xml`
        """
        print("\nObtaining abstractive summaries to: {}".format(self.args.results_summary_dir))
        sum_dir = self.ami_dir + '/abstractive/'
        sum_files = [f for f in os.listdir(sum_dir) if f.endswith('.{}'.format(self.in_file_ext))]
        utils.ensure_dir(self.args.results_summary_dir)

        # Obtain summary with only 1 sentence/highlight
        results_abstractive_summary_dir = '{}/{}-one_highlight/'.format(self.args.results_summary_dir,
                                                                        utils.ABSTRACTIVE_SUMMARY_TAG)
        for sum_filename in sum_files:
            self.extract_abstractive_summary_single_file_single_highlight(sum_dir, sum_filename, results_abstractive_summary_dir)

        # Obtain summary with only all available sentences/highlights
        results_abstractive_summary_dir = '{}/{}/'.format(self.args.results_summary_dir, utils.ABSTRACTIVE_SUMMARY_TAG)
        for sum_filename in sum_files:
            self.extract_abstractive_summary_single_file(sum_dir, sum_filename, results_abstractive_summary_dir)

    def extract_abstractive_summary_single_file_single_highlight(self, summary_dir, summary_filename, results_dir):
        """ Obtain abstractive summary (1 sentence/highlight) from one meeting (one file)
              * Extract text between `abstract` tag
              * Return first element inside this tag

        :param summary_dir: directory containing .xml files with meeting abstract/summary
        :param summary_filename: name of each summary file
        :param results_dir: directory to save .txt files with summaries
        :return:
        """
        # parse an xml file by name
        mydoc = minidom.parse(summary_dir + summary_filename)
        items = mydoc.getElementsByTagName('abstract')
        summary = items[0].firstChild.nextSibling.firstChild.data

        # Save summary
        # results_dir = self.args.results_summary_dir
        results_filename = summary_filename.replace('.{}'.format(self.in_file_ext), '.{}'.format(self.out_file_ext))
        #  summary_filename.split('.{}'.format(self.in_file_ext))[0] + '.summary.txt'  # '.summary.txt'
        self.save_file(summary, results_dir, results_filename)

        return summary

    def extract_abstractive_summary_single_file(self, summary_dir, summary_filename, results_dir):
        """ Obtain abstractive summary (ALL sentences/highlights) from one meeting (one file)
              * Extract text between `abstract` tag
              * Text between `abstract` tag is composed of text in `sentence` tags
              * Return all these tags as a paragraph

        :param summary_dir: directory containing .xml files with meeting abstract/summary
        :param summary_filename: name of each summary file
        :param results_dir: directory to save .txt files with summaries
        :return:
        """
        # parse an xml file by name
        mydoc = minidom.parse(summary_dir + summary_filename)
        items = mydoc.getElementsByTagName('abstract')
        items_sentences = items[0].getElementsByTagName('sentence')
        summary = ''
        for item in items_sentences:
            summary += item.firstChild.data + ' '

        # Save summary
        # results_dir = self.args.results_summary_dir
        results_filename = summary_filename.replace('.{}'.format(self.in_file_ext), '.{}'.format(self.out_file_ext))
        #  summary_filename.split('.{}'.format(self.in_file_ext))[0] + '.summary.txt'  # '.summary.txt'
        self.save_file(summary, results_dir, results_filename)

        return summary
    """ End: ABSTRACTIVE SUMMARY     """

    """ Begin 3/4: EXTRACTIVE SUMMARY     """
    def extract_extractive_summary(self):
        """ Extract summary from each meeting
              * Located in `data/ami_public_manual_1.6.2/extractive/*.xml`
        """
        print("\nObtaining extractive summaries to: {}".format(self.args.results_summary_dir))
        sum_dir = self.ami_dir + '/extractive/'
        utils.ensure_dir(self.args.results_summary_dir)
        results_extractive_summary_dir = '{}/{}/'.format(self.args.results_summary_dir, utils.EXTRACTIVE_SUMMARY_TAG)
        sum_files = [f for f in os.listdir(sum_dir) if f.endswith('.extsumm.{}'.format(self.in_file_ext))]
        for sum_filename in sum_files:
            self.extract_extractive_summary_single_file(sum_dir, sum_filename, results_extractive_summary_dir)
        print("Summaries: {}".format(len(sum_files)))

    def extract_extractive_summary_single_file(self, summary_dir, summary_filename, results_dir):
        """ Obtain extractive summary (ALL sentences/highlights) from one meeting (one file)
              * Extract text between `extsumm` tag
              * Text between `extsumm` tag is composed of children nodes such as the below example:
                * `<nite:child href="ES2002a.B.dialog-act.xml#id(ES2002a.B.dialog-act.dharshi.3)"/>`
                * This node refers to a a node of ID `ES2002a.B.dialog-act.dharshi.3` in a file named `ES2002a.B.dialog-act.xml` in `data/dialogueActs/`
                * This ID is:
                ```
                <dact nite:id="ES2002a.B.dialog-act.dharshi.3" reflexivity="true">
                    <nite:pointer role="da-aspect"  href="da-types.xml#id(ami_da_4)"/>
                    <nite:child href="ES2002a.B.words.xml#id(ES2002a.B.words4)..id(ES2002a.B.words16)"/>
                </dact>
                ```
                * This indicates words 4 to 16 in `ES2002a.B.words.xml`
              * Return all the collected words as a paragraph

        :param summary_dir: directory containing .xml files with meeting abstract/summary
        :param summary_filename: name of each summary file
        :param results_dir: directory to save .txt files with summaries
        :return:
        """
        # parse an xml file by name
        mydoc = minidom.parse(summary_dir + summary_filename)
        mydoc = mydoc.childNodes[0].childNodes[1]  # getElementsByTagName('extsumm')
        items_extsumm = mydoc.childNodes
        summary = ""
        for items_ext in items_extsumm:
            if items_ext.attributes is not None:  # Element
                filename, init_id, final_id = self.obtain_ids(items_ext)
                summary += self.obtain_dialogue_act_node_references(filename, init_id, final_id)

        # Save summary
        # results_dir = self.args.results_summary_dir
        results_filename = summary_filename.replace('.{}'.format(self.in_file_ext), '.{}'.format(self.out_file_ext))
        self.save_file(summary, results_dir, results_filename)

        return summary

    def obtain_dialogue_act_node_references(self, filename, init_id, final_id):
        """ Obtain node references from extractive summary file

        :param filename:
        :param init_id: initial ID for extractive summary
        :param final_id: final ID for extractive summary
        :return:
        """
        sum_dir = self.ami_dir + '/dialogueActs/'

        # Obtain array with dialogAct IDs
        print(init_id)
        id_arr = [init_id]
        if final_id is not None:
            init_id_index = int(init_id.split('dialog-act.')[-1].split('.')[-1])
            final_id_index = int(final_id.split('dialog-act.')[-1].split('.')[-1])
            root_name = final_id.split(str(final_id_index))[0]
            for i in range(init_id_index+1, final_id_index+1):
                id_arr.append(root_name + str(i))

        # parse an xml file by name
        segment_nodes = self.obtain_node_from_textname(sum_dir + filename, id_arr, tag='dact')

        words = self.obtain_dialogue_act_node(segment_nodes)
        return words

    def obtain_dialogue_act_node(self, segment_nodes):
        """ Obtain nodes from references and word references in node.

        :param segment_nodes: nodes representing segment
        :return:
        """
        sum_dir = self.ami_dir + '/words/'

        sentence_segment = ""
        for segment_node in segment_nodes:
            # Obtain child node with words information
            for seg in segment_node.childNodes:
                if seg.attributes is not None:
                    if seg.nodeName == 'nite:child':
                        items_extsumm = seg  # segment_node.childNodes[3]  # Element

            filename, init_id, final_id = self.obtain_ids(items_extsumm)

            # Obtain array with words IDs
            id_arr = [init_id]
            if final_id is not None:
                init_id_index = int(init_id.split('words')[-1])
                final_id_index = int(final_id.split('words')[-1])
                root_name = final_id.split(str(final_id_index))[0]
                for i in range(init_id_index + 1, final_id_index + 1):
                    id_arr.append(root_name + str(i))

            # parse an xml file by name
            word_nodes = self.obtain_node_from_textname(sum_dir + filename, id_arr, tag='w')

            sentence_segment += self.obtain_dialogue_act_word_references(word_nodes)

        return sentence_segment

    def obtain_dialogue_act_word_references(self, word_nodes):
        """ Obtain words from word references

        :param word_nodes: nodes representing words
        :return: string with concatenated words
        """
        words = ""

        for word_node in word_nodes:
            words += word_node.firstChild.data + " "

        return words

    def obtain_ids(self, items_ext):
        href = items_ext.getAttribute('href')
        filename = href.split('#')[0]
        id_tmp = href.split('#')[-1].split(')..id(')
        init_id = id_tmp[0].split('id(')[-1].split(')')[0]
        final_id = None
        if len(id_tmp) > 1:
            final_id = id_tmp[1].split(')')[0]
        return filename, init_id, final_id

    def obtain_node_from_textname(self, path, id_arr, tag):
        mydoc = minidom.parse(path)
        items_dact = mydoc.getElementsByTagName(tag)
        nodes = []
        for item in items_dact:
            nite_id = item.getAttribute('nite:id')
            if nite_id in id_arr:
                nodes.append(item)
        return nodes
    """ End: EXTRACTIVE SUMMARY     """

    """ Begin 4/4: FORMAT SUMMARY INTO .STORY     """
    def check_for_meeting_summary(self, meeting_name, summary_files):
        """ Check if summary exists for a certain meeting

        :param meeting_name: prefix indicating meeting name
        :param summary_files: existing summary files
        :return:
        """
        for s in summary_files:
            if meeting_name in s:
                return s
        return None

    def transform_to_story(self, is_speaker_transcript=False):
        """ Transform AMI Corpus into CNN-DailyMail News Dataset story format

        :param is_speaker_transcript: boolean indicating if transcripts are from each speaker or of all together.
          True means each speaker will have their own file. In this case, each speaker will have a different transcript
          but the same summary.
        :return:
        """
        print("Make .story files")
        if is_speaker_transcript:
            transcript_dir = self.args.results_transcripts_speaker_dir
        else:
            transcript_dir = self.args.results_transcripts_dir
        transcript_files = [f for f in os.listdir(transcript_dir) if f.endswith('.{}'.format(self.out_file_ext))]

        summary_dir = self.args.results_summary_dir + self.args.summary_type + '/'  #'abstractive-test/'
        summary_files = [f for f in os.listdir(summary_dir) if f.endswith('.{}'.format(self.out_file_ext))]

        story_dir = utils.get_new_data_dir_name(transcript_dir, '-stories')
        utils.ensure_dir(story_dir)
        story_dir += self.args.summary_type + '/'
        utils.ensure_dir(story_dir)
        for t in transcript_files:
            # Check if meeting transcript exists
            meeting_name = t.split('.')[0]
            # print(meeting_name)
            s = self.check_for_meeting_summary(meeting_name, summary_files)
            if s is not None:
                if is_speaker_transcript:
                    speaker_letter = t.split('.')[1]
                    story_filename = '{}_{}.story'.format(meeting_name, speaker_letter)
                else:
                    story_filename = '{}.story'.format(meeting_name)

                summary = open(summary_dir+s, 'r').read()
                transcript = open(transcript_dir+t, 'r').read()
                story_file = open(story_dir+story_filename, 'w')

                # Separate summary into sentences
                sentences = self.sent_detector.tokenize(summary.strip())
                story_file.write('{}\n'.format(transcript))
                for sent in sentences:
                    story_file.write('\n\n@highlight\n\n{}'.format(sent))
                story_file.close()
    """ End: FORMAT SUMMARY INTO .STORY     """

    def save_file(self, text, dir, filename):
        utils.ensure_dir(dir)
        file = open(dir + filename, 'w')
        file.write(text)
        file.close()
