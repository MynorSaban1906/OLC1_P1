from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Symbols import Symbols
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST



class Assignment(Instruction) :

    def __init__(self, Id, expresion, fila, columna):
        self.Id = Id
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.arreglo = False

    def interpretar(self, tree, table):

        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Exceptions): return value

        simbolo = Symbols(self.Id, self.expresion.tipo, self.fila, self.columna, value)
    
        result = table.updateTable(simbolo)

        if isinstance(result, Exceptions): return result
        
      
        return None


    def getNodo(self):
        nodo=NodoAST("ASIGNACION")
        nodo.Agregar_Hijo(str(self.getId()))
        nodo.Agregar_Hijo("=")
        nodo.Agregar_Hijo_Nodo(self.getExpresion().getNodo())
        return nodo
        
        


    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

        
    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo



    def getExpresion(self):
        return self.expresion

    def setExpresion(self,expresion):
        self.expresion= expresion

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna