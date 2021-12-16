from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Symbols import Symbols
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
import copy
from Abstract.NodoAST import NodoAST


class StatementArray(Instruction):

    def __init__(self,Id, Lista,Row, Column):
        self.Id=Id
        self.Lista=Lista
        self.Row=Row
        self.Column=Column
        self.arreglo=True



    def interpreter(self, tree, table):
        
        array=[]
        for x in self.getLista():
            if isinstance(x,list):
                array.append(self.PrintArray(tree,table,x))
            else:
                array.append(x.interpreter(tree,table))

        simbolo = Symbols( self.getId(), Type.ARREGLO, self.getRow(), self.getColumn(), array,True)
       

        if(table.SearchAux(simbolo)):

            result = table.updateTable(simbolo)

            if isinstance(result, Exceptions): return result
            
        
            return None
            
        else:       
       
            result = table.setTabla(simbolo, table)

            if isinstance(result, Exceptions): return result


            return None


    def PrintArray(self,tree,table,value):
        aux=[]
        
        if isinstance(value,list):  
            for w in value:
                if isinstance(w,list):
                    aux.append(self.PrintArray(tree,table,w))
                else:
                    val=w.interpreter(tree,table)
                    if isinstance(val,list):
                        aux.append(self.PrintArray(tree,table,w))
                    else:
                        aux.append(w.interpreter(tree,table))
        
        try:
            value2 = value.interpreter(tree, table)  # RETORNA CUALQUIER VALOR para imprimir
        except:
            return aux
        if isinstance(value2,list):  
            aux=self.PrintArray(tree,table,value2)

        return aux





    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.Agregar_Hijo(str(self.getId()))
        exp = NodoAST("DIMENSIONES ARREGLO")
        exp.Agregar_Hijo_Nodo(self.Printray(self.Lista))
        nodo.Agregar_Hijo_Nodo(exp)
        return nodo

    def Printray(self,value):
        aux=NodoAST("ARREGLO")
        if isinstance(value,list):  
            for w in value:
                if isinstance(w,list):
                    aux.Agregar_Hijo_Nodo(self.Printray(w))
                else:
                    val=w.getNodo()
                    if isinstance(val,list):
                        aux.Agregar_Hijo_Nodo( self.PrintArray(w))
                    else:
                        aux.Agregar_Hijo_Nodo(w.getNodo())
        
        try:
            value2 = value.getNodo()  # RETORNA CUALQUIER VALOR para imprimir
        except:
            return aux
        if isinstance(value2,list):  
            aux.Agregar_Hijo_Nodo(self.PrintArray(value2))

        return aux



    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id


    def getLista(self):
        return self.Lista

    def setLista(self, Lista):
        self.Lista=Lista


    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column

    def getArreglo(self):
        return self.arreglo

    def setArreglo(self, arreglo):
        self.arreglo= arreglo