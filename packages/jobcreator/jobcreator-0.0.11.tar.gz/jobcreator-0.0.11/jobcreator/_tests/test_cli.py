import subprocess


def capture(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_run_cli():
    command = ["jobcreator"]
    _, _, exitcode = capture(command)

    assert exitcode == 1
