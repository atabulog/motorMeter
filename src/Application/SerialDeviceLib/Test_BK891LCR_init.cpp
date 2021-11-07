#include "pch.h"
#include "CppUnitTest.h"
#include "BK891LCR.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UT_serDevLib
{
	TEST_CLASS(Test_BK891LCR)
	{
	public:
		TEST_METHOD(Test_class_init)
		{
			BK891LCR device = BK891LCR("COM3");
			Assert::AreEqual("\\\\.\\COM3", device.port);
		}
	};
}
