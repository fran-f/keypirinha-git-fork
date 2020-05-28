#
# Git-Fork wrapper class
# More info at https://github.com/fran-f/keypirinha-git-fork
#
# pylint: disable=C, import-error, relative-beyond-top-level

import keypirinha_util as kpu

import json
import os

class ForkWrapper:

    _fork_path = None
    _fork_exe = None
    _fork_config = None

    def defaultdir():
        localappdata = kpu.shell_known_folder_path("{f1b32785-6fba-4fcf-9d55-7b8e7f157091}")
        return localappdata + "\\Fork\\"

    def __init__(self, path):
        self._fork_path = path
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
        repositoryManager = self._load_config().get("RepositoryManager")
        if not repositoryManager:
            return []

        return repositoryManager.get("Repositories", [])

    def gitinstance(self):
        return self._load_config().get("GitInstancePath") \
            or self._find_embedded_git()

    def openrepository(self, path):
        kpu.shell_execute(self._fork_exe, args=path)

    def openshelltool(self, path):
        tool = self._load_config().get("ShellTool")
        if not tool:
            command = get_bash_for_git_instance(self.gitinstance()) or "cmd.exe"
            kpu.shell_execute(command, working_dir = path)
        else:
            params = get_tool(tool.get("Type"), tool.get("ApplicationPath"), \
                tool.get("Arguments"))
            kpu.shell_execute(
                params['command'],
                args = params['args'],
                working_dir = path
            )

    def _load_config(self):
        with kpu.chardet_open(self._fork_config, mode="rt") as fork_config:
            return json.load(fork_config)

    def _find_embedded_git(self):
        git_instances = self._fork_path + "gitInstance"
        git_exe = git_instances + "\\" + get_last_subdir(git_instances) + "\\bin\\git.exe"
        return git_exe if os.path.isfile(git_exe) else None


def get_tool(toolType, command, args):
    return {
        'CommandPrompt': { 'command': 'cmd.exe', 'args': args },
        'PowerShell': { 'command': 'powershell.exe', 'args': args },
        'WindowsTerminal': { 'command': command, 'args': '-d .' },
    }.get(toolType, { 'command': command, 'args': args })

def get_bash_for_git_instance(git_exe):
    bash_exe = os.path.dirname(git_exe) + "\\bash.exe"
    return bash_exe if os.path.isfile(bash_exe) else None

def get_last_subdir(path):
    return os.listdir(path)[-1]
