import pathlib
import subprocess

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
APP_DIR = PROJECT_ROOT / "app"


def run_command(command, *args, shell=False, **kwargs):
    _command = command if shell else command.split()

    try:
        process = subprocess.run(
            _command, *args, shell=shell, check=True, text=True, **kwargs
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)
    else:
        return process
