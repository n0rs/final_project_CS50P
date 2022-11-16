from project import get_frequency
from project import get_equity
from project import make_url
from unittest.mock import patch


def main():
    test_get_equity()
    test_get_frequency()
    test_make_url()


def test_get_equity():
    with patch("builtins.input", return_value="dax"):
        assert get_equity() == "dax"
    with patch("builtins.input", return_value="dAx"):
        assert get_equity() == "dax"
    with patch("builtins.input", return_value="  dax  "):
        assert get_equity() == "dax"


def test_get_frequency():
    with patch("builtins.input", return_value="daily"):
        assert get_frequency() == "daily"
    with patch("builtins.input", return_value="intraday"):
        assert get_frequency() == "intraday"
    with patch("builtins.input", return_value="weekly"):
        assert get_frequency() == "weekly"
    with patch("builtins.input", return_value="monthly"):
        assert get_frequency() == "monthly"
    with patch("builtins.input", return_value="MONTHLY"):
        assert get_frequency() == "monthly"
    with patch("builtins.input", return_value="moNTHlY"):
        assert get_frequency() == "monthly"
    with patch("builtins.input", return_value="    moNTHlY    "):
        assert get_frequency() == "monthly"


def test_make_url():
    # 200 is the status code for a successful request
    with patch("builtins.input", return_value=5):
        assert make_url(fre="intraday", e="dax").status_code == 200
    assert make_url(fre="daily", e="dax").status_code == 200
    assert make_url(fre="weekly", e="dax").status_code == 200
    assert make_url(fre="monthly", e="dax").status_code == 200


if __name__ == "__main__":
    main()