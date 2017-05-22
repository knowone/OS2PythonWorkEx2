from os import chdir


class Table(object):
    def __init__(self, table_name):
        self._tableName = table_name
        self._tableHeaders = []
        self._tableData = []
        self._dataLines = 0

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

    def __len__(self):
        return self._dataLines

    def set_header(self, table_headers):
        self._tableHeaders = table_headers

    def get_table_name(self):
        return self._tableName

    def get_header(self):
        return self._tableHeaders

    def add_data(self, table_data):
        self._tableData.append(table_data)
        self._dataLines += 1

    def output_to_file(self):
        print(self._dataLines)
        if self._dataLines > 0:
            print("Creating file\n")
            file = open(self._tableName+".csv", "w")
            file.write(str(self._tableHeaders).strip('[]')+"\n")
            for dat in self._tableData:
                file.write(str(dat).strip('[]')+"\n")
            file.close()

sql_file = open("demo.sql", "r")
content = sql_file.read()
tables = []
lines = content.split(";\n")
for line in lines:

    line_header = line.split(" `")
    if line_header[0] == "CREATE TABLE":

        tableName = line_header[1].split("`")[0]
        headers = line.split("(\n")[1].split("\n)")[0].split(",\n")
        tableHeaders = []
        for header in headers:
            if header.split("`")[0].isspace():
                tableHeaders.append(header.split("`")[1])

        tb = Table(tableName)
        tb.set_header(tableHeaders)
        tables.append(tb)


# print(tables)
# index = 0
# for x in tables:
#     if x.get_table_name() == 'active_list_type':
#         break
#     else:
#         index += 1
# table = tables[index]
# table_header = table.get_header()
# for header in table_header:
#     print(header)

for line in lines:
    line_header = line.split(" `")
    if line_header[0] == "INSERT INTO":
        tableName = line_header[1].split("`")[0]
        index = 0
        for x in tables:
            if x.get_table_name() == tableName:
                break
            else:
                index += 1

        foundTable = tables[index]
        data_lines = line.split("VALUES (")[1].split(",(")
        for data in data_lines:
            data = data.split(")")[0]
            data = data.split(",")
            # print(data)
            foundTable.add_data(data)

table = tables[3]
chdir("output")
table.output_to_file()
sql_file.close()
