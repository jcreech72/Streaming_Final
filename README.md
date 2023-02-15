# streaming-05-smart-smoker
Julie Creech 
February 14, 2023
## Creating a Producer

# Using a Barbeque Smoker:
When running a barbeque smoker, we monitor the temperatures of the smoker and the food to ensure everything turns out tasty. Over long cooks, the following events can happen:

The smoker temperature can suddenly decline.
The food temperature doesn't change. At some point, the food will hit a temperature where moisture evaporates. It will stay close to this temperature for an extended period of time while the moisture evaporates (much like humans sweat to regulate temperature). We say the temperature has stalled.

# Sensors
We have temperature sensors track temperatures and record them to generate a history of both (a) the smoker and (b) the food over time. These readings are an example of time-series data, and are considered streaming data or data in motion.

# Streaming Data
Our thermometer records three temperatures every thirty seconds (two readings every minute). The three temperatures are:

the temperature of the smoker itself.
the temperature of the first of two foods, Food A.
the temperature for the second of two foods, Food B.

# Python Code
The Python code will import several modules: Pika, Sys, Webbrowser, CSV, Time and Pickle
Pika is used to connect to RabbitMQ server and send messages
Sys allows us to get command line arguments
Webbrowser is used to open the RabbitMQ Admin site
Time is used to add delay between sending messages
Pickle is used to serialize the tuple messages into binary data

The code offers the user to choose whether they would like to open the RabbitMQ Admin Console. If the code is set to True, it will show the option, but if set to False, the option is not offered.

The code will use Try, Except and Finally clause
First try clause is executed i.e. the code between try and except clause. If there is no exception, then only try clause will run, except clause will not get executed. If any exception occurs, the try clause will be skipped and except clause will run. 
Within the Try function the blocking connection is created to the RabbitMQ server, then a channel is established.
First, the queues are deleted to clear old messages, and then the queues are created. The queues are durable so the messages will persist, which is why they have to be deleted in the beginning. 
Next, the file is open and read. There is a for statement which iterates through the data with if statements to read the data and understand if the value is greater than 0. If it is >0, a variable is established with the value of floater type including the value within the csv file at that line. 
We provide a message showing the values and then prepare the data to be sent over the channel using a routing key. 
The listener has not yet been established; however, I was able to see in the console this reaches RabbitMQ and is sitting in a queue.

Once complete, the connect is closed. 
## How to Run the Program
For this exercise, to show the producer, the V1_Smoker_Emitter.py file can be run within a VS Code terminal. Once run, you will be asked whether you want the console to open, and the default browser will pop open to display the console showing a login or the queues that have been created. 
The code will continue to run until complete. It may be interrupted with a CTRl+C

## Screen Shot of Running Demonstration
![Screenshot 2023-02-14 221059](https://user-images.githubusercontent.com/89232631/218927714-b31acb34-850c-4ec3-8a91-7ba4da1b0741.jpg)
