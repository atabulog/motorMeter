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
	const char query_ID[] = "*IDN?";			//fetch device ID
	const char fetch_data[] = "FETC?";			//fetch current measurement
}

//structure definitions
typedef struct
{
	double primVal;
	std::string primUnit;
	double secVal;
	std::string secUnit;
}measDataStruct;

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
	measDataStruct measData;
	//methods
	void store_measData(std::string s);

};

