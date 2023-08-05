import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from tempfile import mkstemp
import typer

config = {}


def runCommand(command: str):
    _, path = mkstemp()
    with open(path, "w") as buffer:
        process = subprocess.Popen(
            command, stdin=buffer, stdout=buffer, cwd=config["repo"]
        )
        process.wait()

    status = process.returncode

    output = ""
    with open(path) as f:
        output = f.read()

    if status:
        typer.echo(f"{command=}\n{output=}", err=True)
        sys.exit(1)
    return status, output


def signal_handler(signal: int, frame):
    runCommand("git checkout master")
    runCommand("git reset --hard autocommit --")
    sys.exit(0)


def main(repo: Optional[Path] = typer.Argument(Path(""))):
    """Make automatically git commits when coding"""
    typer.echo("Autocommit...")
    if not repo.exists() or not repo.is_dir():
        typer.echo(f"{repo} is not a existing directory.", err=True)
        sys.exit(1)

    config["repo"] = repo

    typer.echo(f"Working on {repo}")

    current_branch = ""
    _, output = runCommand("git branch -a")
    branches = []
    for line in output.split("\n"):
        if "remotes/" in line or not line:
            continue
        branch = line[2:]
        branches.append(branch)
        if line[0] == "*":
            current_branch = branch
    typer.echo(f"{branches=}")
    typer.echo(f"{current_branch=}")

    runCommand(
        f"git checkout {'-b' if 'autocommit' not in branches else ''} autocommit"
    )
    runCommand(f"git reset --hard {current_branch} --")

    while True:
        typer.echo("new loop.")
        _, output = runCommand("git status")
        if "Untracked files" in output or "Changes not staged for commit" in output:
            typer.echo(f"{datetime.now()}:Status Changed")
            typer.echo(output)
            runCommand("git add -A")
        elif "Changes to be committed" in output:
            _, output = runCommand(f'git commit -m "autocommit-{datetime.now()}"')
            typer.echo(f"{datetime.now()}:Auto commit")
            typer.echo(output)
        typer.echo("waiting")

        time.sleep(5)


def run():
    signal.signal(signal.SIGINT, signal_handler)
    typer.run(main)
