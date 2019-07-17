# CHARTextract

![](./RegexNLP-node/icon.png)

*CHARTextract* is a rule-based information extraction tool with the ability to quickly and easily refine rules on-the-fly.

**Tool Documentation**: [https://lks-chart.github.io/CHARTextract-docs/](https://lks-chart.github.io/CHARTextract-docs/)

**Tool Download**: [https://lks-chart.github.io/CHARTextract-docs/08-downloads/tool_download.html](https://lks-chart.github.io/CHARTextract-docs/08-downloads/tool_download.html)


## Getting Started

### Prerequisites
- Install Python: https://www.python.org/downloads/
- Install NodeJS: https://nodejs.org/en/

### Installing and running application (support for Python 3.7 & conda):
- Install the required Python dependencies:

```conda create -n [ENV_NAME] --file package-list.txt```

- Install Node dependencies:

```cd RegexNLP-node && npm install```

- Build executable app:

```./make_dist_py37.cmd```

- Run application from executable file - you can access the app from the executable file or from the browser (localhost:3000):

`./Release/win-unpacked/CHARTextract.exe`


- Run application from node - you can access the app from the browser (localhost:3000):

```cd RegexNLP-node && npm install && npm run start```


## Using the tool

Refer to the documentation for more details.

- We recommend you start off with the [smoking status example tutorial](https://lks-chart.github.io/CHARTextract-docs/07-tutorials/02-smoking-variable-example.html).

- The [rule refinement documentation](https://lks-chart.github.io/CHARTextract-docs/05-rule-refinement/) provides information on the workflow.

## Tests

### Python testing

From the `RegexNLP-py` folder, run the following: `python -m pytest ..\RegexNLP-py_tests\ --cov=.
`

To generate a HTML report of the code coverage:`python -m pytest ..\RegexNLP-py_tests\ --cov=. --cov-report=html` and then open up `htmlcov\index.html`.

## License

This project is licensed under the [MIT License](LICENSE).
