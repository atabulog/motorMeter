// MotorMeterApp.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <windows.h>
#include <iostream>
#include "BK891LCR.h"

int main()
{
	//connect to device
    BK891LCR device = BK891LCR("COM3", true);
	
	//write measurement function
	device.set_measFunc(bk891::MeasFunc::ZTH);
	
	//set and query measurement level
	device.set_measLevel(bk891::MeasLevel::HIGH);
	device.query_measLevel();

	//set and query measurement range
	device.set_measRange(bk891::MeasRange::AUTO);
	device.query_measRange();

	//set and query measurement speed
	device.set_measSpeed(bk891::MeasSpeed::FAST);
	device.query_measSpeed();

	//set and query measurement frequency
	device.query_measFreq();
	device.set_measFreq(53250);

	//query current measurement
	device.fetch_measData();

	//terminate device conn ection
	device.disconnect();
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
