import json
import os

import pytest

from tktl.commands.login import LogInCommand, SetApiKeyCommand
from tktl.core.exceptions import InvalidInputError


def test_set_api_key(capsys):
    cmd = SetApiKeyCommand()
    cmd.execute(api_key=None)
    out, err = capsys.readouterr()
    assert "API Key cannot be empty.\n" == err

    cmd.execute(api_key="ABC")
    assert os.path.exists(os.path.expanduser("~/.config/tktl/config.json"))
    with open(os.path.expanduser("~/.config/tktl/config.json"), "r") as j:
        d = json.load(j)
        assert d["api-key"] == "ABC"


def test_login(capsys):
    cmd = LogInCommand()
    k = os.environ["TEST_USER_API_KEY"]
    assert cmd.execute(k) is True
    out, err = capsys.readouterr()
    assert out == f"Authentication successful for user: {os.environ['TEST_USER']}\n"
    with pytest.raises(InvalidInputError):
        cmd.execute(None)
