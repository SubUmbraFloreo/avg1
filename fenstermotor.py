import os
import pika
import sys

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='aktor')

    def callback(ch, method, properties, body):
        if body == b'True':
            print("Fenster wird geöffnet")
        else:
            print("Fenster wird geschlossen")


    channel.basic_consume(queue='aktor', on_message_callback=callback, auto_ack=True)

    print('[*] Warten auf Nachrichten')
    channel.start_consuming()


except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
except:
    print("Anderer Fehler")