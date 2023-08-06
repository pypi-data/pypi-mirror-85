import git
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--protected_branches', default=["main", "master"], nargs='?')
    args = parser.parse_args()
    repo = git.Repo()
    if repo.active_branch.name in args.protected_branches:
        raise Exception(f"Can't Commit from {repo.active_branch.name}")