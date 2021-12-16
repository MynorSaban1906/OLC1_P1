
from typing import List
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Symbols import Symbols
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST
import copy




class ModifyArray(Instruction):

    def __init__(self,Id, ListArray, NewValue, Row, Column):
        self.Id = Id
        self.ListArray=ListArray
        self.NewValue=NewValue
        self.Row = Row
        self.Column = Column
        self.Type=None

    def interpreter(self, tree, table):
        value = self.getNewValue().interpreter(tree, table) # NewValue a asignar a la posicion del arreglo especificado
        
        if isinstance(value, Exceptions): return value

        simbolo = table.getTabla(self.getId()) # obtinene el el arreglo si no existe da error

        # BUSQUEDA DEL ARREGLO
        value = self.modificarDimensiones(tree, table, copy.copy(self.getListArray()), simbolo.getValue(), value)     #RETORNA EL NewValue SOLICITADO
        if isinstance(value, Exceptions): return value
  
        return value



    def modificarDimensiones(self, tree, table, expresiones, arreglo, NewValue):
        if len(expresiones) == 0:
            if isinstance(arreglo, list):
                return Exceptions("Semantico", "Modificacion a Arreglo incompleto.",  self.getRow(), self.getColumn() )
            return NewValue
        if not isinstance(arreglo, list):
            id=arreglo.interpreter(tree,table)
            return self.modificarDimensiones(tree, table, copy.copy(expresiones), id, NewValue)

        dimension = expresiones.pop(0)
        num = dimension.interpreter(tree, table)
        if isinstance(num, Exceptions): return num
        try:
            value = self.modificarDimensiones(tree, table, copy.copy(expresiones), arreglo[num-1], NewValue)
        except:
            return Exceptions("Semantico", "No se puede acceder a la posicion del arreglo  "+ self.getId() ,  self.getRow(), self.getColumn() )
        if isinstance(value, Exceptions): return value
        if value != None:
            arreglo[num-1] = self.getNewValue().interpreter(tree,table)

        return None


    def getNodo(self):
        nodo = NodoAST("MODIFICACION ARREGLO")
        nodo.Agregar_Hijo(str(self.Id))
        exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.getListArray():
            exp.Agregar_Hijo_Nodo(expresion.getNodo())
        nodo.Agregar_Hijo_Nodo(exp)
        nodo.Agregar_Hijo_Nodo(self.NewValue.getNodo())
        
        return nodo


    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column

    def getListArray(self):
        return self.ListArray

    def setListArray(self, arreglo):
        self.ListArray=arreglo

    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getNewValue(self):
        return self.NewValue

    def setNewValue(self, NewValue):
        self.NewValue=NewValue
