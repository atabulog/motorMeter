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
	const char query_measFunc[] = "MEAS:FUNC?";		//fetch measurement functions
	const char set_measFunc[] = "MEAS:FUNC ";		//set measurement functions
	const char query_measLevel[] = "LEV:AC?";		//fetch measurement level 
	const char set_measLevel[] = "LEV:AC ";			//set measurement level 
	
	//default values
	const double default_measSpeed = 45000;			//default measurement frequency outside audible range

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

	//measurement levels
	const double level_LOW = 0.5;
	const double level_HIGH = 1.0;
	const char strLevel_LOW[] = "0.5";
	const char strLevel_HIGH[] = "1.0";
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

	enum class MeasRange
	{
		AUTO,		//automatically determine freq test range
		HOLD,		//hold current range
	};

	enum class MeasSpeed
	{
		SLOW,		//800ms per measurement (per manual)
		FAST,		//200ms per measurement (per manual)
	};

	enum class MeasLevel
	{
		LOW,		//0.5 Vrms signal (per manual)
		HIGH,		//1.0 Vrms signal (per manual)
	};

	//structure definitions
	//structure for measured data
	typedef struct
	{
		double primVal;				//value for primary measurement
		std::string primUnit;		//unit for primary measurement
		double secVal;				//value for secondary measurement
		std::string secUnit;		//unit for secondary measurement
	}measDataStruct;

	typedef struct
	{
		bk891::MeasFunc measFunc;	//current measurement function
		bk891::MeasLevel level;		//current measurement level
		bk891::MeasRange range;		//current measurement range
		bk891::MeasSpeed speed;		//current measurement speed
		double frequency;			//current measurement frequency
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

	
	//Get current device measurement function with FETC? query
	void fetch_measData(void);

	//public measurement function methods
	//set primary and secondary measurement functions
	void set_measFunc(bk891::MeasFunc func);
	//fetch primary and secondary measurement functions from device
	void query_measFunc(void);

	//public measurement level methods
	//Get current device measurement level from device
	void query_measLevel(void);
	//set measurement level
	void set_measLevel(bk891::MeasLevel level);
	
	//public measurement range methods


	//public measurement speed methods


	//public measurement frequency methods

protected:
	//attributes
	//methods

private:
	//attributes
	bk891::measDataStruct measData;							//structure holding measurement data and unit information
	bk891::measConfigStruct measConfig;						//structure holding measurement configuration information
	std::map<bk891::MeasFunc, std::string> funcConfigMap;	//map holding measurement function information
	std::map<bk891::MeasLevel, std::string> measLevelMap;
	//methods
	//private method to store given preformatted string to measurement data structure
	void store_measData(std::string s);

	//private method to parse primary and secondary measurement function from device query
	void parse_measFunc(std::string s);

	//private method to parse measurement level from device
	void parse_measLevel(std::string s);

	//private method to initialize function config map
	void init_attributeMaps(void);
};


