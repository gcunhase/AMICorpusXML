[![DOI](https://zenodo.org/badge/132586686.svg)](https://zenodo.org/badge/latestdoi/132586686)

## About
* Extracts meetings transcript and summary from [AMI Meeting Corpus](http://groups.inf.ed.ac.uk/ami/download/): extractive and abstractive
* Transforms into CNN-DailyMail News dataset (`.story` files with article and highlight in it)

### Contents
[Requirements](#requirements) • [About AMI Meeting Corpus](#ami-corpus) • [How to Use](#how-to-use) • [How to Cite](#acknowledgement) 
        
## Requirements
Tested on Python 3.6+, Ubuntu 16.04, Mac OS

`pip install -r requirements.txt`

## AMI Meeting Corpus
* [More info](http://groups.inf.ed.ac.uk/ami/download/)
* Number of meetings (including scenario and non-scenario): 171
    * Number of speakers per meeting: 4-5
    * Total number of transcripts: 687
* Number of summaries: 142 (abstractive) and 137 (extractive)
    * Only available for meetings with names starting with *ES*, *IS* and *TS*
    
## How to Use

Download AMI Corpus and extract `.story` files
```
python main_obtain_meeting2summary_data.py --summary_type abstractive
```
> Already made `.story` dataset has been provided under `data/ami-transcripts-stories/`

#### Configuration options

| **Argument**                      | **Type** | **Default**                       |
|-----------------------------------|----------|-----------------------------------|
| `summary_type`                    | string   | `"abstractive"`                   |
| `ami_xml_dir`                     | string   | `"data/"`                         |
| `results_transcripts_speaker_dir` | string   | `"data/ami-transcripts-speaker/"` |
| `results_transcripts_dir`         | string   | `"data/ami-transcript/"`          |
| `results_summary_dir`             | string   | `"data/ami-summary/"`             |
+ `summary_type` is the type of summary to be extracted. Options=[`"abstractive"`, `"extractive"`].
+ `ami_xml_dir` is the directory where the AMI Corpus will be downloaded
+ `results_transcripts_speaker_dir` is the directory where each speaker's transcript will be saved 
+ `results_transcripts_dir` is the directory where each meeting's transcript will be saved
+ `results_summary_dir` is the directory where each meeting's summary will be saved

#### Code explanation
1. Obtain summaries
    * Summaries are originally saved in `data/ami_public_manual_1.6.2/words/*.xml`
    * Example: `EN2001a.A.words.xml`
        * Meeting name: `EN2001`
        * Meetings are divided into 1 hour parts: `a` (each hour is a consecutive lowercase letter)
        * Speaker: `A` (usually there are four speakers named A, B, C and D, but E is sometimes also present)
    * How:
        * Each `.xml` file has a number of tags with the words and their respective times in the audio/video file.
        * In order for us to extract the summaries, we have to put those words back together in sentences and paragraphs.
        * Thus `xml` parsing is required.
    * Output: 2 folders with corresponding .txt files
        * `data/ami-transcripts-speaker/`: meeting transcripts for each speaker
        * `data/ami-transcripts/`: complete meeting transcripts (all speakers together)
              
2. Obtain abstractive summaries
    * Located in `data/ami_public_manual_1.6.2/abstractive/*.xml` 
    * How:
        * Extract text between `abstract` tag
        * Text between `abstract` tag is composed of text in `sentence` tags
        * Return all these tags as a paragraph
    * Output: `data/ami-summary/abstractive/`
    
3. Obtain extractive summaries
    * Located in `data/ami_public_manual_1.6.2/extractive/*.xml`
    * How:
        * Extract text between `extsumm` tag
        * Text between `extsumm` tag is composed of children nodes such as the below examples:
            * Example 1: `<nite:child href="ES2002a.B.dialog-act.xml#id(ES2002a.B.dialog-act.dharshi.3)"/>`
                * This node refers to a node of ID `ES2002a.B.dialog-act.dharshi.3` in a file named `ES2002a.B.dialog-act.xml` in `data/dialogueActs/`
                * This ID is: 
                    ```
                    <dact nite:id="ES2002a.B.dialog-act.dharshi.3" reflexivity="true">
                        <nite:pointer role="da-aspect"  href="da-types.xml#id(ami_da_4)"/>
                        <nite:child href="ES2002a.B.words.xml#id(ES2002a.B.words4)..id(ES2002a.B.words16)"/>
                    </dact>
                    ```
                * This indicates words 4 to 16 in `ES2002a.B.words.xml` in `data/words/`
            * Example 2: `<nite:child href="ES2002a.D.dialog-act.xml#id(ES2002a.D.dialog-act.dharshi.16)..id(ES2002a.D.dialog-act.dharshi.20)"/>`
                * This node refers to nodes of ID `ES2002a.D.dialog-act.dharshi.16` to `20` in a file named `ES2002a.D.dialog-act.xml` in `data/dialogueActs/`
        * Return all the collected words as a paragraph
    * Output: `data/ami-summary/extractive/`
    
## Notes
* XML reader in Python:
    * Minidom vs Element Tree: [Reading XML files in Python](http://stackabuse.com/reading-and-writing-xml-files-in-python/)
    * Minidom: XML parser for Python

* TODO
    * Overlapping meeting transcript
    * Decision abstract

## Acknowledgement
Please star or fork if this code was useful for you. If you use it in a paper, please cite as:
```
@software{cunha_sergio2019ami_xml2story,
    author       = {Gwenaelle Cunha Sergio},
    title        = {{gcunhase/AMICorpusXML: Obtaining Transcript and Abstractive and Extractive Summaries from the AMI Meeting Corpus}},
    month        = oct,
    year         = 2019,
    doi          = {10.5281/zenodo.3518699},
    version      = {v2.0},
    publisher    = {Zenodo},
    url          = {https://github.com/gcunhase/AMICorpusXML}
    }
```  

If you use the [AMI Meeting Corpus](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.95.6326), please also add the following citation:
```
@INPROCEEDINGS{Mccowan05theami,
    author = {I. Mccowan and G. Lathoud and M. Lincoln and A. Lisowska and W. Post and D. Reidsma and P. Wellner},
    title = {The AMI Meeting Corpus},
    booktitle = {In: Proceedings Measuring Behavior 2005, 5th International Conference on Methods and Techniques in Behavioral Research. L.P.J.J. Noldus, F. Grieco, L.W.S. Loijens and P.H. Zimmerman (Eds.), Wageningen: Noldus Information Technology},
    year = {2005}
}
```
