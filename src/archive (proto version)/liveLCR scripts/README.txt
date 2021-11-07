DEPENDENCIES:
All dependencies need to be installed for each user on the computer.

python version
  Python 3.7+

python packages needed for dsmutil:
  pip upgrade: python -m pip install --upgrade pip --user
  pandas: python -m pip install pandas --user
  numpy: python -m pip install numpy --user
  visa: python -m pip install pyvisa --user
  pywin32: python -m pip install pywin32 --user
  pyserial: python -m pip install pyserial --user
  bs4: python -m pip install bs4 --user


THIS NEXT PART IS LIKELY NEVER NECESSARY:
================================================================================
To install dsmutil to your system for other program use, do the following.
dsmutil:
  1. Find your python library site packages folder
    C:\Users\atabulog\AppData\Local\Programs\Python\Python37-32\Lib\site-packages
  2. copy 'dsmutil' folder in programs folder and paste into site-packages. This
     may need admin approval.
================================================================================
