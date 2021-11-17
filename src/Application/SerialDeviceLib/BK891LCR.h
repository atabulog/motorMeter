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
	const char query_measRange[] = "MEAS:RANG?";	//fetch measurement range 
	const char set_measRange[] = "MEAS:RANG ";		//set measurement range
	const char query_measSpeed[] = "MEAS:SPEE?";	//fetch measurement speed
	const char set_measSpeed[] = "MEAS:SPEE ";		//set measurement speed
	const char query_measFreq[] = "FREQ?";			//fetch measurement frequnecy
	const char set_measFreq[] = "FREQ ";			//set measurement frequency
	
	//default values
	const double default_delayms = 50;				//default serial communication delay in ms
	const double default_measFreq = 47500;			//default measurement frequency outside audible range

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
	const char strRange_AUTO[] = "AUTO";
	const char strRange_HOLD[] = "HOLD";
	const char strSpeed_FAST[] = "FAST";
	const char strSpeed_SLOW[] = "SLOW";
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
	//get current measurement range value from device
	void query_measRange(void);
	//set current measurement range for device
	void set_measRange(bk891::MeasRange range);

	//public measurement speed methods
	//query current measurement speed for device
	void query_measSpeed(void);
	//set current measurement speed for device
	void set_measSpeed(bk891::MeasSpeed speed);

	//public measurement frequency methods
	//query current measurement frequency for device
	void query_measFreq(void);
	//set current measurement frequency for device
	void set_measFreq(double freq);

protected:
	//attributes
	//methods

private:
	//attributes
	bk891::measDataStruct measData;							//structure holding measurement data and unit information
	bk891::measConfigStruct measConfig;						//structure holding measurement configuration information
	std::map<bk891::MeasFunc, std::string> funcConfigMap;	//map holding measurement function information
	std::map<bk891::MeasLevel, std::string> measLevelMap;	//map holding measurement level information
	std::map<bk891::MeasSpeed, std::string> measSpeedMap;	//map holding measurement speed information
	std::map<bk891::MeasRange, std::string> measRangeMap;	//map holding measurement range information
	
															//methods
	//private method to store given preformatted string to measurement data structure
	void store_measData(std::string s);

	//private method to parse primary and secondary measurement function from device query
	void parse_measFunc(std::string s);

	//private method to parse measurement level from device
	void parse_measLevel(std::string s);

	//private method to parse measurement speed from device
	void parse_measSpeed(std::string s);

	//private method to parse measurement range from device
	void parse_measRange(std::string s);

	//private method to initialize function config map
	void init_attributeMaps(void);
};


