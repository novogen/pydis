import typing

from .types import (MachineMode, OperandType, OperandVisibility, OperandAction, OperandEncoding, ElementTypes,
                    MemOpType, InstructionEncoding, OpcodeMap, CpuFlag, MaskModes, BroadcastModes, RoundingModes,
                    SwizzleModes, ConversionMode, ExceptionClass, InstructionAttribute, Status)
from .zydis_types import (Instruction as RawInstruction, Operand as RawOperand, OperandMem, OperandPtr, OperandImm,
                          InstructionAvx as RawInstructionAvx, AvxMask as RawAvxMask, AvxBroadcast as RawAvxBroadcast,
                          InstructionMeta as RawInstructionMeta, InstructionRaw)
from .interface import MnemonicGetString, RegisterGetString, RegisterGetClass, RegisterGetId, CalcAbsoluteAddress
from .generate_types import Register as RegisterEnum, InstructionCategory, ISAExt, ISASet, Mnemonic
from .formatter import Formatter, default_formatter


class Register(int):
    def __new__(cls, value: int):
        return int.__new__(cls, RegisterEnum(value))

    def __str__(self) -> str:
        if hasattr(self, '_str'):
            return self._str

        self._str = RegisterGetString(self)
        return self._str

    def __repr__(self) -> str:
        return f'Register({repr(RegisterEnum(self))})'

    @property
    def value(self) -> int:
        return int(self)

    @property
    def name(self) -> str:
        return RegisterEnum(self).name

    @property
    def id(self) -> int:
        return RegisterGetId(self)

    @property
    def register_class(self) -> int:
        return RegisterGetClass(self)


class AvxMask:
    def __init__(self, avx_mask: RawAvxMask) -> None:
        self._avx_mask = avx_mask

    @property
    def mode(self) -> MaskModes:
        return MaskModes(self._avx_mask.mode)

    @property
    def register(self) -> Register:
        return Register(self._avx_mask.reg)

    @property
    def is_control_mask(self) -> bool:
        return bool(self._avx_mask.isControlMask)

    @property
    def underlying_type(self) -> RawAvxMask:
        return self._avx_mask


class AvxBroadcast:
    def __init__(self, avx_broadcast: RawAvxBroadcast) -> None:
        self._avx_broadcast = avx_broadcast

    @property
    def is_static(self) -> bool:
        return bool(self._avx_broadcast.isStatic)

    @property
    def mode(self) -> BroadcastModes:
        return BroadcastModes(self._avx_broadcast.mode)

    @property
    def underlying_type(self) -> RawAvxBroadcast:
        return self._avx_broadcast


class InstructionAvx:
    def __init__(self, instruction_avx: RawInstructionAvx) -> None:
        self._instruction_avx = instruction_avx

    @property
    def vector_length(self) -> int:
        return self._instruction_avx.vectorLength

    @property
    def mask(self) -> AvxMask:
        return AvxMask(self._instruction_avx.mask)

    @property
    def broadcast(self) -> AvxBroadcast:
        return AvxBroadcast(self._instruction_avx.broadcast)

    @property
    def rounding(self) -> RoundingModes:
        return RoundingModes(self._instruction_avx.rounding.mode)

    @property
    def swizzle(self) -> SwizzleModes:
        return SwizzleModes(self._instruction_avx.swizzle.mode)

    @property
    def conversion(self) -> ConversionMode:
        return ConversionMode(self._instruction_avx.conversion.mode)

    @property
    def has_sae(self) -> bool:
        return bool(self._instruction_avx.hasSAE)

    @property
    def has_eviction_hint(self) -> int:
        return bool(self._instruction_avx.hasEvictionHint)

    @property
    def underlying_type(self) -> RawInstructionAvx:
        return self._instruction_avx


class InstructionMeta:
    def __init__(self, instruction_meta: RawInstructionMeta) -> None:
        self._instruction_meta = instruction_meta

    @property
    def category(self) -> InstructionCategory:
        return InstructionCategory(self._instruction_meta.category)

    @property
    def isa_set(self) -> ISASet:
        return ISASet(self._instruction_meta.isaSet)

    @property
    def isa_ext(self) -> ISAExt:
        return ISAExt(self._instruction_meta.isaExt)

    @property
    def exception_class(self) -> ExceptionClass:
        return ExceptionClass(self._instruction_meta.exceptionClass)

    @property
    def underlying_type(self) -> RawInstructionMeta:
        return self._instruction_meta


class MemoryPointer:
    def __init__(self, memory_pointer: OperandPtr) -> None:
        self._memory_pointer = memory_pointer

    @property
    def segment(self) -> int:
        return self._memory_pointer.segment

    @property
    def offset(self) -> int:
        return self._memory_pointer.offset

    @property
    def underlying_type(self) -> OperandImm:
        return self._memory_pointer


# TODO Figure out a way to calculate relative offsets
class MemoryImmediate:
    def __init__(self, memory_immediate: OperandImm) -> None:
        self._memory_immediate = memory_immediate

    @property
    def is_signed(self) -> bool:
        return bool(self._memory_immediate.isSigned)

    @property
    def is_relative(self) -> bool:
        return bool(self._memory_immediate.isRelative)

    @property
    def value(self) -> int:
        return self._memory_immediate.value.s if self.is_signed else self._memory_immediate.value.u

    @property
    def underlying_type(self) -> OperandImm:
        return self._memory_immediate


