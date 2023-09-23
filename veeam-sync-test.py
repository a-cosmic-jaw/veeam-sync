import pytest
import sys
import subprocess

def test_no_logfile():
    result = subprocess.Popen("mkdir /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 2
    assert b"Error: Missing option '--logfile'." in std_err

    result = subprocess.Popen("rm -R /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0