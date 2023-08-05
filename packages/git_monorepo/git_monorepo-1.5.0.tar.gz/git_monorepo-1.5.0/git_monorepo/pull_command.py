import os
import subprocess
import sys
from typing import List, Dict

from termcolor_util import yellow, red

from git_monorepo.project_config import (
    read_config,
    get_current_commit,
    write_synchronized_commits,
    is_synchronized_commits_file_existing,
    _resolve_in_repo,
)


def pull(sync: bool, folders: List[str]) -> None:
    monorepo = read_config()

    # we normalize relative paths, extra slashes, etc
    folders = [_resolve_in_repo(monorepo, it) for it in folders]

    pull_folders = set(folders)
    pull_folders.difference_update(monorepo.repos)

    if pull_folders:
        print(
            red("Error:"),
            red(", ".join(pull_folders), bold=True),
            red("not found in monorepo projects."),
        )
        sys.exit(1)

    for folder_name, repo_location in monorepo.repos.items():
        if folders and not folder_name in folders:
            continue

        absolute_folder_name = os.path.join(monorepo.project_folder, folder_name)

        print(
            yellow(repo_location, bold=True),
            yellow("->"),
            yellow(absolute_folder_name, bold=True),
        )

        initial_commit = get_current_commit(project_folder=monorepo.project_folder)

        if not os.path.isdir(absolute_folder_name):
            subprocess.check_call(
                [
                    "git",
                    "subtree",
                    "add",
                    "-P",
                    folder_name,
                    repo_location,
                    monorepo.current_branch,
                ],
                cwd=monorepo.project_folder,
                env=env_extend(
                    {
                        "EDITOR": "git-monorepo-editor",
                        "GIT_MONOREPO_EDITOR_MESSAGE": f"git-monorepo: Sync {folder_name}",
                    }
                ),
            )
        else:
            subprocess.check_call(
                [
                    "git",
                    "subtree",
                    "pull",
                    "-P",
                    folder_name,
                    repo_location,
                    monorepo.current_branch,
                ],
                cwd=monorepo.project_folder,
                env=env_extend(
                    {
                        "EDITOR": "git-monorepo-editor",
                        "GIT_MONOREPO_EDITOR_MESSAGE": f"git-monorepo: Sync {folder_name}",
                    }
                ),
            )

        current_commit = get_current_commit(project_folder=monorepo.project_folder)

        if current_commit == initial_commit and is_synchronized_commits_file_existing(
            monorepo, repo=folder_name
        ):
            continue

        if not sync:
            print(yellow("Not syncing as requested"))
            continue

        write_synchronized_commits(monorepo, repo=folder_name, commit=initial_commit)


def env_extend(extra_env: Dict[str, str]) -> Dict[str, str]:
    result = dict(os.environ)
    result.update(extra_env)

    return result
