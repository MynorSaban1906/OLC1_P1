from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction
from SymbolsTable.Type import Type
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Table import Table
from Instruction.Break import Break
from Instruction.Continue import Continue
from Instruction.Return import Return
from Abstract.NodoAST import NodoAST



class For(Instruction):

    def __init__(self, id, expresion1, instrucciones,Row, Column, expresion2):
        self.Id=id
        self.expresion1=expresion1
        self.expresion2=expresion2
        self.instrucciones=instrucciones
        self.Row=Row
        self.Column= Column
        self.Type=None
    
    def interpreter(self, tree, table):
        nuevaTabla = Table(table,entorno="For",declaracionTipo="variable",Row=self.Row,Column=self.Column)       #NUEVO ENTORNO
        declaracion = Symbols(self.getId(),Type.ENTERO,self.getRow(),self.getColumn(),0)
        nuevaTabla.setTabla(declaracion,nuevaTabla)
        if isinstance(declaracion, Exceptions): return declaracion # retorna error si no es correcta
        # verifica las expresiones y las analiza antes de pasarlas al for
        #el interprete sirve para que ejecute las instrucciones que se adecuen al Tipo de operacion
     
        if isinstance(self.expresion1,list):
            izq = self.PrintArray(tree,table,self.expresion1)
        else:
            izq = self.expresion1.interpreter(tree, nuevaTabla)
    

            
        if isinstance(izq, Exceptions): return izq
        # sirve por si viene un unario o solo una operacion 
        if self.expresion2 != None:
            der = self.expresion2.interpreter(tree, nuevaTabla)
            if isinstance(der, Exceptions): return der

        
        if self.expresion2 !=None:
            for x in range(izq,der):
                nuevaTabla2 = Table(nuevaTabla,entorno="For",declaracionTipo="variable",Row=self.Row,Column=self.Column)       #NUEVO ENTORNO
                for iterator in self.instrucciones:

                    simb = Symbols(self.getId(), Type.ENTERO , self.Row, self.Column, x)
                    re = nuevaTabla2.updateTable(simb)
                    if isinstance(re, Exceptions): return re

                    result= iterator.interpreter(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL FOR
                    if isinstance(result, Exceptions) :
                        tree.getExcepciones().append(result)

                    if isinstance(result, Break): return None
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return None
                    
        else: # si solo tiene una expresion entonces va a recorrer esa expresion
            for x in izq:
                nuevaTabla2 = Table(nuevaTabla,entorno="For",declaracionTipo="variable",Row=self.Row,Column=self.Column)       #NUEVO ENTORNO
                for iterator in self.instrucciones:
                    if isinstance(self.expresion1,list):
                        simb = Symbols(self.getId(), Type.ENTERO, self.Row, self.Column, x)
                    else:
                        simb = Symbols(self.getId(), self.expresion1.getType(), self.Row, self.Column, x)
                    re = nuevaTabla2.updateTable(simb)
                    if isinstance(re, Exceptions): return re

                    result= iterator.interpreter(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL FOR
                    if isinstance(result, Exceptions) :
                        tree.getExcepciones().append(result)

                    if isinstance(result, Break): return None
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return None

    def getNodo(self):
        nodo=NodoAST("FOR")
        nodo.Agregar_Hijo(self.Id)
        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        
        return nodo
        
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
