import pika
import sys
import time
import pickle
from collections import deque

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
queue_name1 = "01-smoker"
queue_name2 = "02-food-A"
queue_name3 = "03-food-B"

channel.queue_declare(queue=queue_name1, durable=True)
channel.queue_declare(queue=queue_name2, durable=True)
channel.queue_declare(queue=queue_name3, durable=True)




channel.start_listening()

# define a main function to run the program matching the task_queue with the worker
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
    
        channel = connection.channel()
    def smoker_callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b".")) #simulate work
        print(" [x] Done.")
        channel.basic_ack(delivery_tag = method.delivery_tag)
        channel.basic_consume(queue=queue_name1, on_message_callback=smoker_callback, on_message_callback=smoker_callback, auto_ack=False)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    

    def food_a_callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b".")) #simulate work
        print(" [x] Done.")
        ch.basic_ack(delivery_tag = method.delivery_tag)
        channel.basic_consume(queue=queue_name2, on_message_callback=food_a_callback, on_message_callback=food_a_callback, auto_ack=False)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def food_b_callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b".")) #simulate work
        print(" [x] Done.")
        channel.basic_consume(queue=queue_name3, on_message_callback=food_b_callback, on_message_callback=food_b_callback, auto_ack=False)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

        #use channel to queue delete
        channel.queue_delete(queue="01-smoker")
        channel.queue_delete(queue="02-food-A")
        channel.queue_delete(queue="03-food-B")

        #use the channel to declare a queue
        channel.queue_declare(queue="01-smoker", durable=True)
        channel.queue_declare(queue="02-food-A", durable=True)
        channel.queue_declare(queue="03-food-B", durable=True)

        # set the prefetch count to 1
        channel.basic_qos(prefetch_count=1)

        # Configure the queue to call the callback function when a message is received
        channel.basic_consume(queue="01-smoker")
        channel.basic_consume(queue="02-food-A")
        channel.basic_consume(queue="03-food-B")

        #print a message to show the program is running
        print(" [*] Waiting for messages. To exit press CTRL+C")

        #start the program
        channel.start_consuming()

  

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed and changing the queue name
    main("localhost")