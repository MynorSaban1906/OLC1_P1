from SymbolsTable.Type import Type
from Instruction.Function import Function
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST


class Typeof(Function):
    def __init__(self, nombre,parametros,instrucciones,Row, Column):
        self.Id = nombre
        self.Row = Row
        self.parametros=parametros  
        self.instrucciones = instrucciones
        self.Column = Column
        self.Type = Type.NULO

    def interpreter(self, tree, table):

        simbolo = table.getTabla("typeof##param1") # crea una variable con el nombre complicado, algo que nunca vendra
        
        if simbolo ==None:
            return Exceptions("Semantico", "No se encontro el parametro de TypeOf ", self.getRow(),self.getColumn())

        if isinstance(simbolo.value,list):
            self.setType("ARREGLO -> " + self.simb(simbolo.getType().name))
        else:
            self.setType(self.simb(simbolo.getType().name)) # se pasa el Type de dato el cual siempre seria Type cadena

        return str(self.getType()) # se devuelve el valor ya tuncado por la funcion math.trunc 


    def getNodo(self):
        nodo=NodoAST("TYPEOF")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo
        

    def simb(self,Type):
        if Type=="ENTERO":
            return "Int64"
        elif Type=="CADENA":
            return "String"
        elif Type=="BOOLEANO":
            return "Bool"
        elif Type=="CHARACTER":
            return "Char"
        elif Type=="NULO":
            return "Null"
        elif Type=="ARREGLO":
            return "ARREGLO"
        elif Type=="DECIMAL":
            return "float64"

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