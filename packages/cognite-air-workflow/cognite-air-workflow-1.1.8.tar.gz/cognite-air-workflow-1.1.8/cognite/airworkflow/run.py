import os
import sys
from itertools import product

import cognite.airworkflow.constants as const
from cognite.airworkflow.function_deployer import FunctionDeployer
from cognite.airworkflow.master_config import get_deployments, get_master_config
from cognite.airworkflow.model.schedule_assets import execute
from cognite.airworkflow.model_asset_hierarchy import ModelAssetHierarchy
from cognite.airworkflow.util import cdf, env, functions, github


def handle_asset_hierarchy():
    _, project_to_config = get_master_config()
    for project, config in project_to_config.items():
        print(f"Running Model Asset Hierarchy create/update for project {project}")
        ModelAssetHierarchy(config, project).create_or_update()


def handle_function_deployments():
    github_event_name = env.get_env_value("GITHUB_EVENT_NAME")
    github_ref = env.get_env_value("GITHUB_REF")
    is_delete = "IS_DELETE" in os.environ and os.environ["IS_DELETE"] == "true"
    is_pr = github_event_name == "pull_request"

    assert (
        len(sys.argv) >= 3 and sys.argv[2]
    ), "Expected a function name passed as a command line argument, but got nothing"
    function_name = sys.argv[2].split("/")[-1] if "/" in sys.argv[2] else sys.argv[2]
    print(f"HANDLING {github_event_name} ON {github_ref} FOR FUNCTION {function_name}")

    for deployment in get_deployments(function_name):
        FunctionDeployer(deployment, is_delete, is_pr).handle_deployment()


def handle_delete_functions():
    """
    1. Find name of all functions that should be deployed: Based on what's on master and what's in PRs
    2. List all functions currently deployed
    3. Delete the diff
    """
    _, project_to_config = get_master_config()
    for project, config in project_to_config.items():
        function_paths = [functions.get_relative_function_path(p) for p in config]
        pr_refs = github.get_open_pr_refs()
        all_functions = [functions.get_function_name(f, latest=True) for f in function_paths] + [
            functions.get_function_name(f, pr=True, ref=ref) for ref, f in list(product(pr_refs, function_paths))
        ]

        info = const.PROJECT_TO_API_KEYS[project]
        client = cdf.experimental_client(info.project)
        dangling = functions.list_dangling_function(client, all_functions, name_prefix=env.get_repo_name_auto())
        for function in dangling:
            functions.delete_function(client, function.external_id)


def handle_deploy_infrastructure_schedules():
    _, project_to_config = get_master_config()
    for project, config_dict in project_to_config.items():
        info = const.PROJECT_TO_API_KEYS[project]
        client = cdf.experimental_client(info.project)
        execute(client)


def handle_call_schedulemanager():
    _, project_to_config = get_master_config()
    for project in project_to_config:
        client = cdf.experimental_client(project)
        client.functions.call(external_id="cognitedata/air-functions/schedulemanager:latest")


if __name__ == "__main__":

    if sys.argv[1] == "model":
        handle_asset_hierarchy()
    elif sys.argv[1] == "function":
        handle_function_deployments()
    elif sys.argv[1] == "delete":
        handle_delete_functions()
    elif sys.argv[1] == "infraschedules":
        handle_deploy_infrastructure_schedules()
    elif sys.argv[1] == "call_schedulemanager":
        handle_call_schedulemanager()
