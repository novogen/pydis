import unittest

from pydis.formatter import Formatter
from pydis.decoder import decode


class TestFormatter(unittest.TestCase):

    def test_init(self):
        # No exception should be raise
        formatter = Formatter()

    def test_format_instruction(self):
        formatter = Formatter()

        instruction = next(decode(b'Q'))

        self.assertEqual(formatter.format_instruction(instruction.underlying_type), 'push rcx')

    def test_uppercase_letters(self):
        formatter = Formatter()
        formatter.uppercase_letters = True

        instruction = next(decode(b'Q'))

        self.assertEqual(formatter.format_instruction(instruction.underlying_type), 'PUSH RCX')


if __name__ == '__main__':
    unittest.main()
