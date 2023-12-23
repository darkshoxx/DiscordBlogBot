import pytest

from DiscordBlogBot.main import print_secret

@pytest.mark.unit
def test_print_secret():
    """Checks that print_secret returns a hash value."""
    secret_int = 165843841834
    secret_string = "lsearokghq34£()*!£$%^&*()"
    encoded_int = print_secret(secret_int)
    encoded_string = print_secret(secret_string)
    assert type(encoded_int) == str
    assert type(encoded_string) == str
    assert secret_int != encoded_int
    assert secret_string != encoded_string

    class Unstringifyable(object):
        def __str__(self):
            raise TypeError('Can not by stringified')

    a = Unstringifyable()
    random_float = print_secret(a)
    assert type(random_float) == float
