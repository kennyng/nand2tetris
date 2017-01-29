#!/usr/bin/env python
"""The SymbolTable Module.

Provides a symbol table abstraction. The symbol table associates the identifier names found in the program with identifier properties needed for comilation: type, kind, and running index. The symbol table for Jack programs has two nested scopes (class/subroutine).
EXPORTED CLASSES: SymbolTable

"""


class SymbolTable:
   
    def __init__(self, class_table):
        """Creates a new empty symbol table."""
        self._class_table = class_table
        self._sub_table = {}

    def define(self, name, type, kind):
        """Defines a new identifier of a given name, type, and kind and assigns it a running index.

        STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.

        """
        index = self.subroutine_count(kind)
        self._sub_table[name] = (type, kind, index)

    def var_count(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope."""
        count = self.subroutine_count(kind)
        if self._class_table:
            return count + self._class_table.var_count(kind)
        else:
            return count

    def subroutine_count(self, kind):
        """Returns the number varaibles of the given kind already defined within current subroutine scope."""
        count = 0
        for _, (_, identifier_kind, _) in self._sub_table.items():
            if identifier_kind == kind:
                count += 1
        return count

    def find(self, name):
        """Returns the named identifier (type, kind, index) defined in the current scope."""
        if name in self._sub_table:
            return self._sub_table[name]
        elif self._class_table:
            return self._class_table.find(name)
        else:
            return None

    def kind_of(self, name):
        """Returns the kind of the named identifier in the current scope.

        If the identifier is unknown in the current scope, returns NONE.

        """
        return self.find(name)[1]

    def type_of(self, name):
        """Returns the type of the named identifier in the current scope."""
        return self.find(name)[0]

    def index_of(self, name):
        """Returns the index assigned to the named identifier."""
        return self.find(name)[2]


