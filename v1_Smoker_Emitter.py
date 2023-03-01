"""
    This program sends a message to a queue on the RabbitMQ server after reading a csv file called tasks.csv.
    Will import the CsvReader class from the csv_reader.py module.
    Will import the time module to use the sleep function to simulate work.
    Pika imports are used to connect to the RabbitMQ server and send messages.
    Sys is used to get the command line arguments.
    Webbrowser is used to open the RabbitMQ Admin site.
    Time is used to add a delay between sending messages.
    Pickle is used to serialize the tuple messages into binary data.

    The code includes an option to open the RabbitMQ Admin site. 
    This code is set to false, but if you want to use it, change the value to True.
    Make tasks harder/longer-running by adding dots at the end of the message.

    Author: Julie Creech
    Date: February 10, 2023

"""

import pika
import sys
import webbrowser
import csv
import time
import pickle 



# Offer to open the RabbitMQ Admin website
#if show_offer is set to False, the code will not run, but if set to True, the code will run
show_offer = "True"
def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    
    #print()
    if show_offer == "True":
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()
#Define message sending function
def send_message(host: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server 
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel 
        ch = conn.channel()
        # use the channel to delete the queues if they exist 
        ch.queue_delete(queue="01-smoker")
        ch.queue_delete(queue="02-food-A")
        ch.queue_delete(queue="03-food-B")
        # use the channel to declare the durable queues 
        ch.queue_declare(queue="01-smoker", durable=True)
        ch.queue_declare(queue="02-food-A", durable=True)
        ch.queue_declare(queue="03-food-B", durable=True)

        # open the input file
        input_file = open("smoker-temps.csv", "r")
        # read the input file
        reader = csv.reader(input_file,delimiter=",")
        # skip the headers
        next(reader, None)
        # get message from each row of file
        for row in reader:
            # read a row from the file and assign the values to variables 
            Time, Smoker_Temp, Food_A_Temp, Food_B_Temp = row
            # convert only non empty strings to float length of string is greater than 0 
            if(len(Smoker_Temp) > 0):
                Smoker_Temp = float(Smoker_Temp)
            if(len(Food_A_Temp) > 0):
                Food_A_Temp = float(Food_A_Temp)
            if(len(Food_B_Temp) > 0):
                Food_B_Temp = float(Food_B_Temp)
                
            # create a message for the smoker temp, food a temp, and food b temp
            smoker_message = (Time, Smoker_Temp)
            food_a_message = (Time, Food_A_Temp)
            food_b_message = (Time, Food_B_Temp)

            # Serialize the tuple messages into binary data using the pickle module
            binary_smoker_message = pickle.dumps(smoker_message)
            binary_food_a_message = pickle.dumps(food_a_message)
            binary_food_b_message = pickle.dumps(food_b_message)
            

            # send the message to an individual queue using the routing key to identify the queue to send to 
            ch.basic_publish(exchange="", routing_key="01-smoker", body=binary_smoker_message)
            ch.basic_publish(exchange="", routing_key="02-food-A", body=binary_food_a_message)
            ch.basic_publish(exchange="", routing_key="03-food-B", body=binary_food_b_message)

            # print a message to the console for the user to see what is happening 
            print(f" [x] Sent {smoker_message}")
            print(f" [x] Sent {food_a_message}")
            print(f" [x] Sent {food_b_message}")

            # wait 30 seconds before sending next temp
            #time.sleep(1)
        # close the file
        input_file.close()

    # handle the exception if the connection to the server fails
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()



# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # show the offer to open Admin Site if show_offer is set to true, else open automatically
    if show_offer == "True":
        offer_rabbitmq_admin_site()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()
    # Use the send_message function to start the stream
    send_message ("localhost")
    