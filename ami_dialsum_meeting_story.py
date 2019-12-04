import argparse
import os
import nltk

__author__ = "Gwena Cunha"

"""
    DialSum paper uses a modification of the AMI Meeting Corpus:
        - train/test/valid split is available in different directories
        - Original files format: file `in` with input and file `sum` with summaries, 1 per line
        - Needed for comparison
        - Paper: https://www.csie.ntu.edu.tw/~yvchen/doc/SLT18_DialSum.pdf
        - Code: https://github.com/MiuLab/DialSum
        
    Objective of this code:
        - Convert AMI_DialSum data to CNN-DailyMail News Dataset story format
        - Resulting files: *.story
    
    Code based on my previous code: https://github.com/gcunhase/AMICorpusXML
"""


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def transform_to_story(args, sent_detector):
    """ Transform AMI Corpus into CNN-DailyMail News Dataset story format
    """
    print("Make .story files")
    data_dir = args.ami_dialsum_data_dir
    results_dir = args.results_story_dir

    for data_type in ['train', 'test', 'valid']:
        # Open in (meeting transcript) and sum (summary) files
        in_lines = open(data_dir + data_type + '/' + args.input_filename).readlines()
        sum_lines = open(data_dir + data_type + '/' + args.summary_filename).readlines()

        # Ensure results directory with train/test/valid directories exists
        results_dir_data_type = results_dir + data_type
        ensure_dir(results_dir_data_type)

        for i, (in_line, sum_line) in enumerate(zip(in_lines, sum_lines)):
            print(i)
            story_filename = '/in_{}.story'.format(i)
            story_file = open(results_dir_data_type + story_filename, 'w')

            # Write transcript
            story_file.write('{}\n'.format(in_line))

            # Separate summary into sentences
            sentences = sent_detector.tokenize(sum_line.strip())
            for sent in sentences:
                story_file.write('\n\n@highlight\n\n{}'.format(sent))
            story_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts file to .story')
    parser.add_argument('--ami_dialsum_data_dir', type=str, default='data/ami_dialsum_corpus/',
                        help='AMI DialSum Corpus directory')
    parser.add_argument('--input_filename', type=str, default='in',
                        help='AMI DialSum Corpus input filename')
    parser.add_argument('--summary_filename', type=str, default='sum',
                        help='AMI DialSum Corpus summary (target) filename')
    parser.add_argument('--results_story_dir', type=str,
                        default='data/ami_dialsum_corpus_stories/',
                        help='AMI Corpus .story files')
    args = parser.parse_args()

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    transform_to_story(args, sent_detector)
