
from datetime import datetime

class Exceptions:

    def __init__(self, type, description, row, column):
        self.type=type
        self.description=description
        self.row=row
        self.column=column
        self.hora= datetime.now().strftime('%d-%m-%y %H:%M:%S')

    # este metodo devuelve un objeto de tipo excepción

    def toString(self):
        return " > Error type " +self.type + "  - Description " + self.description + "  in [" + str(self.row) + "," + str(self.column) + "]" + " Hora : "+str(self.hora)

