# region [Imports]

# * Standard Library Imports -->
import re
from abc import ABC, abstractmethod

# * Gid Imports -->
import gidlogger as glog

# endregion[Imports]

__updated__ = '2020-11-14 15:58:38'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class GidAttConfigAbstract(ABC):
    def __init__(self, config_file):
        self.config_file = config_file
        self.timedelta_template = "{negative}days: {days}, hours: {hours}, minutes: {minutes}, seconds: {seconds}"
        self.timedelta_regex = re.compile(r"^days:\s*?(?P<days>\d*?),\s*?hours:\s*?(?P<hours>\d*?),\s*?minutes:\s*?(?P<minutes>\d*?),\s*?seconds:\s*?(?P<seconds>\d*?)$")
        self.typus_data = {}
        self.added_attributes = []

    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def save(self):
        ...

    @abstractmethod
    def new_section(self, section_name, **options):
        ...

    @abstractmethod
    def _edit_dict_attribute(self, section, **kwargs):
        ...

    # region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
