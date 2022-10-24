# Nextflow cloud backend
## Dependencies
* Build tools (Ubuntu: `build-essential`, Arch Linux: `base-devel`)
* C/C++-header for PostgreSQL (Ubuntu: `libpq-dev`, Arch Linux: `postgresql-libs`)
* C/C++-headers for libev (Ubuntu: `libev-dev`, Arch Linux: `libev`)
* Rust Compiler
* Docker
* Python 3.x  (have a look into the `Pipfile`)
* [pyenv](https://github.com/pyenv/pyenv)
* [pipenv](https://pipenv.pypa.io/en/latest/)


## Configuration
### Backend configuration
The configuration for the backend is split into multiple files for different environments:
| file | read order | environment | purpose |
| --- | --- | --- | --- |
| `config.yaml` | 1 | all | config definition |
| `config.development.yaml` | 2 | development | contains all necessary information for the development environment |
| `config.production.yaml` | 2 | production | some minor adjustments for production |
| `config.local.yaml` | 4 | all | excluded from GIT, serves as user specific overwrite |

The environment is set by the environment variable `NF_CLOUD_ENV`. The default environment is `development`.

You can overwrite some configuration variables and the environment with CLI arguments. For more information run `pipenv run python -m nf_cloud_backend --help`

#### Workflow configuration
Workflows are defined under the key `workflows`.
Each workflows key is the name of the workflows.
Necessary attributes are:
* `directory`: string; Path the workflow directory
* `script`: string; Name of the main script
Optional attributes:
* `nextflow_parameters`: string array; paramters which are passed to the run command; each part of the paramters is a single element in the array, e.g. `-profile docker` => `["-profile", "docker"]`


##### Dynamic and static workflow arguments
Arguments under the key `args` which are passed to the workflow/script.
Each argument is defined by a name and a type.
* Path selector
    The path is relative to the working directory of each workflow.
    * type: `path`
    * additional keys:
        * `selectable_files`: boolean; default: false; if true, files are selectable
        * `selectable_folders`: boolean; default: false; if true, folders are selectable
* Multiple path selector
    Selected paths will passed as comma separated list to the workflow.
    Each path is relative to the working directory of each workflow.
    * type: `paths`
    * additional keys:
        * `selectable_files`: boolean; default: false; if true, files are selectable
        * `selectable_folders`: boolean; default: false; if true, folders are selectable
* Number input
    * type: `number`
* Text input
    * type: `text`
    * additional attributes:
        * `is_multiline`: boolean; default: false; if true, text input will be a multiline textarea
* Wildcard:
    Text field to define a wildcard path, e.g. `/*.txt`
    * type: `file-glob`
If a default value is provided, just add a additional key `value` with the actual value.


----

# Exploring the code
Each Flaskapp has an attribute url_map (see https://stackoverflow.com/questions/13317536/get-list-of-all-routes-defined-in-the-flask-app). Upon starting the app, if the environment is a dev environment, all known routes are displayed on the console.