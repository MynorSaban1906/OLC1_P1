from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST

class Break(Instruction):
    def __init__(self, Row, Column):
        self.Row = Row
        self.Column=Column
        

    def interpreter(self, tree, table):
        return self


    def getNodo(self):
        nodo=NodoAST("BREAK")
        return nodo
        
    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
