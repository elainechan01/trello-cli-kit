# module imports

# dependencies imports
from cli_test_helpers import shell

# misc imports

def test_run():
    """Test to check running the package as a module"""
    res = shell("trellocli --help")
    assert res.exit_code == 0

def test_config():
    """Test to check config command"""
    res = shell("trellocli config --help")
    assert res.exit_code == 0

def test_create():
    """Test to check create command"""
    res = shell("ttrellocli create --help")
    assert res.exit_code == 0

def test_list():
    """Test to check list command"""
    res = shell("ttrellocli list --help")
    assert res.exit_code == 0
