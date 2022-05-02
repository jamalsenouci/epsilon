import epsilon._utils
import os
import shutil
import pytest

@pytest.fixture(scope='function')
def remove_file_structure():
    yield epsilon._utils.create_project(name="test_dir", filepath="./epsilon/tests/")
    print("teardown test project")
    if os.path.exists("./epsilon/tests/test_dir"):
        shutil.rmtree("test_dir")


@pytest.mark.usefixtures('remove_file_structure')
def test_create_project():
    os.chdir(os.pardir)
    if not os.path.exists('./test_dir'):
        raise AssertionError
    if not os.path.exists('./test_dir/config'):
        raise AssertionError
    if not os.path.exists('./test_dir/processing'):
        raise AssertionError
    if not os.path.exists('./test_dir/models'):
        raise AssertionError

@pytest.mark.usefixtures('remove_file_structure')
def test_no_overwrite():
    if os.path.realpath(os.curdir).split("\\")[-1] != "test_dir":
        raise AssertionError
