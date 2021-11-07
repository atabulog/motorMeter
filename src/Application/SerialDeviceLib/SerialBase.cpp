/*
SerialBase object source file for windows serial port interaction.

serial base class for generic serial devices. This is used to handle
the windows API level logic and expose an abstracted serial object to the
developer.
*/

//includes
#include <iostream>
#include <vector>
#include "SerialBase.h"


//constructor
SerialBase::SerialBase(std::string port, bool printMessage)
{
	//init general params
	strcpy_s(this->port, serial::portStrLen, (serial::port_header + port).c_str());
	this->hcomm = INVALID_HANDLE_VALUE;
	this->printMessageFlag = printMessage;

	//init buffer specific data
	this->readBuffer;
	memset(this->readBuffer, 0, sizeof(this->readBuffer));
	this->writeBuffer;
	memset(this->writeBuffer, 0, sizeof(this->writeBuffer));
	this->readStatus = false;
	this->writeStatus = false;
	this->readIndex = 0;
	this->writeIndex = 0;

	//init dcb data
	this->dcb;
	this->dcbPtr = &this->dcb;
	this->dcb.DCBlength = sizeof(this->dcb);

	//init timeout data
	this->timeout;
	this->timeoutPtr = &this->timeout;

}


//deconstructor
SerialBase::~SerialBase(void) {}


//connect object to physical device on stored COM port with supplied configuration settings.
void	SerialBase::connect(void)
{
	//attempts serial connection until a max attempt count is reached
	for (uint32_t i = 0; i < serial::maxConnAttemps; i++)
	{
		//establish generic connection to IO resource
		this->hcomm = CreateFileA(this->port,
			GENERIC_READ | GENERIC_WRITE,		//Read/Write
			0,																		// No Sharing
			0,																		// No Security
			OPEN_EXISTING,										// Open existing port only
			FILE_ATTRIBUTE_NORMAL,					// Non Overlapped I/O
			NULL);															// Null for Comm Devices

		//continue to configuration if connection established
		if (this->hcomm != INVALID_HANDLE_VALUE)
		{
			//confgure IO resource for serial communication with dcb and commTimeout.	
			SetCommState(this->hcomm, this->dcbPtr);
			SetCommTimeouts(this->hcomm, this->timeoutPtr);
			break;
		}
	}


	//print connection messages
	if (this->hcomm == INVALID_HANDLE_VALUE)
	{
		this->print_message(serial::connectionFailedMsg);
	}
	else
	{
		this->print_message(serial::connectionSuccessMsg);
	}
}


// disconnect object from serial device on given COM port.
void	SerialBase::disconnect(void)
{
	//Close connection to the Serial Port
	CloseHandle(this->hcomm);

	//print message if allowed
	if (this->printMessageFlag)
	{
		std::cout << serial::disconnectMsg;
	}
}


//reads data from device and stores at top of read buffer.
void	SerialBase::read(void)
{
	//create temp number of bytes read
	DWORD numBytesRead = 0;
	//read from serial device.
	this->readStatus = ReadFile(this->hcomm,
		this->readBuffer,
		sizeof(this->readBuffer),
		&numBytesRead,
		NULL);
}


//writes data in write buffer to device.
void	 SerialBase::write(void)
{
	//create temp number of bytes written
	DWORD numBytesWritten = 0;
	//write packet to device
	this->writeStatus = WriteFile(this->hcomm,
		this->writeBuffer,
		this->writeIndex,
		&numBytesWritten,
		NULL);
}


//prints given message if printMessageFlag attribute is true
void SerialBase::print_message(LPCSTR msg)
{
	if (this->printMessageFlag)
	{
		std::cout << msg << "\n";
	}
}


void SerialBase::append_CR(void)
{
	if (this->writeIndex < serial::writeBufferSize - 1)
	{
		this->writeBuffer[this->writeIndex++] = serial::CR;
	}
	else
	{
		this->writeBuffer[this->writeIndex] = serial::CR;
	}
}


void SerialBase::append_LF(void)
{
	if (this->writeIndex < serial::writeBufferSize - 1)
	{
		this->writeBuffer[this->writeIndex++] = serial::LF;
	}
	else
	{
		this->writeBuffer[this->writeIndex] = serial::LF;
	}
}


void SerialBase::append_CRLF(void)
{
	// append necessary formatting into buffer
	if (this->writeIndex < serial::writeBufferSize - 2)
	{
		this->writeBuffer[this->writeIndex++] = serial::CR;
		this->writeBuffer[this->writeIndex++] = serial::LF;
	}
	else
	{
		this->writeBuffer[this->writeIndex - 1] = serial::CR;
		this->writeBuffer[this->writeIndex++] = serial::LF;
	}
}

/*
*generic serial functions
*/
//return string array of currently connected COM ports
std::vector<std::string> get_activeComPorts(void)
{
	//use this as a reference https://riptutorial.com/windows/example/32102/listing-all-serial-ports-
	//TODO: makes this actually work instead of returning an empty string vector
	std::vector<std::string> temp;
	return temp;
}