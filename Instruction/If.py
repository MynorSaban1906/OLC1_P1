from Abstract.Instruction import Instruction
from SymbolsTable.Type import Type
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Table import Table
from Instruction.Break import Break
from Instruction.Continue import Continue
from Instruction.Return import Return
from Abstract.NodoAST import NodoAST





class If(Instruction):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, ElseIf, Row, Column):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = ElseIf
        self.Row = Row
        self.Column = Column

    def interpreter(self, tree, table):
        condicion = self.condicion.interpreter(tree, table)
        if isinstance(condicion, Exceptions): return condicion

        if self.condicion.Type == Type.BOOLEANO:
            if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                nuevaTabla = Table(table,entorno="IF",declaracionTipo="variable",Row=self.Row,Column=self.Column)       #NUEVO ENTORNO
                for instruccion in self.instruccionesIf:
                    result = instruccion.interpreter(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Exceptions) :
                        tree.getExcepciones().append(result)
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result
                    if isinstance(result, Break): return result
            else:               #ELSE
                if self.instruccionesElse != None:
                    nuevaTabla = Table(table,entorno="IF",declaracionTipo="variable",Row=self.Row,Column=self.Column)        #NUEVO ENTORNO
                    for instruccion in self.instruccionesElse:
                        result = instruccion.interpreter(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Exceptions) :
                            tree.getExcepciones().append(result)
                        if isinstance(result, Return): return result
                        if isinstance(result, Break): return result
                        if isinstance(result, Continue): return result
                elif self.elseIf != None:
                    result = self.elseIf.interpreter(tree, table)
                    if isinstance(result, Exceptions): return result
                    if isinstance(result, Return): return result
                    if isinstance(result, Break): return result
                    if isinstance(result, Continue): return result

        else:
            return Exceptions("Semantico", "Type de dato no booleano en IF.", self.Row, self.Column)




    def getNodo(self):
        nodo=NodoAST("IF")

        instruccionesIf=NodoAST("INSTRUCCIONES IF")
        for instr in self.instruccionesIf:
            instruccionesIf.Agregar_Hijo_Nodo(instr.getNodo())
        nodo.Agregar_Hijo_Nodo(instruccionesIf)

        if self.instruccionesElse != None:
            instruccionesElse=NodoAST("INSTRUCCIONES ELSE")
            for instr in self.instruccionesElse:
                instruccionesElse.Agregar_Hijo_Nodo(instr.getNodo())
            nodo.Agregar_Hijo_Nodo(instruccionesElse)

        elif self.elseIf != None:
            nodo.Agregar_Hijo_Nodo(self.elseIf.getNodo())
        
        return nodo