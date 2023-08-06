import shutil
import subprocess


def _get_exec():
    """
    checks if dmenu is installed on path.

    returns: string, path to binary
    """
    dmenu = shutil.which("dmenu")
    if not dmenu:
        raise EnvironmentError("No dmenu installed")
    else:
        return dmenu


def run_dmenu(words=[]):
    """
    Runs dmenu
    """
    if not words:
        command = ["echo", "Search wikipedia"]
    else:
        command = ["echo", '\n'.join(words)]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)
    result = subprocess.check_output([
        _get_exec(), "-p", "WikiP | Word:"], stdin=ps.stdout)
    ps.wait()
    return result


