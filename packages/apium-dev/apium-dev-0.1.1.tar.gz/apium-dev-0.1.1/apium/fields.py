from collections import OrderedDict
from datetime import datetime

ORDER_DEFAULT = 1000000


class Undefined:
    """
    Type for api-field if field does not exist in json.
    This field is not None, exactly does not exist.
    """

    # TODO: add __slots__ to lite class
    pass


UNDEF = Undefined()


class BaseField:
    pass


class Field(BaseField):
    def __init__(
        self,
        validators=None,
        required=False,
        nullable=True,
        default=UNDEF,
        order=ORDER_DEFAULT,
    ):
        self.value = UNDEF
        if validators is not None and not isinstance(validators, list):
            raise TypeError('validators is not iterable')
        self.validators = validators if validators else []
        self.required = required
        self.nullable = nullable
        self.default = default
        self.order = order

    def __get__(self, obj, cls):
        return self.value

    def __set__(self, obj, value):
        self.method_cache = obj.method_cache
        self.value = value
        if self.value == UNDEF and self.default != UNDEF:
            if callable(self.default):
                self.value = self.default()
            else:
                self.value = self.default
        self._validate_first()
        self.value = self.format()
        self._validate_next()

    def format(self):
        return self.value

    def _validate_first(self):
        if self.required and self.value == UNDEF:
            raise ValueError('Field is required')
        if not self.nullable and self.value is None:
            raise ValueError('Expected not null')

    def _validate_next(self):
        if self.value not in [None, UNDEF]:
            for validator in self.validators:
                validator(self.value)
            self.validate()

    def validate(self):
        """Override in class-child"""
        pass


class Int(Field):
    def format(self):
        try:
            return int(float(self.value))
        except (ValueError, TypeError):
            return self.value

    def validate(self):
        super(Int, self).validate()
        if not isinstance(self.value, int):
            raise ValueError('Expected int')


class Float(Field):
    def format(self):
        try:
            return float(self.value)
        except (ValueError, TypeError):
            return self.value

    def validate(self):
        super(Float, self).validate()
        if not isinstance(self.value, float):
            raise ValueError('Expected float')


class Str(Field):
    def __init__(
        self,
        blank=True,
        strip=True,
        cut=None,
        min_lenght=None,
        max_lenght=None,
        *args,
        **kwargs
    ):
        super(Str, self).__init__(*args, **kwargs)
        self.blank = blank
        self.strip = strip
        self.cut = cut
        self.min_lenght = min_lenght
        self.max_lenght = max_lenght

    def format(self):
        value = self.value
        if value not in [None, UNDEF]:
            if not isinstance(value, (str, int, float)):
                raise TypeError('Expected str')
            value = str(value)
            if self.strip:
                value = value.strip()
            if self.cut is not None:
                value = value[:self.cut]
        return value

    def validate(self):
        value = self.value
        if not self.blank and value == '':
            raise ValueError('Expected not blank')
        value_len = len(value)
        min_lenght = self.min_lenght
        max_lenght = self.max_lenght
        if min_lenght is not None and value_len < min_lenght:
            raise ValueError(f'Str min lenght must be {min_lenght}')
        if max_lenght is not None and value_len > max_lenght:
            raise ValueError(f'Str max lenght must be {max_lenght}')


class Dict(Field):
    def __init__(self, blank=True, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self.blank = blank

    def validate(self):
        if not isinstance(self.value, dict):
            raise TypeError('Expected dict (json)')
        if not self.blank and self.value == {}:
            raise ValueError('Expected not blank')


class Email(Str):
    def validate(self):
        super(Email, self).validate()
        if '@' not in self.value:
            raise ValueError('Expected email')


class Date(Str):
    def format(self):
        self.value = super(Date, self).format()
        try:
            return datetime.strptime(self.value, '%Y-%m-%d')
        except Exception:
            raise TypeError('Expected date %Y-%m-%d')


class List(Field):
    def __init__(self, blank=True, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.blank = blank

    def validate(self):
        if not isinstance(self.value, list):
            raise ValueError('Expected list')
        if not self.blank and self.value == []:
            raise ValueError('Expected not blank')


class MetaObjField(type):
    def __new__(self, name, bases, namespace):
        cls = super(MetaObjField, self).__new__(self, name, bases, namespace)
        cls._fields = getattr(cls, '_fields', {})
        cls._fields.update({
            key: val.order
            for key, val in namespace.items()
            if isinstance(val, BaseField)
        })
        cls._fields = OrderedDict(
            sorted(cls._fields.items(), key=lambda item: item[1])
        )
        return cls


class Obj(BaseField, metaclass=MetaObjField):
    def __init__(
        self,
        validators=None,
        required=False,
        nullable=True,
        blank=True,
        default=UNDEF,
        order=ORDER_DEFAULT,
        fields=None,
    ):
        print('class objfield init')
        self.value = UNDEF
        if validators is not None and not isinstance(validators, list):
            raise TypeError('validators is not iterable')
        self.validators = validators if validators else []
        self.required = required
        self.nullable = nullable
        self.blank = blank
        self.default = default
        self.order = order

        if isinstance(fields, dict):
            self._fields = {}
            for key, val in fields.items():
                setattr(type(self), key, val)
                if isinstance(val, BaseField):
                    self._fields.update({key: val.order})
            self._fields = OrderedDict(
                sorted(self._fields.items(), key=lambda item: item[1])
            )

    def __set__(self, obj, value):
        self.method_cache = obj.method_cache
        self.value = value
        if self.value == UNDEF and self.default != UNDEF:
            if callable(self.default):
                self.value = self.default()
            else:
                self.value = self.default
        self._validate_first()
        self.value = self.format()

        print('O F {}'.format(self._fields))
        obj_value = {} if self.value == UNDEF else self.value
        for key in self._fields:
            try:
                print('OBJF - {} : {}'.format(key, obj_value.get(key, UNDEF)))
                setattr(self, key, obj_value.get(key, UNDEF))
                validator = getattr(self, 'validate_{}'.format(key), None)
                if validator:
                    validator(getattr(self, key))
            except Exception as exc:
                raise ValueError('{}: {}'.format(key, exc))

        self._validate_next()

    def format(self):
        return self.value

    def _validate_first(self):
        if self.required and self.value == UNDEF:
            raise ValueError('Field is required')
        if not self.nullable and self.value is None:
            raise ValueError('Expected not None')
        if self.value == UNDEF:
            self.value = {}

    def _validate_next(self):
        if self.value is not {}:
            for validator in self.validators:
                validator(self)
            self.validate()

    def validate(self):
        # TODO: check is dict before set subfields
        if not isinstance(self.value, dict):
            raise TypeError('Expected dict (json)')
        if not self.blank and self.value == {}:
            raise ValueError('Expected not blank')
