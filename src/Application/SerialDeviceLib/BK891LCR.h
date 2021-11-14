/*
B&K 891 LCR meter object header file for serial port communication.

class for B&K 891 LCR meter serial device. This is used as the wrapper over the
device's communication API.
*/
#pragma once

//includes
#include<windows.h>
#include "SerialBase.h"

namespace bk891
{
	const char query_ID[] = "*IDN?";				//fetch device ID
	const char fetch_data[] = "FETC?";				//fetch current measurement
	const char query_measParams[] = "MEAS:FUNC?";	//fetch measurement parameters
	//enum definitions
	//primary measurement symbols
	typedef enum
	{
		Cs,						//series capacitance
		Cp,						//parallel capacitance
		Ls,						//series inductance
		Lp,						//parallel inductance
		Z,						//impedance
		Y,						//admittance
		R_prim,					//Resistance at current AC frequency and level
		G_prim,					//Conductance
		DCR,					//DC resistance
	}primMeasEnum;

	//secondary measurement symbols for all primary measurements
	typedef enum
	{
		Q,						//Q factor
		D,						//Dialectric value
		R_sec,					//resistance
		G_sec,					//conductance
		THETA,					//phase angle
		X,						//reactance
		B,						//susceptance
	}secMeasEnum;

	//structure definitions
	//structure for measured data
	typedef struct
	{
		double primVal;								//value for primary measurement
		std::string primUnit;						//unit for primary measurement
		double secVal;								//value for secondary measurement
		std::string secUnit;						//unit for secondary measurement
	}measDataStruct;

	//structure for configuration data
	typedef struct
	{
		primMeasEnum primMeas;
	}measSettingsStruct;
}
//object definition
class BK891LCR : public virtual SerialBase
{
public:
	//attributes
	//methods
	//constructor
	BK891LCR(std::string port, bool printMessage = false);
	//deconstructor
	~BK891LCR(void);
	//writes given data to write buffer and appends with proper term char(s)
	void pack_writeBuff(LPCSTR data);


	/*
	* DEVICE INTERACTION METHODS
	*/
	//Get device ID from SCPI *IDN? query
	void get_devID(void);

	//Get current device measurement with FETC? query
	void fetch_meas(void);

protected:
	//attributes
	//methods

private:
	//attributes
	bk891::measDataStruct measData;
	//methods
	void store_measData(std::string s);
};

