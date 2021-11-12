#pragma once

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers


//namespace
namespace strTools
{
	const std::string whitespace = " \n\r\t\f\v";


	//prototypes
	//remove all leading whitespace from string
	std::string ltrim(const std::string& s);

	//remove all trailing whitespace from string
	std::string rtrim(const std::string& s);

	//remove all leading and trailing whitespace from string
	std::string trim(const std::string& s);

	//split string into string vector by given delimiter
	std::vector<std::string> split(const std::string& s, std::string delim);

}
