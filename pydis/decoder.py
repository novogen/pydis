from ctypes import create_string_buffer, byref

import typing

from .types import MachineMode, AddressWidth, Status, DecoderMode
from .zydis_types import MaxInstructionLength
from .interface import DecoderInit, DecoderDecodeBuffer, DecoderEnableMode
from .instruction import Instruction


class Decoder:
    def __init__(self, mode: MachineMode = MachineMode.Long64,
                 address_width: AddressWidth = AddressWidth.Width64) -> None:
        status, self._decoder = DecoderInit(mode, address_width)

        if status != Status.Success:
            raise Exception(f'Failed to initialize the decoder: {status.name}')

    @property
    def minimal(self) -> bool:
        return self.is_mode_enabled(DecoderMode.Minimal)

    @minimal.setter
    def minimal(self, enabled: bool) -> None:
        self.set_mode(DecoderMode.Minimal, enabled)

    def is_mode_enabled(self, mode: DecoderMode) -> bool:
        return bool(self._decoder.decoderMode[mode])

    def set_mode(self, mode: DecoderMode, enabled: bool) -> None:
        status = DecoderEnableMode(self._decoder, mode, enabled)
        if status != Status.Success:
            raise Exception(f'Failed to set mode: {status.name}')

    def decode_instruction(self, buffer: bytes, address: int = 0,
                           buffer_offset: int = 0) -> Instruction:
        if not (0 <= buffer_offset < len(buffer)):
            raise IndexError("offset out of range")

        length = max(len(buffer) - buffer_offset, MaxInstructionLength)
        buf = create_string_buffer(buffer[buffer_offset:buffer_offset + length], length)

        status, instruction = DecoderDecodeBuffer(self._decoder, buf, length, address)

        if status != Status.Success:
            raise Exception(f'Failed while decoding: {status.name}')

        return Instruction(instruction)

    def decode(self, buffer: bytes, address: int = 0,
               buffer_offset: int = 0) -> typing.Generator[Instruction, None, None]:
        if not (0 <= buffer_offset < len(buffer)):
            raise IndexError("offset out of range")

        length = len(buffer)
        buf = create_string_buffer(buffer, length)

        while True:
            status, instruction = DecoderDecodeBuffer(self._decoder, byref(buf, buffer_offset),
                                                      length - buffer_offset, address)

            if status != Status.Success:
                break

            instruction = Instruction(instruction)
            buffer_offset += instruction.length
            address += instruction.length
            yield instruction

        if status != Status.NoMoreData:
            raise Exception(f'Failed while decoding: {status.name}')


def decode(buffer, address: int = 0, mode: MachineMode = MachineMode.Long64,
           address_width: AddressWidth = AddressWidth.Width64) -> typing.Generator[Instruction, None, None]:
    decoder = Decoder(mode, address_width)

    return decoder.decode(buffer, address)
