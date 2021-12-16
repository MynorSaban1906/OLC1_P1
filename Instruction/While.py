from Abstract.Instruction import Instruction
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from SymbolsTable.Symbols import Symbols
from Instruction.Continue import Continue
from Instruction.Break import Break
from Instruction.Return import Return
from SymbolsTable.Table import Table
from Abstract.NodoAST import NodoAST

class While(Instruction):
    def __init__(self, Conditional, Instr, Row, Column):
        self.Conditional = Conditional
        self.Instr = Instr
        self.Row = Row
        self.Column = Column

    def interpreter(self, tree, table):
        while True:
            Conditional = self.getConditional().interpreter(tree, table)
            if isinstance(Conditional, Exceptions): return Conditional

            if self.getConditional().Type == Type.BOOLEANO:
                if bool(Conditional) == True:   # VERIFICA SI ES VERDADERA LA Conditional
                    nuevaTabla = Table(table,entorno="WHILE",declaracionTipo="variable",Row=self.Row,Column=self.Column)      #NUEVO ENTORNO
                    for instruccion in self.getInstr():
                        result = instruccion.interpreter(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Exceptions) :
                            tree.getExcepciones().append(result)
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                else:
                    break
            else:
                return Exceptions("Semantico", "Type de dato no booleano en while.", self.Row, self.Column)


    def getNodo(self):
        nodo=NodoAST("WHILE")

        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.Instr:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        
        return nodo


    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column

    def getConditional(self):
        return self.Conditional

    def setConditional(self, COnditional):
        self.Conditional=COnditional

    def getInstr(self):
        return self.Instr

    def setInstr(self, Instr):
        self.Instr =Instr