/*
B&K 891 LCR meter object header file for serial port communication.

class for B&K 891 LCR meter serial device. This is used as the wrapper over the
device's communication API.
*/
#pragma once

//includes
#include <windows.h>
#include <map>
#include "SerialBase.h"


namespace bk891Internal
{
	//commands
	const char query_ID[] = "*IDN?";				//fetch device ID
	const char fetch_data[] = "FETC?";				//fetch current measurement
	const char query_measParams[] = "MEAS:FUNC?";	//fetch measurement parameters
	const char set_measParams[] = "MEAS:FUNC ";		//set measurement parameters

	//function strings
	const char func_default[] = "";
	const char func_CSQ[] = "CSQ";
	const char func_CSD[] = "CSD";
	const char func_CSR[] = "CSR";
	const char func_CPQ[] = "CPQ";
	const char func_CPD[] = "CPD";
	const char func_CPR[] = "CPR";
	const char func_CPG[] = "CPG";
	const char func_LSQ[] = "LSQ";
	const char func_LSD[] = "LSD";
	const char func_LSR[] = "LSR";
	const char func_LPQ[] = "LPQ";
	const char func_LPD[] = "LPD";
	const char func_LPR[] = "LPR";
	const char func_LPG[] = "LPG";
	const char func_ZTH[] = "ZTH";
	const char func_YTH[] = "YTH";
	const char func_RX[] = "RX";
	const char func_GB[] = "GB";
}

namespace bk891
{										
	//measurement function enum class
	enum class MeasFunc
	{
		DEFAULT,	//default unselected value
		CSQ,		//series capacitance & Q factor
		CSD,		//series capacitance & Dialec. factor
		CSR,		//series capacitance & resistance
		CPQ,		//parallel capacitance & Q factor
		CPD,		//parallel capacitance & Dialec. factor
		CPR,		//parallel capacitance & resistance
		CPG,		//parallel capacitance & conductance
		LSQ,		//series inductance & Q factor
		LSD,		//series inductance & Dialec. factor
		LSR,		//series inductance & resistance
		LPQ,		//parallel inductance & Q factor
		LPD,		//parallel inductance & Dialec. factor
		LPR,		//parallel inductance & resistance
		LPG,		//parallel inductance & conductance
		ZTH,		//impedance and phase
		YTH,		//admittance and phase
		RX,			//resistance and reactance
		GB,			//conductance and susceptance
	};

	//structure definitions
	//structure for measured data
	typedef struct
	{
		double primVal;								//value for primary measurement
		std::string primUnit;						//unit for primary measurement
		double secVal;								//value for secondary measurement
		std::string secUnit;						//unit for secondary measurement
	}measDataStruct;

	typedef struct
	{
		bk891::MeasFunc measFunc;
		double frequency;
	}measConfigStruct;
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
	
	//set primary and secondary measurement functions
	void set_measFunc(bk891::MeasFunc func);

	//fetch primary and secondary measurement functions from device
	void query_measFunc(void);

protected:
	//attributes
	//methods

private:
	//attributes
	bk891::measDataStruct measData;							//structure holding measurement data and unit information
	bk891::measConfigStruct measConfig;						//structure holding measurement configuration information
	std::map<bk891::MeasFunc, std::string> funcConfigMap;	//map holding measurement function information

	//methods
	//private method to store given preformatted string to measurement data structure
	void store_measData(std::string s);

	//private method to parse primary and secondary measurement function from device query
	void parse_measFunc(std::string s);

	//private method to initialize function config map
	void init_funcConfig(void);
};


