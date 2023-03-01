"""
    This program listens for work messages contiously. 
    Start multiple versions to add more workers.  
    Each row a task and received and acknolwedged invididually.
    Screen shots in Readme.md
    Run this program in a terminal window.
    Multiple producers and a single consumer
For the listener, we need to do the following:
    import pike and sys to connect to the RabbitMQ server and send messages.
    import time to use the sleep function to simulate work.
    import deque to use a double ended queue to store the messages.
    Import smtplib to send email alerts

    Author: Julie Creech
    Date: February 9, 2023 Modified February 27, 2023

"""

import pika
import sys
import time
import pickle
from collections import deque
#import smtplib for the actual sending function
import smtplib
#import email modules to format and send email
from email.mime.text import MIMEText


#limit smoker readings to last 2.5 minutes/5 readings
smoker_deque = deque(maxlen=5)
#limit food a readings to last 10 minutes/20 readings
food_a_deque = deque(maxlen=20)
#limit food b readings to last 10 minutes/20 readings
food_b_deque = deque(maxlen=20)

# define a callback function to be called when a message is received
def smoker_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    print(f" [x] Received {pickle.loads(body)} on 01-smoker")
    #acknowledge the message was received and processed
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    #convert message from binary to tuple
    message = pickle.loads(body)
    #add temp to deque
    if isinstance(message[1], float):
        smoker_deque.appendleft(message)

    #only perform check if deque has recorded
    #find first item in deque
    cur_smoker_deque_temp = smoker_deque[0]
    #get current temp
    smoker_temp_current = cur_smoker_deque_temp[1]

    #find last item in deque
    last_smoker_deque_temp = smoker_deque[-1]
    #get last temp
    smoker_temp_last = last_smoker_deque_temp[1]

    #compare first and last message if have been in the deque for 5 readings
    if len(smoker_deque) == 5:
        #find temp of last item in deque
        if smoker_temp_last - smoker_temp_current >= 15:
            #send alert if smoker has decreased by 15 degrees or more
            print(f"Smoker Alert! Smoker has decreased by 15 degrees or more in 2.5 minutes from {smoker_temp_last} to {smoker_temp_current}")
        else: #print current temp
            print(f"Current smoker temp is {smoker_temp_current}")
    else: #print current temp if deque is not full
        print(f"Current smoker temp is {smoker_temp_current}")

# define a callback function to be called when a message is received
def food_a_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    print(f" [x] Received {pickle.loads(body)} on 02-food-A")
    #acknowledge the message was received and processed
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    #convert message from binary to tuple
    message = pickle.loads(body)
    #add temp to deque
    if isinstance(message[1], float):
        food_a_deque.appendleft(message)
        #only perform check if deque has recorded
        #find first item in deque
        cur_food_a_deque_temp = food_a_deque[0]
        #get current temp
        food_a_temp_current = cur_food_a_deque_temp[1]

        #find last item in deque
        last_food_a_deque_temp = food_a_deque[-1]
        #get last temp
        food_a_temp_last = last_food_a_deque_temp[1]

        #compare first and last message if have been in the deque for 20 readings
        if len(food_a_deque) == 20:
            if (abs(food_a_temp_last)) - (abs(food_a_temp_current)) < 1:
                #send alert if food a has decreased by less than 1 degree in 10 minutes
                print(f"Food A Alert! Food Stall!! Food A has decreased by less than 1 degree in 10 minutes from {food_a_temp_last} to {food_a_temp_current}")
                then = time.time() #remember when we sent the alert
                #wait 5 minutes
                time.sleep(300)
                #check if temp has changed
                if (abs(food_a_temp_last)) - (abs(food_a_temp_current)) < 1:
                    #send alert if food a has decreased by less than 1 degree in 10 minutes
                    print(f"Food A Alert! Food Stall!! Food A has decreased by less than 1 degree in 10 minutes from {food_a_temp_last} to {food_a_temp_current}")
                    #send email alert if food a has decreased by less than 1 degree in 10 minutes
                    print(f"Email Alert! Food Stall!! Food A has decreased by less than 1 degree in 10 minutes from {food_a_temp_last} to {food_a_temp_current}")
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login('julie0818abrams@gmail.com', '$tr3aming101')
                        subject = 'Food A Alert! Food Stall!!'
                        body = f"Food A has decreased by less than 1 degree in 10 minutes from {food_a_temp_last} to {food_a_temp_current}"
                        msg = f'Subject: {subject}\n\n{body}'
                        smtp.sendmail('julie0818abrams@gmail.com')
                    #now = time.time() #remember when we sent the alert
                    #wait 5 minutes
                    #time.sleep(300)
                    #check if temp has changed
                else: #print current temp
                    print(f"Current food a temp is {food_a_temp_current}")
            else: #print current temp if deque is not full
                print(f"Current food a temp is {food_a_temp_current}")

