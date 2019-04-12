## About
* Extracts meetings transcript and summary from [AMI Corpus](http://groups.inf.ed.ac.uk/ami/download/)
* Transforms into CNN-DailyMail News dataset (`.story` files with article and highlight in it)

#### Contents
[AMI Corpus](#ami-corpus-info) • [Story Dataset](#story-dataset) • [How to Make](#how-to-make) 
        
## AMI Corpus info
* Number of meetings (including scenario and non-scenario): 171
    * Number of speakers per meeting: 4-5
    * Total number of transcripts: 687
* Number of summaries: 142
    * Abstract info is only available for meetings with names starting with *ES*, *IS* and *TS*

## Story Dataset
Already made `.story` dataset has been provided under `data/ami-transcripts-stories/`

## How to Make
Make dataset from scratch: download AMI Corpus and extract `.story` files
```
python main_extract_meeting_text.py
```

#### Configuration options

| **Argument**                      | **Type** | **Default**                         | **Required?** |
|-----------------------------------|----------|-------------------------------------|---------------|
| `ami_xml_dir`                     | string   | `"data/"`                         | No            |
| `results_transcripts_speaker_dir` | string   | `"data/ami-transcripts-speaker/"` | No            |
| `results_transcripts_dir`         | string   | `"data/ami-transcript/"`          | No            |
| `results_summary_dir`             | string   | `"data/ami-summary/"`             | No            |
+ `ami_xml_dir` is the directory where the AMI Corpus will be downloaded
+ `results_transcripts_speaker_dir` is the directory where each speaker's transcript will be saved 
+ `results_transcripts_dir` is the directory where each meeting's transcript will be saved
+ `results_summary_dir` is the directory where each meeting's summary will be saved

#### AMI Corpus final output structure

        assets
        +-- ami-summary 
        +-- ami-transcripts-speaker
        +-- ami-transcripts-speaker-stories
        +-- ami-transcripts-stories
        +-- ami_public_manual_1.6.2
        |   +-- abstractive
        |   ...
        |   +-- words
        |   ...

## Credit/Requirements
* Tested on Ubuntu 16.04, Python 3.6
* Minidom vs Element Tree: [Reading XML files in Python](http://stackabuse.com/reading-and-writing-xml-files-in-python/)
* Minidom: XML parser for Python

## TODO
* Overlapping meeting transcript
* Decision abstract
