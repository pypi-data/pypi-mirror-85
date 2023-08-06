"""Automatic determination of local ChemStation paths on this system"""
import os
import re
import time
import configparser
import pathlib
import logging
import threading
from typing import Union, List, Tuple

logger = logging.getLogger(__name__)


# acquiring regex
_acq_re = re.compile(
    'CURRDATAFILE:(?P<file_number>\d+)\|(?P<file_name>[^\n]+)'
)


class AcquisitionSearch:
    # lock if acquisition file is found
    _located = threading.Event()

    data_paths: List[pathlib.Path] = []

    instances: List['AcquisitionSearch'] = []

    # flag to indicate whether the "start all monitors" flag has been set
    _all_started: bool = False

    def __init__(self,
                 data_path: Union[str, pathlib.Path],
                 cycle_time: float = 1.,
                 always_search: bool = False,
                 autostart: bool = True,
                 ):
        """
        An Agilent ChemStation data path monitoring class. This class will monitor for sequence flags and will live-update
        acquiring status, the current data file, and the current sample number.

        :param data_path: file path to the data directory
        :param cycle_time: cycle time to check for updates to the file
        :param always_search: flag to enable continuous searching, even when a file has been located in another instance
        :param autostart: flag to control autostart (if the all started flag is set, setting this to True will prevent
            the monitor thread from starting and require the user to start the thread manually)
        """
        if isinstance(data_path, pathlib.Path) is False:
            data_path = pathlib.Path(data_path)
        if data_path.is_absolute() is False:
            data_path = data_path.absolute()
        if data_path in self.data_paths:
            raise ValueError(f'the path {data_path} is already being searched')
        self.data_paths.append(data_path)
        self.data_parent = data_path
        self._acquiring_path: pathlib.Path = None
        self._current_number: int = None
        self._current_file: str = None
        self.cycle_time = cycle_time
        self._monitor_thread = threading.Thread(
            target=self._acquiring_monitor,
            daemon=True,
        )
        self._killswitch = threading.Event()
        self.instances.append(self)
        self.always_search = always_search
        if self._all_started and autostart:
            self._monitor_thread.start()

    def __eq__(self, other: Union[str, pathlib.Path, 'AcquisitionSearch']):
        if isinstance(other, AcquisitionSearch):
            return self.data_parent == other.data_parent
        elif type(other) is str:
            return str(self.data_parent) == other
        elif isinstance(other, pathlib.Path):
            return self.data_parent == other
        else:
            return False

    def __str__(self):
        out = f'{self.data_parent}'
        if self.acquiring is True:
            out += ' ACQUIRING'
        return out

    def __repr__(self):
        return f'{self.__class__.__name__} {self.data_parent} {"ACQUIRING" if self.acquiring else ""}'

    @property
    def acquiring_path(self) -> pathlib.Path:
        """path to the acquiring file"""
        return self._acquiring_path

    @property
    def current_number(self) -> int:
        """current acquiring number indicated in acquiring file"""
        return self._current_number

    @property
    def current_file(self) -> pathlib.Path:
        """currently acquiring file indicated in acquiring file"""
        if self._current_file is not None:
            return self._acquiring_path.parent / self._current_file

    @property
    def acquiring(self) -> bool:
        """whether acquiring is indicated in the target directory"""
        return self.acquiring_path is not None

    @property
    def subdirectories(self) -> List[pathlib.Path]:
        """subdirectories of the root folder"""
        return [
            directory
            for directory in self.data_parent.iterdir()
            if directory.is_dir()
        ]

    @property
    def newsorted_subdirectories(self) -> List[pathlib.Path]:
        """subdirectories of the root path sorted by date modified in newest to oldest order"""
        return sorted(
            self.subdirectories,
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )

    def find_acquiring(self) -> Union[pathlib.Path, None]:
        """
        Locates ACQUIRING.TXT files in the directory. This file appears when ChemStation is acquiring
        a sequence. The search prioritizes newer subdirectories.

        :return: path to acquiring.txt (if found)
        """
        in_current_dir = list(self.data_parent.glob('ACQUIRING.TXT'))
        if len(in_current_dir) > 0:
            return in_current_dir[0]
        for subdir in self.newsorted_subdirectories:
            try:
                return next(subdir.glob('**/ACQUIRING.TXT'))
            except StopIteration:
                continue

    @staticmethod
    def current_num_and_file(path: Union[str, pathlib.Path]) -> Tuple[int, str]:
        """
        Returns the current number in the sequence and the name of the data file being acquired.

        :param path: path to parse
        :return: current file number, current file name
        """
        with open(path, 'rt', encoding='utf16') as f:
            contents = f.read()
        match = _acq_re.search(contents)
        if match is None:
            raise ValueError(f'The contents of ACQUIRING.TXT could not be parsed: {contents}')
        return (
            int(match.group('file_number')),
            match.group('file_name')
        )

    def _clear_acquiring(self):
        """clears acquiring status if the instance is currently acquiring"""
        if self._acquiring_path is not None:
            self._acquiring_path = None
            self._located.clear()

    def _acquiring_monitor(self):
        """
        Searches for and monitors acquiring files in the target directory.
        """
        while True:
            if self._killswitch.isSet():
                self._clear_acquiring()
                break

            # current instance does not have a path AND always search or another instance has not found a file
            if self._acquiring_path is None and self.always_search or not self._located.is_set():
                # logger.debug('attempting to locate acquiring file')
                acquiring_path = self.find_acquiring()
                # if there is one file, update
                if acquiring_path is not None:
                    logger.info('ACQUIRING.TXT located')
                    if self._located.is_set():
                        raise ValueError(
                            f'multiple matches for ACQUIRING.TXT were found in the chemstation data directories. '
                            f'This usually results when ChemStation did not exit cleanly. Please locate and '
                            f'remove the old acquiring file. '
                        )
                    self._located.set()  # indicate that a file has been found
                    self._acquiring_path = acquiring_path
                    continue

                # if no files
                else:
                    # logger.debug('no acquiring file located')
                    continue

            # if a file was previously located, process
            elif self._acquiring_path is not None:
                # if the file has disappeared, set to None and clear flag
                if self._acquiring_path.is_file() is False:
                    logger.info('ACQUIRING.TXT disappeared')
                    self._acquiring_path = None
                    self._located.clear()  # clear location flag
                    continue

                # todo verify that this always works
                # parse and retrieve current number and file
                try:
                    self._current_number, self._current_file = self.current_num_and_file(self._acquiring_path)
                except (ValueError, PermissionError) as e:
                    logger.debug(e)
                    self._current_number = None
                    self._current_file = None

            # wait cycle time
            time.sleep(self.cycle_time)

    def start_monitor(self):
        """starts the acquiring monitor thread"""
        if self._monitor_thread.is_alive() is False:
            logger.info(f'starting acquiring monitor on {self.data_parent}')
            self._monitor_thread.start()

    def kill_monitor(self):
        """cleanly terminates the monitor thread"""
        self._killswitch.set()
        # wait for clean exit
        while self._monitor_thread.is_alive():
            time.sleep(0.01)

    def parent_of_path(self, path: Union[str, pathlib.Path]) -> bool:
        """
        Checks whether the provided path is a parent of the instance's path. (The instance's path is a subfolder of
        the provided path.

        :param path: pathlike
        :return: provided path is parent
        """
        if isinstance(path, pathlib.Path) is False:
            path = pathlib.Path(path)
        path = path.absolute()
        if len(path.parts) < len(self.data_parent.parts):
            return path.parts == self.data_parent.parts[:len(path.parts)]
        return False

    @classmethod
    def start_monitoring_all_paths(cls):
        """starts the monitor thread on all data paths"""
        if cls._all_started is False:
            logger.debug('starting all monitor threads')
            cls._all_started = True
            for inst in cls.instances:
                inst.start_monitor()

    @classmethod
    def kill_all_monitors(cls):
        """terminates all monitor threads"""
        logger.debug('terminating all monitor threads')
        for inst in cls.instances:
            inst.kill_monitor()

    @classmethod
    def get_by_path(cls,
                    path: Union[str, pathlib.Path],
                    always_search: bool = False,
                    autostart: bool = True,
                    ) -> 'AcquisitionSearch':
        """
        Retrieves an instance by path. If the path is already being monitored, the existing instance is returned.
        Otherwise creates a new instance.

        :param path: pathlike
        :param always_search: flag to enable continuous searching, even when a file has been located in another instance
        :param autostart: flag to control autostart (if the all started flag is set, setting this to True will prevent
            the monitor thread from starting and require the user to start the thread manually)
        """
        if isinstance(path, pathlib.Path) is False:
            path = pathlib.Path(path)
        if path.is_absolute() is False:
            path = path.absolute()
        if cls.parent_of_any_path(path):
            raise ValueError(f'the provided path "{path}" is a parent of one or more AcquisitionSearch paths')
        elif path in cls.data_paths:
            # if path already exists, return
            for inst in cls.instances:
                if inst.data_parent == path:
                    return inst
        # otherwise, create a new data monitor
        return cls(path, always_search=always_search, autostart=autostart)

    @classmethod
    def parent_of_any_path(cls, path: Union[str, pathlib.Path]) -> bool:
        """
        Checks whether the provided path is a parent of any path instance.

        :param path: path to check
        :return: parent of any path
        """
        if isinstance(path, pathlib.Path) is False:
            path = pathlib.Path(path)
        return any([
            inst.parent_of_path(path)
            for inst in cls.instances
        ])

    @classmethod
    def sequence_is_running(cls) -> bool:
        """True if any acquisition search instance is aware of an acquiring flag file"""
        # todo classproperty
        return cls._located.is_set()

    @classmethod
    def acquiring_instance(cls) -> 'AcquisitionSearch':
        """retrieve the currently acquiring instance"""
        # todo classproperty
        if cls._located.is_set() is False:
            raise ValueError(f'No acquisition flag file has been identified')
        for inst in cls.instances:
            if inst.acquiring is True:
                return inst

    @classmethod
    def acquiring_instance_num_and_file(cls) -> Tuple[int, pathlib.Path]:
        """
        Retrieves the current number and file name of the currently acquiring path

        :return: sample number, sample path
        """
        # todo classproperty
        currently_acquiring = cls.acquiring_instance()
        return currently_acquiring.current_number, currently_acquiring.current_file

    @classmethod
    def wait_for_acquiring(cls,
                           timeout: float = None,
                           cycle_time: float = 0.1,
                           ) -> Union['AcquisitionSearch', None]:
        """
        Waits for the acquiring flag file to appear in registered instances. Once found, the acquiring instance is
        returned.

        :param timeout: Optional timeout to prevent eternal waits
        :param cycle_time: cycle time for checks
        :return: acquiring instance once located
        """
        logger.info(f'waiting for ChemStation acquisition flag file {f"timeout: {timeout} s" if timeout else ""}')
        if timeout is not None:
            timeout = time.time() + timeout
        # wait for appearance of file
        while cls._located.is_set() is False:
            if timeout and time.time() > timeout:
                logger.info('timeout reached, no acquiring flag file was identified')
                return  # return None if timeout is reached
            time.sleep(cycle_time)
        logger.info(f'acquiring instance located')
        return cls.acquiring_instance()


