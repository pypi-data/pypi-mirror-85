1	Introduction

The ReMAP SDK has been created in the context of the ReMAP project inside the WP2, it enables the algorithms for prognostics and diagnostics to use the data coming from the airline nodes, this first version is focused on WP5. Only using this SDK the models will be able to has access to this data and the metadata describing the data sources created by the airline staff.
This document and the design of this first ReMAP SDK version has been developed from the requirements collected in the document ReMAP ‘tasets for WP5’ describing the operations that algorithms within the ReMAP project need to interact with the data.
The ReMAP SDK has been developed for python and can be found on the python repository PyPI.

2	SDK

The ReMAP SDK is writen in python and designed to work inside the ReMAP platform to have access to the data and metadata, hence it must be used only inside the ReMAP platform, A testing environment will be developed including this public available python module.
This version of the SDK has been developed in python and supports python 2 and python 3, following the requirements found for WP5, it can be found on the pip repository for python in the url https://pypi.org/project/remapSDK/. The SDK contains the python code for the SDK and some python code for demonstration including some data to perform the tests, these files are just for demonstration purposes and the data within this files does not come from any real aircraft component.

2.1	SDK Structure

The SDK can be downloaded from PyPI in the url mentioned above, once downloaded you can find this folder structure:

    sdk
    |   remapSDK                
    |    |- __init__.py                             #packaging file
    |    |- remapSDK.py                             #python code    
    |    |- demo                                    #demo folder
    |    |    |- __init__.py                        #packaging file
    |    |    |- test_remapSDK.py                   #demo code
    |    |    |- testing_env.py                     #demonstration environment
    |    |    |- data                               #data folder
    |    |        |- dataset.csv                    #data file in csv format
    |    |        |- tasks.csv                      #tasks file in csv format
    |    |        |- schedule.csv                   #schedule file in csv format
    |    |        |- metadata.json                  #metadata file in json format
    |    |        |- sdk_config.json                #File containing SDK configuration information
    |    |        |- secret                         #File containing sdk configuration information
    |- README.MD                                    #Description and usage of the module
    |- setup.py                                     #Python packaging information for the module

The files __init__.py are packaging files for python modules. 
The demo folder contains the python code to test the SDK and to simulate the ReMAP environment. The data folder contains fake data just for demonstration purposes.
The ReMAP platform serves data files automatically to the SDK through the environment, for demonstrartion purposes the SDK expects to find these data files are provided under the demo directory, the information on these files is fake and does not come from any real aircraft.


2.2.	SDK Methods

As part of the security control, the models only can access the data using the functions of the ReMAP SDK. The SDK provides the methods needed to get any information related to the data set and the dataset itself.

    getStartTime () : timestamp - Returns the start timestamp defined for the dataset

    getEndTime (): timestamp - Returns the end timestamp defined for the dataset

    getTailNumber () : string - Returns the aircraft’s tail number for the dataset 

    getParamPartNumber (ParamName) : string - Returns the part number for the parameter passed to the function
    
    getAircraft () : json - Returns the aircraft model for this dataset

    getMetadata (): metadata [] - Returns the JSON containing the metadata for the model. See Annex to see the json format

    getReplacements () : replacement [] - Returns the list of the replacements including parameter, part number and replacement date, if someone occurs. See annex to see the json format.

    getDataset () : String - Returns the route to the dataset file. Useful to retrieve the file and access directly to the information inside it.

    getSchedule () : String - Returns the route to the schedule file. Useful to retrieve the file and access directly to the information inside it.

    getTasks () : String - Returns the route to the tasks file. Useful to retrieve the file and access directly to the information inside it.

    sendOutput(jsonoutput) : json - Send the output of the model to the ReMAP platform to be stored, Returns the output sent with the mongo id of the database. This function expects a JSON with the following structure:

        {
            "rulUnit": "test_rul_unit",
            "rulValue": 5,
            "distributionType": "Normal",
            "distributionParameters": [
                {
                    name: "mean",
                    value: 824
                },
                {
                    name: "std",
                    value: 13.2
                }
            ],
            "confidenceInterval": {
                "min": 800,
                "max": 850
            }
        }

        - rulUnit: String. Unit of the output eg. Flight cycles, flight hours

        - rulValue: Number. the value of the rul output with unit above, eg. 400

        - distributionType: String. Type of distribution (Normal, Exponential…)

        - distributionParameters: Array. Array of distribution parameters
            
            - name: String

            - value: Number

        confidenceInterval:

            - min: Number. Confidence interval lower bound

            - max: Number. Confindence interval upper bound

    sendScheduleOutput(jsonoutput) : json - Send the output of the model to the ReMAP platform to be stored, Returns the output sent with the mongo id of the database.


