## Pre-requisites
- Install Python: https://www.python.org/downloads/
- Install NodeJS: https://nodejs.org/en/

## Build Python executable (Python 3.7):
- Set up virtual environment for RegexNLP-py and download requirements: `conda create --name env_name --file spec-file-py37.txt`
- Build: `make_dist_py37.cmd`.

## Running Node app:
- Install packages: `npm install`
- Start electron app: `npm run start-electron`
