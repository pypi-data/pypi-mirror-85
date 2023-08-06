import argparse
import os
from lmc_runner.functions import Functions
from lmc_runner.data import Data


def run():
    parser = argparse.ArgumentParser(
        description='Run LMC assembly code!')
    parser.add_argument(
        'name',
        help='LMC assembly code file name')
    args = parser.parse_args()

    if not os.path.isfile(args.name):
        print('Cannot find file {}'.format(args.name))
        return

    with open(args.name) as f:
        script = list(filter(
            lambda x: x.strip() != '',
            f.read().splitlines()))

    load(script)


# loads script into RAM
def load(script):
    # mapping variable names to values
    variables = {}

    # indentify variables and add to map
    for x, line in enumerate(script):
        block = line.strip().split()
        if block[0].upper() not in Functions.mapping.keys():
            variables[block[0]] = x
            del block[0]

        # add code block to RAM
        Data.RAM[x] = block

    # replace vairables in RAM with mapped values
    Data.RAM = [
        [variables[word] if word in variables.keys() else word
         for word in block]
        for block in Data.RAM]

    # replace DAT blocks with corresponding value
    for address, block in enumerate(Data.RAM):
        try:
            if block[0] == 'DAT':
                Data.RAM[address] = (
                    int(block[1]) if len(block) == 2 else 0)
        except:
            print('parsing error on line {}'.format(address + 1))
            return

    execute()


# executes data in RAM
def execute():
    while(True):
        try:
            block = Data.RAM[Data.PC]
            code = block[0].upper()
            if code == 'HLT':
                break

            # get address stored in block, if any
            address = None
            if len(block) == 2:
                address = block[1]

            # execute function based on code string
            Functions.mapping[code].__func__(address)
            Data.PC += 1
        except:
            print('runtime error on line {}'.format(Data.PC + 1))
            return
