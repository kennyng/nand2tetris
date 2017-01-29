'''
The SymbolTable module creates and maintains the corresponedence between symbols and
their meaning(RAM and ROM addresses).

'''


class SymbolTable:
    # Creates new symbol table, initialized with predefined symbols and pre-allocated RAM 
    # addresses, rather than just an empty table
    def __init__(self):
        self._symbol_table = {
            'SP':     0,
            'LCL':    1,
            'ARG':    2,
            'THIS':   3,
            'THAT':   4,
            'SCREEN': 0x4000,
            'KBD':    0x6000,
        }
        # Add R0 - R15 to Symbol Table
        for i in range(16):
            self._symbol_table['R%s' %i] = i
        # Set base address for variable symbols
        self._variable_addr = 16

    # Adds the pair (symbol, address) to symbol table
    def add_entry(self, symbol, address):
        self._symbol_table[symbol] = address

    # Adds variables to the symbol table, starting at base RAM address 16 and then 
    # consecutive emmory locations 
    def add_variable(self, symbol):
        self.add_entry(symbol, self._variable_addr)
        self._variable_addr += 1

    # Checks whether symbol table contains specified symbol
    def contains(self, symbol):
        return symbol in self._symbol_table

    # Returns the address associated with the symbol
    def get_address(self, symbol):
        return self._symbol_table[symbol]


# Builds the initial symbol table for the first pass, adds only L_COMMANDs to symbol table
class SymbolTableBuilder:
    def __init__(self, parser):
        self._parser = parser

    def build(self):
        count = 0
        symbol_table = SymbolTable()

        while self._parser.has_more_commands():
            self._parser.advance()
            if self._parser.command_type() != 'L_COMMAND':
                count += 1
            else:
                symbol_table.add_entry(self._parser.symbol(), count)
        return symbol_table

