import subprocess


def subprocess_call(cmd_string):
    print(cmd_string)
    cmd = cmd_string.split(" ")
    subprocess.call(cmd)
