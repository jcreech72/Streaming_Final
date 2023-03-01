# Streaming_Final
Julie Creech 
February 21, 2023
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
V3_Listening_worker.py is the verison of the listener that provides a pause for smoker A when it is stalled. 

Once complete, the connect is closed. 
## How to Run the Program
For this exercise, to show the producer, the V1_Smoker_Emitter.py file can be run within a VS Code terminal. Once run, you will be asked whether you want the console to open, and the default browser will pop open to display the console showing a login or the queues that have been created. 
The code will continue to run until complete. It may be interrupted with a CTRl+C
The listener to run is V3_listening_worker.py because it includes a wait when the smoker A stalls. The wait will provide some time so no alerting is done during tha time. 

## Screen Shot of Running Demonstration

Screen shots of all working with the first alert noted:
![First Alert Screenshot 2023-02-27 205146](https://user-images.githubusercontent.com/89232631/222028929-73315c10-305c-4a04-ac1c-b74b5cb857a5.jpg)

Pause 5 min when temperature stalled
![Pause 5 Min Screenshot 2023-02-27 204733](https://user-images.githubusercontent.com/89232631/222028988-88f18a60-a7e1-4f48-a1d9-b3dd72f49aa9.jpg)

RabbitMQ queue
![Screenshot 2023-02-27 204656](https://user-images.githubusercontent.com/89232631/222029094-2cfe070b-07a4-4b9a-91f9-abc99d428497.jpg)

Smoker Temp Decreased by 15 Min
![Smoker Temp Decreased by 15 min Screenshot 2023-02-27 204859](https://user-images.githubusercontent.com/89232631/222029157-9f2f09de-4d9e-4e98-b829-c9ee27bc621d.jpg)

Exception worked after pause
![After Pause Exception Screenshot 2023-02-27 205235](https://user-images.githubusercontent.com/89232631/222029215-46a5c1f7-ba07-4de0-9be7-0cfe0a9c7f69.jpg)
