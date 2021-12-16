from SymbolsTable.Type import Type, RelationalOperator
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST



class Relational(Instruction):
    def __init__(self, Operator, OperacionIzq, OperacionDer, Row, Column):
        self.Operator = Operator
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Row = Row
        self.Column = Column
        self.Type = Type.BOOLEANO
        # verifica las instrucciones de cada Operator
        #el . interprete sirve para que ejecute las instrucciones que se adecuen al Type de operacion
        
    
    def interpreter(self, tree, table):
        izq = self.OperacionIzq.interpreter(tree, table)
        if isinstance(izq, Exceptions): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpreter(tree, table)
            if isinstance(der, Exceptions): return der


        if self.Operator == RelationalOperator.MAYORQUE:
            # OPERACION SOLO DE ENTEROS
            return izq>der
          

        if self.Operator == RelationalOperator.MENORQUE:
            # OPERACION SOLO DE ENTEROS
            return izq<der

        if self.Operator == RelationalOperator.IGUALIGUAL:
            # OPERACION DE IGUALDAD ==
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.CHARACTER and self.OperacionDer.Type == Type.CHARACTER:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == str(self.obtenerVal(self.OperacionDer.Type, der))
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == str(self.obtenerVal(self.OperacionDer.Type, der))
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == str(self.obtenerVal(self.OperacionDer.Type, der))
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.CADENA:
                return self.obtenerVal(self.OperacionIzq.Type, izq) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.Type, izq)) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.Type, izq)) == self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.Type, izq)) == self.obtenerVal(self.OperacionDer.Type, der)
                
            return Exceptions("Semantico", "Type Erroneo de operacion para ==.", self.getRow(), self.getColumn())

        if self.Operator == RelationalOperator.MENORIGUAL:
            # OPERACION SOLO DE ENTEROS
            return izq<=der

        if self.Operator == RelationalOperator.MAYORIGUAL:
            # OPERACION SOLO DE ENTEROS
            return izq>=der

        if self.Operator == RelationalOperator.DIFERENTE:
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Type, izq)!= self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.CHARACTER and self.OperacionDer.Type == Type.CHARACTER:
                return self.obtenerVal(self.OperacionIzq.Type, izq) !=self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.CADENA:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CADENA:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.CADENA:
                return self.obtenerVal(self.OperacionIzq.Type, izq) != self.obtenerVal(self.OperacionDer.Type, der)
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.CADENA:
                return self.obtenerVal(self.OperacionIzq.Type, izq) !=self.obtenerVal(self.OperacionDer.Type, der)

            return Exceptions("Semantico", "Type Erroneo de operacion para !=.", self.getRow(), self.getColumn())


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