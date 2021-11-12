#include "CppUnitTest.h"
#include "..\SerialDeviceLib\SerialBase.h"
#include "..\SerialDeviceLib\SerialBase.cpp"
#include "..\SerialDeviceLib\BK891LCR.h"
#include "..\SerialDeviceLib\BK891LCR.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace unitTestsSerialDeviceLib
{
	TEST_CLASS(unitTestsSerialDeviceLib)
	{
	public:
		
		TEST_METHOD(test_objectInit)
		{
			BK891LCR device = BK891LCR("COM3");
			Assert::AreEqual("\\\\.\\COM3", device.port);
		}
	};

	TEST_CLASS(unitTestsBK891LCR)
	{
	public:
		TEST_METHOD(Test_store_measData)
		{
			//create null connection device
			BK891LCR device = BK891LCR("COM3");
			Assert::AreEqual("\\\\.\\COM3", device.port);
		}
	};
}
