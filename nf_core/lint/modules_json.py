#!/usr/bin/env python

from nf_core.modules.modules_command import ModuleCommand
from nf_core.modules.modules_json import ModulesJson


def modules_json(self):
    """Make sure all modules described in the ``modules.json`` file are actually installed

    Every module installed from ``nf-core/modules`` must have an entry in the ``modules.json`` file
    with an associated version commit hash.

    * Failure: If module entries are found in ``modules.json`` for modules that are not installed
    """
    passed = []
    warned = []
    failed = []

    # Load pipeline modules and modules.json
    modules_command = ModuleCommand(self.wf_path)
    modules_json = ModulesJson(self.wf_path)
    modules_json.load()
    modules_json_dict = modules_json.modules_json

    if modules_json:
        modules_command.get_pipeline_modules()

        all_modules_passed = True

        for repo in modules_json_dict["repos"].keys():
            # Check if the modules.json has been updated to keep the
            if "modules" not in modules_json_dict["repos"][repo] or "git_url" not in modules_json_dict["repos"][repo]:
                failed.append(
                    f"Your `modules.json` file is outdated. Please remove it and reinstall it by running any module command"
                )
                continue

            for key in modules_json_dict["repos"][repo]["modules"]:
                if not key in modules_command.module_names[repo]:
                    failed.append(f"Entry for `{key}` found in `modules.json` but module is not installed in pipeline.")
                    all_modules_passed = False

        if all_modules_passed:
            passed.append("Only installed modules found in `modules.json`")
    else:
        warned.append("Could not open `modules.json` file.")

    return {"passed": passed, "warned": warned, "failed": failed}
