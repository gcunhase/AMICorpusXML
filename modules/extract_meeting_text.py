
import argparse
from modules import utils
from modules. AMICorpusHandler import AMICorpusHandler


""" Module to parse XML in Python using minidom
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts transcript and summary from AMI Corpus.')
    parser.add_argument('--ami_xml_dir', type=str, default=utils.project_dir_name()+'assets/',
                        help='AMI Corpus download directory')
    parser.add_argument('--results_transcripts_speaker_dir', type=str,
                        default=utils.project_dir_name()+'assets/ami-transcripts-speaker/',
                        help='AMI Corpus transcripts per speaker')
    parser.add_argument('--results_transcripts_dir', type=str,
                        default=utils.project_dir_name()+'assets/ami-transcripts/',
                        help='AMI Corpus transcripts')
    parser.add_argument('--results_summary_dir', type=str,
                        default=utils.project_dir_name() + 'assets/ami-summary/',
                        help='AMI Corpus summaries')
    args = parser.parse_args()

    # print(args.ami_xml_dir)

    amiCorpusHandler = AMICorpusHandler(args)
    corpus_dir = amiCorpusHandler.get_corpus_directory()

    # Extract transcript for each subject
    amiCorpusHandler.extract_transcript(do_transcripts_speaker=True)

    # Extract summary
    amiCorpusHandler.extract_summary()
