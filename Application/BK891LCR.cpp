/*
B&K 891 LCR meter object source file for serial port communication.

class for B&K 891 LCR meter serial device. This is used as the wrapper over the
device's communication API.
*/

//includes
#include <string>
#include <iostream>
#include "BK891LCR.h"

//Constructor
BK891LCR::BK891LCR(std::string port)
	: SerialBase(port)
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

	//establish serial connection with these settings
	this->connect();
}

///Deconstructor
BK891LCR::~BK891LCR(void) {}

//
void BK891LCR::pack_writeBuff(LPCSTR data)
{
	//load given string in write buffer bytewise
	for (this->writeIndex=0; this->writeIndex < strlen(data); this->writeIndex++)
	{
		this->writeBuffer[this->writeIndex] = data[this->writeIndex];
	}
	//handle CR+LF termination
	this->append_CRLF();
}