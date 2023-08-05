import re
import os
from email.utils import parseaddr
import urllib.parse

from cnfrm.exceptions import ValidationError

__all__ = ["Field", "NumberField", "FloatField", "IntegerField",
           "EmailField", "PathField", "FileField", "DirectoryField", "UrlField", "ChoiceField"]


class Field():
    base_type = str

    def __init__(self, default=None, required=True):
        self.default = default
        self.required = required

        if default is not None:
            self.validate(default)

        self.value = None

    def validate(self, value):
        if self.required and value is None:
            raise ValidationError("Cannot set required field to None")
        return True

    def _raise_validation(self, value):
        raise ValidationError(
            f"{value} is not valid for {self.__class__.__name__}")

    def is_valid(self):
        if not self.required:
            return True

        if self.value is not None:
            return True
        if self.default is not None:
            return True

        return False

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance._values.get(self, self.default)

    def __set__(self, instance, value):
        if self.validate(value):
            instance._values[self] = value
        else:
            # Usually validate should have raised already.
            # Let's do it again. Just in case...
            raise ValidationError(
                f"'{value}' is not a valid value for {self.__class__.__name__}")


class ChoiceField(Field):
    def __init__(self, choices, default=None, required=True) -> None:
        self.choices = choices
        super().__init__(default=default, required=required)
    
    def validate(self, value):
        if value not in self.choices:
            raise ValidationError(f"{value} is not a valid choice for field {self}")

        return super().validate(value)


class NumberField(Field):
    base_type = int

    def __init__(self, default=None, required=True, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(default, required)

    def validate(self, value):
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(
                f"Min-value constraint not satisfied: '{value}'")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(
                f"Max-value constraint not satisfied: '{value}'")

        return super().validate(value)


class IntegerField(NumberField):

    def validate(self, value):
        int_value = int(value)
        if int_value != value:
            self._raise_validation(value)

        return super().validate(int_value)


class FloatField(NumberField):
    base_type = float

    def validate(self, value):
        float_value = float(value)
        if float_value != value:
            self._raise_validation(value)

        return super().validate(float_value)


class EmailField(Field):
    rex = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9\.-]+\.[A-Z]{2,63}$")

    def validate(self, value):
        _name, addr = parseaddr(value)
        if self.rex.match(addr.upper()):
            return True

        raise ValidationError(f"Not a valid email address: '{addr}'")


class PathField(Field):
    pass


class FileField(PathField):
    def validate(self, value):
        if not os.path.isfile(value):
            raise ValidationError(f"Not a file: '{value}'")

        return True


class DirectoryField(PathField):
    def validate(self, value):
        if not os.path.isdir(value):
            raise ValidationError(f"Not a directory: '{value}'")

        return True


class UrlField(Field):
    def validate(self, value):
        result = urllib.parse.urlparse(value)

        if not result.scheme:
            raise ValidationError(f"no scheme provided for url: {value}")
        if not result.path:
            raise ValidationError(f"no path provided for url: {value}")
        if not result.netloc:
            raise ValidationError(f"no domain provided for url: {value}")

        return True
