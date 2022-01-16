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

	//initialize map attributes
	this->init_attributeMaps();
	
	//configure default measurement data
	this->measData.primVal = 0.0;
	this->measData.primUnit = "";
	this->measData.secUnit = "";
	this->measData.secVal = 0.0;

	//configure default measurement configuration
	this->measConfig.measFunc = bk891::MeasFunc::DEFAULT;
	this->measConfig.level = bk891::MeasLevel::HIGH;
	this->measConfig.range = bk891::MeasRange::AUTO;
	this->measConfig.speed = bk891::MeasSpeed::FAST;
	this->measConfig.frequency = bk891Internal::default_measFreq;
	

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
void BK891LCR::fetch_measData(void)
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
	std::string temp = bk891Internal::set_measFunc + this->funcConfigMap[func];
	this->measConfig.measFunc = func;
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
	this->pack_writeBuff(bk891Internal::query_measFunc);
	this->write();

	//read response and print message
	this->read();
	//parse out measurement function from first three chars in read buffer
	this->parse_measFunc(strTools::rtrim(this->readBuffer));
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



//Get current device measurement level from device
void BK891LCR::query_measLevel(void)
{
	//pack stored string for given measurement function and write to device
	this->pack_writeBuff(bk891Internal::query_measLevel);
	this->write();

	//read response and print message
	this->read();
	//parse out measurement level from response on first three bytes of read buffer
	this->parse_measLevel(strTools::rtrim(this->readBuffer));
	this->print_message(this->readBuffer);
}

//set measurement level
void BK891LCR::set_measLevel(bk891::MeasLevel level)
{
	//build command string and update current level
	std::string temp = bk891Internal::set_measLevel + this->measLevelMap[level];
	this->measConfig.level = level;
	//pack stored string for given measurement function and write to device
	this->pack_writeBuff(temp.c_str());
	this->write();

	//read response and print message
	this->read();
	this->print_message(this->readBuffer);
}

void BK891LCR::parse_measLevel(std::string s)
{
	//compare strings to determine measurement level
	if (!s.compare(bk891Internal::strLevel_HIGH))
	{
		this->measConfig.level = bk891::MeasLevel::HIGH;
	}
	else if (!s.compare(bk891Internal::strLevel_LOW))
	{
		this->measConfig.level = bk891::MeasLevel::LOW;
	}
}


//get current measurement range value from device
void BK891LCR::query_measRange(void)
{
	//pack stored string for given measurement function and write to device
	this->pack_writeBuff(bk891Internal::query_measRange);
	this->write();
	//read response
	this->read();
	//parse out measurement range then print message
	this->parse_measRange(strTools::rtrim(this->readBuffer));
	this->print_message(this->readBuffer);
}
//set current measurement range for device
void BK891LCR::set_measRange(bk891::MeasRange range)
{
	//build command string and update current value
	std::string temp = bk891Internal::set_measRange + this->measRangeMap[range];
	this->measConfig.range = range;

	//pack command and write to device
	this->pack_writeBuff(temp.c_str());
	this->write();

	//read response and print message
	this->read();
	this->print_message(this->readBuffer);
}

//private method to parse measurement range from device
void BK891LCR::parse_measRange(std::string s)
{
	//compare strings to determine mesurement range
	if (!s.compare(bk891Internal::strRange_AUTO))
	{
		this->measConfig.range = bk891::MeasRange::AUTO;
	}
	else if (!s.compare(bk891Internal::strRange_HOLD))
	{
		this->measConfig.range = bk891::MeasRange::HOLD;
	}
}



//query current measurement speed for device
void BK891LCR::query_measSpeed(void)
{
	//pack command string and write to device
	this->pack_writeBuff(bk891Internal::query_measSpeed);
	this->write();
	//read reponse
	this->read();
	//parse out measurement speed
	this->parse_measSpeed(strTools::rtrim(this->readBuffer));
	this->print_message(this->readBuffer);
}
//set current measurement speed for device
void BK891LCR::set_measSpeed(bk891::MeasSpeed speed)
{
	//build command string and update current value
	std::string temp = bk891Internal::set_measSpeed + this->measSpeedMap[speed];
	this->measConfig.speed = speed;

	//pack command and write to device
	this->pack_writeBuff(temp.c_str());
	this->write();

	//read response and print message
	this->read();
	this->print_message(this->readBuffer);
}

//private method to parse measurement speed from device
void BK891LCR::parse_measSpeed(std::string s)
{
	//compare strings to determine mesurement range
	if (!s.compare(bk891Internal::strSpeed_FAST))
	{
		this->measConfig.speed = bk891::MeasSpeed::FAST;
	}
	else if (!s.compare(bk891Internal::strSpeed_SLOW))
	{
		this->measConfig.speed = bk891::MeasSpeed::SLOW;
	}
}



//query current measurement frequency for device
void BK891LCR::query_measFreq(void)
{
	//pack command string and write to device
	this->pack_writeBuff(bk891Internal::query_measFreq);
	this->write();
	//read response
	this->read();
	//parse out measurement frequency and print message
	this->measConfig.frequency = std::stod(std::string(this->readBuffer));
	this->print_message(this->readBuffer);
}

//set current measurement frequency for device
void BK891LCR::set_measFreq(double freq)
{
	//build command string and update current value
	this->measConfig.frequency = freq;
	std::string temp = bk891Internal::set_measFreq + std::to_string(this->measConfig.frequency);

	//pack commadn and write to device
	this->pack_writeBuff(temp.c_str());
	this->write();

	//read response and print message
	this->read();
	this->print_message(this->readBuffer);

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
void BK891LCR::init_attributeMaps(void)
{
	//add all enum keys and appropriate string value pairs to config map
	
	//measurement function map
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
	
	//measurement level map
	this->measLevelMap.insert(std::pair<bk891::MeasLevel, std::string>(bk891::MeasLevel::LOW, bk891Internal::strLevel_LOW));
	this->measLevelMap.insert(std::pair<bk891::MeasLevel, std::string>(bk891::MeasLevel::HIGH, bk891Internal::strLevel_HIGH));
	
	//measurement speed map
	this->measSpeedMap.insert(std::pair<bk891::MeasSpeed, std::string>(bk891::MeasSpeed::FAST, bk891Internal::strSpeed_FAST));
	this->measSpeedMap.insert(std::pair<bk891::MeasSpeed, std::string>(bk891::MeasSpeed::SLOW, bk891Internal::strSpeed_SLOW));

	//measurement range map
	this->measRangeMap.insert(std::pair<bk891::MeasRange, std::string>(bk891::MeasRange::AUTO, bk891Internal::strRange_AUTO));
	this->measRangeMap.insert(std::pair<bk891::MeasRange, std::string>(bk891::MeasRange::HOLD, bk891Internal::strRange_HOLD));
}