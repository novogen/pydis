from ctypes import (c_uint8, c_uint16, c_uint32, c_int64, c_uint64, c_size_t, c_char_p, Structure, Union, POINTER,
                    CFUNCTYPE)


MaxInstructionLength = 15
MaxOperandCount = 10
MaxCPUFlag = 20
MaxDecoderMode = 8


class Decoder(Structure):
    _fields_ = [('machineMode', c_uint8),
                ('addressWidth', c_uint8),
                ('decoderMode', c_uint8 * MaxDecoderMode)]


class OperandValue(Union):
    _fields_ = [('s', c_int64),
                ('u', c_uint64)]


class OperandReg(Structure):
    _fields_ = [('value', c_uint8)]


class OperandMemDisp(Structure):
    _fields_ = [('hasDisplacement', c_uint8),
                ('value', c_int64)]


class OperandMem(Structure):
    _fields_ = [('type', c_uint8),
                ('segment', c_uint8),
                ('base', c_uint8),
                ('index', c_uint8),
                ('scale', c_uint8),
                ('disp', OperandMemDisp)]


class OperandPtr(Structure):
    _fields_ = [('segment', c_uint16),
                ('offset', c_uint32)]


class OperandImm(Structure):
    _fields_ = [('isSigned', c_uint8),
                ('isRelative', c_uint8),
                ('value', OperandValue)]


class Operand(Structure):
    _fields_ = [('id', c_uint8),
                ('type', c_uint8),
                ('visibility', c_uint8),
                ('action', c_uint8),
                ('encoding', c_uint8),
                ('size', c_uint16),
                ('elementType', c_uint8),
                ('elementSize', c_uint16),
                ('elementCount', c_uint16),
                ('reg', OperandReg),
                ('mem', OperandMem),
                ('ptr', OperandPtr),
                ('imm', OperandImm)]


class Prefixes(Structure):
    _fields_ = [('data', c_uint8 * (MaxInstructionLength - 1)),
                ('count', c_uint8),
                ('hasF0', c_uint8),
                ('hasF3', c_uint8),
                ('hasF2', c_uint8),
                ('has2E', c_uint8),
                ('has36', c_uint8),
                ('has3E', c_uint8),
                ('has26', c_uint8),
                ('has64', c_uint8),
                ('has65', c_uint8),
                ('has66', c_uint8),
                ('has67', c_uint8)]


class Rex(Structure):
    _fields_ = [('isDecoded', c_uint8),
                ('data', c_uint8 * 1),
                ('W', c_uint8),
                ('R', c_uint8),
                ('X', c_uint8),
                ('B', c_uint8)]


class Xop(Structure):
    _fields_ = [('isDecoded', c_uint8),
                ('data', c_uint8 * 3),
                ('R', c_uint8),
                ('X', c_uint8),
                ('B', c_uint8),
                ('m_mmmm', c_uint8),
                ('W', c_uint8),
                ('vvvv', c_uint8),
                ('L', c_uint8),
                ('pp', c_uint8)]


class Vex(Structure):
    _fields_ = [('isDecoded', c_uint8),
                ('data', c_uint8 * 3),
                ('R', c_uint8),
                ('X', c_uint8),
                ('B', c_uint8),
                ('m_mmmm', c_uint8),
                ('W', c_uint8),
                ('vvvv', c_uint8),
                ('L', c_uint8),
                ('pp', c_uint8)]


class Evex(Structure):
    _fields_ = [('isDecoded', c_uint8),
                ('data', c_uint8 * 4),
                ('R', c_uint8),
                ('X', c_uint8),
                ('B', c_uint8),
                ('R2', c_uint8),
                ('mm', c_uint8),
                ('W', c_uint8),
                ('vvvv', c_uint8),
                ('pp', c_uint8),
                ('z', c_uint8),
                ('L2', c_uint8),
                ('L', c_uint8),
                ('b', c_uint8),
                ('V2', c_uint8),
                ('aaa', c_uint8)]


class Mvex(Structure):
    _fields_ = [('isDecoded', c_uint8),
                ('data', c_uint8 * 4),
                ('R', c_uint8),
                ('X', c_uint8),
                ('B', c_uint8),
                ('R2', c_uint8),
                ('mmmm', c_uint8),
                ('W', c_uint8),
                ('vvvv', c_uint8),
                ('pp', c_uint8),
                ('E', c_uint8),
                ('SSS', c_uint8),
                ('V2', c_uint8),
                ('kkk', c_uint8)]


class Modrm(Structure):
    _fields_ = [('isDecoded', c_uint8),
                ('data', c_uint8 * 1),
                ('mod', c_uint8),
                ('reg', c_uint8),
                ('rm', c_uint8)]


class Sib(Structure):
    _fields_ = [('isDecoded', c_uint8),
                ('data', c_uint8 * 1),
                ('scale', c_uint8),
                ('index', c_uint8),
                ('base', c_uint8)]


class Disp(Structure):
    _fields_ = [('value', c_int64),
                ('size', c_uint8),
                ('offset', c_uint8)]


