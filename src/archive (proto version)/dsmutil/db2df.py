"""
Author: Austin Tabulog
Date: 12/03/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Module for converting sqlite query data to panas DataFrame.
"""
#imports
from pandas import DataFrame

def db2df(c, res, table, exclude=[], include=[]):
    """Converts sqlite query results to pandas DataFrame.
    Args:
        c (sqlite3.Cursor): cursor to db.
        res (list): result from sqlite query.
        table (str): name of table in db.
    returns:
        df (pd.DataFrame): Dataframe containing sqlite query.
    """
    # get columns from db
    qry = f"SELECT * FROM {table}"
    colRes = c.execute(qry)

    # if columns to be excluded
    if exclude != []:
        names = [des[0] for des in colRes.description if des[0] not in exclude]
    # if columns to be included
    elif include != []:
        names = [des[0] for des in colRes.description if des[0] in include]
    # if neither
    else:
        names = [des[0] for des in colRes.description]

    # return df
    return  DataFrame(res, columns=names)
