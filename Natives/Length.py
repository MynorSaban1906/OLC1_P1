from Expressions.Primitive import Primitive
from Abstract.Instruction import Instruction
from SymbolsTable.Type import Type
from Instruction.Function import Function
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST



class Length(Function):
    def __init__(self, nombre,parametros,instrucciones,Row, Column):
        self.Id = nombre
        self.Row = Row
        self.parametros=parametros  
        self.instrucciones = instrucciones
        self.Column = Column
        self.Type = Type.NULO

    def interpreter(self, tree, table):


        simbolo = table.getTabla("length##param1") # crea una variable con el nombre complicado, algo que nunca vendra
        
        if simbolo ==None:
            return Exceptions("Semantico", "No se encontro el parametro de la funcion Length ", simbolo.getFila(),simbolo.getColumna())

        if isinstance(simbolo.value,list):
            self.setType(Type.ENTERO)
            return len(simbolo.value)+1

        if isinstance(simbolo,Primitive):
            
            return len(simbolo)# se devuelve el valor ya redondeado "lista para imprimir" 

        if isinstance(simbolo,str):
            
            return len(simbolo)# se devuelve el valor ya redondeado "lista para imprimir" 
        

        self.setType(Type.ENTERO) # se pasa el Type de dato el cual siempre seria Type entero
      

        return len(simbolo.getValue())# se devuelve el valor ya redondeado "lista para imprimir" 





    def getNodo(self):
        nodo=NodoAST("LENGTH")
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