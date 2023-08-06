from lmc_runner.data import Data


class Functions:
    @staticmethod
    def out(address):
        print(Data.ACC)

    @staticmethod
    def inp(address):
        Data.ACC = int(input('Input: '))

    @staticmethod
    def lda(address):
        Data.ACC = Data.RAM[int(address)]

    @staticmethod
    def sta(address):
        Data.RAM[int(address)] = Data.ACC

    @staticmethod
    def add(address):
        Data.ACC += Data.RAM[int(address)]

    @staticmethod
    def sub(address):
        Data.ACC -= Data.RAM[int(address)]

    @staticmethod
    def brp(address):
        if Data.ACC >= 0:
            Data.PC = int(address) - 1

    @staticmethod
    def brz(address):
        if Data.ACC == 0:
            Data.PC = int(address) - 1

    @staticmethod
    def bra(address):
        Data.PC = int(address) - 1

    @staticmethod
    def dat(address):
        Data.RAM[Data.PC] = int(address)

    mapping = {
        'OUT': out,
        'INP': inp,
        'LDA': lda,
        'STA': sta,
        'ADD': add,
        'SUB': sub,
        'BRP': brp,
        'BRZ': brz,
        'BRA': bra,
        'DAT': dat,
        'HLT': '',
    }
