from ctypes import (c_uint8, c_uint16, c_uint32, c_int64, c_uint64, c_void_p, c_size_t, Structure, Union, CDLL, POINTER,
                    pointer, c_char_p)
import typing

from .zydis_types import Decoder, Instruction, Operand
from .types import Feature, MachineMode, AddressWidth, Status, DecoderMode, CpuFlagAction
from.generate_types import Mnemonic


_zydis = CDLL('libZydis.dylib')

# TODO See if byref can be used in these case

_zydis.ZydisGetVersion.argtypes = ()
_zydis.ZydisGetVersion.restype = c_uint64

_zydis.ZydisIsFeatureEnabled.argtypes = (c_uint8,)
_zydis.ZydisIsFeatureEnabled.restype = c_uint8

_zydis.ZydisDecoderInit.argtypes = (POINTER(Decoder), c_uint8, c_uint8)
_zydis.ZydisDecoderInit.restype = c_uint32

_zydis.ZydisDecoderEnableMode.argtypes = (POINTER(Decoder), c_uint8, c_uint8)
_zydis.ZydisDecoderEnableMode.restype = c_uint32

_zydis.ZydisDecoderDecodeBuffer.argtypes = (POINTER(Decoder), c_void_p, c_size_t, c_uint64, POINTER(Instruction))
_zydis.ZydisDecoderDecodeBuffer.restype = c_uint32

_zydis.ZydisCalcAbsoluteAddress.argtypes = (POINTER(Instruction), POINTER(Operand), POINTER(c_uint64))
_zydis.ZydisCalcAbsoluteAddress.restype = c_uint32

_zydis.ZydisGetAccessedFlagsByAction.argtypes = (POINTER(Instruction), c_uint8, POINTER(c_uint32))
_zydis.ZydisGetAccessedFlagsByAction.restype = c_uint32

_zydis.ZydisMnemonicGetString.argtypes = (c_uint64,)
_zydis.ZydisMnemonicGetString.restype = c_char_p


def GetVersion() -> typing.Tuple[int, int , int, int]:
    version_number = _zydis.ZydisGetVersion()

    major = (version_number & 0xFFFF000000000000) >> 48
    minor = (version_number & 0x0000FFFF00000000) >> 32
    patch = (version_number & 0x00000000FFFF0000) >> 16
    build = (version_number & 0x000000000000FFFF)

    return major, minor, patch, build


def IsFeatureEnabled(feature: Feature) -> bool:
    return bool(_zydis.ZydisIsFeatureEnabled(feature))


def DecoderInit(machine_mode: MachineMode, address_width: AddressWidth) -> typing.Tuple[Status, Decoder]:
    decoder = Decoder()
    status = Status(_zydis.ZydisDecoderInit(pointer(decoder), machine_mode, address_width))

    return (status, decoder)


def DecoderEnableMode(decoder: Decoder, mode: DecoderMode, enabled: bool) -> Status:
    return Status(_zydis.ZydisDecoderEnableMode(pointer(decoder), mode, enabled))


def DecoderDecodeBuffer(decoder: Decoder, buffer: typing.Sequence[c_uint8], length: int, instructionPointer: int)\
        -> typing.Tuple[Status, Instruction]:
    instruction = Instruction()
    status = Status(_zydis.ZydisDecoderDecodeBuffer(pointer(decoder), buffer, length, instructionPointer,
                                                    pointer(instruction)))

    return (status, instruction)


def CalcAbsoluteAddress(instruction: Instruction, operand: Operand) -> typing.Tuple[Status, int]:
    address = c_uint64()
    status = Status(_zydis.ZydisCalcAbsoluteAddress(pointer(instruction), operand, address))

    return (status, address.value)


def GetAccessedFlagsByAction(instruction: Instruction, action: CpuFlagAction) -> typing.Tuple[Status, int]:
    flags = c_uint32()
    status = Status(_zydis.ZydisGetAccessedFlagsByAction(pointer(instruction), action, flags))

    return (status, flags)

def MnemonicGetString(mnemonic: Mnemonic) -> str:
    string = _zydis.ZydisMnemonicGetString(mnemonic.value)
    return string.decode('ascii') if string is not None else ''
