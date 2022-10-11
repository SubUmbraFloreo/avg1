import pika, sys, os


class Fenster:
    offen = False

    def set_status(self, status):
        self.offen = status


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='sensor')

    fenster = Fenster()


    def callback(ch, method, properties, body):
        print("Der aktuelle CO2-Wert ist:", end=" ")
        co2_wert = int(body)
        print(co2_wert)

        oeffnen = co2_wert > 1000

        if fenster.offen and oeffnen:
            print("Das Fenster ist bereits offen")
        elif fenster.offen and not oeffnen:
            fenster.set_status(False)
            print("Fenster wird geschlossen")
            channel.basic_publish(exchange='',
                                  routing_key='aktor',
                                  body=str(False))
        elif not fenster.offen and oeffnen:
            fenster.set_status(True)
            print("Das Fenster wird geöffnet")
            channel.basic_publish(exchange='',
                                  routing_key='aktor',
                                  body=str(True))
        else:
            print("Das Fenster ist bereits geschlossen")


    channel.basic_consume(queue='sensor', on_message_callback=callback, auto_ack=True)

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
