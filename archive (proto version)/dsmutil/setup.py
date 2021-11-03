#!/usr/bin/env python
"""
Author: Austin Tabulog
Date: 02/08/2021
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: describe setup file for pip wheel creation.
"""

#imports
from distutils.core import setup

#NOT A WORKING VERSION AND COMPLETELY UNTESTED
setup(name='dsmutil',
      version='1.0',
      description='DSM internal python utilities',
      author='Austin Tabulog',
      author_email='atabulog@dynamic-structures.com',
      packages=['dsmutil'],
     )
