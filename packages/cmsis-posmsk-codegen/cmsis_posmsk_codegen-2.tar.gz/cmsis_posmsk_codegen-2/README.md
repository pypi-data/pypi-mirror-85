
# cmsis_posmsk_codegen

[![Build Status](https://travis-ci.com/metebalci/cmsis_posmsk_codegen.svg?branch=master)](https://travis-ci.com/metebalci/cmsis_posmsk_codegen)

cmsis_posmsk_codegen is a small utility to generate Pos and Msk definitions for registers, particularly for CMSIS projects. It can be used for any project but the Pos and Msk definitions are compatible with other definitions in CMSIS v5.

# Installation

```
$ pip install cmsis_posmsk_codegen
```

then use:

```
$ cmsis_posmsk_codegen reg.yaml
```

# Register Definition (yaml)

One or more registers are defined in a yaml file like this:

```
REG_1:
  - FIELD_1: 2
  - FIELD_2: 3
  - RESERVED: 27
REG_2
  - RESERVED: 3
  - RESERVED: 5
  - FIELD_1: 24
```

The field names are taken as it is for code generation. Since the generated code is C definitions, you probably want to write both register and field names in upper case.

The number next to field name after colon is the number of bits of this field. It is assumed registers are 32-bit, so the total of bits of all fields in a register definiiton has to be 32-bit. If it is not, an error is generated and no output is given.

If a field name is called RESERVED, no definition is generated, and its bits are skipped. Since this field is not generated, there can be more than one field named RESERVED. However, any other name (both registers and fields) has to be unique. If you want to keep a reserved field, name it with a number like RESERVED0.

In addition to register and field names, a prefix is added to each definition. This prefix is the filename without extension of the input file given. Prefix is implicitly converted to uppercase.

A yaml file named test.yaml with the contents above generates a Pos and Msk definition pair like this one for each field (so in total 3 pairs for example above, omitting the ones called RESERVED):

```
#define TEST_REG_1_FIELD_1_Pos   2U
#define TEST_REG_1_FIELD_1_Msk   (3UL << ETM_REG_1_FIELD_1_Pos)
```

An example yaml, `etm.yaml`, is given in github repo (but not in PyPI package). It describes ARM ETM registers.

`test.yaml` and `test.expected` in the repo are used at travis build.
