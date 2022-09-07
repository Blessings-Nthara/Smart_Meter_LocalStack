# Smart_Meter_LocalStack

## Summary

### This project is aimed to simulate the functionality of a smart meter to measure electricity consumption. 

### I have based this project on a Serverless architecture due to the reason that smart meters can be installed in almost every building which means alot of devices resulting in producing large data sets which needs to be proccessed. Another contributing factor for choosing Serverless architecture is that the smart meter is assumed to regulary send data to the energy company about the amount of electricity energy consumed by a customer in every hour. Due to the large number of smart meters an electricity supplying company can have installed in a country/countries it is neccessary to take advantage of the benefits the cloud has to offer such as storage and computing services.


### This Project has been developed in Python and also using Django Framework for web application. Localstack was used to mock  AWS services. Localstack provides a testing environment on our local machine with the same APIs as the real AWS services. We can switch to using the real AWS services only in the production environment and beyond.  

## Run the project

### To run this project the machine has to have the following installed:

### 1. Docker
### 2. Python 3.10.6
### 3. pip
### 4. Django
### 5. dynamodb-admin
### 6. Boto3

### LocalStack Docker container must be executed with docker run command

### Once all the above requirements are met we firstly need to execute our index.py script to create a Customers table in dynamodb(For demonstration purposes only two customers are included in customerdata.json).Index.py populates our database with customer information.

### Secondly we need to deploy our lambda function which will perform all the necessary operations to manipulate all the data our smart meters will send. To deploy this function we need to execute main_utils.py. This script will deploy our lambda function in Localstack.

### Thirdly we need to run our generatedata.py script inorder to simulate our smart meter . This script will send us data every minute and our lambda function will perform all the necessary operations such as measuring the energy used and deducting from the customers Balance. It is assumed that a customer prepays for the electricity and according to the energy used the balance is deducted.

### Lastly the django server should be started. To start django we need to navigate to mysites directory and run the command (python .\manage.py runserver) and once it starts successfully we should visit (http://localhost:8000/app/)  to see all the analytics. From the mentioned link we can see how much energy is performed at a particular time both in a table form and on graph.





