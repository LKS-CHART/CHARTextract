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
  - Data file (this should have a column for the text data, the ID): `fake_data\TB_FakeNotes_2018.xlsx`
  - Data ID column (column where ID is stored in the data file) : 0
  - Data column (column where text is stored in the data file): 1
  - Data first row: 1
  - Concatenate Data (set this to True if same ID has multiple text data): False
  - Create Train and Validation Set (set to True if no train file and no valid label file provided): False 
  - Prediction Mode (set to True if we are not evaluating on the Validation set): False
  - Train file (this should have a column for the ID and the labels): `fake_data\TB_FakeNotes_train.xlsx`
  - Valid file (this should have a column for the ID and the labels): `fake_data\TB_FakeNotes_valid.xlsx`
  - Label ID Column (column where ID is stored in Train and Valid file - this should be the same for both files): 0
  - Label First Row: 1
  - Rules Folder: `fake_data\rules` make sure you have write permissions for this folder
- On the `Variable Settings` page
