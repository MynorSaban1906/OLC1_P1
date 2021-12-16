from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction

# solo devuelve el Value del id
class Params(Instruction):
    def __init__(self, Value, Row, Column):
        self.Type=None
        self.Value = Value
        self.Row = Row
        self.Column = Column

    def interpreter(self, tree, table):
        
        value=self.Value.interpreter(tree,table)
        

        if isinstance(value,list):
            self.setType(value.getType())
        else:
            self.setType(value.getType())

        return self.getType()


    
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