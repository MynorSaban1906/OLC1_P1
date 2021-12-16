from SymbolsTable.Type import Type,LogicOperator
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction, Instruction
from Abstract.NodoAST import NodoAST


class Logic(Instruction):
    def __init__(self, Operator, OperacionIzq, OperacionDer, Row, Column):
        self.Operator = Operator
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Row = Row
        self.Column = Column
        self.Type = Type.BOOLEANO

    # operaciones logicas 
    # se inerpretan cada instruccion segun el Operator en este caso es el simbolo 
    # lo cual debe de generar una respuesta booleana
    def interpreter(self, tree, table):
        izq = self.OperacionIzq.interpreter(tree, table)
        if isinstance(izq, Exceptions): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpreter(tree, table)
            if isinstance(der, Exceptions): return der

        if self.Operator == LogicOperator.AND:
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) and self.obtenerVal(self.OperacionDer.Type, der)
            return Exceptions("Semantico", "Type Erroneo de operacion para AND &&. ", self.Row, self.Column)
        elif self.Operator == LogicOperator.OR:
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) or self.obtenerVal(self.OperacionDer.Type, der)
            return Exceptions("Semantico", "Type Erroneo de operacion para OR ||. ", self.Row, self.Column)
        elif self.Operator == LogicOperator.NOT:
            if self.OperacionIzq.Type == Type.BOOLEANO:
                return not self.obtenerVal(self.OperacionIzq.Type, izq)
            return Exceptions("Semantico", "Type Erroneo de operacion para NOT !. ", self.Row, self.Column)
        return Exceptions("Semantico", "Type de Operacion no Especificado. ", self.Row, self.Column)

    def obtenerVal(self, Type, val):
        if Type == Type.ENTERO:
            return int(val)
        elif Type == Type.DECIMAL:
            return float(val)
        elif Type == Type.BOOLEANO:
            return bool(val)
        return str(val)



    def getNodo(self):
        nodo= NodoAST("EXPRESSION")  
        if self.OperacionDer != None:
            nodo.Agregar_Hijo_Nodo(self.OperacionIzq.getNodo())
            nodo.Agregar_Hijo(self.simb(self.Operator.name))
            nodo.Agregar_Hijo_Nodo(self.OperacionDer.getNodo())
        else:
            nodo.Agregar_Hijo(self.simb(self.Operator.name))
            nodo.Agregar_Hijo_Nodo(self.OperacionIzq.getNodo())
            
            
        return nodo



    def simb(self, Operator):
        if Operator=="NOT":
            return "!"
        elif Operator=="AND":
            return "&&"
        elif Operator=="OR":
            return "||"



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
