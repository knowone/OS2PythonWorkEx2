class Table(object):
    def __init__(self, table_name):
        self._tableName = table_name
        self._tableData = []

    def __setitem__(self, key, value):
        self._tableData.insert(key, value)

    def __getitem__(self, item):
        return self._tableData[item]

    def add(self, table_data):
        self._tableData.append(table_data)


file = open("demo.sql", "r")
content = file.read()
table = []
lines = content.split("\n")
for line in lines:
    lineContent = line.split(" `")
    if lineContent[0] == "CREATE TABLE":
        print(lineContent[1].split("`")[0])

file.close()
