import os
import subprocess
from typing import List


REPOS = os.path.expanduser("~/repos")


def execute_git_commands(commands: List[List[str]], *, repo: str) -> None:
    for command in commands:
        try:
            subprocess.run(command, check=True, cwd=f"{REPOS}/{repo}")
        except subprocess.CalledProcessError as e:
            execute_git_commands(
                [
                    ["git", "reset", "HEAD", "."],
                    ["git", "clean", "-fd"],
                    ["git", "checkout", "."],
                ],
                repo=repo,
            )
            raise e