class Imm(Structure):
    _fields_ = [('isSigned', c_uint8),
                ('isRelative', c_uint8),
                ('value', OperandValue),
                ('size', c_uint8),
                ('offset', c_uint8)]


class InstructionRaw(Structure):
    _fields_ = [('prefixes', Prefixes),
                ('rex', Rex),
                ('xop', Xop),
                ('vex', Vex),
                ('evex', Evex),
                ('mvex', Mvex),
                ('modrm', Modrm),
                ('sib', Sib),
                ('disp', Disp),
                ('imm', Imm * 2)]


class AvxMask(Structure):
    _fields_ = [('mode', c_uint8),
                ('reg', c_uint8),
                ('isControlMask', c_uint8)]


class AvxBroadcast(Structure):
    _fields_ = [('isStatic', c_uint8),
                ('mode', c_uint8)]


class AvxRounding(Structure):
    _fields_ = [('mode', c_uint8)]


class AvxSwizzle(Structure):
    _fields_ = [('mode', c_uint8)]


class AvxConversion(Structure):
    _fields_ = [('mode', c_uint8)]


class InstructionAvx(Structure):
    _fields_ = [('vectorLength', c_uint16),
                ('mask', AvxMask),
                ('broadcast', AvxBroadcast),
                ('rounding', AvxRounding),
                ('swizzle', AvxSwizzle),
                ('conversion', AvxConversion),
                ('hasSAE', c_uint8),
                ('hasEvictionHint', c_uint8)]


class InstructionMeta(Structure):
    _fields_ = [('category', c_uint8),
                ('isaSet', c_uint8),
                ('isaExt', c_uint8),
                ('exceptionClass', c_uint8)]


class InstructionAccessFlag(Structure):
    _fields_ = [('action', c_uint8)]


class Instruction(Structure):
    _fields_ = [('machineMode', c_uint8),
                ('mnemonic', c_uint16),
                ('length', c_uint8),
                ('data', c_uint8 * MaxInstructionLength),
                ('encoding', c_uint8),
                ('opcodeMap', c_uint8),
                ('opcode', c_uint8),
                ('stackWidth', c_uint8),
                ('operandWidth', c_uint8),
                ('addressWidth', c_uint8),
                ('operandCount', c_uint8),
                ('operands', Operand * MaxOperandCount),
                ('attributes', c_uint64),
                ('instructionAddress', c_uint64),
                ('accessedFlags', InstructionAccessFlag * (MaxCPUFlag + 1)),
                ('avx', InstructionAvx),
                ('meta', InstructionMeta),
                ('raw', InstructionRaw)]


class String(Structure):
    _fields_ = [('buffer', c_char_p),
                ('length', c_size_t),
                ('capacity', c_size_t)]


FormatterFunc = CFUNCTYPE(c_char_p, POINTER(String), POINTER(Instruction), c_char_p)
FormatterOperandFunc = CFUNCTYPE(c_char_p, POINTER(String), POINTER(Instruction), POINTER(Operand), c_char_p)
FormatterRegisterFunc = CFUNCTYPE(c_char_p, POINTER(String), POINTER(Instruction), POINTER(Operand), c_uint8, c_char_p)
FormatterAddressFunc = CFUNCTYPE(c_char_p, POINTER(String), POINTER(Instruction), POINTER(Operand), c_uint64, c_char_p)
FormatterDecoratorFunc = CFUNCTYPE(c_char_p, POINTER(String), POINTER(Instruction), POINTER(Operand), c_uint8, c_char_p)


class Formatter(Structure):
    _fields_ = [('letterCase', c_uint8),
                ('forceMemorySegment', c_uint8),
                ('forceMemorySize', c_uint8),
                ('formatAddress', c_uint8),
                ('formatDisp', c_uint8),
                ('formatImm', c_uint8),
                ('hexUppercase', c_uint8),
                ('hexPrefix', POINTER(String)),
                ('hexPrefixData', String),
                ('hexSuffix', POINTER(String)),
                ('hexSuffixData', String),
                ('hexPaddingAddress', c_uint8),
                ('hexPAddingDisp', c_uint8),
                ('hexPaddingImm', c_uint8),
                ('funcPreInstruction', FormatterFunc),
                ('funcPostInstruction', FormatterFunc),
                ('funcPreOperand', FormatterOperandFunc),
                ('funcPostOperand', FormatterOperandFunc),
                ('funcFormatInstruction', FormatterFunc),
                ('funcFormatOperandReg', FormatterOperandFunc),
                ('funcFormatOperandMem', FormatterOperandFunc),
                ('funcFormatOperandPtr', FormatterOperandFunc),
                ('funcFormatOperandImm', FormatterOperandFunc),
                ('funcPrintMnemonic', FormatterFunc),
                ('funcPrintRegister', FormatterRegisterFunc),
                ('funcPrintAddress', FormatterAddressFunc),
                ('funcPrintDisp', FormatterOperandFunc),
                ('funcPrintImm', FormatterOperandFunc),
                ('funcPrintMemSize', FormatterOperandFunc),
                ('funcPrintPrefixes', FormatterFunc),
                ('funcPrintDecorator', FormatterDecoratorFunc)]
