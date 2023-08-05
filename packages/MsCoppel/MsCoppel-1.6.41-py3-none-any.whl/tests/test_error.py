from MsCoppel import ErrorMs
import pytest
from demo_error import Error


def test_c():
    with pytest.raises(ErrorMs, match=r"-4"):
        Error()
