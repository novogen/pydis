from ctypes import create_string_buffer, byref

import typing

from .types import MachineMode, AddressWidth, Status
from .interface import DecoderInit, DecoderDecodeBuffer
from .instruction import Instruction


def decode(buffer, address: int = 0, mode: MachineMode = MachineMode.Long64,
           address_width: AddressWidth = AddressWidth.Width64) -> typing.Generator[Instruction, None, None]:
    status, decoder = DecoderInit(mode, address_width)

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
        raise Exception(f'Failed while decoding: {status.name}')
