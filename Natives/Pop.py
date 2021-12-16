from Abstract.Instruction import Instruction
from SymbolsTable.Type import OperationsMath,Type
from SymbolsTable.Exceptions import Exceptions
import math
from Instruction.Function import Function
from Abstract.NodoAST import NodoAST
import copy

class Pop(Instruction):

    def __init__(self, Id, Row, Column):
        self.Id = Id
        self.Row = Row
        self.Column = Column
        self.Type = Type



    def interpreter(self, tree, table):

        simbo = table.getTabla(self.Id) # obtinene el el arreglo si no existe da error

        if simbo == None:
            return Exceptions("Semantico", "Arreglo " + self.getId() + " no encontrado", self.getRow(), self.getColumn() )

        # obtiene el arreglo 
        
        Arreglo = self.Buscar(tree, table,simbo.value)   #RETORNA EL ARREGLO DE DIMENSIONES
    
        if isinstance(Arreglo,Exceptions):return Arreglo
        
        return Arreglo


    def Buscar(self, tree, table,arreglo):
        

       
        return arreglo.pop()


    def getNodo(self):
        nodo=NodoAST("POP")
        return nodo