class MemoryOperand:
    def __init__(self, memory_operand: OperandMem) -> None:
        self._memory_operand = memory_operand

    @property
    def type(self) -> MemOpType:
        return MemOpType(self._memory_operand.type)

    @property
    def segment(self) -> Register:
        return Register(self._memory_operand.segment)

    @property
    def base(self) -> Register:
        return Register(self._memory_operand.base)

    @property
    def index(self) -> Register:
        return Register(self._memory_operand.index)

    @property
    def scale(self) -> int:
        return self._memory_operand.scale

    @property
    def displacement(self) -> int:
        if self._memory_operand.disp.hasDisplacement:
            return self._memory_operand.disp.value
        return 0

    @property
    def underlying_type(self) -> OperandMem:
        return self._memory_operand


class Operand:
    def __init__(self, operand: RawOperand, instruction: RawInstruction = None, index: int = -1) -> None:
        self._operand = operand
        self._instruction = instruction
        self._index = index

    @property
    def id(self) -> int:
        return self._operand.id

    @property
    def type(self) -> OperandType:
        return OperandType(self._operand.type)

    @property
    def visibility(self) -> OperandVisibility:
        return OperandVisibility(self._operand.visibility)

    @property
    def action(self) -> OperandAction:
        return OperandAction(self._operand.action)

    @property
    def encoding(self) -> OperandEncoding:
        return OperandEncoding(self._operand.encoding)

    @property
    def size(self) -> int:
        return self._operand.size

    @property
    def element_size(self) -> int:
        return self._operand.elementSize

    @property
    def element_type(self) -> ElementTypes:
        return ElementTypes(self._operand.elementType)

    @property
    def element_count(self) -> int:
        return self._operand.elementCount

    @property
    def register(self) -> Register:
        return Register(self._operand.reg.value)

    @property
    def memory(self) -> MemoryOperand:
        if hasattr(self, '_memory'):
            return self._memory

        self._memory = MemoryOperand(self._operand.mem)
        return self._memory

    @property
    def pointer(self) -> MemoryPointer:
        if hasattr(self, '_pointer'):
            return self._pointer

        self._pointer = MemoryPointer(self._operand.ptr)
        return self._pointer

    @property
    def immediate(self) -> MemoryImmediate:
        if hasattr(self, '_immediate'):
            return self._immediate

        self._immediate = MemoryImmediate(self._operand.imm)
        return self._immediate

    @property
    def underlying_type(self) -> RawOperand:
        return self._operand

    @property
    def absolute_address(self) -> typing.Optional[int]:
        status, address = CalcAbsoluteAddress(self._instruction, self._operand)
        if status == Status.Success:
            return address
        return None

    def to_string(self, formatter: Formatter = default_formatter) -> str:
        if self._index >= 0:
            return formatter.format_operand(self._instruction, self._index)

        return ''

    def __str__(self) -> str:
        return self.to_string()


class Instruction:
    def __init__(self, instruction: RawInstruction) -> None:
        self._instruction = instruction

    @property
    def machine_mode(self) -> MachineMode:
        return MachineMode(self._instruction.machineMode)

    @property
    def mnemonic(self) -> str:
        if hasattr(self, '_mnemonic'):
            return self._mnemonic

        self._mnemonic = MnemonicGetString(self.mnemonic_value)
        return self._mnemonic

    @property
    def mnemonic_value(self) -> Mnemonic:
        return Mnemonic(self._instruction.mnemonic)

    @property
    def length(self) -> int:
        return self._instruction.length

    @property
    def bytes(self) -> bytes:
        return bytes(self._instruction.data[0:self._instruction.length])

    @property
    def encoding(self) -> InstructionEncoding:
        return InstructionEncoding(self._instruction.encoding)

    @property
    def opcode_map(self) -> OpcodeMap:
        return OpcodeMap(self._instruction.opcodeMap)

    @property
    def opcode(self) -> int:
        return self._instruction.opcode

    @property
    def stack_width(self) -> int:
        return self._instruction.stackWidth

    @property
    def operand_width(self) -> int:
        return self._instruction.operandWidth

    @property
    def address_width(self) -> int:
        return self._instruction.addressWidth

    @property
    def operands(self) -> [Operand]:
        if hasattr(self, '_operands'):
            return self._operands

        self._operands = [Operand(operand, self._instruction, i)
                          for i, operand in enumerate(self._instruction.operands[:self._instruction.operandCount])]
        return self._operands

    @property
    def attributes(self) -> InstructionAttribute:
        return InstructionAttribute(self._instruction.attributes)

    @property
    def address(self) -> int:
        return self._instruction.instructionAddress

    # TODO double check functionality of this property
    @property
    def accessed_flags(self) -> [CpuFlag]:
        return [CpuFlag(flag.action) for flag in self._instruction.accessedFlags]

    @property
    def avx(self) -> InstructionAvx:
        return InstructionAvx(self._instruction.avx)

    @property
    def meta(self) -> InstructionMeta:
        return InstructionMeta(self._instruction.meta)

    # TODO Copy returned type and add type annotation
    @property
    def raw(self) -> InstructionRaw:
        return self._instruction.raw

    @property
    def underlying_type(self) -> RawInstruction:
        return self._instruction

    def to_string(self, formatter: Formatter = default_formatter) -> str:
        return formatter.format_instruction(self._instruction)

    def __str__(self) -> str:
        return self.to_string()

    # TODO consider if more information should be added to the string
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.mnemonic})'
