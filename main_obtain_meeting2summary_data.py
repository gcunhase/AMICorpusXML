
import argparse
import utils
from AMICorpusHandler import AMICorpusHandler

""" Main file that call AMICorpusHandler to extract transcripts, abstractive and extractive summaries.
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts transcript and summary from AMI Corpus.')
    parser.add_argument('--summary_type', type=str, default=utils.ABSTRACTIVE_SUMMARY_TAG,
                        help='Type of summary to be extracted. Options=["{}", "{}"].'.
                        format(utils.ABSTRACTIVE_SUMMARY_TAG, utils.EXTRACTIVE_SUMMARY_TAG))
    # parser.add_argument('--ami_xml_dir', type=str, default=os.path.join(project_dir, 'data/'),
    parser.add_argument('--ami_xml_dir', type=str, default='data/',
                        help='AMI Corpus download directory')
    parser.add_argument('--results_transcripts_speaker_dir', type=str,
                        # default=os.path.join(project_dir, 'data/ami-transcripts-speaker/'),
                        default='data/ami-transcripts-speaker/',
                        help='AMI Corpus transcripts per speaker')
    parser.add_argument('--results_transcripts_dir', type=str,
                        # default=os.path.join(project_dir, 'data/ami-transcripts/'),
                        default='data/ami-transcripts/',
                        help='AMI Corpus transcripts')
    parser.add_argument('--results_summary_dir', type=str,
                        # default=os.path.join(project_dir, 'data/ami-summary/'),
                        default='data/ami-summary/',
                        help='AMI Corpus summaries')
    args = parser.parse_args()

    # 1. Downloads original AMI Corpus and saves in `data/ami_public_manual_1.6.2`
    amiCorpusHandler = AMICorpusHandler(args)

    # 2. Extract transcript for each subject (words/*.xml -> meeting transcripts)
    amiCorpusHandler.extract_transcript(do_transcripts_speaker=True)

    # 3. Extract summary
    if args.summary_type == utils.ABSTRACTIVE_SUMMARY_TAG:
        amiCorpusHandler.extract_abstractive_summary()
    else:  # extractive
        amiCorpusHandler.extract_extractive_summary()

    # 4. Make .story files as in CNN-DailyMail News Dataset
    #   A. For all speakers at once
    amiCorpusHandler.transform_to_story()
    #   B. For each speaker individually. Different transcript, same summary.
    amiCorpusHandler.transform_to_story(is_speaker_transcript=True)