class ChemStationConfig:
    registered_chemstations: List['ChemStationConfig'] = []

    DEFAULT_INI_LOCATION = 'C:\\ProgramData\\Agilent Technologies\\ChemStation\\ChemStation.ini'

    def __init__(self,
                 data_path: Union[str, pathlib.Path] = None,
                 core_path: Union[str, pathlib.Path] = None,
                 method_path: Union[str, pathlib.Path] = None,
                 sequence_path: Union[str, pathlib.Path] = None,
                 version: str = None,  # todo accept packaging version
                 number: int = None,
                 ):
        """
        A class for managing pathing attributes for ChemStation instances installed on the current system.

        :param data_path: default data path for the installation
        :param core_path: core installation path (location of the "CORE" directory)
        :param method_path: path to methods
        :param sequence_path: path to sequences
        :param version: ChemStation version
        :param number: published ChemStation number
        """
        self._core = None
        self._data = None
        self._method = None
        self._sequence = None
        self.core_path = core_path
        self.data_path = data_path
        self.method_path = method_path
        self.sequence_path = sequence_path
        self.version: Union[str, None] = version
        self.registered_chemstations.append(self)
        self.number = number

    @property
    def core_path(self) -> pathlib.Path:
        """path to the CORE installation folder"""
        return self._core

    @core_path.setter
    def core_path(self, value: Union[str, pathlib.Path]):
        if value is not None:
            if isinstance(value, pathlib.Path) is False:
                value = pathlib.Path(value)
            self._core = value

    @property
    def data_path(self) -> AcquisitionSearch:
        """path to the default data directory"""
        return self._data

    @data_path.setter
    def data_path(self, value: Union[str, pathlib.Path]):
        if value is not None:
            self._data = AcquisitionSearch.get_by_path(value)

    @property
    def method_path(self) -> pathlib.Path:
        """path to the method save directory"""
        return self._method

    @method_path.setter
    def method_path(self, value: Union[str, pathlib.Path]):
        if value is not None:
            if isinstance(value, pathlib.Path) is False:
                value = pathlib.Path(value)
            self._method = value

    @property
    def sequence_path(self) -> pathlib.Path:
        """path to the sequence save directory"""
        return self._sequence

    @sequence_path.setter
    def sequence_path(self, value: Union[str, pathlib.Path]):
        if value is not None:
            if isinstance(value, pathlib.Path) is False:
                value = pathlib.Path(value)
            self._sequence = value

    @classmethod
    def construct_from_ini(cls, ini_path: Union[str, pathlib.Path] = None) -> List['ChemStationConfig']:
        """
        Constructs ChemStation config instances as defined in the provided INI file. If no INI is provided, the
        default ChemStation INI location will be used.

        :param ini_path: path to INI file location. The provided INI file is expected to have the structure used by
            ChemStation ini files.
        :return: instances created via the ini
        """
        def get_from_ini(section, *keys, default=None):
            """
            Attempts to retrieve the keys in order from the provided section. If no keys exist, the default value is
            returned.

            :param section: section name
            :param keys: keys to attempt to retrieve from the section in order
            :param default: default value to return if not found
            """
            for key in keys:
                try:
                    return configuration.get(section, key)
                except configparser.NoOptionError:
                    continue
            logger.error(f'no provided keys were defined in the section {section} ({keys})')
            return default

        if ini_path is None:
            ini_path = cls.DEFAULT_INI_LOCATION
        ini_path = pathlib.Path(ini_path)
        if ini_path.is_file() is False:
            logger.debug(f'the provided INI file "{ini_path}" does not exist')
            return []  # if this file does not exist, do not register
        configuration = configparser.ConfigParser()
        result = configuration.read(
            ini_path,
            encoding='utf16',
        )
        version = configuration.get('PCS', 'REV')
        inst = 1
        out = []
        while True:
            try:
                pcsnum = f'PCS,{inst}'
                out.append(cls(
                    core_path=get_from_ini(pcsnum, '_EXEPATH$'),
                    method_path=get_from_ini(pcsnum, '_METHPATH$', '_CONFIGMETPATH$'),
                    sequence_path=get_from_ini(pcsnum, '_SEQPATH$', '_CONFIGSEQPATH$'),
                    data_path=get_from_ini(pcsnum, '_DATAPATH$'),
                    version=version,
                    number=inst,
                ))
                inst += 1
            except configparser.NoSectionError:
                break
        logger.debug(f'identified {len(cls.registered_chemstations)} from INI file')
        return out

    @classmethod
    def construct_from_env(cls, env_name: str = 'hplcfolder'):
        """
        Constructs an instance from an environment variable name. If the environment variable is not set, no action
        is taken.

        :param env_name: environment variable name
        """
        path = os.environ.get(env_name)
        if path is not None:
            try:
                return cls.get_by_data_path(path)
            except ValueError:
                return cls(
                    data_path=path,
                )

    @classmethod
    def get_by_data_path(cls, path: Union[str, pathlib.Path]) -> 'ChemStationConfig':
        """
        Retrieves an instance by its data path. If the data path is not associated with an instance, an error is raised.

        :param path: path to check for
        :return: chemstation config instance
        """
        for inst in cls.registered_chemstations:
            if inst.data_path == path:
                return inst
        raise ValueError(f'the path "{path}" is not associated with any instances')
