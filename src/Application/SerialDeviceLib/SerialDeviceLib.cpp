// SerialDeviceLib.cpp : Defines the functions for the static library.
//
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include "SerialBase.h"
#include "framework.h"

//remove all leading whitespace from string
std::string strTools::ltrim(const std::string& s)
{
    size_t start = s.find_first_not_of(strTools::whitespace);
    if (start == std::string::npos)
    {
        return "";
    }
    else
    {
        return s.substr(start);
    }
}

//remove all trailing whitespace from string
std::string strTools::rtrim(const std::string& s)
{
    size_t end = s.find_last_not_of(strTools::whitespace);
    if (end == std::string::npos)
    {
        return "";
    }
    else
    {
        return s.substr(0, end + 1);
    }
}

//remove all leading and trailing whitespace from string
std::string strTools::trim(const std::string& s)
{
    return rtrim(ltrim(s));
}

//split string into string vector by given delimiter
std::vector<std::string> strTools::split(const std::string& s, std::string delim)
{
    //temp vars
    std::vector<std::string> strVect;
    size_t start = 0U;
    size_t end = s.find(delim);

    //loop through string and store data up to delim
    while (end != std::string::npos)
    {
        strVect.push_back(s.substr(start, end - start));
        //change the start and end indexes
        start = end + delim.length();
        end = s.find(delim, start);
    }
    //catch the final case
    strVect.push_back(s.substr(start, end));

    return strVect;
}


