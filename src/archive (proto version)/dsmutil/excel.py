# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 11/20/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Module to envoke an active excel workbook instance.
"""
#imports
import win32com.client as win32
from pandas import ExcelFile, read_excel, DataFrame
from numpy import column_stack


def create_instance(path=None):
    """ Create exel application instance through win32com.
    Args:
    [OPTIONAL]
        path: path to excel file to open.
    Returns:
        wb (win32.GetActiveObject.Workbook): new excel workbook to save data.

    NOTE: FUNCTION DOES NOT SAVE WORKBOOK, ONLY INVOKES WORKBOOK OBJECT.
    """
    try:  # check if excel is already open, set flag, and set screen settings
        excel = win32.GetActiveObject("Excel.Application")
        excel.Visible = True
        excel.ScreenUpdating = False
        wasOpenFlag = True
    except:  # if not, create new instance, set flag, and set screen settings
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        excel.ScreenUpdating = False
        wasOpenFlag = False
    if path == None:
        wb = excel.Workbooks.Add()
    else:
        wb = excel.Workbooks.Open(path)
    return wb


def connect_currentInstance(path):
    """Connect to an open and active excel workbook.
    Args:
        path (str): path active excel file.
    Returns:
        wb (win32.GetActiveObject.Workbook): instance to given workbook.
    """
    #create excel application instance
    excel = win32.GetActiveObject("Excel.Application")
    excel.Visible = True
    excel.ScreenUpdating = True
    #connect application instance to given workbook and return to user
    return excel.Workbooks.Open(path)


def save_instance(path, wb):
    """ Save exel application instance through win32com.
    Args:
        wb (win32.Excel.Application.workbook): wb instance to save.
        path (path): full path of file to save.
    DOES:
        saves wb instance to given location.
    """
    wb.SaveAs(path)
    wb.Close()


def write_sheet(wb, data, sheetname):
    """ Write new sheet to exel application instance through win32com.
    Args:
        wb (win32.Excel.Application.workbook): wb instance to save.
        data (pd.DataFrame): formatted data to be written to excel sheet.
        sheetname (str): name of sheet.
    Note:
        This function could be adapted to write lists to excel easily if cols
        was a function input, index was generated internally or ignored, and
        data was passed in as a list or list of lists.
    """
    # create new sheet if sheetname does not exist
    sheetnames = [sheet.Name for sheet in wb.sheets]
    # select sheet if sheet exists
    if sheetname in sheetnames:
        for i in range(wb.sheets.count):
            if wb.sheets(i+1).Name == sheetname:
                sheet = wb.sheets(i+1)
    # else add new sheet to wb
    else:
        sheet = wb.sheets.Add(Before=None, After=wb.sheets(wb.sheets.count))
        sheet.name = sheetname

    # create temp variables
    cols = data.columns.values.tolist()
    index = data.index.values.tolist()
    dataList = data.values.tolist()

    # write columns to first row starting with second column
    sheet.Range(sheet.Cells(1,1), sheet.Cells(1, len(cols))).Value = cols
    #write data values
    sheet.Range(sheet.Cells(2,1),
        sheet.Cells(len(dataList)+1, len(dataList[0]))).Value = dataList


def xl2df(path, exclude=[]):
    """Converts excel (*.xlsx) file into dictionary of pandas dataframes.
    Args:
        path (filepath): path to excel file.
        exclude (list): list of sheets to exclude by sheetname.
    Returns:
        dataDict (dict): dictionary of excel data with sheetname as key, and
                         pandas dataFrame of sheet data as value.
    Note:
        Formatting is raw, and follows exactly what was in the excel sheet.
    """
    dataDict = dict()
    sheetnames = ExcelFile(path).sheet_names
    for sheet in sheetnames:
        if sheet not in exclude:
            dataDict[sheet] = read_excel(io=path, sheet_name=sheet)
        else:
            pass
    return dataDict


def get_tfsTable(path, sheet, table):
    """Returns specified and formatted tfs table from excel as pd.DataFrame.
    Args:
        path (filepath): path to excel file.
        sheet (str): data sheetname.
        table (str): sqlite data table.
    returns:
        df (pd.DataFrame):specified tfs table in pandas dataFrame with torque
                          values as the index, and frequencies as the columns.
    """
    #import entire sheet
    df = read_excel(path, sheet_name=sheet)
    cdf = read_excel(path, sheet_name=sheet)

    # find breaks in tables
    lowStop = int(
        df[df["Lowest speed"] == "Average speed"].index.values)
    avgStop = int(
        df[df["Lowest speed"] == "Peak speed"].index.values)

    # grab table specific data
    if table == "minData":
        df = df.iloc[0:lowStop]
    elif table == "avgData":
        df = df.iloc[lowStop-1 + 2:avgStop]
    elif table == "maxData":
        df = df.iloc[avgStop-1 + 2:]
    else:
        raise KeyError("table specified is not supported.")

    #create columns for df
    df.columns = ["Torque"] + df.iloc[0][1:].values.tolist()
    #set index to torque values
    df = df.set_index(df["Torque"])
    #remove frequency row, and drop torque column
    df = df.tail(-1)
    df = df.drop(["Torque"], axis=1)
    return df
