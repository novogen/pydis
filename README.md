# pydis

Pydis is a python binding for the [Zydis disassembler library](https://github.com/zyantific/zydis).


```python
import pydis

instructions = b'\x51\x8d\x45\xff\x50\xff\x75\x0c\xff\x75\x08\xff\x15\xa0\xa5\x48\x76\x85\xc0\x0f\x88\xfc\xda\x02\x00'
instruction_pointer = 0x007FFFFFFF400000

for instruction in pydis.decode(instructions, instruction_pointer):
    print(instruction)
```
Output:
```assembly
push rcx
lea eax, [rbp-0x01]
push rax
push [rbp+0x0C]
push [rbp+0x08]
call [0x008000007588A5B1]
test eax, eax
js 0x007FFFFFFF42DB15
```

The module uses the same field names as Zydis with the exception that snake_case is used instead of camelCase.

## Requirements
Pydis requires a python version >=3.6. The package has been tested on macOS, linux, and windows running cpython. Since 
pydis uses `ctypes` to interface with zydis it may or may not work on other interpreters.

## Installing
```bash
pip install py-dis
```
or you can build from source as described below.

## Building
MacOS and linux machines will need cmake and a C compiler in order to build Zydis. Windows machines will need Visual 
Studios. Pydis does not use any python modules beyond ones provided by a default python installation.

With the tooling installed running: `python setup.py build install` will build Zydis and install the package.

## Usage
Documentation is currently being worked on. For now the example script [pydisinfo](../master/scripts/pydisinfo) is
the best place to look for example usage.
