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
        """Get an item from Data list"""

        return self._tableData[item]

    def __delitem__(self, key):
        """Delete an item in key index from data table"""

        del self._tableData[key]

    def __repr__(self):
        """Table is represented by the table name"""

        return repr(self._tableName)

    def __str__(self):
        return str(self._tableName)

    def __len__(self):
        """Table length is the amount of data lines it contains"""

        return self._dataLines

    def get_header(self):
        """Set the header lines for the table"""

        return self._tableHeaders

    def set_header(self, table_headers):
        """Sets the headers for the table"""

        self._tableHeaders = table_headers

    def get_table_name(self):
        """Get the name of the table (filename)"""

        return self._tableName

    def add_data(self, table_data):
        """Add data to the table into data list"""

        self._tableData.append(table_data)
        self._dataLines += 1

    def output_to_file(self):
        """Build the table file, creating the file iff the table contains at
        least 1 data entry. 
        Prints the file name and the amount og entries in the table to 
        console"""

        if self._dataLines > 0:
            print("Creating table ", str(self), " with ", self._dataLines,
                  "entries\n")

            "append a .csv to filename"
            file = open(self._tableName+".csv", "w")

            "Write headers:"
            "Perform a string sanitation before writing to file"
            for head in self.get_header():
                file.write(str(head).strip("[]'")+',')

            file.write("\n")

            "Write data to table"
            "Perform more sanitation on each value of the data line"
            for dat in self._tableData:
                for value in dat:
                    file.write(str(value).strip('[]"')+',')
                file.write("\n")
            file.close()


def create_tables_from_sql(sql_file):
    """Parse the SQL file into Table classes and return a list of Table 
    classes created."""

    content = sql_file.read()
    tables = []
    "Split by ;\n to extract each line of code "
    lines = content.split(";\n")

    for line in lines:

        line_header = line.split(" `")

        "If command is CREATE TABLE:"
        "Line header[0] is the first command from the user"
        if line_header[0] == "CREATE TABLE":

            "table name is in the first part of the rest of the user command"
            table_name = line_header[1].split("`")[0]

            "Cleanup the string from various commas"
            headers = line.split("(\n")[1].split("\n)")[0].split(",\n")
            table_headers = []
            for header in headers:

                "Header values are prefixed by only spaces"
                if header.split("`")[0].isspace():

                    "Take only the name of the header"
                    table_headers.append(header.split("`")[1])

            "Create a Table, update its headers and insert into tables"
            tb = Table(table_name)
            tb.set_header(table_headers)
            tables.append(tb)

        "If command is INSERT INTO"
        if line_header[0] == "INSERT INTO":

            "Put into this table:"
            table_name = line_header[1].split("`")[0]
            "Find the correct table in the tables list by table name"
            index = 0
            for x in tables:
                if x.get_table_name() == table_name:
                    break
                else:
                    index += 1

            found_table = tables[index]

            "Extract the values of the data line"
            data_lines = line.split("VALUES (")[1].split(",(")
            for data in data_lines:
                data = data.split(")")[0]
                data = data.split(",")
                found_table.add_data(data)

    return tables


def main():
    """Main opens the SQL file for reading, calls the create_table function"""
    file = open("demo.sql", "r")
    tables = create_tables_from_sql(file)
    file.close()
    "Try to create a directory."
    try:
        mkdir("output", 0o755, )
        "If already exists, continue"
    except FileExistsError:
        pass

    chdir("output")

    "Create the Table files"
    for table in tables:
        table.output_to_file()

main()
