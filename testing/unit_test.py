import pytest

from DiscordBlogBot.main import print_secret


@pytest.mark.unit
def test_print_secret():
    """Checks that print_secret returns a hash value."""
    secret_int = 165843841834  # nosec
    secret_string = "lsearokghqrakesldlkerua"  # nosec
    encoded_int = print_secret(secret_int)
    encoded_string = print_secret(secret_string)
    assert isinstance(encoded_int, str)
    assert isinstance(encoded_string, str)
    assert secret_int != encoded_int
    assert secret_string != encoded_string

    class Unstringifyable:
        def __str__(self):
            raise TypeError("Can not by stringified")

    a = Unstringifyable()
    random_float = print_secret(a)
    assert isinstance(random_float, float)
