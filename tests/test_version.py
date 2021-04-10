import pytest

from gh_release.version import Version


@pytest.mark.parametrize(
    ("verstring", "expected"),
    [
        ("0.0.0", True),
        ("0.0.0-beta", True),
        ("0.1.0", True),
        ("1010.100.0", True),
        ("1010.100.0-suffix", True),
        ("mat", False),
    ],
)
def test_is_version_string(verstring, expected):
    assert Version.is_version_string(verstring) == expected
