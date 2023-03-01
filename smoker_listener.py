"""
    This program listens for work messages contiously. 
    Alerts will be sent for rapid changes in smoker temp, or food temp stalls.  

    Author: Matt Goeckel
    Date: 17 February 2023

"""

import pika
import sys
import time
from collections import deque

# set up deques for later use
smoker_deque = deque(maxlen=5)
food1_deque = deque(maxlen=20)
food2_deque = deque(maxlen=20)


# delete our queues so old messages don't come in
def delete_queue(host: str, queue_name: str):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host))
    ch = conn.channel()
    ch.queue_delete(queue=queue_name)

# define a callback function to be called when a message is received
def smoker_callback(ch, method, properties, body):
    message = body.decode()
    # decode the binary message body to a string
    #print(f" [x] Smoker Received {message}")           #DEBUG TOOL
    # now it can be deleted from the queue. We have received it and stored the message in a variable
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # discard the date/time and add the number to the deque
    cur_smoker_temp = message[20:-1]
    if cur_smoker_temp == '':
        #print("No Smoker Temp Reading")
        pass
    else:
        cur_smoker_temp = float(cur_smoker_temp)
        smoker_deque.append(cur_smoker_temp)

        # if 2.5 minutes have not passed, do not worry about checking temperatures yet
        if len(smoker_deque) == 5:
            # look through all smoker temps in the last 2.5 minutes
            # We check it against each of the last 5 readings, so that even if the change was 15deg in the last 30 seconds, we'll know immediately instead of 2 minutes from now
            i=0
            while i < 4:
                # identify the current smoker temp from the deque
                cur_temp = smoker_deque[4]
                # discard the date/time and convert from string to float number
                # now identify the previous temp
                prev_temp = smoker_deque[i]
                i = i+1
                # compare the temps. If it has decreased by over 15, print an alert
                if (prev_temp - cur_temp) > 15.0:
                    print("Smoker Alert: The smoker has decreased by more than 15 degrees in the last 2.5 minutes")
                    print(f" Timestamp: {message}")
                    # clear the deque so we don't have multiple alerts in a row
                    smoker_deque.clear()
                    #set i = 5 to break the loop so we don't get a deque index out of range error
                    i = 5



def food1_callback(ch, method, properties, body):
    message = body.decode()
    # decode the binary message body to a string
    #print(f" [x] Food1 Received {message}")            #DEBUG TOOL
    # now it can be deleted from the queue. We have received it and stored the message in a variable
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # discard the date/time and add the number to the deque
    cur_food1_temp = message[20:-1]
    if cur_food1_temp == "":
        #print("Food1 Slot is Empty")                   #DEBUG TOOL
        pass
    else:
        cur_food1_temp = float(cur_food1_temp)
        food1_deque.append(cur_food1_temp)

        # if 10 minutes have not passed since the food was added, don't worry about checking temps yet
        if len(food1_deque) == 20:
            # identify the current smoker temp from the deque
            cur_temp = food1_deque[19]      
            # now identify the previous temp
            prev_temp = food1_deque[0]
            # check food 1's current temperature vs 10 minutes ago
            # if it dropped by more than 1 degree, the loop will execute
            if (cur_temp - prev_temp) < -1:
                print("Food Stall: Food 1 has decreased by more than 1 degree over the last 10 minutes")
                print(f" Timestamp: {message}")
                # clear the deque so we don't have multiple alerts in a row
                food1_deque.clear()           

def food2_callback(ch, method, properties, body):
    message = body.decode()
    # decode the binary message body to a string
    # print(f" [x] Food2 Received {message}")       #DEBUG TOOL
    # now it can be deleted from the queue. We have received it and stored the message in a variable
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # discard the date/time and add the number to the deque
    cur_food2_temp = message[20:-1]
    if cur_food2_temp == "":
        #print("Food2 Slot is Empty")               #DEBUG TOOL
        pass
    else:
        cur_food2_temp = float(cur_food2_temp)
        food2_deque.append(cur_food2_temp)
    
        if len(food2_deque) == 20:
            # identify the current & previous smoker temp from the deque
            cur_temp = food2_deque[19]
            prev_temp = food2_deque[0]
            # check food 2's current temperature vs 10 minutes ago
            # if it is less than 1 degree, the loop will execute
            # if it dropped by more than 1 degree, the loop will execute
            if (cur_temp - prev_temp) < 0:
                print("Food Stall: Food 2 has decreased by more than 1 degree over the last 10 minutes")
                print(f" Timestamp: {message}")
                # clear the deque so we don't have multiple alerts in a row
                food2_deque.clear()               


# define a main function to run the program
def main(hn: str = "localhost", q1: str = "smoker", q2: str = "food1", q3: str = "food2"):

# delete queues first so no old messages arrive
    delete_queue(hn, q1)
    delete_queue(hn, q2)
    delete_queue(hn, q3)

    try:
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare the smoker queue
        channel.queue_declare(queue=q1, durable=True)

        # configure the channel to listen on the smoker queue,  
        # use the callback function for the smoker and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume(queue=q1, on_message_callback=smoker_callback)

        # now do the same for the two food queues
        channel.queue_declare(queue=q2, durable=True)
        channel.basic_consume(queue=q2, on_message_callback=food1_callback)

        channel.queue_declare(queue=q3, durable=True)
        channel.basic_consume(queue=q3, on_message_callback=food2_callback)

        # print a message to the console for the user
        print(" [*] Ready to receive temps. To exit press CTRL+C")
        #print(smoker_deque) #DEBUG TOOLS
        #print(food1_deque)
        #print(food2_deque)

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main("localhost", "smoker", "food1", "food2")
