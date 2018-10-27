from enum import IntEnum, IntFlag


class MachineMode(IntEnum):
    Invalid = 0

    ''' 64 bit mode. '''
    Long64 = 1

    ''' 32 bit protected mode. '''
    LongCompat32 = 2

    ''' 16 bit protected mode. '''
    LongCompat16 = 3

    ''' 32 bit protected mode. '''
    Legacy32 = 4

    ''' 16 bit protected mode. '''
    Legacy16 = 5

    ''' 16 bit real mode. '''
    Real16 = 6


class AddressWidth(IntEnum):
    Invalid = 0
    Width16 = 16
    Width32 = 32
    Width64 = 64


class DecoderMode(IntEnum):
    """ Values that represent decoder-modes. """

    ''' Enables minimal instruction decoding without semantic analysis. '''
    Minimal = 0

    ''' Enables the AMD-branch mode. '''
    AMDBranches = 1

    ''' Enables KNC compatibility-mode. '''
    KNC = 2

    ''' Enables the MPX mode. '''
    MPX = 3

    ''' Enables the CET mode. '''
    CET = 4

    ''' Enables the LZCNT mode. '''
    LZCNT = 5

    ''' Enables the TZCNT mode. '''
    TZCNT = 6

    ''' Enables the WBNOINVD mode. '''
    WBNOINVD = 7


class Status(IntEnum):

    ''' The operation completed successfully. '''
    Success = 0

    ''' An invalid parameter was passed to a function. '''
    InvalidParameter = 1

    ''' An attempt was made to perform an invalid operation. '''
    InvalidOperation = 2

    ''' A buffer passed to a function was too small to complete the requested operation. '''
    InsufficientBufferSize = 3

    ''' An attempt was made to read data from an input data-source that has no more data '''
    NoMoreData = 4

    ''' An general error occured while decoding the current instruction. The instruction '''
    DecodingError = 5

    ''' The instruction exceeded the maximum length of 15 bytes. '''
    InstructionTooLong = 6

    ''' The instruction encoded an invalid register. '''
    BadRegister = 7

    ''' A lock-prefix (F0) was found while decoding an instruction that does not support '''
    IllegalLock = 8

    ''' A legacy-prefix (F2, F3, 66) was found while decoding a XOP/VEX/EVEX/MVEX '''
    IllegalLegacyPrefix = 9

    ''' A rex-prefix was found while decoding a XOP/VEX/EVEX/MVEX instruction. '''
    IllegalRex = 10

    ''' An invalid opcode-map value was found while decoding a XOP/VEX/EVEX/MVEX-prefix. '''
    IllegalMap = 11

    ''' An error occured while decoding the EVEX-prefix. '''
    MalformexEvex = 12

    ''' An error occured while decoding the MVEX-prefix. '''
    MalformexMvex = 13

    ''' An invalid write-mask was specified for an EVEX/MVEX instruction. '''
    InvalidMast = 14

    ''' Returning this status code in operand-related custom formatter callbacks will cause '''
    SkipOperand = 15

    ''' The base value for user-defined status codes. '''
    User = 0x10000000


class RegisterClass(IntEnum):

    ''' 8-bit general-purpose registers. '''
    GPR8 = 0

    ''' 16-bit general-purpose registers. '''
    GPR16 = 1

    ''' 32-bit general-purpose registers. '''
    GPR32 = 2

    ''' 64-bit general-purpose registers. '''
    GPR64 = 3

    ''' Floating point legacy registers. '''
    X87 = 4

    ''' Floating point multimedia registers. '''
    MMX = 5

    ''' 128-bit vector registers. '''
    XMM = 6

    ''' 256-bit vector registers. '''
    YMM = 7

    ''' 512-bit vector registers. '''
    ZMM = 8

    ''' Flags registers. '''
    Flags = 9

    ''' Instruction-pointer registers. '''
    IP = 10

    ''' Segment registers. '''
    Segment = 11

    ''' Test registers. '''
    Test = 12

    ''' Control registers. '''
    Control = 13

    ''' Debug registers. '''
    Debug = 14

    ''' Mask registers. '''
    Mask = 15

    ''' Bound registers. '''
    Bound = 16


class Feature(IntEnum):
    Evex = 0
    Mvex = 1


