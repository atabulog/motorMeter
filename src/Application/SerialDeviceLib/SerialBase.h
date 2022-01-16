/*
SerialBase object header file for windows serial port interaction.

Serial  base class for generic serial devices. This is used to handle
the windows API level logic and expose an abstracted serial object to the
developer.
*/

#pragma once

//includes
#include <Windows.h>
#include <vector>
#include <string.h>

//default constants for serial base object
namespace serial
{
	const  uint32_t readBufferSize = 8192;			//max number of chars read from read buffer at a time.
	const uint32_t writeBufferSize = 256;			//max number of chars written to seial device at a time.
	const uint32_t maxConnAttemps = 5;				//max number of connection attempts before connection error.
	const char portStrLen = 13;						//supports port in the form of '\\\\.\\COMXX'
	const char CR = 0x0D;							//hex val for ASCII \r
	const char LF = 0x0A;							//hex val for ASCII \n
	const char nullChar = 0x00;						//hex vall for ASCII NULL
	const char connectionSuccessMsg[] = "Serial connection established\n";
	const char connectionFailedMsg[] = "Serial connection failed\n";
	const char disconnectMsg[] = "Serial device disconnected\n";
	const char port_header[] = "\\\\.\\";
}


//serial base object
class SerialBase
{
public:
	//attributes
	char	port[serial::portStrLen];				//pointer to string defining port
	char	readBuffer[serial::readBufferSize];		//buffer holding read data
	char	writeBuffer[serial::writeBufferSize];	//buffer holding write data
	bool	printMessageFlag;						//flag that determines if serial data and connection messages are printed.
	bool	readStatus;								//status flag of most recent serial read
	bool	writeStatus;							//status flag of most recent serial write

	//methods
	//object constructor
	SerialBase(std::string port, bool printMessage = false);
	//object deconstructor
	~SerialBase();

	//connect object to physical device on stored COM port with supplied configuration settings.
	void	connect(void);
	// disconnect object from serial device on given COM port.
	void	disconnect(void);

	//reads data from device and stores at top of read buffer.
	void	read(void);
	//writes data in write buffer to device.
	void	 write(void);

	//virtual function to load data to the write buffer. must be formatted properly per device.
	virtual void pack_writeBuff(LPCSTR data) = 0;

	//prints given message if printMessageFlag attribute is true
	void print_message(LPCSTR msg);

protected:
	//attributes
	DWORD			writeIndex;				//current index location of writeBuffer
	DWORD			readIndex;				//current index location of readBuffer
	HANDLE			hcomm;					//handle to serial connection
	DCB				dcb;					//data control block defining serial connection parameters
	LPDCB			dcbPtr;					//pointer to DCB data
	COMMTIMEOUTS	timeout;				//timeout struct defining serial timeout parameters
	LPCOMMTIMEOUTS	timeoutPtr;				//pointer to timeout struct

	//methods
	//safely append CR '\r' to write buffer
	void	append_CR(void);
	//safely append LF '\n' to write buffer
	void	append_LF(void);
	//safely append CR and LF '\r\n' to write buffer
	void	append_CRLF(void);

private:
	//attributes
	//methods
};


/*
*generic serial functions
*/
//return string array of currently connected COM ports
std::vector<std::string> get_activeComPorts(void);