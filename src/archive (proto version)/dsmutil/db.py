"""
Author: Austin Tabulog
last updated: 10/28/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Database module for data migration scripts.
"""
# imports
import sqlite3
import dsmutil
from os import getcwd

def init_db():
    """Initalize database in motor performance folder from the local schema.
    Args:
        None.
    Returns:
        c (sqlite3.cursor): live db cursor for use.
        conn (sqlite3.connection): live db connection.
    """
    schemaPath, _ = dsmutil.selectFile(title="Select schema.", extension="*.sql")
    qry = open(schemaPath, "r").read()
    folderpath, _ = dsmutil.selectFolder()
    conn = sqlite3.connect(folderpath+"dsmutil.db")
    c = conn.cursor()
    c.executescript(qry)
    conn.commit()
    print("A new database has been initalized.")
    return c, conn


def connect_db(filepath=None):
    """Connect to existing DUSM database.
    Args:
        None.
    Returns:
        c (sqlite3.cursor): live db cursor for use.
        conn (sqlite3.connection): live db connection.
    """
    if filepath == None:
        filepath, _ = dsmutil.selectFile(title="Select database.",
                                         extension="*.db")
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    return c, conn


def write_tfs(df, table, c, conn, logPath=None):
    """Writes tfs data outputted from import_TFSfile() to sqlite db.
    Args:
        tfsData (pd.DataFrame): dataFrame of data two write to given table.
        table (str): name of table to write to.
        c (sqlite3.cursor): cursor in db.
        conn (sqlite3.connection): connection to db.
    [OPTIONAL]
        logPath (path): logfile path to show errors; Defaults to current working directory.
    Returns:
        None.
    """
    #write formatted data to table through pandas
    try:
        df.to_sql(table, con=conn, index=False, if_exists="append")
    except:
        # try to write with sqlite for failures due to name collision
        if type(logPath) == type(None):
            logPath = getcwd()+"\\log.txt"
            with open(logPath, "a") as log:
                log.write(
                    f"Error writing {df.testID.iloc[0]} to {table}\n")
                log.close()
        print(f"error in {df.motorID.iloc[0]}")
