from django.db import models

from .key import Key, get_wallet

_DEFAULT_MAX_LENGTH = 64


class BitcoinField(models.CharField):

    description: str = "Bitcoin Field enables a Bit Key implementation on a CharField"
    _max_length_default: bool
    _default_set: bool

    def __init__(self, *args, **kwargs):
        self._max_length_default = False
        if 'max_length' not in kwargs:
            kwargs['max_length'] = _DEFAULT_MAX_LENGTH
            self._max_length_default = True

        self._default_set = False
        if 'default' not in kwargs:
            kwargs['default'] = get_wallet
            self._default_set = True

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self._max_length_default:
            del kwargs["max_length"]
        if self._default_set:
            del kwargs["default"]
        return name, path, args, kwargs

    def to_python(self, value) -> Key:
        if isinstance(value, Key) or value is None:
            return value
        return get_wallet(value)

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_prep_value(self, value) -> str:
        if isinstance(value, Key):
            return value.to_wif()
        else:
            return value




