import pytest

from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

def test_email_invalid():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail&.com", "armStrongCann0n", "Isaac", "Schneider")

def test_email_double():
    clear_v1()
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    with pytest.raises(InputError):
            auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")

def test_password_short():
    clear_v1()
    with pytest.raises(InputError):
            auth_register_v1("11037.666@gmail.com", "arm11", "Issac", "Schneider")

def test_name_first_long():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "arm11", "MynameisYoshikageKira.Im33yearsold.MyhouseisinthenortheastsectionofMorioh", "Schneider")

def test_name_last_long():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "arm11", "Isaac", "MynameisYoshikageKira.Im33yearsold.MyhouseisinthenortheastsectionofMorioh")

def test_name_first_short():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "arm11", "", "Schneider")

def test_name_last_short():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "arm11", "Isaac", "")

def test_valid_user():
    clear_v1()
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")

    