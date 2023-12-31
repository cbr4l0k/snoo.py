
<img src=".docs/logo.jpeg"></img>

# Snoo.py


**Snoo.py** is our loyal companion, which allows us to quickly generate documentation for our projects. It unlocks a never-before-seen ability for any developer team to document their projects in less than 5 minutes with a cost of less than 2 USD.

**Snoo.py** generates:

1. Interactive project tree containing files and document descriptions inside it.
2. 3D graph view of components inside the project, particularly scripts in the project, including the code filename, and how they relate to each other.
3. A coupling and cohesion analysis of the project driven by OpenAI's top models like GPT-3.5 turbo.
4. Usage percentage interactive plot, allowing visualization of how much a file is used.


![Resulting report](.docs/report_matas.gif)


## Table of contents
- [Requirements](#requirements)
- [Installation and setup](#installation-and-setup)
    - [Enviroment variables](#environment-variables)
- [Run project](#run-project)
- [Project architecture](#project-architecture)
- [Side notes](#side-notes)
- [Next steps](#next-steps)


## Requirements
- `Python 3.11` or higher.
- `JavaScript D3` _(version 7.85)_.
- [`tree`](https://gitlab.com/OldManProgrammer/unix-tree) _(version v2.1.1)_.


## Installation and setup
```bash
git clone github.com/cbr4lok/como-lavarse-las-manos.git
cd como-lavarse-las-manos
python -m venv venv 
source ./venv/bin/activate
pip install -r requirements.txt
```
### Environment variables


| Field Name       | Explaination                                                   |
|------------------|----------------------------------------------------------------|
| OUTPUTS_PATH     | `Folder containing the outputs`  |
| PROJECTS_PATH    | `Folder containing the projects that are available for analys. Insert yours here.`|
| OPEN_AI_API_KEY  | `Insert your secret OpenAI api key here.`|
| DEFAULT_LLM      | `Add the default model to use when using the model. This could be one of the OpenAI models like 'gpt-3.5-turbo' or 'gpt-3.5-turbo-16k' our preffered option is 'gpt-3.5-turbo-16k'.` |


## Run project 

This is how you can run our project:

```python 
python3 src/snoo.py <project_path_to_analize>
```

![running live example](.docs/demo.gif)


## Project architecture

![Project backend architechture](.docs/class-diagram-backend.svg)


## Side notes

- _Our solution has been tested on Linux only, so we recommend sticking to this operating system, particularly in Arch-based distributions. This should also work without effort in other kinds of Linux distributions._

- _We recommend visualizing this program in Google Chrome due to the fact that different browsers may change the HTML layout. We've developed this web interface with Google Chrome in mind. We do not guarantee a good layout if viewed in other browsers._

- _It's MANDATORY to have a .gitignore file in the project in order to avoid spending computing power on analizing files inside the `__pycache__` folder, for example, the rule is to add eveything you do not want to be analized inside the .gitignore file_.

## Next steps

1. Retraining a new instance of `GPT-3.5-turbo-16k` that performs better at generating this reports.

2. Build an id system for dependency easy management instead of full paths which also spend more tokens.

3. Add memory to LLMs chains in order to achieve better results and to be able to implement other tecniques like chain of thought.

4. Expand support for new languages _(this is designing new prompts and expanding the file managment techniques used in the report class)_.
