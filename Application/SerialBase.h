/*
SerialBase object header file for windows serial port interaction.

Serial  base class for generic serial devices. This is used to handle
the windows API level logic and expose an abstracted serial object to the
developer.
*/

#pragma once

//includes
#include <Windows.h>
#include <string.h>

//default constants for serial base object
namespace serial
{
	const  uint32_t readBufferSize = 8192;			//max number of chars read from read buffer at a time.
	const uint32_t writeBufferSize = 256;				//max number of chars written to seial device at a time.
	const uint32_t maxConnAttemps = 5;				//max number of connection attempts before connection error.
	const char CR = 0x0D;
	const char LF = 0x0A;
	const char connectionSuccessMsg[] = "Connection established";
	const char connectionFailedMsg[] = "Connection failed";
	const char port_header[] = "\\\\.\\";
}

//serial base object
class SerialBase
{
public:
	//attributes
	LPCSTR					port;																//pointer to string defining port
	bool						printMessageFlag;										//flag that determines if serial data and connection messages are printed.
	char						readBuffer[serial::readBufferSize];		//buffer holding read data
	char						writeBuffer[serial::writeBufferSize];	//buffer holding write data
	bool						readStatus;													//status flag of most recent serial read
	bool						writeStatus;													//status flag of most recent serial write

	//methods
	//object constructor
	SerialBase(std::string port);
	//object deconstructor
	~SerialBase();

	//connect object to physical device on stored COM port with supplied configuration settings.
	void	connect(LPDCB dcbPtr, LPCOMMTIMEOUTS timeoutPtr);
	// disconnect object from serial device on given COM port.
	void	disconnect(void);

	//reads data from device and stores at top of read buffer.
	void	read(void) ;
	//writes data in write buffer to device.
	void	 write(void) ;

	//virtual function to load data to the write buffer. must be formatted properly per device.
	virtual void pack_writeBuff(LPCSTR data) = 0;

	//prints given message if printMessageFlag attribute is true
	void print_message(LPCSTR msg);


protected:
	//attributes
	uint32_t			writeIndex;									//current index location of writeBuffer
	uint32_t			readIndex;									//current index location of readBuffer
	HANDLE			hcomm;											//handle to serial connection
	
	//methods
	//safely append CR '\r' to write buffer
	void					append_CR(void);
	//safely append LF '\n' to write buffer
	void					append_LF(void);
	//safely append CR and LF '\r\n' to write buffer
	void					append_CRLF(void);

private:
	//attributes
	//methods
};

