#
# Git-Fork wrapper class
# More info at https://github.com/dreadnaut/keypirinha-git-fork
#

import keypirinha_util as kpu

import json
import os

class ForkWrapper:

    def defaultdir():
        localappdata = kpu.shell_known_folder_path("{f1b32785-6fba-4fcf-9d55-7b8e7f157091}") 
        return localappdata + "\\Fork\\";

    def __init__(self, path):
        self._fork_exe = os.path.join(path, "Fork.exe")
        self._fork_config = os.path.join(path, "settings.json")

        exe_exists = os.path.isfile(self._fork_exe) 
        config_exists = os.path.isfile(self._fork_config) 

        if not (exe_exists and config_exists):
            raise ValueError("Fork is not installed in %s" % (path))

    def executable(self):
        return self._fork_exe

    def icon(self):
        return "@%s,0" % self._fork_exe

    def repositories(self):
        with kpu.chardet_open(self._fork_config, mode="rt") as fork_config:
            data = json.load(fork_config)

        repositoryManager = data.get("RepositoryManager")
        if not repositoryManager:
            return []

        return repositoryManager.get("Repositories", [])

    def openrepository(self, path):
        kpu.shell_execute(self._fork_exe, args=path)
