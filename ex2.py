class Table(object):
    def __init__(self, table_name):
        self._tableName = table_name
        self._tableHeaders = []
        self._tableData = []

    def __setitem__(self, key, value):
        self._tableData[key] = value

    def __getitem__(self, item):
        return self._tableData[item]

    def __delitem__(self, key):
        del self._tableData[key]

    def __repr__(self):
        return repr(self._tableName)

    def __str__(self):
        return str(self._tableName)

    def set_header(self, table_headers):
        self._tableHeaders = table_headers

    def add_data(self, table_data):
        self._tableData.append(table_data)

    def output_to_file(self):
        if len(self._tableData) > 0:
            file = open(self._tableName, "w")
            file.write(self._tableHeaders)
            for data in self._tableData:
                file.write(data)
            file.close()

sql_file = open("demo.sql", "r")
content = sql_file.read()
table = []
lines = content.split(";\n")
for line in lines:

    line_header = line.split(" `")
    if line_header[0] == "CREATE TABLE":
        # print(x, line_header[0])
        tableName = line_header[1].split("`")[0]
        # print(tableName)
        headers = line.split("(\n")[1].split("\n)")[0].split(",\n")
        tableHeaders = []
        for header in headers:
            tableHeaders.append(header.split("`")[1])
        tb = Table(tableName)
        tb.set_header(tableHeaders)
        table.append(tb)


print(table)

for line in lines:
    lineContent = line.split()

sql_file.close()