class CpuFlag(IntEnum):
    """ Values that represent CPU-flags. """

    ''' Carry flag. '''
    CF = 0

    ''' Parity flag. '''
    PF = 1

    ''' Adjust flag. '''
    AF = 2

    ''' Zero flag. '''
    ZF = 3

    ''' Sign flag. '''
    SF = 4

    ''' Trap flag. '''
    TF = 5

    ''' Interrupt enable flag. '''
    IF = 6

    ''' Direction flag. '''
    DF = 7

    ''' Overflow flag. '''
    OF = 8

    ''' I/O privilege level flag. '''
    IOPL = 9

    ''' Nested task flag. '''
    NT = 10

    ''' Resume flag. '''
    RF = 11

    ''' Virtual 8086 mode flag. '''
    VM = 12

    ''' Alignment check. '''
    AC = 13

    ''' Virtual interrupt flag. '''
    VIF = 14

    ''' Virtual interrupt pending. '''
    VIP = 15

    ''' Able to use CPUID instruction. '''
    ID = 16

    ''' FPU condition-code flag 0. '''
    C0 = 17

    ''' FPU condition-code flag 1. '''
    C1 = 18

    ''' FPU condition-code flag 2. '''
    C2 = 19

    ''' FPU condition-code flag 3. '''
    C3 = 20


class CpuFlagAction(IntEnum):
    """ Values that represent CPU-flag actions. """

    NoAction = 0  # Named "None" in Zydis
    Tested = 1
    TestedModified = 2
    Modified = 3
    Set0 = 4
    Set1 = 5
    Undefined = 6


class ExceptionClass(IntEnum):
    """ Values that represent exception-classes. """

    NoException = 0
    SSE1 = 1
    SSE2 = 2
    SSE3 = 3
    SSE4 = 4
    SSE5 = 5
    SSE7 = 6
    AVX1 = 7
    AVX2 = 8
    AVX3 = 9
    AVX4 = 10
    AVX5 = 11
    AVX6 = 12
    AVX7 = 13
    AVX8 = 14
    AVX11 = 15
    AVX12 = 16
    E1 = 17
    E1NF = 18
    E2 = 19
    E2NF = 20
    E3 = 21
    E3NF = 22
    E4 = 23
    E4NF = 24
    E5 = 25
    E5NF = 26
    E6 = 27
    E6NF = 28
    E7NM = 29
    E7NM128 = 30
    E9NF = 31
    E10 = 32
    E10NF = 33
    E11 = 34
    E11NF = 35
    E12 = 36
    E12NP = 37
    K20 = 38
    K21 = 39


class VectorLength(IntEnum):
    """ Values that represent vector-lengths. """

    Invalid = 0
    Length128 = 128
    Length256 = 256
    Length512 = 512


class MaskModes(IntEnum):
    """ Values that represent AVX mask-modes. """

    Invalid = 0

    ''' The embedded mask register is used as a merge-mask. This is the default mode for all EVEX/MVEX-instructions. '''
    Merge = 1

    ''' The embedded mask register is used as a zero-mask. '''
    Zero = 2


class MemOpType(IntEnum):
    """ Values that represent memory-operand types. """

    ''' Normal memory operand. '''
    Mem = 0

    ''' The memory operand is only used for address-generation. No real memory-access is caused. '''
    Agen = 1

    ''' A memory operand using `SIB` addressing form, where the index register is not used
        in address calculation and scale is ignored. No real memory-access is caused.
    '''
    MIB = 2


class BroadcastModes(IntEnum):
    """ Values that represent AVX broadcast-modes. """

    Invalid = 0
    Mode_1_To_2 = 1
    Mode_1_To_4 = 2
    Mode_1_To_8 = 3
    Mode_1_To_16 = 4
    Mode_1_To_32 = 5
    Mode_1_To_64 = 6
    Mode_2_To_4 = 7
    Mode_2_To_8 = 8
    Mode_2_To_16 = 9
    Mode_4_To_8 = 10
    Mode_4_To_16 = 11
    Mode_8_To_16 = 12


class RoundingModes(IntEnum):
    """ Values that represent AVX rounding-modes. """

    Invalid = 0
    Nearest = 1
    Down = 2
    Up = 3
    Zero = 4


class SwizzleModes(IntEnum):
    """ Values that represent swizzle-modes. """

    Invalid = 0
    DCBA = 1
    CDAB = 2
    BADC = 3
    DACB = 4
    AAAA = 5
    BBBB = 6
    CCCC = 7
    DDDD = 8


class ConversionMode(IntEnum):
    """ Values that represent conversion-modes. """

    Invalid = 0
    Float_16 = 1
    SInt_8 = 2
    UInt_8 = 3
    SInt_16 = 4
    UInt_16 = 5


