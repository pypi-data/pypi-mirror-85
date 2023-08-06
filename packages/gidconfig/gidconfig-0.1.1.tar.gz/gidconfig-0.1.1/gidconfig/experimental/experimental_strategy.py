# region [Imports]

# * Standard Library Imports -->
import os

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from gidconfig.utility.functions import pathmaker
from gidconfig.experimental.experimental_ini import GidAttConfigIni

# endregion[Imports]

__updated__ = '2020-11-14 01:44:46'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class ConfigStrategos:
    config_instances = {}
    ini_class = GidAttConfigIni
    json_class = None

    @classmethod
    def borrow_config(cls, config_file):
        config_file = pathmaker(config_file)
        _out = cls.config_instances.get(config_file, None)
        if _out is None:
            _out = cls._create_new_config_instance(config_file)
            cls.config_instances[config_file] = _out
        return _out

    @classmethod
    def _create_new_config_instance(cls, config_file):
        _extension = os.path.basename(config_file).split('.')[-1]
        if _extension == 'ini':
            _cfg = cls._new_ini_config(config_file)
        else:
            return None
        return _cfg

    @classmethod
    def _new_ini_config(cls, config_file):
        _new = cls.ini_class(config_file)
        _new.load()
        return _new

    @classmethod
    def _new_json_config(cls, config_file):
        pass

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
