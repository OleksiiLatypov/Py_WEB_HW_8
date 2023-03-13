import pika
from models import Contact
import connect


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_send_list')
    channel.queue_declare(queue='sms_send_list')

    contacts = Contact.objects()
    for contact in contacts:
        if contact.email_priority:
            channel.basic_publish(exchange='',
                                  routing_key='email_send_list',
                                  body=f'Hello, {contact.full_name}!'.encode())
            contact.update(send_message=True)
        else:
            channel.basic_publish(exchange='',
                                  routing_key='sms_mailing_list',
                                  body=f'Hello, {contact.full_name}!'.encode())
            contact.update(send_message=True)
    connection.close()


if __name__ == '__main__':
    main()
