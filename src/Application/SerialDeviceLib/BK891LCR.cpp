/*
B&K 891 LCR meter object source file for serial port communication.

class for B&K 891 LCR meter serial device. This is used as the wrapper over the
device's communication API.
*/

//includes
#include <string>
#include <map>
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
	this->measData.primVal = 0.0;
	this->measData.primUnit = "";
	this->measData.secUnit = "";
	this->measData.secVal = 0.0;

	//initialize default measurement function
	this->init_funcConfig();

	//establish serial connection with these settings
	this->connect();
}


///Deconstructor
BK891LCR::~BK891LCR(void) {}


//
void BK891LCR::pack_writeBuff(LPCSTR data)
{
	//wipe all data in write buffer up to write index
	memset(this->writeBuffer, serial::nullChar, this->writeIndex);

	//load given string in write buffer bytewise
	for (this->writeIndex = 0; this->writeIndex < strlen(data); this->writeIndex++)
	{
		this->writeBuffer[this->writeIndex] = data[this->writeIndex];
	}
	//handle CR+LF termination and add to write index tally
	this->append_CRLF();
}



/*
* DEVICE INTERACTION METHODS
*/
//Get device ID from SCPI *IDN? query
void BK891LCR::get_devID(void)
{
	//pack query and write to device
	this->pack_writeBuff(bk891Internal::query_ID);
	this->write();
	//read response and print message
	this->read();
	this->print_message(this->readBuffer);
}

//Get current device measurement with FETC? query
void BK891LCR::fetch_meas(void)
{
	//pack query and write to device
	this->pack_writeBuff(bk891Internal::fetch_data);
	this->write();

	//read response and print message
	this->read();
	//store data from read buffer into measurement data struct
	this->store_measData(std::string(this->readBuffer));
	this->print_message(this->readBuffer);	
}


//set primary and secondary measurement functions
void BK891LCR::set_measFunc(bk891::MeasFunc func)
{
	std::string temp = bk891Internal::set_measParams + this->funcConfigMap[func];
	//pack stored string for given measurement function and write to device
	this->pack_writeBuff(temp.c_str());
	this->write();

	//read response and print message
	this->read();
	this->print_message(this->readBuffer);
}

//fetch primary and secondary measurement functions from device
void BK891LCR::query_measFunc(void)
{
	//pack stored string for given measurement function and write to device
	this->pack_writeBuff(bk891Internal::query_measParams);
	this->write();

	//read response and print message
	this->read();
	//parse out measurement function from first three chars in read buffer
	this->parse_measFunc(std::string(this->readBuffer, 3));
	this->print_message(this->readBuffer);
}

//private method to parse primary and secondary measurement function from device query
void BK891LCR::parse_measFunc(std::string s)
{
	//iterate through map to find match
	for (const auto& any : this->funcConfigMap)
	{
		//if string matches current value
		if (!s.compare(any.second))
		{
			//update meas config with acompanying key
			this->measConfig.measFunc = any.first;
			break;
		}
	}
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
		try
		{
			//trim leading and trailing whitespace
			tempStr = strTools::trim(tempStr);
			//split by central whitespace (two space) and store to subVect
			subVect = strTools::split(tempStr, "  ");
			//catch bad split error
			if (subVect.size() == 1)
			{
				throw(subVect.size());
			}
			//store to primary data
			else if (i == 0)
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
		//exit loop if bad split
		catch(unsigned int index)
		{
			(void)index;
			break;
		}
		
	}
}

//private method to initialize function config map
void BK891LCR::init_funcConfig(void)
{
	//add all enum keys and appropriate string value pairs to config map
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::DEFAULT, ""));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::CSQ, bk891Internal::func_CSQ));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::CSD, bk891Internal::func_CSD));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::CSR, bk891Internal::func_CSR));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::CPQ, bk891Internal::func_CPQ));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::CPD, bk891Internal::func_CPD));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::CPR, bk891Internal::func_CPR));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::CPG, bk891Internal::func_CPG));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::LSQ, bk891Internal::func_LSQ));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::LSD, bk891Internal::func_LSD));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::LSR, bk891Internal::func_LSR));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::LPQ, bk891Internal::func_LPQ));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::LPD, bk891Internal::func_LPD));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::LPR, bk891Internal::func_LPR));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::LPG, bk891Internal::func_LPG));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::ZTH, bk891Internal::func_ZTH));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::YTH, bk891Internal::func_YTH));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::RX, bk891Internal::func_RX));
	this->funcConfigMap.insert(std::pair<bk891::MeasFunc, std::string>(bk891::MeasFunc::GB, bk891Internal::func_GB));
}