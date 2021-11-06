// Application.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <Windows.h>
#include "BK891LCR.h"

int main()
{
	//connect to device
	BK891LCR device = BK891LCR("COM3");
	//report device ID
	device.get_devID();
	//disconnect on exit
	device.disconnect();

	
	return 0;
}
