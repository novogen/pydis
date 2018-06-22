import unittest
import pydis


instructions = b'\x51\x8d\x45\xff\x50\xff\x75\x0c\xff\x75\x08\xff\x15\xa0\xa5\x48\x76\x85\xc0\x0f\x88\xfc\xda\x02\x00'
instruction_pointer = 0x007FFFFFFF400000


class TestDecoder(unittest.TestCase):
    def test_decoding_bytes(self):
        decoder = pydis.Decoder()

        self.assertListEqual(list(map(str, decoder.decode(instructions, instruction_pointer))),
                             ['push rcx',
                              'lea eax, [rbp-0x01]',
                              'push rax',
                              'push [rbp+0x0C]',
                              'push [rbp+0x08]',
                              'call [0x008000007588A5B1]',
                              'test eax, eax',
                              'js 0x007FFFFFFF42DB15'])

        # Ensure that the data wasn't modified and that the decoder still can decode.
        self.assertEqual(len(list(decoder.decode(instructions, instruction_pointer))), 8)

    def test_decode_instruction(self):
        decoder = pydis.Decoder()

        self.assertEqual(str(decoder.decode_instruction(instructions)), 'push rcx')

        # Check the offset works
        self.assertEqual(str(decoder.decode_instruction(instructions, buffer_offset=1)), 'lea eax, [rbp-0x01]')

        with self.assertRaises(IndexError):
            decoder.decode_instruction(instructions, buffer_offset=len(instructions))


if __name__ == '__main__':
    unittest.main()
