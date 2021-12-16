from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST

# solo devuelve el Value del id
class Primitive(Instruction):
    def __init__(self, Type, Value, Row, Column):
        self.Type = Type
        self.Value = Value
        self.Row = Row
        self.Column = Column

    def interpreter(self, tree, table):

        return self.getValue()


    def getNodo(self):
        nodo=NodoAST("PRIMITIVE")
        nodo.Agregar_Hijo(str(self.getValue()))
        return nodo
        

    
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getValue(self):
        return self.Value

    def setValue(self, Value):
        self.Value = Value

        
    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column