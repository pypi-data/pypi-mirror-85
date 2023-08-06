# The-Octopus-Test Automation Framework.


![Logo](https://the-octopus.github.io/OctopusHTMLReportResources/Logo_large.png)



**Th-Octopus-Test** is a **Free** Test Automation Framework for E2E Testing, that built on python programming language. Using Selenium and APPIUM test automation tools.

**Th-Octopus-Test**  is a **Hybrid** test automation framework, that combines features of (Modular, Keyword Driven and Data driven).

## Concepts Included:

* Data Driven.

* Keyword Driven.

* Page Object pattern .  [POM ](https://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html)

* Common web page interaction methods.

* Common Mobile App interaction methods.

* Objects shared repository.

* ExtentReport template for reporting.

## Installation

### Required Tools

* Microsoft Access database engine 2010. [Access Engine 2010](https://www.microsoft.com/en-sa/download/details.aspx?id=13255)

* Python. [Python](https://www.python.org/downloads/release/python-350/)

* Selenium WebDriver. [seleniumhq.org](https://www.seleniumhq.org/)

* APPIUM. [appium.io](http://appium.io/)

* VS Code or any python editor.


### Supportive Libraries:

* Install Microsoft Access database engine 2010.

* Install Python 3.5 and above.

* Configure python path and pip tools. in windows , open system variables and edit the path variable and add paths.

* Install selenium libraries using pip from command line.

```console

pip install -U selenium

```

* Install APPIUM libraries using pip from command line.

```console

pip install Appium-Python-Client

```

* Download Selenium Drivers: Selenium requires a driver to interact with the chosen browser.

* Chrome: [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

* Edge: [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

* Firefox: [FireFoxDriver](https://github.com/mozilla/geckodriver/releases)

* Safari: [SafariDriver](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)


### The-Octopus-Test Framework:

* Install the Octopus Test Framework

```console

pip install the-octopus-test

```

# Getting started :

### Clone the sample Test project [The-Octopus-Sample-Test](https://github.com/the-octopus/octopus-sample-test/)

### Please follow the structure and naming of the sample project:

```console
<Octopus_Sample_Test>
    +--------------------------+
    |                          |
    |                          |
    |<reports>                 |
    |                          |
    |<resourcses>              |                        
    |    <ChromeDriver>        |
    |    <ChromeDriver>        |
    |    <ChromeDriver>        |
    |    <ChromeDriver>        |
    |    <TestData>            |
    |       ControlFile.xlsx   |
    |<test>                    |                        
    |    <pages>               |
    |       loginPage.py       |
    |       homePage.py        |
    |       ....               |
    |       ....               |
    |    <scenarios>           |
    |       testScenarios.py   |
    |                          |
    |                          |
    |main.py                   |    
    |                          |
    |                          |
    |                          |
    +--------------------------+
```
### Open the project in your prefered IDE, I recommend VS Code editor. 

### **Follow the instructions in the [ README.MD ](https://github.com/the-octopus/octopus-sample-test/) file at the sample project**.

### Enjoy your test automation activities, and increase productivity with **the-octopus-test** python framework.


# License
The-Octopus-Test Python Framework is licensed under the LICENSE file in the root directory of the project.



## Please for more details do not hesitate to contact me at [LinkedIn](https://www.linkedin.com/in/abdelghany-abdelaziz)