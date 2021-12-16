from SymbolsTable.Type import Type
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST


class Id(Instruction):

# identifica que que Type y obtiene el valor de ella 
# aqui se verifica si ya existe y si no lo guarda la variable
    def __init__(self, Id, Row, Column):
        self.Id = Id
        self.Row = Row
        self.Column = Column
        self.Type = None
        
    def interpreter(self, tree, table):
        simbolo = table.getTabla(self.Id)
        
        if simbolo == None:
            return Exceptions("Semantico", "Variable " + self.Id + " no encontrada.", self.Row, self.Column)
        

        self.Type = simbolo.getType()
        
        return simbolo.getValue()

        
    def getNodo(self):
        nodo=NodoAST("ID")
        nodo.Agregar_Hijo(str(self.getId()))
        return nodo
        



    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

        
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type


    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
