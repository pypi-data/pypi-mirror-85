import os
import sys
from pathlib import Path
from typing import Dict

from ruamel.yaml import YAML

import cognite.airworkflow.util.file as file
from cognite.airworkflow.util import env


def load_yaml(path: Path) -> Dict:
    yaml = YAML(typ="safe").load(path)
    assert isinstance(yaml, dict)
    return yaml


working_path = env.get_env_value("PWD")
ROOT_DIR = Path(working_path)
FUNCTIONS_PATH = ROOT_DIR / "functions"
IGNORE_MODELS_PATH = ROOT_DIR / ".ignore_models"

# Paths within a functions folder
FUNCTION_REL_PATH = Path("function")
FUNCTION_REL_CONFIG_PATH = FUNCTION_REL_PATH / "config.yaml"


def project_name_finder() -> str:
    ignore_models = file.read_file_to_list(IGNORE_MODELS_PATH)
    directory_contents = os.listdir(FUNCTIONS_PATH)
    directory_paths = list(
        map(
            lambda x: FUNCTIONS_PATH / x,
            filter(lambda x: x not in ignore_models, directory_contents),
        )
    )
    function_paths = [x / FUNCTION_REL_CONFIG_PATH for x in directory_paths if os.path.isdir(x)]

    if not function_paths:
        raise ValueError("No config files have been defined ! Please define config files for your function !")
        sys.exit(1)
    config_path = function_paths[0]
    yamlload = load_yaml(config_path)
    try:
        project_name = yamlload["modelSettings"]["deploy"]
        if len(project_name) > 1:
            raise ValueError("Please declare only a single project name in the function ")
            sys.exit(1)
        elif len(project_name) == 0:
            raise ValueError("Please declare a project name in the function config file!")
            sys.exit(1)
        else:
            return str(project_name[0])
    except KeyError:
        sys.exit(1)