# define a callback function to be called when a message is received
def food_b_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    print(f" [x] Received {pickle.loads(body)} on 03-food-B")
    #acknowledge the message was received and processed
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    #convert message from binary to tuple
    message = pickle.loads(body)
    #add temp to deque
    if isinstance(message[1], float):
        food_b_deque.appendleft(message)
        #only perform check if deque has recorded
        #find first item in deque
        cur_food_b_deque_temp = food_b_deque[0]
        #get current temp
        food_b_temp_current = cur_food_b_deque_temp[1]

        #find last item in deque
        last_food_b_deque_temp = food_b_deque[-1]
        #get last temp
        food_b_temp_last = last_food_b_deque_temp[1]

        #compare first and last message if have been in the deque for 20 readings
        if len(food_b_deque) == 20:
            if (abs(food_b_temp_last)) - (abs(food_b_temp_current)) <1:
                #send alert if food b has decreased by less than 1 degree in 10 minutes
                print(f"Food B Alert! Food B has decreased by less than 1 degree in 10 minutes from {food_b_temp_last} to {food_b_temp_current}")
            else:
                #print current temp
                print(f"Current food b temp is {food_b_temp_current}")
        else: #print current temp if deque is not full
            print(f"Current food b temp is {food_b_temp_current}")

            #find last item in deque
            last_food_b_deque_temp = food_b_deque[-1]
            #get last temp
            food_b_temp_last = last_food_b_deque_temp[1]

            #compare first and last message if have been in the deque for 20 readings
            if len(food_b_deque) == 20:
                if (abs(food_b_temp_last)) - (abs(food_b_temp_current)) <1:
                    #send alert if food b has decreased by less than 1 degree in 10 minutes
                    print(f"Food B Alert! Food Stall! Food B has decreased by less than 1 degree in 10 minutes from {food_b_temp_last} to {food_b_temp_current}")
                else:
                    #print current temp
                    print(f"Current food b temp is {food_b_temp_current}")
            else: #print current temp if deque is not full
                print(f"Current food b temp is {food_b_temp_current}")
                
# define a callback function to be called when a message is received
def main(hn: str):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can raise an exception, include it in the try clause
    try:
        #try to connect to the rabbitmq server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    #except, if there is an error
    except Exception as e:
        #print the error
        print(f"Error connecting to rabbitmq server: {e}")
        #exit the program
        sys.exit(1)
    try:
        #use the connection to create a channel
        channel = connection.channel()

        #use the channel to declare a queue
        channel.queue_declare(queue="01-smoker", durable=True)
        channel.queue_declare(queue="02-food-A", durable=True)
        channel.queue_declare(queue="03-food-B", durable=True)

        # set the prefetch count to 1
        channel.basic_qos(prefetch_count=1)

        # Configure the queue to call the callback function when a message is received
        channel.basic_consume(queue="01-smoker", on_message_callback=smoker_callback)
        channel.basic_consume(queue="02-food-A", on_message_callback=food_a_callback)
        channel.basic_consume(queue="03-food-B", on_message_callback=food_b_callback)

        #print a message to show the program is running
        print(" [*] Waiting for messages. To exit press CTRL+C")

        #start the program
        channel.start_consuming()

    #except, if there is an error
    except Exception as e:
        #print the error
        print(f"Error consuming messages: {e}")
        #exit the program
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continous listening.")
        sys.exit(0)
    finally:
        print(" Closing connection to rabbitmq server.")
        connection.close()

#standard boilerplate to call the main function
#this is the first function that is called when the program is run
#without executing the main function, the program will not run
#if this is the program that is being run, then execute the main function
if __name__ == "__main__":
    #call the main function
    main("localhost")