3  SDK Installation

The SDK has been developed in python3, it has been packaged as a python module and uploaded to PYPI (Python Pakage Index) to make it publicly available. It can be found in: https://pypi.org/project/remapSDK/. It is highly recommended to install always the latest version in the repository.
To install the SDK we recommend to use Pip, a python Package magament tool, that helps to install and manage python modules, you can use a different one if you like. 
Before starting with the installation check that you have the correct python version and pip installed. Once you have this prerequisites, to intall the sdk type in your terminal:

    >> pip install 'remapSDK'

To upgrade the latest version of the module:

    >>pip install --upgrade PackageName

Once the module is installed with pip, you can start using it in your python script in you IDE.
For more information about python modules installation visit: https://packaging.python.org/tutorials/installing-packages/


4	SDK Usage

Once you have installed python3 and the ReMAP SDK you can start creating your python script and using the SDK module to access the aircraft data and metadata.

    To use the Remap SDK it needs to be imported in your script, 

    from remapSDK import remapSDK

the remapSDK is the module to be imported from the remapSDK Folder. If the module has been installed with pip you do not need to change this import line, if you have moved or change the name of the folder containing the module, you will need to update this line.

    Create and SDK instance:

The SDK is a python class and needs to be instatiated to be configured properly:

    remapSdk=remapSDK.Sdk()

Once you have created an instance of the sdk class you can start using the methods in the sdk described in section 2.2.

This is an example of using the sdk methods:

    start=remapSdk.getStartTime()
    print(start)

    end_date=remapSdk.getEndTime()
    print(end_date)

    tailno=remapSdk.getTailNumber()
    print(tailno)

    partNo=remapSdk.getParamPartNumber("param1")
    print(partNo)

    partNo=remapSdk.getMetadata()
    print(partNo)

    partNo=remapSdk.getReplacements()
    print(partNo)

To export the result of the algorithm we need to create a json object with the output:
this output json has a format described in section 2.2.
Later, this json is passed as an argument to the sendOutput(json) method of the sdk as parameter. This method of the sdk sent this json to the ReMAP platform to be stored and returns the stored document in the database

    jsonoutput=  {
        "rulUnit": "test_rul_unit",
        "rulValue": 5,
        "distributionType": "Normal",
        "distributionParameters": [
            {
                "name": "mean",
                "value": 824
            },
            {
                "name": "std",
                "value": 13.2
            }
        ],
        "confidenceInterval": {
            "min": 800,
            "max": 850
        }
    }

    output=remapSdk.sendOutput( jsonoutput)
    print(output)


5	SDK Demo

The ReMAP SDK has been developed to work in the ReMAP platform inside an environment with configuration files, its use outside the platform is discouraged as the ReMAP environment must be emuated not just the configuraiton files but also the APIs the SDK uses to interact, extract the authentication token and send the output.
To ease and illustrate the use of the sdk a demo environment has been added to the sdk. This environment is recreated with two folders, data folder contains the configuration files the SDK needs to work, the tests folder contains two mains pyhton files besides the __init__.py, the testing_env.py file contains the python code to emulate the this environment, the test_remap.py file launch the SDK tests. 
Note that the testing environment runs a REST API Server on port 5000, you can change the port number inside this file.


6	SDK Requirements and dependencies

The SDK has some requirements to work work with it.

    - Python3: It has been developed using this version of python.
    - Pip: This is the python package manager enabling us to install the SDK.
    - The SDK will NOT WORK outside the ReMAP platform

The ReMAP SDK has some extra dependencies to work, they can be seen in the requirements.txt file under the root directory, in this file the modules required by the SDK are listed, and will be automatically installed when install the SDK with the pip install command:

    - Request	
    The requests module allows the SDK to send HTTP requests using Python. This will allow the SDK to obtain the access token to for security environment and send the output to the ReMAP repository.

    - Flask	
    Flask is a lightweight web application framework designed to make getting started quick and easy, with the ability to scale up to complex applications. The testing environment uses this module to emulate the ReMAP environment.
    This requirement is only for the demo and does not affect to the SDK.