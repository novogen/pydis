import unittest
import pydis


class TestExampleCode(unittest.TestCase):
    def test_example_code(self):
        instructions = b'\x51\x8d\x45\xff\x50\xff\x75\x0c\xff\x75\x08\xff\x15\xa0\xa5\x48\x76\x85\xc0\x0f\x88\xfc\xda' \
                       b'\x02\x00'
        instruction_pointer = 0x007FFFFFFF400000

        lines = []
        for instruction in pydis.decode(instructions, instruction_pointer):
            lines.append(str(instruction))

        self.assertListEqual(lines,
                             ['push rcx',
                              'lea eax, [rbp-0x01]',
                              'push rax',
                              'push [rbp+0x0C]',
                              'push [rbp+0x08]',
                              'call [0x008000007588A5B1]',
                              'test eax, eax',
                              'js 0x007FFFFFFF42DB15'])


if __name__ == '__main__':
    unittest.main()
