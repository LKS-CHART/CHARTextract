## Pre-requisites
- Install Python: https://www.python.org/downloads/
- Install NodeJS: https://nodejs.org/en/

## Build Python executable (support for Python 3.6 and Python 3.7):
- Set up virtual environment 
- Install Node dependencies: `cd RegexNLP-node && npm install`
- Install python dependencies depending on version of python being used: `pip install -r requirements.txt`
- run `make_dist_py36.cmd` or `make_dist_py37.cmd`
- run `Release/win-unpacked/nlp_tool.exe`
You can access the app from the executable file or from the browser (localhost:3000).

## Running Node app (in the browser):
- `cd RegexNLP-node`
- Install packages: `npm install`
- Start electron app: `npm run start`

## Using the tool
- On the `Settings` page, upload the following files:
  - Data file (this should have a column for the text data, the ID): `fake_data\fake_notes.csv`
  - Data ID column (column where ID is stored in the data file) : 0
  - Data column (column where text is stored in the data file): 1
  - Data first row: 1
  - Concatenate Data (set this to True if same ID has multiple text data): True
  - Create Train and Validation Set (set to True if no train file and no valid label file provided): False 
  - Prediction Mode (set to True if we are not evaluating on the Validation set): False
  - Train file (this should have a column for the ID and the labels): `fake_data\fake_notes_train.csv`
  - Valid file (this should have a column for the ID and the labels): `fake_data\fake_notes_valid.csv`
  - Label ID Column (column where ID is stored in Train and Valid file - this should be the same for both files): 0
  - Label First Row: 1
  - Rules Folder: `fake_data\rules` make sure you have write permissions for this folder
- On the `Variable Settings` page
  - Click on the `default` button and select the `smoking_status` variable
  - Label Column (column where labels are stored in the train and valid file): 1
  - Required Dictionaries (if dictionaries are used, type in the name - all dictionaries can be found in `Release\win-unpacked\dictionaries\`): leave this blank
  - Use Dictionary Preprocessor (set to True if we want to only keep sentences that have words from the dictionary): False
  - Specify Function with Python (deprecated): False
- Classifier Settings
  - Classifier type: RegexClassifier
    - RegexClassifier: regular expression match at a sentence-level
    - CaptureClassifier: regular expression match + extracts captured group (e.g., will retrieve number of years smoked)
    - TemporalRegexClassifier (deprecated)
  - Negative Label (from the labels files, this is the label used for any example that is not positive) : "Not dictated"
    - If score is 0: the data point will be assigned the negative label
  - Class name and bias (each label can be assigned a bias)
- From the `Rules` view, toggle the `Advanced Mode` to directly edit the regular expressions.

## Rules format
- Example:
```
!Current smoker
#Don't forget to save the file to preserve the new name.
"smok",3,"former","i",0,"quit","r",1,"does not","i",0
```
- The first line has the variable name prefixed by an exclamation mark.
- All comments are denoted by `#`
- Each line has the following format:
`"primary_rule",primary_score,"Secondary Rule","rule_type",secondary_score,"Secondary Rule 2","rule_type",secondary_score`.
- The classifier goes through each rule one sentence at a time.
- The classifier first tries to the primary rule. If no match is found, it moves on to the next sentence.
- If the primary rule matches, that sentence is given the `primary_score`.
- The classifier then checks for `ignore` secondary rules (i.e., rule_type = "i"). If any of them match, the sentence is ignored (i.e., no score is assigned)
- The classifier then checks for `replace` and `add` secondary rules (i.e., rule_type = "r", "a"). 
  - If a replace rule matches, the sentence's score is replaced with `secondary_score`. The first replace rule that doesn't match stops the loop.
  - If an add rule matches, the `secondary_score` is added to the cumulative sentence score.
- rule_types can also have modifiers: "b","a". These are specified by appending to rule_type. E.g "ra","ib","aa"
  - The sentence is split into three: everything before the primary rule, the primary rule match, everything after the primary rule match.
  - "b" indicates a match before the primary rule.
  - "a" indicates a match after the primary rule.
  - e.g. `"smok",0,"not","rb",0`
  - e.g. `she smokes but not on weekends` is labeled `smoker`
    - `"smok",0,"not","rb",1` This sentence would get a score of 0 with this rule
    - `"smok",0,"not","a",2` This sentence would get a score of 2 with this rule


