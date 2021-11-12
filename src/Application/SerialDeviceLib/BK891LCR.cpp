/*
B&K 891 LCR meter object source file for serial port communication.

class for B&K 891 LCR meter serial device. This is used as the wrapper over the
device's communication API.
*/

//includes
#include <string>
#include <iostream>
#include "BK891LCR.h"
#include "framework.h"


//Constructor
BK891LCR::BK891LCR(std::string port, bool printMessage)
	: SerialBase(port, printMessage)
{
	//configure dcb with proper settings
	this->dcb.BaudRate = 57600;
	this->dcb.ByteSize = 8;
	this->dcb.Parity = 0;
	this->dcb.StopBits = 1;
	this->dcb.fDtrControl = DTR_CONTROL_DISABLE;
	this->dcb.fRtsControl = RTS_CONTROL_DISABLE;

	//configure timeout with proper settings
	this->timeout.ReadIntervalTimeout = 50;
	this->timeout.ReadTotalTimeoutConstant = 100;
	this->timeout.WriteTotalTimeoutConstant = 100;

	//configure default measurement data
	this->measData.primUnit = "";
	this->measData.primVal = 0.0;
	this->measData.secUnit = "";
	this->measData.secVal = 0.0;

	//establish serial connection with these settings
	this->connect();
}


///Deconstructor
BK891LCR::~BK891LCR(void) {}


//
void BK891LCR::pack_writeBuff(LPCSTR data)
{
	//load given string in write buffer bytewise
	for (this->writeIndex = 0; this->writeIndex < strlen(data); this->writeIndex++)
	{
		this->writeBuffer[this->writeIndex] = data[this->writeIndex];
	}
	//handle CR+LF termination
	this->append_CRLF();
}



/*
	* DEVICE INTERACTION METHODS
	*/
	//Get device ID from SCPI *IDN? query
void BK891LCR::get_devID(void)
{
	//pack query and write to device
	this->pack_writeBuff(bk891::query_ID);
	this->write();
	//read response and print message
	this->read();
	this->print_message(this->readBuffer);
}

void BK891LCR::fetch_meas(void)
{
	//pack query and write to device
	this->pack_writeBuff(bk891::fetch_data);
	this->write();

	//read response and print message
	this->read();
	this->print_message(this->readBuffer);

	this->store_measData(std::string(this->readBuffer));
	
}


//private function to store measurement data
void BK891LCR::store_measData(std::string s)
{
	//temp vars
	std::vector<std::string> readVect;
	std::vector<std::string> subVect;

	//populate vector by separating by comma
	readVect = strTools::split(s, ",");

	//iterate through vector and track index
	int i = 0;
	for (auto& tempStr : readVect)
	{
		//trim leading and trailing whitespace
		tempStr = strTools::trim(tempStr);
		//split by central whitespace (two space) and store to subVect
		subVect = strTools::split(tempStr, "  ");
		//store to primary data
		if (i == 0)
		{
			this->measData.primUnit = subVect[1];
			this->measData.primVal = std::stod(subVect[0]);
		}
		//store to secondary data
		else if (i == 1)
		{
			this->measData.secUnit = subVect[1];
			this->measData.secVal = std::stod(subVect[0]);
		}
		else
		{
			break;
		}
		i++;
	}
}
