from SymbolsTable.Type import Type
from Instruction.Function import Function
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST


class Uppercase(Function):
    def __init__(self, nombre,parametros,instrucciones,Row, Column):
        self.Id= nombre
        self.Row = Row
        self.parametros=parametros  
        self.instrucciones = instrucciones
        self.Column = Column
        self.Type = Type.NULO

    def interpreter(self, tree, table):

        simbolo = table.getTabla("uppercase##param1") # crea una variable con el nombre complicado, algo que nunca vendra

        if simbolo ==None:
            return Exceptions("Semantico", "No se encontro el parametro de Uppercase ", self.getRow(),self.getColumn())

        if simbolo.getType() != Type.CADENA: # si no es igual al Type cadena entraria en un error
            return Exceptions("Semantico", "No se puede usar Uppercase  en  Type " +simbolo.getType() , self.getRow(),self.getColumn())
    

        self.setType(simbolo.getType()) # se pasa el Type de dato el cual siempre seria Type cadena
        
        return simbolo.getValue().upper() # se devuelve el valor en solo mayusculas


    def getNodo(self):
        nodo=NodoAST("UPPERCASE")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo



    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

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