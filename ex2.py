""" 
This program was written by Omer Schwartz
    email: kno34w.one.omer at2 g[mail] dot com (remove numbers and brackets)
    
    This program takes an indented SQL file, containing table description
    and data, and creates for each table a separate csv file with the table
    header and tables.
"""
# ------------------------------------------------------------------------------
from os import chdir, mkdir


class Table(object):
    """
        Class Table represents a table class the contains a table name, headers
        and data with a data lines counter. 
        The class will have specific methods to add data to the table, and write
        the table to a file.
    """
    def __init__(self, table_name):
        """Initialize the Table object with table_name as the table name and
        File name"""

        self._tableName = table_name
        self._tableHeaders = []
        self._tableData = []
        self._dataLines = 0     # counter for number of data lines added

    def __setitem__(self, key, value):
        """Set the item in key index into the Data list"""

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
        if self._dataLines > 0:
            print("Creating table ", str(self), " with ", self._dataLines,
                  "entries\n")
            file = open(self._tableName+".csv", "w")
            for head in self.get_header():
                file.write(str(head).strip("[]'")+',')

            file.write("\n")
            for dat in self._tableData:
                for value in dat:
                    file.write(str(value).strip('[]"')+',')
                file.write("\n")
            file.close()


def main():
    sql_file = open("demo.sql", "r")
    content = sql_file.read()
    tables = []
    lines = content.split(";\n")
    for line in lines:

        line_header = line.split(" `")
        if line_header[0] == "CREATE TABLE":

            table_name = line_header[1].split("`")[0]
            headers = line.split("(\n")[1].split("\n)")[0].split(",\n")
            table_headers = []
            for header in headers:
                if header.split("`")[0].isspace():
                    table_headers.append(header.split("`")[1])

            tb = Table(table_name)
            tb.set_header(table_headers)
            tables.append(tb)

    for line in lines:
        line_header = line.split(" `")
        if line_header[0] == "INSERT INTO":
            table_name = line_header[1].split("`")[0]
            index = 0
            for x in tables:
                if x.get_table_name() == table_name:
                    break
                else:
                    index += 1

            found_table = tables[index]
            data_lines = line.split("VALUES (")[1].split(",(")
            for data in data_lines:
                data = data.split(")")[0]
                data = data.split(",")
                # print(data)
                found_table.add_data(data)

    sql_file.close()
    mkdir("output", 0o755)
    chdir("output")
    for table in tables:
        table.output_to_file()

main()
