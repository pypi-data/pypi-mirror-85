import subprocess

from termcolor_util import yellow, green

from git_monorepo.project_config import (
    read_config,
    GitMonorepoConfig,
    write_synchronized_commits,
    is_synchronized_commits_file_existing,
)
from git_monorepo.pull_command import env_extend


def push():
    monorepo = read_config()
    something_changed = False

    for folder_name, repo_location in monorepo.repos.items():
        if is_repo_unchanged(monorepo, folder_name):
            print(
                green(repo_location, bold=True),
                green("->"),
                green(folder_name, bold=True),
                green("UNCHANGED", bold=True),
            )
            continue

        something_changed = True

        print(
            yellow(repo_location, bold=True),
            yellow("->"),
            yellow(folder_name, bold=True),
            yellow("PUSH", bold=True),
        )
        subprocess.check_call(
            [
                "git",
                "subtree",
                "push",
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

    if not something_changed and is_synchronized_commits_file_existing(monorepo):
        return

    # we need to update the last commit file with the new value
    write_synchronized_commits(monorepo)


def is_repo_unchanged(monorepo: GitMonorepoConfig, folder_name: str) -> bool:
    """
    We check if the sub-repo is changed. This is done via a log that could happen
    against multiple branches if this is a merge.
    :param monorepo:
    :param folder_name:
    :return:
    """
    # if no commits are synchronized, we need to mark this repo as changed
    # first, so the changes are being pushed
    if (
        not monorepo.synchronized_commits
        or folder_name not in monorepo.synchronized_commits
    ):
        return False

    for last_commit in monorepo.synchronized_commits[folder_name]:
        folder_log = (
            subprocess.check_output(
                ["git", "log", f"{last_commit}..HEAD", "--", folder_name],
                cwd=monorepo.project_folder,
            )
            .decode("utf-8")
            .strip()
        )

        if folder_log:
            return False

    return True
