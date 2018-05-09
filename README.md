## About
* Extracts meetings transcript and summary from [AMI Corpus](http://groups.inf.ed.ac.uk/ami/download/)
   * Number of meetings (including scenario and non-scenario): 171
        * Number of speakers per meeting: 4-5
        * Total number of transcripts: 687
   * Number of summaries: 142
        * Information is not available for *EN* meeting, only *ES*, *IS*, *TS* meetings

* Transforms into CNN-DailyMail News dataset (*.story* files with article and highlight in it)

## Code
* Configuration options:
  
    | **Argument**                      | **Type** | **Default**                         | **Required?** |
    |-----------------------------------|----------|-------------------------------------|---------------|
    | `ami_xml_dir`                     | string   | `"assets/"`                         | No            |
    | `results_transcripts_speaker_dir` | string   | `"assets/ami-transcripts-speaker/"` | No            |
    | `results_transcripts_dir`         | string   | `"assets/ami-transcript/"`          | No            |
    | `results_summary_dir`             | string   | `"assets/ami-summary/"`             | No            |

    + `ami_xml_dir` is the directory where the AMI Corpus will be downloaded
    + `results_transcripts_speaker_dir` is the directory where each speaker's transcript will be saved 
    + `results_transcripts_dir` is the directory where each meeting's transcript will be saved
    + `results_summary_dir` is the directory where each meeting's summary will be saved

* AMI Corpus final results:

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
* Minidom vs Element Tree: [Reading XML files in Python](http://stackabuse.com/reading-and-writing-xml-files-in-python/)
* Minidom: XML parser for Python
* OS: Ubuntu 16.04
