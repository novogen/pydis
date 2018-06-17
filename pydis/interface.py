import os
import sys
from ctypes import c_uint8, c_uint32, c_uint64, c_void_p, c_size_t, CDLL, POINTER, pointer, c_char_p, c_int16
import typing

from .zydis_types import Decoder, Instruction, Operand, Formatter
from .types import (Feature, MachineMode, AddressWidth, Status, DecoderMode, CpuFlagAction, FormatterStyle,
                    FormatterProperty, RegisterClass)
from.generate_types import Mnemonic, Register


if sys.platform == 'darwin':
    _library_name = 'libZydis.dylib'
elif sys.platform in ('cygwin', 'win32'):
    _library_name = 'Zydis.dll'
else:
    _library_name = 'libZydis.so'

_zydis = CDLL(os.path.join(os.path.dirname(__file__), 'lib', _library_name))

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

_zydis.ZydisRegisterGetId.argtypes = (c_uint8,)
_zydis.ZydisRegisterGetId.restype = c_int16

_zydis.ZydisRegisterGetClass.argtypes = (c_uint8,)
_zydis.ZydisRegisterGetClass.restype = (c_uint8)

_zydis.ZydisRegisterGetString.argtypes = (c_uint8,)
_zydis.ZydisRegisterGetString.restype = c_char_p

_zydis.ZydisFormatterInit.argtypes = (POINTER(Formatter), c_uint8)
_zydis.ZydisFormatterInit.restype = c_uint32

_zydis.ZydisFormatterSetProperty.argtypes = (POINTER(Formatter), c_uint8, c_void_p)
_zydis.ZydisFormatterSetProperty.restype = c_uint32

_zydis.ZydisFormatterSetHook.argtypes = (POINTER(Formatter), c_uint8, POINTER(c_void_p))
_zydis.ZydisFormatterSetHook.restype = c_uint32

_zydis.ZydisFormatterFormatInstruction.argtypes = (POINTER(Formatter), POINTER(Instruction), c_char_p, c_uint32)
_zydis.ZydisFormatterFormatInstruction.restype = c_uint32

_zydis.ZydisFormatterFormatInstructionEx.argtypes = (POINTER(Formatter), POINTER(Instruction), c_char_p, c_uint32,
                                                     c_void_p)
_zydis.ZydisFormatterFormatInstructionEx.restype = c_uint32

_zydis.ZydisFormatterFormatOperand.argtypes = (POINTER(Formatter), POINTER(Instruction), c_uint8, c_char_p, c_uint32)
_zydis.ZydisFormatterFormatOperand.restype = c_uint32

_zydis.ZydisFormatterFormatOperandEx.argtypes = (POINTER(Formatter), POINTER(Instruction), c_uint8, c_char_p, c_uint32,
                                                 c_void_p)
_zydis.ZydisFormatterFormatOperandEx.restype = c_uint32


def GetVersion() -> typing.Tuple[int, int, int, int]:
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


def RegisterGetId(register: Register) -> int:
    return _zydis.ZydisRegisterGetId(register)


def RegisterGetClass(register: Register) -> RegisterClass:
    return RegisterClass(_zydis.ZydisRegisterGetClass(register))


def RegisterGetString(register: Register) -> str:
    string = _zydis.ZydisRegisterGetString(register)
    return string.decode('ascii') if string is not None else ''


def FormatterInit(style: FormatterStyle = FormatterStyle.Intel) -> typing.Tuple[Status, Formatter]:
    formatter = Formatter()
    status = Status(_zydis.ZydisFormatterInit(pointer(formatter), style))

    return (status, formatter)


def FormatterSetProperty(formatter: Formatter, property: FormatterProperty, value: int) -> Status:
    return Status(_zydis.ZydisFormatterSetProperty(pointer(formatter), property, value))


def FormatterFormatInstruction(formatter: Formatter, instruction: Instruction) -> typing.Tuple[Status, str]:
    buffer = b'\x00' * 128
    status = Status(_zydis.ZydisFormatterFormatInstruction(pointer(formatter), pointer(instruction),
                                                           buffer, len(buffer)))
    buffer = buffer.decode('ascii').partition('\x00')[0] if status == Status.Success else ''
    return (status, buffer)


def FormatterFormatOperand(formatter: Formatter, instruction: Instruction, index: int) -> typing.Tuple[Status, str]:
    buffer = b'\x00' * 128
    status = Status(_zydis.ZydisFormatterFormatOperand(pointer(formatter), pointer(instruction), index, buffer,
                                                       len(buffer)))
    buffer = buffer.decode('ascii').partition('\x00')[0] if status == Status.Success else ''
    return (status, buffer)
