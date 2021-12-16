
from Abstract.Instruction import Instruction
from SymbolsTable.Type import OperationsMath,Type
from SymbolsTable.Exceptions import Exceptions
import math
from Abstract.NodoAST import NodoAST


class MathematicalOperations(Instruction):

    def __init__(self, Operator, OperacionIzq, OperacionDer, Row, Column):
        self.Operator = Operator
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Row = Row
        self.Column = Column
        self.Type = None

        
    def interpreter(self, tree, table):
        # verifica las instrucciones de cada Operador
        #el interprete sirve para que ejecute las instrucciones que se adecuen al Type de operacion
        izq = self.OperacionIzq.interpreter(tree, table)
        if isinstance(izq, Exceptions): return izq

        if self.OperacionDer != None:
            der = self.OperacionDer.interpreter(tree, table)
            if isinstance(der, Exceptions): return der

        # sirve por si viene una operacion  que se requiere 

         

        if self.Operator == OperationsMath.LOG10:
            if izq<0:
                return Exceptions("Semantico", "Error al operar un negativo en LOG10 ", self.getRow(), self.getColumn())

            if self.OperacionIzq.Type == Type.ENTERO :
                self.Type = Type.DECIMAL
                
                return math.log10(self.obtenerVal(self.OperacionIzq.Type, izq))
            elif self.OperacionIzq.Type == Type.DECIMAL :
                self.Type = Type.DECIMAL
                return math.log10(self.obtenerVal(self.OperacionIzq.Type, izq))

        elif self.Operator == OperationsMath.LOG:
            if izq<0:
                return Exceptions("Semantico", "Error al operar un negativo en LOG ", self.getRow(), self.getColumn())

            self.Type = Type.DECIMAL
    
            return math.log(self.obtenerVal(self.OperacionDer.Type, der),self.obtenerVal(self.OperacionIzq.Type, izq))



    def getNodo(self):
        if self.Operator==OperationsMath.LOG:
            nodo=NodoAST("LOG10")
            return nodo

        else:
            nodo=NodoAST("LOG")
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
