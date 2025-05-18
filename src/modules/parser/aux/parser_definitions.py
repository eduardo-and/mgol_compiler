import csv


class ParserDefinitions:
    parseTablePath = "../assets/parse_table.csv"
    def __init__(self):
        self.parseTable = self.loadTable()    
        
    def loadTable(self):
        with open(self.parseTablePath, 'r') as file:
            reader = csv.reader(file)
            self.parseTable = {rows[0]: rows[1:] for rows in reader}
        return self.parseTable