class ElementTypes(IntEnum):
    """ Values that represent element-types. """

    Invalid = 0
    Struct = 1
    UInt = 2
    Int = 3
    Float_16 = 4
    Float_32 = 5
    Float_64 = 6
    Float_80 = 7
    LongBCD = 8


class OperandType(IntEnum):
    """ Values that represent operand-types. """

    ''' The operand is not used. '''
    Unused = 0

    ''' The operand is a register operand. '''
    Register = 1

    ''' The operand is a memory operand. '''
    Memory = 2

    ''' The operand is a pointer operand with a segment:offset lvalue. '''
    Pointer = 3

    ''' The operand is an immediate operand. '''
    Immediate = 4


class OperandEncoding(IntEnum):
    """ Values that represent operand-encodings. """

    NoEncoding = 0  # Named "None" in Zydis
    ModRM_Reg = 1
    ModRM_RM = 2
    Opcode = 3
    NDSNDD = 4
    IS4 = 5
    Mask = 6
    Disp_8 = 7
    Disp_16 = 8
    Disp_32 = 9
    Disp_64 = 10
    Disp_16_32_64 = 11
    Disp_32_32_64 = 12
    Disp_16_32_32 = 13
    UImm_8 = 14
    UImm_16 = 15
    UImm_32 = 16
    UImm_64 = 17
    UImm_16_32_64 = 18
    UImm_32_32_64 = 19
    UImm_16_32_32 = 20
    SImm_8 = 21
    SImm_16 = 22
    SImm_32 = 23
    SImm_64 = 24
    SImm_16_32_64 = 25
    SImm_32_32_64 = 26
    SImm_16_32_32 = 27
    JImm_8 = 28
    JImm_16 = 29
    JImm_32 = 30
    JImm_64 = 31
    JImm_16_32_64 = 32
    JImm_32_32_64 = 33
    JImm_16_32_32 = 34


class OperandVisibility(IntEnum):
    """ Values that represent operand-visibilities. """

    Invalid = 0

    ''' The operand is explicitly encoded in the instruction. '''
    Explicit = 1

    ''' The operand is part of the opcode, but listed as an operand. '''
    Implicit = 2

    ''' The operand is part of the opcode, and not typically listed as an operand. '''
    Hidden = 3


class OperandAction(IntFlag):
    """ Values that represent operand-actions. """

    Invalid = 0

    ''' The operand is read by the instruction. '''
    Read = 1

    ''' The operand is written by the instruction (must write). '''
    Write = 2

    ''' The operand is read and written by the instruction (must write). '''
    ReadWrite = 3

    ''' The operand is conditionally read by the instruction. '''
    Cond_Read = 4

    ''' The operand is conditionally written by the instruction (may write). '''
    Cond_Write = 5

    ''' The operand is read and conditionally written by the instruction (may write). '''
    Read_Cond_Write = 6

    ''' The operand is written and conditionally read by the instruction (must write). '''
    Write_Cond_Read = 7

    # TODO Double check - This seems weird that Mask_Write and Mask_Read are the same
    ''' Mask combining all flags. '''
    Mask = 7


class InstructionEncoding(IntEnum):
    """ Values that represent instruction-encodings. """

    Invalid = 0

    ''' The instruction uses the default encoding. '''
    Default = 1

    ''' The instruction uses the AMD 3DNow-encoding. '''
    Encoding_3DNow = 2

    ''' The instruction uses the AMD XOP-encoding. '''
    XOP = 3

    ''' The instruction uses the VEX-encoding. '''
    VEX = 4

    ''' The instruction uses the EVEX-encoding. '''
    EVEX = 5

    ''' The instruction uses the MVEX-encoding. '''
    MVEX = 6


class OpcodeMap(IntEnum):
    """ Values that represent opcode-maps. """

    Default = 0
    Map_0F = 1
    Map_0F38 = 2
    Map_0F3A = 3
    Map_0F0F = 4
    Map_XOP8 = 5
    Map_XOP9 = 6
    Map_XOPA = 7


