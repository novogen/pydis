import unittest
import struct

from pydis.instruction import (Operand, RawOperand, OperandMem, MemoryOperand, OperandImm,
                               MemoryImmediate, OperandPtr, MemoryPointer)
from pydis.types import MemOpType, OperandVisibility, OperandAction, OperandEncoding, ElementTypes
from pydis.generate_types import Register


# TODO Fix the padding here so it works on 32bit systems as well.
operand_mem_format = 'BBBBB3xB7xq'
operand_ptr_format = 'H2xI'
operand_imm_format = 'BB6xQ'
operand_format = 'BBBBBxHBxHHBx24s8s16s'

class TestOperand(unittest.TestCase):

    def test_operand_decoding(self):
        operand_bytes = struct.pack(operand_format,
                                    1,  # id
                                    MemOpType.Mem.value,  # type
                                    OperandVisibility.Explicit.value,  # visibility
                                    OperandAction.Read.value,  # action
                                    OperandEncoding.Opcode.value,  # encoding
                                    1,  # size
                                    ElementTypes.Int.value,  # elementType
                                    2,  # elementSize
                                    1,  # elementCount
                                    Register.BL.value,  # reg.value
                                    b'\x00' * 24,  # operandMem
                                    b'\x00' * 8,  # operandPtr
                                    b'\x00' * 16)  # operandImm

        raw_operand = RawOperand.from_buffer_copy(operand_bytes)
        operand = Operand(raw_operand)

        # Test that all the fields decoded as expected
        self.assertEqual(operand.id, 1)
        self.assertEqual(operand.type, MemOpType.Mem)
        self.assertEqual(operand.visibility, OperandVisibility.Explicit)
        self.assertEqual(operand.action, OperandAction.Read)
        self.assertEqual(operand.encoding, OperandEncoding.Opcode),
        self.assertEqual(operand.size, 1)
        self.assertEqual(operand.element_type, ElementTypes.Int)
        self.assertEqual(operand.element_size, 2)
        self.assertEqual(operand.element_count, 1)
        self.assertEqual(operand.register, Register.BL)


    def test_memory_operand(self):
        operand_mem_bytes = struct.pack(operand_mem_format, MemOpType.Agen.value,
                                        Register.EAX, Register.ECX, Register.EDX, 1, 1, 0)
        raw_operand_mem = OperandMem.from_buffer_copy(operand_mem_bytes)
        operand_mem = MemoryOperand(raw_operand_mem)

        # Test that all the fields decoded as expected
        self.assertEqual(operand_mem.type, MemOpType.Agen)
        self.assertEqual(operand_mem.segment, Register.EAX)
        self.assertEqual(operand_mem.base, Register.ECX)
        self.assertEqual(operand_mem.index, Register.EDX)
        self.assertEqual(operand_mem.displacement, 0)

        operand_mem_bytes = struct.pack(operand_mem_format, 1, 1, 1, 1, 1, 0, 1)
        raw_operand_mem = OperandMem.from_buffer_copy(operand_mem_bytes)
        operand_mem = MemoryOperand(raw_operand_mem)

        # Test that if there is no displacement the field is set to 0
        self.assertEqual(operand_mem.displacement, 0)

    def test_memory_pointer(self):
        operand_ptr_bytes = struct.pack(operand_ptr_format,
                                        5,  #segment
                                        1)  # offset
        raw_operand_ptr = OperandPtr.from_buffer_copy(operand_ptr_bytes)
        operand_ptr = MemoryPointer(raw_operand_ptr)

        # Test that all the fields decoded as expected
        self.assertEqual(operand_ptr.segment, 5)
        self.assertEqual(operand_ptr.offset, 1)

    def test_memory_immediate(self):
        operand_imm_bytes = struct.pack('BB6xQ', 1, 1, 0)
        raw_operand_imm = OperandImm.from_buffer_copy(operand_imm_bytes)
        operand_imm = MemoryImmediate(raw_operand_imm)

        # Test that all the fields decoded as expected
        self.assertEqual(operand_imm.is_signed, True)
        self.assertEqual(operand_imm.is_relative, True)
        self.assertEqual(operand_imm.value, 0)


if __name__ == '__main__':
    unittest.main()
