# region [Imports]

# * Standard Library Imports -->

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from gidconfig.standard.classes import ConfigHandler
from gidconfig.utility.functions import pathmaker

# endregion [Imports]

__updated__ = '2020-11-14 15:10:42'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]

# region [Factories]


class ConfigRental:
    config_instances = {}
    appdata = None

    @classmethod
    def set_appdata(cls, appdata_object):
        cls.appdata = appdata_object

    @classmethod
    def get_config(cls, file_name, cfg_folder=None):
        if cls.appdata is None and cfg_folder is None:
            raise FileExistsError('appdata has not been set')
        _folder = cls.appdata['config'] if cfg_folder is None else pathmaker(cfg_folder)
        _file = pathmaker(_folder, file_name)

        _out_cfg = cls.config_instances.get(_file, None)
        if _out_cfg is None:
            _out_cfg = ConfigHandler(config_file=_file)
            cls.config_instances[_file] = _out_cfg
        return _out_cfg


# endregion [Factories]

# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
