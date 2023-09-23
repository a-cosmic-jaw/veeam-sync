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

def test_no_source():
    result = subprocess.Popen("mkdir /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --destination /tmp/destination --logfile=/tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 2
    assert b"Error: Missing option '--source'." in std_err

    result = subprocess.Popen("rm -R /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

def test_no_destination():
    result = subprocess.Popen("mkdir /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --logfile=/tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 2
    assert b"Error: Missing option '--destination'." in std_err

    result = subprocess.Popen("rm -R /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

def test_content_of_logfile():
    result = subprocess.Popen("mkdir /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 0
    assert b"Logfile found and write permission granted." in std_out
    with open('/tmp/logfile') as log:
        if "Logfile found and write permission granted." in log.read():
            assert True
        else:
            assert False

    result = subprocess.Popen("rm -R /tmp/source /tmp/destination", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0


def test_if_destination_does_not_exists():
    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 1
    assert b"Source folder does not exist." in std_err
    
    