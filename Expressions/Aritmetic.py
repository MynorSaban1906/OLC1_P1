from SymbolsTable.Type import Type, ArithmeticOperator
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST

class Aritmetic(Instruction):

    def __init__(self, Operator, OperacionIzq, OperacionDer, Row, Column):
        self.Operator = Operator
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Row = Row
        self.Column = Column
        self.Type = None  
        

    def interpreter(self, tree, table):
        # verifica las instrucciones de cada Operator
        #el interprete sirve para que ejecute las instrucciones que se adecuen al Type de operacion
        izq = self.OperacionIzq.interpreter(tree, table)
        if isinstance(izq, Exceptions): return izq
        # sirve por si viene un unario o solo una operacion 
        if self.OperacionDer != None:
            der = self.OperacionDer.interpreter(tree, table)
            if isinstance(der, Exceptions): return der

        # aqui se verifica el Type de operaciones aritmeticas que se realizar 

        if self.Operator == ArithmeticOperator.MAS: #SUMA
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter + String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der) 
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CHARACTER: 
                self.Type = Type.CHARACTER
                numero= izq + ord(der)
                return chr(numero)


            # OPERACION SOLO DE DECIMALES
            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter + String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CHARACTER: 
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Decimal +Booleano ", self.getRow() , self.getColumn())



            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Booleano + String", self.getRow() , self.getColumn())
          
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der) 
                        
            # OPERACION SOLO DE CHAR
            if self.OperacionIzq.Type == Type.CHARACTER and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.CHARACTER
                numero= der + ord(izq)
                return chr(numero)



            return Exceptions("Semantico", "Type Erroneo de operacion para +.", self.getRow(), self.getColumn())


        if self.Operator == ArithmeticOperator.MENOS: # RESTA ....
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter - String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der) 
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CHARACTER: 
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Entero - Char ", self.getRow() , self.getColumn())

            # OPERACION SOLO DE DECIMALES

            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter - String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der)



            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Booleano  String", self.getRow() , self.getColumn())
          
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) - self.obtenerVal(self.OperacionDer.Type, der) 
                        


            # OPERACION SOLO DE CHAR
            if self.OperacionIzq.Type == Type.CHARACTER and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.CHARACTER
                numero= der - ord(izq)
                return chr(numero)
            elif self.OperacionIzq.Type == Type.CHARACTER and self.OperacionDer.Type == Type.CHARACTER:
                self.Type = Type.CHARACTER
                numero= ord(izq) - ord(der)
                return chr(numero)


            return Exceptions("Semantico", "Type Erroneo de operacion para - .", self.getRow(), self.getColumn())



        if self.Operator == ArithmeticOperator.POR: # MULTIPLICACION....
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter - String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der) 
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CHARACTER: 
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Entero - Char ", self.getRow() , self.getColumn())


            # OPERACION SOLO DE DECIMALES

            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter - String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)



            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Booleano  String", self.getRow() , self.getColumn())
          
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.BOOLEANO
                num= self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
                if num==0:
                    return False
                else:
                    return True 
                        

            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.CADENA:
                self.Type = Type.CADENA
                return self.obtenerVal(self.OperacionIzq.Type, izq) + self.obtenerVal(self.OperacionDer.Type, der)

            return Exceptions("Semantico", "Type Erroneo de operacion para * .", self.getRow(), self.getColumn())


        if self.Operator == ArithmeticOperator.DIV: # DIVICION....
            self.Type = Type.DECIMAL
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter - String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.BOOLEANO: 
                s
                if(der):
                    return "Inf\n"
                
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der) 
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CHARACTER: 
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Entero - Char ", self.getRow() , self.getColumn())


            # OPERACION SOLO DE DECIMALES

            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter - String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)



            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Booleano  String", self.getRow() , self.getColumn())
          
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) / self.obtenerVal(self.OperacionDer.Type, der)



            return Exceptions("Semantico", "Type Erroneo de operacion para / .", self.getRow(), self.getColumn())


        if self.Operator == ArithmeticOperator.POT: # POTENCIA....

            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter ^ String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der) 
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.CHARACTER: 
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Entero ^ Char ", self.getRow() , self.getColumn())


            # OPERACION SOLO DE DECIMALES

            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Enter - String ", self.getRow() , self.getColumn())
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der)



            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.BOOLEANO
                if((self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der))==1):
                    return True
                else:
                    False
                
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.CADENA:
                #mando a un error
                return Exceptions("Semantico", " No se puede realizar operacion Booleano  String", self.getRow() , self.getColumn())
          
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.BOOLEANO
                if((self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der))==1):
                    return True
                else:
                    False



            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.CADENA
                return self.obtenerVal(self.OperacionIzq.Type, izq) * self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.BOOLEANO:
                self.Type = Type.CADENA
                if(self.OperacionIzq==True):
                    return self.obtenerVal(self.OperacionIzq.Type, izq)
                else:
                    return "\n"

            return Exceptions("Semantico", "Type Erroneo de operacion para ^ .", self.getRow(), self.getColumn())



        if self.Operator == ArithmeticOperator.MOD: # POTENCIA....

            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) % self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) % self.obtenerVal(self.OperacionDer.Type, der)

            elif self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) % self.obtenerVal(self.OperacionDer.Type, der) 
 

            # OPERACION SOLO DE DECIMALES

            if self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) % self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) % self.obtenerVal(self.OperacionDer.Type, der)
            elif self.OperacionIzq.Type == Type.DECIMAL and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) % self.obtenerVal(self.OperacionDer.Type, der)



            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                return self.obtenerVal(self.OperacionIzq.Type, izq) % self.obtenerVal(self.OperacionDer.Type, der)

                
            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.DECIMAL:
                self.Type = Type.DECIMAL
                return self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der)

            elif self.OperacionIzq.Type == Type.BOOLEANO and self.OperacionDer.Type == Type.BOOLEANO: 
                self.Type = Type.BOOLEANO
                if((self.obtenerVal(self.OperacionIzq.Type, izq) ** self.obtenerVal(self.OperacionDer.Type, der))==1):
                    return True
                else:
                    False

            return Exceptions("Semantico", "Type Erroneo de operacion para % .", self.getRow(), self.getColumn())


        elif self.Operator == ArithmeticOperator.UMENOS:#NEGATIVIDAD UMENOS
            if self.OperacionIzq.Type == Type.ENTERO :
                self.Type = Type.ENTERO
                return -self.obtenerVal(self.OperacionIzq.Type, izq)
            elif self.OperacionIzq.Type == Type.DECIMAL :
                self.Type = Type.DECIMAL
                return -self.obtenerVal(self.OperacionIzq.Type, izq)

            return Exceptions("Semantico", "Type Erroneo de operacion para menos unario.", self.getRow(), self.getColumn())



    #se castea el valor que tiene para que no de error al ejecutarse en el interprete
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
        if Operator=="MAS":
            return "+"
        elif Operator=="MENOS":
            return "-"
        elif Operator=="DIV":
            return "/"
        elif Operator=="POR":
            return "*"
        elif Operator=="POT":
            return "**"
        elif Operator=="MOD":
            return "%"
        elif Operator=="UMENOS":
            return "-"
        elif Operator=="AUMENTO":
            return "++"
        elif Operator=="DECREMENTO":
            return "--"


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

 
    def getOperacionIzq(self):
        return self.OperacionIzq

    def setOperacionIzq(self, OperacionIzq):
        self.OperacionIzq=OperacionIzq

    def getOperacionDer(self):
        return self.OperacionDer

    def setOperacionDer(self, OperacionDer):
        self.OperacionDer=OperacionDer
