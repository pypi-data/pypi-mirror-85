import subprocess

from termcolor_util import yellow, green

from git_monorepo.project_config import (
    read_config,
    GitMonorepoConfig,
    write_synchronized_commits,
    is_synchronized_commits_file_existing,
    get_current_commit,
)
from git_monorepo.pull_command import env_extend


def push(force: bool):
    monorepo = read_config()

    for folder_name, repo_location in monorepo.repos.items():
        if is_repo_unchanged(monorepo, folder_name) and not force:
            print(
                green(repo_location, bold=True),
                green("->"),
                green(folder_name, bold=True),
                green("UNCHANGED", bold=True),
            )
            continue

        print(
            yellow(repo_location, bold=True),
            yellow("->"),
            yellow(folder_name, bold=True),
            yellow("PUSH", bold=True),
        )

        initial_commit = get_current_commit(project_folder=monorepo.project_folder)

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
                    "GIT_MONOREPO_EDITOR_MESSAGE": f"git-monorepo: push {folder_name}",
                }
            ),
        )

        current_commit = get_current_commit(project_folder=monorepo.project_folder)

        # we need to update the last commit file with the new value
        # the commit is the current_commit, since this is already pushed
        write_synchronized_commits(monorepo, repo=folder_name, commit=current_commit)


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
