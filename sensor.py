import os
import random

import pika
import sys
import time

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='sensor')
    while True:
        co2_wert = random.randint(400, 1500)

        channel.basic_publish(exchange='',
                              routing_key='sensor',
                              body=str(co2_wert))

        print("Wert weitergegeben")
        # 60s Warten
        time.sleep(10)  # TODO auf 60 ändern
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
except:
    print("Anderer Fehler")
