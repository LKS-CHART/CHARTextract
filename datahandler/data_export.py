import openpyxl
from openpyxl import Workbook
from openpyxl.compat import range
from util.string_functions import as_text
import re

def _format_worksheet(worksheet):
    """Resizes the columns to match the length of the largest data entry within the column
    
    Arguments:
        worksheet {openpyxl worksheet} -- The worksheet which you are formatting
    """

    for column_cells in worksheet.columns:
        #Getting length of longest data entry + 3
        length = max(len(as_text(cell.value)) for cell in column_cells) + 3
        #Setting size of column
        worksheet.column_dimensions[column_cells[0].column].width = length

def _typecast_cols(column_values):
    """Converts numeric values into floats or ints
    
    Arguments:
        column_values {list} -- List of lists where each sublist is a column
    
    Returns:
        column_values {list} -- Typecasted list of lists where each sublist is a column
    """

    def type_cast_val(val):
        #If it is a regular integer
        if val.isdigit():
            return int(val)
        #If it is a decimal number
        elif re.match("^\d+?\.\d+?$", val):
            return float(val)
        #Anything else is returns the stringified value
        else:
            return as_text(val)

    column_values = [[type_cast_val(val) for val in column] for column in column_values]

    return column_values

def export_data_to_excel(filename, column_values, row_headers=None, mode="r"):
    """Exports data to given excel file
    
    Arguments:
        filename {String} -- Path to excel file
        column_values {list} -- List of lists where each sublist is a column containing data
    
    Keyword Arguments:
        row_headers {list} -- Column Titles (default: {None})
        mode {str} -- Append data to existing excel file - "a". Replace data and create new excel file if it does not exist - "r". (default: {"r"})
    """


    #If replace
    if mode == "r":
        #Create workbook and set active worksheet "DATA"
        wb = Workbook()

        ws1 = wb.active
        ws1.title = "Data"

        #Appending headers
        if row_headers:
            ws1.append(row_headers)

        #Formatting and typecasting columns and data
        _format_worksheet(ws1)
        column_values = _typecast_cols(column_values)

        #Adding data to worksheet row by row
        for row in zip(*column_values):
            ws1.append(row)

    #If append
    elif mode == "a":
        #Load workbook
        wb = openpyxl.load_workbook(filename)
        sheet_names = wb.get_sheet_names()

        #Append data to first sheet
        for sheet_name in sheet_names:
            cur_ws = wb[sheet_name]
            if row_headers:
                cur_ws.append(row_headers)

            for row in zip(*_typecast_cols(column_values)):
                cur_ws.append(row)
            
            break

    wb.save(filename=filename)

# export_data_to_excel("test.xlsx", [["1", "2"], ["3","4"]], ["Column Header: {0}".format(i) for i in range(10)])
# export_data_to_excel("test.xlsx", [["1.0", "2.1"], ["3.0","4.1"]], mode="a")
