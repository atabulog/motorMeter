// MotorMeterApp.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <windows.h>
#include <iostream>
#include "BK891LCR.h"

int main()
{
    BK891LCR device = BK891LCR("COM3", true);
	device.query_measLevel();
	
	//write measurement function
	device.set_measFunc(bk891::MeasFunc::ZTH);
	Sleep(100);
	device.set_measLevel(bk891::MeasLevel::HIGH);
	Sleep(100);
	device.query_measLevel();

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