class InstructionAttribute(IntFlag):
    NoAttributes = 0x0
    Has_ModRM = 0x1
    Has_SIB = 0x2
    Has_Rex = 0x4
    Has_Xop = 0x8
    Has_Vex = 0x10
    Has_Evex = 0x20
    Has_Mvex = 0x40
    Is_Relative = 0x80
    Is_Priviledged = 0x100
    Is_Far_Branch = 0x1000000000
    Accepts_Lock = 0x200
    Accepts_Rep = 0x400
    Accepts_Repe = 0x800
    # Accepts_Repz = 0x1000
    Accepts_Repne = 0x1000
    # Accepts_Repnz = 0x1000
    Accepts_Bound = 0x2000
    Accepts_XAcquire = 0x4000
    Accepts_XRelease = 0x8000
    Accepts_Hle_Without_Lock = 0x10000
    Accepts_Branch_Hints = 0x20000
    Accepts_Segment = 0x40000
    Has_Lock = 0x80000
    Has_Rep = 0x100000
    Has_Repe = 0x200000
    # Has_Repz = 0x200000
    Has_Repne = 0x400000
    # Has_Repnz = 0x400000
    Has_Bound = 0x800000
    Has_XAcquire = 0x1000000
    Has_XRelease = 0x2000000
    Has_Branch_Not_Taken = 0x4000000
    Has_Branch_Taken = 0x8000000
    Has_Segment = 0x3F0000000
    Has_Segment_CS = 0x10000000
    Has_Segment_SS = 0x20000000
    Has_Segment_DS = 0x40000000
    Has_Segment_ES = 0x80000000
    Has_Segment_FS = 0x100000000
    Has_Segment_GS = 0x200000000
    Has_Operand_Size = 0x400000000
    Has_Address_Size = 0x800000000


class FormatterStyle(IntEnum):
    Intel = 0


class FormatterProperty(IntEnum):
    Uppercase = 0
    MemSeg = 1
    MemSize = 2
    Address_Format = 3
    Displacement_Format = 4
    Immediate_Format = 5
    Hex_Uppercase = 6
    Hex_Prefix = 6
    Hex_Suffix = 7
    Hex_Padding_Address = 8
    Hex_Padding_Displacement = 9
    Hex_Padding_Immediate = 10


class LetterCase(IntEnum):
    Default = 0
    Lower = 1
    Upper = 2


class AddressFormat(IntEnum):
    Absolute = 0
    Relative_Signed = 1
    Relative_Unsigned = 2


class DisplacementFormat(IntEnum):
    Hex_Signed = 0
    Hex_Unsigned = 1


class ImmediateFormat(IntEnum):
    Hex_Auto = 0
    Hex_Signed = 1
    Hex_Unsiged = 2


class FormatterHookType(IntEnum):

    ''' This function is invoked before the formatter formats an instruction. '''
    Pre_Instruction = 0

    ''' This function is invoked after the formatter formatted an instruction. '''
    Post_Instruction = 1

    ''' This function is invoked before the formatter formats an operand. '''
    Pre_Operand = 2

    ''' This function is invoked after the formatter formatted an operand. '''
    Post_Operand = 3

    ''' This function refers to the main formatting function. '''
    Format_Instruction = 4

    ''' This function is invoked to format a register operand. '''
    Format_Operand_Reg = 5

    ''' This function is invoked to format a memory operand. '''
    Format_Operand_Mem = 6

    ''' This function is invoked to format a pointer operand. '''
    Format_Operand_Ptr = 7

    ''' This function is invoked to format an immediate operand. '''
    Format_Operand_Imm = 8

    ''' This function is invoked to print the instruction mnemonic. '''
    Print_Mnemonic = 9

    ''' This function is invoked to print a register. '''
    Print_Register = 10

    ''' This function is invoked to print an absolute address. '''
    Print_Address = 11

    ''' This function is invoked to print a memory displacement value. '''
    Print_Disp = 12

    ''' This function is invoked to print an immediate value. '''
    Print_Imm = 13

    ''' This function is invoked to print the size of a memory operand. '''
    Print_Memsize = 14

    ''' This function is invoked to print the instruction prefixes. '''
    Print_Prefixes = 15

    ''' This function is invoked after formatting an operand to print a `EVEX`/`MVEX` '''
    Print_Decorator = 16


class DecoratorType(IntEnum):

    ''' The embedded-mask decorator. '''
    Mask = 0

    ''' The broadcast decorator. '''
    Bc = 1

    ''' The rounding-control decorator. '''
    Rc = 2

    ''' The suppress-all-exceptions decorator. '''
    Sae = 3

    ''' The register-swizzle decorator. '''
    Swizzle = 4

    ''' The conversion decorator. '''
    Conversion = 5

    ''' The eviction-hint decorator. '''
    Eh = 6
