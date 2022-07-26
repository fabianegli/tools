import json
import os
import shutil

from nf_core.modules.modules_json import ModulesJson
from nf_core.modules.modules_repo import (
    NF_CORE_MODULES_BASE_PATH,
    NF_CORE_MODULES_NAME,
    NF_CORE_MODULES_REMOTE,
    ModulesRepo,
)


def test_get_modules_json(self):
    """Checks that the get_modules_json function returns the correct result"""
    mod_json_path = self.pipeline_dir / "modules.json"
    with open(mod_json_path, "r") as fh:
        mod_json_sb = json.load(fh)

    mod_json_obj = ModulesJson(self.pipeline_dir)
    mod_json = mod_json_obj.get_modules_json()

    # Check that the modules.json hasn't changed
    assert mod_json == mod_json_sb


def test_mod_json_update(self):
    """Checks whether the update function works properly"""
    mod_json_obj = ModulesJson(self.pipeline_dir)
    # Update the modules.json file
    mod_repo_obj = ModulesRepo()
    mod_json_obj.update(mod_repo_obj, "MODULE_NAME", "GIT_SHA", False)
    mod_json = mod_json_obj.get_modules_json()
    assert "MODULE_NAME" in mod_json["repos"][NF_CORE_MODULES_NAME]["modules"]
    assert "git_sha" in mod_json["repos"][NF_CORE_MODULES_NAME]["modules"]["MODULE_NAME"]
    assert "GIT_SHA" == mod_json["repos"][NF_CORE_MODULES_NAME]["modules"]["MODULE_NAME"]["git_sha"]


def test_mod_json_create(self):
    """Test creating a modules.json file from scratch""" ""
    mod_json_path = self.pipeline_dir / "modules.json"
    # Remove the existing modules.json file
    os.remove(mod_json_path)

    # Create the new modules.json file
    # (There are no prompts as long as there are only nf-core modules)
    ModulesJson(self.pipeline_dir).create()

    # Check that the file exists
    assert mod_json_path.exists()

    # Get the contents of the file
    mod_json_obj = ModulesJson(self.pipeline_dir)
    mod_json = mod_json_obj.get_modules_json()

    mods = ["fastqc", "multiqc"]
    for mod in mods:
        assert mod in mod_json["repos"][NF_CORE_MODULES_NAME]["modules"]
        assert "git_sha" in mod_json["repos"][NF_CORE_MODULES_NAME]["modules"][mod]


def test_mod_json_up_to_date(self):
    """
    Checks if the modules.json file is up to date
    when no changes have been made to the pipeline
    """
    mod_json_obj = ModulesJson(self.pipeline_dir)
    mod_json_before = mod_json_obj.get_modules_json()
    mod_json_obj.check_up_to_date()
    mod_json_after = mod_json_obj.get_modules_json()

    # Check that the modules.json hasn't changed
    assert mod_json_before == mod_json_after


def test_mod_json_up_to_date_module_removed(self):
    """
    Reinstall a module that has an entry in the modules.json
    but is missing in the pipeline
    """
    # Remove the fastqc module
    fastqc_path = self.pipeline_dir / "modules" / NF_CORE_MODULES_NAME / "fastqc"
    shutil.rmtree(fastqc_path)

    # Check that the modules.json file is up to date, and reinstall the module
    mod_json_obj = ModulesJson(self.pipeline_dir)
    mod_json_obj.check_up_to_date()

    # Check that the module has been reinstalled
    files = ["main.nf", "meta.yml"]
    assert fastqc_path.exists()
    for f in files:
        assert (fastqc_path / f).exists()


def test_mod_json_up_to_date_reinstall_fails(self):
    """
    Try reinstalling a module where the git_sha is invalid
    """
    mod_json_obj = ModulesJson(self.pipeline_dir)

    # Update the fastqc module entry to an invalid git_sha
    mod_json_obj.update(ModulesRepo(), "fastqc", "INVALID_GIT_SHA", True)

    # Remove the fastqc module
    fastqc_path = self.pipeline_dir / "modules" / NF_CORE_MODULES_NAME / "fastqc"
    shutil.rmtree(fastqc_path)

    # Check that the modules.json file is up to date, and remove the fastqc module entry
    mod_json_obj.check_up_to_date()
    mod_json = mod_json_obj.get_modules_json()

    # Check that the module has been removed from the modules.json
    assert "fastqc" not in mod_json["repos"][NF_CORE_MODULES_NAME]["modules"]


def test_mod_json_repo_present(self):
    """Tests the repo_present function"""
    mod_json_obj = ModulesJson(self.pipeline_dir)

    assert mod_json_obj.repo_present(NF_CORE_MODULES_NAME) is True
    assert mod_json_obj.repo_present("INVALID_REPO") is False


def test_mod_json_module_present(self):
    """Tests the module_present function"""
    mod_json_obj = ModulesJson(self.pipeline_dir)

    assert mod_json_obj.module_present("fastqc", NF_CORE_MODULES_NAME) is True
    assert mod_json_obj.module_present("INVALID_MODULE", NF_CORE_MODULES_NAME) is False
    assert mod_json_obj.module_present("fastqc", "INVALID_REPO") is False
    assert mod_json_obj.module_present("INVALID_MODULE", "INVALID_REPO") is False


def test_mod_json_get_module_version(self):
    """Test the get_module_version function"""
    mod_json_obj = ModulesJson(self.pipeline_dir)
    mod_json = mod_json_obj.get_modules_json()
    assert (
        mod_json_obj.get_module_version("fastqc", NF_CORE_MODULES_NAME)
        == mod_json["repos"][NF_CORE_MODULES_NAME]["modules"]["fastqc"]["git_sha"]
    )
    assert mod_json_obj.get_module_version("INVALID_MODULE", NF_CORE_MODULES_NAME) is None


def test_mod_json_get_git_url(self):
    """Tests the get_git_url function"""
    mod_json_obj = ModulesJson(self.pipeline_dir)
    assert mod_json_obj.get_git_url(NF_CORE_MODULES_NAME) == NF_CORE_MODULES_REMOTE
    assert mod_json_obj.get_git_url("INVALID_REPO") is None


def test_mod_json_get_base_path(self):
    """Tests the get_base_path function"""
    mod_json_obj = ModulesJson(self.pipeline_dir)
    assert mod_json_obj.get_base_path(NF_CORE_MODULES_NAME) == NF_CORE_MODULES_BASE_PATH
    assert mod_json_obj.get_base_path("INVALID_REPO") is None


def test_mod_json_dump(self):
    """Tests the dump function"""
    mod_json_obj = ModulesJson(self.pipeline_dir)
    mod_json = mod_json_obj.get_modules_json()
    # Remove the modules.json file
    mod_json_path = self.pipeline_dir / "modules.json"
    os.remove(mod_json_path)

    # Check that the dump function creates the file
    mod_json_obj.dump()
    assert mod_json_path.exists()

    # Check that the dump function writes the correct content
    with open(mod_json_path, "r") as f:
        mod_json_new = json.load(f)
    assert mod_json == mod_json_new
