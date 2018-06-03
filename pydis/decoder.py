from ctypes import create_string_buffer, byref

import typing

from .types import (MachineMode, AddressWidth, DecoderMode, Status, OperandType, OperandVisibility, OperandAction,
                    OperandEncoding, ElementTypes, MemOpType, InstructionEncoding, OpcodeMap, CpuFlag, MaskModes,
                    BroadcastModes, RoundingModes, SwizzleModes, ConversionMode, ExceptionClass, InstructionAttribute)
from .zydis_types import (Instruction as RawInstruction, Operand as RawOperand, OperandMem, OperandPtr, OperandImm,
                          InstructionAvx as RawInstructionAvx, AvxMask as RawAvxMask, AvxBroadcast as RawAvxBroadcast,
                          InstructionMeta as RawInstructionMeta)
from .interface import DecoderInit, DecoderDecodeBuffer, MnemonicGetString
from .generate_types import Register, InstructionCategory, ISAExt, ISASet, Mnemonic

class AvxMask:
    def __init__(self, avx_mask: RawAvxMask):
        self.mode = MaskModes(avx_mask.mode)
        self.register = Register(avx_mask.reg)
        self.is_control_mask = bool(avx_mask.isControlMask)


class AvxBroadcast:
    def __init__(self, avx_broadcast: RawAvxBroadcast):
        self.is_static = bool(avx_broadcast.isStatic)
        self.mode = BroadcastModes(avx_broadcast.mode)


class InstructionAvx:
    def __init__(self, instruction_avx: RawInstructionAvx):
        self.vector_length = instruction_avx.vectorLength
        self.mask = AvxMask(instruction_avx.mask)
        self.broadcast = AvxBroadcast(instruction_avx.broadcast)
        self.rounding = RoundingModes(instruction_avx.rounding.mode)
        self.swizzle = SwizzleModes(instruction_avx.swizzle.mode)
        self.conversion = ConversionMode(instruction_avx.conversion.mode)
        self.has_sae = bool(instruction_avx.hasSAE)
        self.has_eviction_hint = bool(instruction_avx.hasEvictionHint)


class InstructionMeta:
    def __init__(self, instruction_meta: RawInstructionMeta):
        self.category = InstructionCategory(instruction_meta.category)
        self.isa_set = ISASet(instruction_meta.isaSet)
        self.isa_ext = ISAExt(instruction_meta.isaExt)
        self.exception_class = ExceptionClass(instruction_meta.exceptionClass)


class MemoryPointer:
    def __init__(self, memory_pointer: OperandPtr):
        self.segment = memory_pointer.segment
        self.offset = memory_pointer.offset


class MemoryImmediate:
    def __init__(self, memory_immediate: OperandImm):
        # TODO Figure out a way to calculate relative offsets
        self.is_signed = bool(memory_immediate.isSigned)
        self.is_relative = bool(memory_immediate.isRelative)

        if self.is_signed:
            self.value = memory_immediate.value.s
        else:
            self.value = memory_immediate.value.u


class MemoryOperand:
    def __init__(self, memory_operand: OperandMem):
        self.type = MemOpType(memory_operand.type)
        self.segment = Register(memory_operand.segment)
        self.base = Register(memory_operand.base)
        self.index = Register(memory_operand.index)
        self.scale = memory_operand.scale

        self.displacement = None
        if memory_operand.disp.hasDisplacement:
            self.displacement = memory_operand.disp.value


class Operand:
    def __init__(self, operand: RawOperand):
        self.id = operand.id
        self.type =  OperandType(operand.type)
        self.visibility = OperandVisibility(operand.visibility)
        self.action = OperandAction(operand.action)
        self.encoding = OperandEncoding(operand.encoding)
        self.size = operand.size
        self.elementSize = operand.elementSize
        self.elementType = ElementTypes(operand.elementType)
        self.elementCount = operand.elementCount
        self.register = Register(operand.reg.value)
        self.memory = MemoryOperand(operand.mem)
        self.pointer = MemoryPointer(operand.ptr)
        self.immediate = MemoryImmediate(operand.imm)


class Instruction:
    def __init__(self, instruction: RawInstruction):
        self.machine_mode = MachineMode(instruction.machineMode)
        self.mnemonic_value = Mnemonic(instruction.mnemonic)
        self.length = instruction.length
        self.data = bytes(instruction.data)
        self.encoding = InstructionEncoding(instruction.encoding)
        self.opcodeMap = OpcodeMap(instruction.opcodeMap)
        self.opcode = instruction.opcode
        self.stackWidth = instruction.stackWidth
        self.operandWidth = instruction.operandWidth
        self.addressWidth = instruction.addressWidth
        self.operandCount = instruction.operandCount
        self.operands = [Operand(operand) for operand in instruction.operands[:instruction.operandCount]]
        self.attributes = InstructionAttribute(instruction.attributes)
        self.instructionAddress = instruction.instructionAddress
        self.accessedFlags = [CpuFlag(flag.action) for flag in instruction.accessedFlags]  # TODO double check this
        self.avx = InstructionAvx(instruction.avx)
        self.meta = InstructionMeta(instruction.meta)
        self.raw = instruction.raw  # TODO reevaluate if this needs to be converted at all.

    @property
    def mnemonic(self):
        return MnemonicGetString(self.mnemonic_value)


def decode(buffer, address: int = 0, mode: MachineMode = MachineMode.Long64,
           addressWidth: AddressWidth = AddressWidth.Width64) -> typing.Generator[Instruction, None, None]:
    status, decoder = DecoderInit(mode, addressWidth)

    if status != Status.Success:
        raise Exception(f'Failed to initialize the decoder: {status.name}')

    # TODO Improve this shouldn't need to copy
    buffer = create_string_buffer(buffer, len(buffer))
    buffer_offset = 0
    while True:
        status, instruction = DecoderDecodeBuffer(decoder, byref(buffer, buffer_offset), len(buffer) - buffer_offset,
                                                  address)

        if status != Status.Success:
            break

        instruction = Instruction(instruction)
        buffer_offset += instruction.length
        address += instruction.length
        yield instruction

    if status != Status.NoMoreData:
        raise Exception(f'Failed while decoding: {status}')
