# region [Imports]

# * Standard Library Imports -->
from functools import partial

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from gidconfig.utility.functions import loadjson
from gidconfig.experimental.experimental_abstract import GidAttConfigAbstract

# endregion[Imports]

__updated__ = '2020-11-14 16:05:22'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class GidAttConfigJson(GidAttConfigAbstract):
    def __init__(self, config_file):
        super().__init__(config_file)

    def load(self):
        _config_dict = loadjson(self.config_file)
        for section, value in _config_dict.items():
            setattr(self, section, value)
            self.added_attributes.append(section)
            setattr(self, 'set_' + section, partial(self._edit_dict_attribute, section))
            self.added_attributes.append('set_' + section)


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
