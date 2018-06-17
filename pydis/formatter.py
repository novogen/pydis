from .types import (Status, FormatterStyle, FormatterProperty, LetterCase, AddressFormat, DisplacementFormat,
                    ImmediateFormat)
from .interface import FormatterInit, FormatterSetProperty, FormatterFormatInstruction, FormatterFormatOperand
from .zydis_types import Instruction


class Formatter:
    def __init__(self, style: FormatterStyle = FormatterStyle.Intel) -> None:
        status, formatter = FormatterInit(style)

        if status != Status.Success:
            raise Exception(f'Failed to initialize the decoder: {status.name}')

        self._formatter = formatter

    def format_instruction(self, instruction: Instruction) -> str:
        status, string = FormatterFormatInstruction(self._formatter, instruction)
        if status != Status.Success:
            raise Exception(f'Failed to format instruction: {status.name}')

        return string

    def format_operand(self, instruction: Instruction, operand_index: int) -> str:
        status, string = FormatterFormatOperand(self._formatter, instruction, operand_index)
        if status != Status.Success:
            raise Exception(f'Failed to format operand: {status.name}')

        return string

    @property
    def uppercase_letters(self) -> bool:
        return self._formatter.letterCase == LetterCase.Upper

    @uppercase_letters.setter
    def uppercase_letters(self, uppercase: bool) -> None:
        FormatterSetProperty(self._formatter, FormatterProperty.Uppercase, uppercase)

    @property
    def uppercase_hex(self) -> bool:
        return bool(self._formatter.hexUppercase)

    @uppercase_hex.setter
    def uppercase_hex(self, uppercase: bool) -> None:
        FormatterSetProperty(self._formatter, FormatterProperty.Hex_Uppercase, uppercase)

    @property
    def print_segment_registers(self) -> bool:
        return bool(self._formatter.forceMemorySegment)

    @print_segment_registers.setter
    def print_segment_registers(self, print_segment_register: bool) -> None:
        FormatterSetProperty(self._formatter, FormatterProperty.MemSeg, print_segment_register)

    @property
    def print_operand_sizes(self) -> bool:
        return bool(self._formatter.forceMemorySize)

    @print_operand_sizes.setter
    def print_operand_sizes(self, print_operand_size: bool) -> None:
        FormatterSetProperty(self._formatter, FormatterProperty.MemSize, print_operand_size)

    @property
    def address_format(self) -> AddressFormat:
        return AddressFormat(self._formatter.formatAddress)

    @address_format.setter
    def address_format(self, format: AddressFormat) -> None:
        FormatterSetProperty(self._formatter, FormatterProperty.Address_Format, format)

    @property
    def displacement_format(self) -> DisplacementFormat:
        return DisplacementFormat(self._formatter.formatAddress)

    @displacement_format.setter
    def displacement_format(self, format: DisplacementFormat) -> None:
        FormatterSetProperty(self._formatter, FormatterProperty.Displacement_Format, format)

    @property
    def immediate_format(self) -> ImmediateFormat:
        return ImmediateFormat(self._formatter.formatAddress)

    @immediate_format.setter
    def immediate_format(self, format: ImmediateFormat) -> None:
        FormatterSetProperty(self._formatter, FormatterProperty.Immediate_Format, format)


default_formatter: Formatter = Formatter()
