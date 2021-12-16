from SymbolsTable.Type import Type
from Instruction.Function import Function
from SymbolsTable.Exceptions import Exceptions
import math
from Abstract.NodoAST import NodoAST


class Float(Function):
    def __init__(self, nombre,parametros,instrucciones,Row, Column):
        self.Id = nombre
        self.Row = Row
        self.parametros=parametros  
        self.instrucciones = instrucciones
        self.Column = Column
        self.Type = Type.NULO

    def interpreter(self, tree, table):
        simbolo = table.getTabla("float##param1") # crea una variable con el nombre complicado, algo que nunca vendra
        
        if simbolo ==None:
            return Exceptions("Semantico", "No se encontro el parametro de Float ", self.getRow(),self.getColumn())

        if simbolo.getType() not in(Type.ENTERO, Type.DECIMAL): # si no es igual al Type entero o decimal este entraria en un error
            return Exceptions("Semantico", "No se puede usar Float  "  , simbolo.getRow(),simbolo.getColumn())
     
      
        self.setType(simbolo.getType()) # se pasa el Type de dato el cual siempre seria Type cadena
        
        return float(simbolo.getValue())# se devuelve el valor ya tuncado por la funcion math.trunc 
            



    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getParametros(self):
        return self.parametros

    def setParametros(self, parametros):
        self.parametros=parametros

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

        
    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column