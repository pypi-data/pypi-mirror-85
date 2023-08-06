#!/usr/bin/env python
import yaml
import sys


def main():
    if len(sys.argv) == 1:
        print("Usage: cmsis_posmsk_codegen <reg_definitions.yaml>")
        sys.exit(-1)
    y = yaml.load(open(sys.argv[1], 'r'), Loader=yaml.Loader)
    defs = []
    maxlen = 0
    for (reg, fields) in y.items():
        bit = 32
        for field in fields:
            for (field_name, field_len) in field.items():
                field_name = field_name.strip()
                # omit field if it is named RESERVED
                if field_name != 'RESERVED':
                    pos_def_define = "#define"
                    pos_def_label = "ETM_%s_%s_Pos" % (reg, field_name)
                    pos_def = pos_def_define + " " + pos_def_label
                    pos_def_v = "%uU" % (bit - field_len,)
                    msk_def = "#define ETM_%s_%s_Msk" % (reg, field_name)
                    msk_def_v = "(%uUL << %s)" % (pow(2, field_len) - 1, pos_def_label)
                    defs.append((pos_def, pos_def_v, msk_def, msk_def_v))
                    if len(pos_def) > maxlen:
                        maxlen = len(pos_def)
                    if len(msk_def) > maxlen:
                        maxlen = len(msk_def)
                bit = bit - field_len
        if bit != 0:
            print("ERROR while processing register: %s, because number of bits in yaml is not 32 but %d." % (reg, 32 - bit))
            sys.exit(-1)

    for (pos_def, pos_def_v, msk_def, msk_def_v) in defs:
        print(pos_def, end='')
        print(" " * (maxlen - len(pos_def) + 1), end='')
        print(pos_def_v)
        print(msk_def, end='')
        print(" " * (maxlen - len(msk_def) + 1), end='')
        print(msk_def_v)


if __name__ == '__main__':
    main()
