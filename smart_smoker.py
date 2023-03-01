"""
    This program sends a message to a queue on the RabbitMQ server.
    It simulates reading the temperatures of food in a smoker and sends messages regarding those readings.

    Author: Matt Goeckel
    Date: 10 February 2023

"""
import csv
import time
import pika
import sys
import webbrowser


# Our data file
input_file = open('smokertemps.csv', "r")

# create a csv reader for our comma delimited data
reader = csv.reader(input_file, delimiter=",")



def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()
# create a variable to check if we even run the offer funciton
show_offer = False

def send_message(host: str, queue_name: str, message: str):
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
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()



# This allows us to import this module and use its functions without executing the code below.
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    if show_offer == True:
        offer_rabbitmq_admin_site()


    next(reader, None)  # skip the headers
    for row in reader:
        # read a row from the file
        TimeUTC,Channel1,Channel2,Channel3 = row

        # use an fstring to create a message from our data
        # notice the f before the opening quote for our string?
        smokerTemp = f"[{TimeUTC}, {Channel1}]"
        food1Temp = f"[{TimeUTC}, {Channel2}]"
        food2Temp = f"[{TimeUTC}, {Channel3}]"
    
        # prepare a binary (1s and 0s) message to stream
        smokerMessage = smokerTemp.encode()
        food1Message = food1Temp.encode()
        food2Message = food2Temp.encode()

        send_message('localhost', 'smoker', smokerMessage)
        send_message('localhost', 'food1', food1Message)
        send_message('localhost', 'food2', food2Message)
        print (f"Sent temps for time {TimeUTC}.")

        # sleep for a few seconds
        time.sleep(30)