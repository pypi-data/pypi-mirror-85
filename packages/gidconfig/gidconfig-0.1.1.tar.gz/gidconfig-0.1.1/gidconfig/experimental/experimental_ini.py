# region [Imports]

# * Standard Library Imports -->
from datetime import datetime, timedelta
from functools import partial
from collections import namedtuple
from configparser import ConfigParser

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from gidconfig.experimental.experimental_abstract import GidAttConfigAbstract

# endregion[Imports]

__updated__ = '2020-11-14 01:41:32'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class GidAttConfigIni(GidAttConfigAbstract):
    forbidden_section_chars = [' ', '.', '-']
    typus_tuple = namedtuple('TypusTuple', ['typus', 'prefix', 'transformer'])

    def __init__(self, config_file):
        super().__init__(config_file)
        self.configparser = ConfigParser(allow_no_value=True, interpolation=None)
        self.list_seperator = ','
        self.typus_data = {'list': self.typus_tuple(list, '-LIST-', self._list_transformer),
                           'set': self.typus_tuple(set, '-SET-', self._set_transformer),
                           'tuple': self.typus_tuple(tuple, '-TUPLE-', self._tuple_transformer),
                           'float': self.typus_tuple(float, '-FLOAT-', self._float_transformer),
                           'datetime': self.typus_tuple(datetime, '-DATETIME-', self._datetime_transform),
                           'timedelta': self.typus_tuple(timedelta, '-TIMEDELTA-', self._timedelta_transform)}

    def load(self):
        for added_attribute in self.added_attributes:
            delattr(self, added_attribute)
        self.added_attributes = []
        self.configparser.read(self.config_file)
        for section in self.configparser.sections():
            if any(forbidden_char in section for forbidden_char in self.forbidden_section_chars):
                raise AttributeError(f"forbidden character in section name '{section}'")
            setattr(self, section, {})
            self.added_attributes.append(section)
            setattr(self, 'set_' + section, partial(self._edit_dict_attribute, section))
            self.added_attributes.append('set_' + section)
            for option in self.configparser.options(section):
                _value = self.configparser.get(section, option)
                _value = self._check_convert_int(_value)
                _value = self._check_convert_boolean(_value)
                for _, typus_item in self.typus_data.items():
                    try:
                        if typus_item.prefix in _value:
                            _value = _value.replace(typus_item.prefix, '')
                            _value = typus_item.transformer(_value)
                    except TypeError:
                        pass

                getattr(self, section)[option] = _value

    def _list_transformer(self, in_value, direction='load'):
        if direction == "load":
            _out = in_value.strip().split(self.list_seperator)
            _out = list(map(self._strip_it, _out))
            _out = list(map(self._check_convert_int, _out))
            _out = list(map(self._check_convert_boolean, _out))
        elif direction == 'save':
            _item_string = ', '.join(map(str, in_value))
            _out = self.typus_data['list'].prefix + ' ' + _item_string
        return _out

    @ staticmethod
    def _check_convert_boolean(item):
        _bool_true_values = ['yes', 'true', 'on']
        _bool_false_values = ['no', 'false', 'off']
        try:
            if any(btrue.casefold() == item.casefold() for btrue in _bool_true_values):
                return True
            elif any(bfalse.casefold() == item.casefold() for bfalse in _bool_false_values):
                return False
            else:
                return item
        except AttributeError:
            return item

    @ staticmethod
    def _strip_it(item):
        return item.strip()

    @ staticmethod
    def _check_convert_int(item):
        try:
            _out = int(item)
        except ValueError:
            _out = item
        return _out

    @ staticmethod
    def _set_transformer(item, direction='load'):
        pass

    @ staticmethod
    def _float_transformer(item, direction='load'):
        pass

    @ staticmethod
    def _tuple_transformer(item, direction='load'):
        pass

    def _datetime_transform(self, item, direction='load'):
        if direction == 'load':
            return datetime.strptime(item.strip(), "%Y-%m-%dT%H:%M:%S")
        elif direction == 'save':
            return self.typus_data['datetime'].prefix + ' ' + item.isoformat(timespec='seconds')

    def _timedelta_transform(self, item, direction='load'):
        if direction == 'load':
            _neg = ''
            if 'negative' in item:
                _neg = '-'
            _match = self.timedelta_regex.search(item.replace('negative', '').strip())

            _out = {key: int(_neg + value) for key, value in _match.groupdict().items()}

            return timedelta(**_out)

        elif direction == 'save':
            _total_seconds = item.total_seconds()
            _neg = 'negative ' if str(_total_seconds).startswith('-') else ''
            _total_seconds = abs(_total_seconds)
            _days, remainder = divmod(_total_seconds, 60 * 60 * 24)
            _hours, remainder = divmod(remainder, 60 * 60)
            _minutes, _seconds = divmod(remainder, 60)
            _out = self.typus_data['timedelta'].prefix + ' '
            return _out + self.timedelta_template.format(negative=_neg, days=round(_days), hours=round(_hours), minutes=round(_minutes), seconds=round(_seconds))

    def save(self):
        with open(self.config_file, 'w') as confile:
            self.configparser.write(confile)
        self.load()

    def _edit_dict_attribute(self, section, **kwargs):
        for key, value in kwargs.items():
            for _, typus_item in self.typus_data.items():
                if isinstance(value, typus_item.typus):
                    value = typus_item.transformer(value, direction='save')
            self.configparser.set(section, key, str(value))
        self.save()

    def new_section(self, section_name, **options):
        self.configparser.add_section(section_name)
        self._edit_dict_attribute(section_name, **options)
        self.save()

    def register_new_typus(self, name, compare_type, prefix, transformer):
        self.typus_data[name] = self.typus_tuple(compare_type, prefix, transformer)
        self.save()

# region[Main_Exec]


if __name__ == '__main__':
    pass
# endregion[Main_Exec]
