import unittest
import struct

from pydis.instruction import (Instruction, RawInstruction, InstructionAvx, RawInstructionAvx, InstructionMeta,\
                               RawInstructionMeta)
from pydis.types import (MachineMode, InstructionEncoding, MaskModes, BroadcastModes, RoundingModes, SwizzleModes,
                         ConversionMode, ExceptionClass, InstructionAttribute)
from pydis.generate_types import InstructionCategory, ISAExt, ISASet, Mnemonic

instruction_format = 'BxHB15sBBBBBBB640sQQ21sx12s4s168sxx'
avx_format = 'HBBBBBBBBBB'
meta_format = 'BBBB'

class TestInstruction(unittest.TestCase):
    def test_instruction_decode(self):
        instruction_bytes = struct.pack(instruction_format,
                                        MachineMode.Long64.value,
                                        Mnemonic.MOV.value,  # mnemonic
                                        1,  # length
                                        b'Q\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # data
                                        InstructionEncoding.Default.value,
                                        0,  # opcodeMap
                                        81,  # opcode
                                        64,  # stackWidth
                                        32,  # operandWidth
                                        64,  # addressWidth
                                        3,  # operandCount
                                        b'\x00' * 640,  # operands
                                        (InstructionAttribute.Has_SIB | InstructionAttribute.Has_Lock).value,
                                        4194304,  # instructionAddress
                                        b'\x00' * 21,  # accessFlags
                                        b'\x00' * 12,  # avx
                                        b'\x00' * 4,  # meta
                                        b'\x00' * 168)  # raw

        raw_instruction = RawInstruction.from_buffer_copy(instruction_bytes)

        instruction = Instruction(raw_instruction)

        self.assertEqual(instruction.machine_mode, MachineMode.Long64)
        self.assertEqual(instruction.mnemonic_value, Mnemonic.MOV)  # TODO check once this is in
        self.assertEqual(instruction.length, 1)
        self.assertEqual(instruction.encoding, InstructionEncoding.Default)
        self.assertEqual(instruction.opcode_map, 0)
        self.assertEqual(instruction.opcode, 81)
        self.assertEqual(instruction.stack_width, 64)
        self.assertEqual(instruction.operand_width, 32)
        self.assertEqual(instruction.address_width, 64)
        self.assertEqual(len(instruction.operands), 3)
        self.assertEqual(instruction.attributes, InstructionAttribute.Has_SIB | InstructionAttribute.Has_Lock)
        self.assertEqual(instruction.address, 4194304)

    def test_avx_decode(self):
        avx_bytes = struct.pack(avx_format,
                                2,  # vectorLength
                                MaskModes.Merge.value,  # mask.mode
                                10,  # mask.reg
                                1,  # mask.isControlMask
                                0,  # broadcast.isStatic
                                BroadcastModes.Mode_1_To_2.value,  # broadcast.mode
                                RoundingModes.Down.value,  # rounding.mode
                                SwizzleModes.BADC.value,  # swizzle.mode
                                ConversionMode.SInt_16.value,  # conversion.mode
                                0,  # hasSAE
                                1)  # hasEvictionHint

        raw_avx = RawInstructionAvx.from_buffer_copy(avx_bytes)

        avx = InstructionAvx(raw_avx)

        self.assertEqual(avx.vector_length, 2)
        self.assertEqual(avx.mask.mode, MaskModes.Merge)
        # self.assertEqual(avx.mask.reg, None)  # TODO check once this is in
        self.assertEqual(avx.mask.is_control_mask, True)
        self.assertEqual(avx.broadcast.is_static, False)
        self.assertEqual(avx.broadcast.mode, BroadcastModes.Mode_1_To_2)
        self.assertEqual(avx.rounding, RoundingModes.Down)
        self.assertEqual(avx.swizzle, SwizzleModes.BADC)
        self.assertEqual(avx.conversion, ConversionMode.SInt_16)
        self.assertEqual(avx.has_sae, False)
        self.assertEqual(avx.has_eviction_hint, True)

    def test_meta_decode(self):
        meta_bytes = struct.pack(meta_format,
                                 InstructionCategory.AES.value,
                                 ISASet.AVX.value,
                                 ISAExt.AES.value,
                                 ExceptionClass.E1.value)

        raw_meta = RawInstructionMeta.from_buffer_copy(meta_bytes)

        meta = InstructionMeta(raw_meta)

        self.assertEqual(meta.category, InstructionCategory.AES)
        self.assertEqual(meta.isa_set, ISASet.AVX)
        self.assertEqual(meta.isa_ext, ISAExt.AES)
        self.assertEqual(meta.exception_class, ExceptionClass.E1)

    def test_mnemonic_string(self):
        # TODO replace this block once the Instruction class constructor is improved
        instruction_bytes = struct.pack(instruction_format,
                                        MachineMode.Long64.value,
                                        Mnemonic.MOV.value,  # mnemonic
                                        1,  # length
                                        b'Q\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # data
                                        InstructionEncoding.Default.value,
                                        0,  # opcodeMap
                                        81,  # opcode
                                        64,  # stackWidth
                                        32,  # operandWidth
                                        64,  # addressWidth
                                        3,  # operandCount
                                        b'\x00' * 640,  # operands
                                        (InstructionAttribute.Has_SIB | InstructionAttribute.Has_Lock).value,
                                        4194304,  # instructionAddress
                                        b'\x00' * 21,  # accessFlags
                                        b'\x00' * 12,  # avx
                                        b'\x00' * 4,  # meta
                                        b'\x00' * 168)  # raw

        raw_instruction = RawInstruction.from_buffer_copy(instruction_bytes)

        instruction = Instruction(raw_instruction)

        self.assertEqual(instruction.mnemonic, 'mov')

if __name__ == '__main__':
    unittest.main()
