import pytest
import sys
import subprocess
import os

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


def test_if_source_does_not_exists():
    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 1
    assert b"Source folder does not exist." in std_err

def test_if_destination_does_not_exists():
    result = subprocess.Popen("mkdir /tmp/source", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 0
    assert b"Destination folder created." in std_out
    with open('/tmp/logfile') as log:
        if not "Destination folder created." in log.read():
            assert False

    result = subprocess.Popen("rm -R /tmp/source /tmp/destination /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

def test_if_logfile_path_no_write_permission():
    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /etc/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 2
    assert b"Could not open logfile for writing." in std_err

def test_destination_directory_missing_permissions():
    result = subprocess.Popen("mkdir /tmp/source", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /etc/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 3
    assert b"Could not create destination directory." in std_err

    result = subprocess.Popen("rm -R /tmp/source /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

def test_create_destination_directory_if_missing():
    result = subprocess.Popen("mkdir /tmp/source", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 0
    assert b"Destination folder created." in std_out
    with open('/tmp/logfile') as log:
        assert "Destination folder created." in log.read()
    
    assert os.path.exists("/tmp/destination")

    result = subprocess.Popen("rm -R /tmp/source /tmp/destination /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

def test_copy_file_from_source_to_destination():
    result = subprocess.Popen("mkdir /tmp/source", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("touch /tmp/source/a_file", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 0
    assert b"Copied '/tmp/source/a_file' to '/tmp/destination/a_file'." in std_out
    with open('/tmp/logfile') as log:
        assert "Copied '/tmp/source/a_file' to '/tmp/destination/a_file'." in log.read()

    result = subprocess.Popen("rm -R /tmp/source /tmp/destination /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

def test_copy_file_from_source_to_destination_multiple_subdirs():
    result = subprocess.Popen("mkdir -p /tmp/source/subdir", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("touch /tmp/source/a_file", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("touch /tmp/source/subdir/a_file2", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0

    result = subprocess.Popen("python3 veeam-sync.py --source /tmp/source --destination /tmp/destination --logfile /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = result.communicate()

    assert result.returncode == 0
    assert b"Copied '/tmp/source/a_file' to '/tmp/destination/a_file'." in std_out
    with open('/tmp/logfile') as log:
        assert "Copied '/tmp/source/a_file' to '/tmp/destination/a_file'." in log.read()

    assert os.path.isdir("/tmp/source/subdir")
    assert os.path.isfile("/tmp/source/subdir/a_file2")
    
    result = subprocess.Popen("rm -R /tmp/source /tmp/destination /tmp/logfile", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.communicate()
    assert result.returncode == 0