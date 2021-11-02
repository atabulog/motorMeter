# MotorMeter V-0.0.1
Desktop application to characterize motors from impedance data

## Overview
MotorMeter is a desktop application to serve as a one stop shop for establishing piezo based motor characteristics through impedance analysis. This tool integrates the hardware strengths of benchtop impedance analyzers with a user friendly desktop application for in-depth analysis. The MotorMeter application enables low end impedance analyzers to be extended and perform measurements with few limitations. This wealth of experimental data can be investigated further with a built in equivalent circuit analysis tool called Zfit.

One key feature of the MotorMeter application is the Zfit engine. The Zfit engine is based on the open source python application of the same name by Gerrit Barrere at Exality.com. The Zfit engine fits experimental data to a given RLC circuit and backs out the values of the constituent components. The act of analyzing an electromechanical system like a piezo actuator as a circuit is called equivalent circuit analysis. This level of analysis provides a standard comparison of piezo actuators, and allows a complex system to be simplified into logical segments that determine system behavior.

## Requirements
MotorMeter is written as a Windows 10 application for a very specific internal need. There is no current plan to support any other platform.  

## Development Notes
MotorMeter is written by a single developer to better encapsulate and extend a set of internal software tools written while designing a complex type of piezo actuator. The initial software package extended the capabilities of the B&K 891 LCR meter and gave a simple user interface to interact with the test data. The initial version of this software was an excel template file that used macros tied to buttons as a front end. This then called a python backend to carry out the serial communication and data manipulation. The tested motor could be further analyzed with an impedance simulator for equivalent circuits. This approach worked well for internal development but struggled to be deployed on other systems at the same facility. This application is more of a passion project to complete a useful tool that enables some truly valuable analysis to be done with piezo based actuators.

## Special Thanks
I want to give a special shout out to Gerrit Barrere at Exality.com for his work on the python Zfit tool. Gerrit's work took this application from a quality of life improvement to a truly powerful tool. Gerrit laid a large foundation for analyzing complex circuit behavior and his work was generously laid out as open source to enable further development like this.

I would also like to thank my software and electronics mentor Matt P. Matt saw the potential in this design approach and the necessary software. Its not often an engineer with over 20 years of experience in a highly specialized field looks so fondly on an avant garde solution to an old problem.

Finally a large thanks to my wife and daughter who sacrificed a lot of family time for this application. 
