from Abstract.Instruction import Instruction
from SymbolsTable.Type import OperationsMath,Type
from SymbolsTable.Exceptions import Exceptions
import math
from Instruction.Function import Function
from Abstract.NodoAST import NodoAST


class Sqrt(Function):

    def __init__(self, nombre,parametros,instrucciones,Row, Column):
        self.Id = nombre
        self.Row = Row
        self.parametros=parametros  
        self.instrucciones = instrucciones
        self.Column = Column
        self.Type = Type.NULO


        
    def interpreter(self, tree, table):
        # verifica las instrucciones de cada Operador
        #el interprete sirve para que ejecute las instrucciones que se adecuen al Type de operacion
        simbolo = table.getTabla("sqrt##param1") # crea una variable con el nombre complicado, algo que nunca vendra
        
        if simbolo ==None:
            return Exceptions("Semantico", "No se encontro el parametro de SQRT", self.getRow(),self.getColumn())

        self.setType(Type.CADENA)

        return math.sqrt(simbolo.getValue()) # se devuelve el valor ya tuncado por la funcion math.trunc 


        # sirve por si viene una operacion  que se requiere 



    def getNodo(self):
        nodo=NodoAST("SQRT")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo



   #se castea el valor que tiene para que no de error al ejecutarse en el interprete
    def obtenerVal(self, Type, val):
        if Type == Type.ENTERO:
            return int(val)
        elif Type == Type.DECIMAL:
            return float(val)
        elif Type == Type.BOOLEANO:
            return bool(val)
        return str(val)
        

    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
 
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

 
    def getOperacionIzq(self):
        return self.OperacionIzq

    def setOperacionIzq(self, OperacionIzq):
        self.OperacionIzq=OperacionIzq

    def getOperacionDer(self):
        return self.OperacionDer

    def setOperacionDer(self, OperacionDer):
        self.OperacionDer=OperacionDer
