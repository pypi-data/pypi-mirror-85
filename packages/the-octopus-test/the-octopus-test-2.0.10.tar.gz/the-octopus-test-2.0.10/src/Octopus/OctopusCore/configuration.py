#!/usr/bin/env python3

class Configuration:
  connectionStrings =	{    
    "ExcelConn":"Driver={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};DBQ=[ControlFileName];",
  }

  appSettings =	{
    "ControlFileName": "\\resources\\TestData\\ControlFile.xlsx",
    "Browser.DefaultTimeout": "10",
    "ChromeDriverPath": "\\resources\\ChromeDriver\\chromedriver.exe",
    "FirFoxDriverPath": "\\resources\\FireFoxDriver\\geckodriver.exe",
    "IEedgeDriverPath": "\\resources\\IEedgeDriver\\MicrosoftWebDriver.exe",
    "ReportPath":"\\reports"
  }


