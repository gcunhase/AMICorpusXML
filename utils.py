
import os


ABSTRACTIVE_SUMMARY_TAG = 'abstractive'
EXTRACTIVE_SUMMARY_TAG = 'extractive'


def project_dir_name():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    return current_dir


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_new_data_dir_name(data_dir, extension):
    data_dir_split = data_dir.split("/")
    new_data_dir = ""
    for i in range(0, len(data_dir_split)-2):
        new_data_dir = new_data_dir+data_dir_split[i]+"/"
    new_data_dir = new_data_dir+data_dir_split[max(0, len(data_dir_split)-2)]+extension+"/"
    # print("New data_dir: "+new_data_dir)
    return new_data_dir
