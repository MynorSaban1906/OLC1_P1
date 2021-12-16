
from SymbolsTable.Type import Type
from SymbolsTable.Exceptions import Exceptions
from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST

class Return(Instruction):
    
    def __init__(self, expresion, Row, Column):
        self.expresion = expresion
        self.Row = Row
        self.Column = Column
        self.Type = None
        self.result = None

    def interpreter(self, tree, table):
        result = self.expresion.interpreter(tree, table)
        if isinstance(result, Exceptions): return result
        # obtiene el Type de dato que trae la funcion y lo guarda el return para igualarlo a una variable o retornarla
        # se obtiene de la sig: opera la expresiones y obtiene el resultado y luego lo devuelve
        #pero en este caso se obtiene el Type de dato que tiene la expresion 
        #y se iguala al Type de dato del return
        self.setType(self.getExpresion().getType())

        self.result=result         # aqui se devuelve el valor en si, lo que se quiere devolver da la funcion o ciclo


        return self



    def getNodo(self):
        nodo=NodoAST("Return")

        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo



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

    def getExpresion(self):
        return self.expresion

    def setExpresion(self,expresion):
        self.expresion=expresion