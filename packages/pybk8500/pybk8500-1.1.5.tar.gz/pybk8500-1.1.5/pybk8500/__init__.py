from pybk8500.__meta__ import version as __version__

from pybk8500.utils import parse_number
from pybk8500.parser import ChecksumError, MessageTypeError, Parser

# Why bother giving top level access to these classes?
# from pybk8500.field_types import Field, BytesField, StrField, \
#     IntField, Int8Field, Int16Field, Int32Field, FloatField, ScalarFloatField

from pybk8500.commands import \
    Message, CC_Commands, CV_Commands, CW_Commands, CR_Commands, \
    CommandStatus, SetRemote, SetRemoteOperation, RemoteOn, RemoteOff, LoadSwitch, LoadOn, LoadOff, \
    SetMaxVoltage, ReadMaxVoltage, SetMaxCurrent, ReadMaxCurrent, SetMaxPower, ReadMaxPower, \
    SetMode, ReadMode, \
    CC, SetCCModeCurrent, ReadCCModeCurrent, SetModeCurrent, ReadModeCurrent, \
    CV, SetCVModeVoltage, ReadCVModeVoltage, SetModeVoltage, ReadModeVoltage, \
    CW, SetCWModePower, ReadCWModePower, SetModePower, ReadModePower, \
    CR, SetCRModeResistance, ReadCRModeResistance, SetModeResistance, ReadModeResistance, \
    SetCCModeTransientCurrentAndTiming, ReadCCModeTransientParameters, \
    SetCVModeTransientVoltageAndTiming, ReadCVModeTransientParameters, SetCWModeTransientPowerAndTiming, \
    ReadCWModeTransientParameters, SetCRModeTransientResistanceAndTiming, ReadCRModeTransientParameters, \
    SelectListOperation, ReadListOperation, SetHowListsRepeat, ReadHowListsRepeat, SetNumberOfSteps, \
    ReadNumberOfSteps, SetOneStepCurrentAndTime, ReadOneStepCurrentAndTime, SetOneStepVoltageAndTime, \
    ReadOneStepVoltageAndTime, SetOneStepPowerAndTime, ReadOneStepPowerAndTime, SetOneStepResistanceAndTime, \
    ReadOneStepResistanceAndTime, SetListFileName, ReadListFileName, SetMemoryPartition, ReadMemoryPartition, \
    SaveListFile, RecallListFile, SetMinimumVoltage, ReadMinimumVoltage, SetTimerValueForLoadOn, \
    ReadTimerValueForLoadOn, SetTimerStateLoadOn, ReadTimerStateLoadOn, SetCommunicationAddress, \
    SetLocalControlState, SetRemoteSensingState, ReadRemoteSensingState, SelectTriggerSource, \
    ReadTriggerSource, TriggerElectronicLoad, SaveDCLoadSettings, RecallDCLoadSettings, SelectFunctionType, \
    GetFunctionType, ReadInput, ReadInputVoltageCurrentPowerState, GetProductInfo, ReadBarCode


try:
    from pybk8500.send_cmd import CommunicationManager
except (ImportError, Exception) as err:
    class CommunicationManager(object):
        error = err

        def __new__(cls, *args, **kwargs):
            raise EnvironmentError('Missing dependent "pyserial" or "continuous_threading" library! {}'
                                   .format(cls.error)) from cls.error

try:
    from pybk8500.run_profile import parse_number, ProfileManager, ProfileRow, Profile
except (ImportError, Exception) as err:
    class ProfileManager(object):
        error = err

        def __new__(cls, *args, **kwargs):
            raise EnvironmentError(str(cls.error)) from cls.error

    parse_number = ProfileManager
    ProfileRow = ProfileManager
    Profile = ProfileManager

try:
    from pybk8500.plot_csv import parse_csv, plot_csv_file, plot_csv_files
except (ImportError, Exception) as err:
    class parse_csv(object):
        error = err

        def __new__(cls, *args, **kwargs):
            raise EnvironmentError('Missing dependency "matplotlib"! '.format(cls.error)) from cls.error

    plot_csv_file = parse_csv
    plot_csv_files = parse_csv

try:
    from pybk8500.combine_csv import combine_csv_files
except (ImportError, Exception) as err:
    class combine_csv_files(object):
        error = err

        def __new__(cls, *args, **kwargs):
            raise EnvironmentError('Missing dependency "matplotlib"! '.format(cls.error)) from cls.error
