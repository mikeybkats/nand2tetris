# translates each field into its corresponding binary value

def code_dest(mnemonic):
    if mnemonic == None:
        mnemonic = "0"
    destTable = dict([
        ("", "000"),
        ("0", "000"),
        ("M", "001"),
        ("D", "010"),
        ("MD", "011"),
        ("A", "100"),
        ("AM", "101"),
        ("AD", "110"),
        ("AMD", "111"),
    ])
    return destTable.get(mnemonic)


def code_comp(mnemonic):
    if mnemonic == None:
        mnemonic = "0"
    compTable = dict([
        ("0", "0101010"),
        ("1", "0111111"),
        ("-1", "0111010"),
        ("D", "0001100"),
        ("A", "0110000"),
        ("!D", "0001101"),
        ("!A", "0110001"),
        ("-D", "0001111"),
        ("-A", "0110011"),
        ("D+1", "0011111"),
        ("A+1", "0110111"),
        ("D-1", "0001110"),
        ("A-1", "0110010"),
        ("D+A", "0000010"),
        ("A-D", "0000111"),
        ("D-A", "0010011"),
        ("D&A", "0000000"),
        ("D|A", "0010101"),
        # below values are for comp when A value of binary instruction equals 1
        ("M", "1110000"),
        ("!M", "1110001"),
        ("-M", "1110011"),
        ("M+1", "1110111"),
        ("M-1", "1110010"),
        ("D+M", "1000010"),
        ("M-D", "1000111"),
        ("D-M", "1010011"),
        ("D&M", "1000000"),
        ("D|M", "1010101"),
    ])
    return compTable.get(mnemonic)


def code_jump(mnemonic):
    if mnemonic == None:
        mnemonic = "0"
    jumpValues = dict([
        ("", "000"),
        ("0", "000"),
        ("JGT", "001"),
        ("JEQ", "010"),
        ("JGE", "011"),
        ("JLT", "100"),
        ("JNE", "101"),
        ("JLE", "110"),
        ("JMP", "111"),
    ])
    return jumpValues.get(mnemonic)
