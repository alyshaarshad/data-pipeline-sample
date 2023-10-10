import boto3
import json 
import transform_messages as tm
import upload_message as um
import database_connection as db
import os
from dotenv import load_dotenv

def process_messages(root_queue_url, num_messages, queue_access_key,queue_secret, queue_token, db_host, db_port, db_user, db_password, db_name, table_name):
    # Connect to the queue
    sqs = boto3.client('sqs', region_name='ap-south-1',endpoint_url=root_queue_url,
                   aws_access_key_id= queue_access_key,
                   aws_secret_access_key= queue_secret,
                   aws_session_token=queue_token)
    
    # create the queue
    response = sqs.create_queue(QueueName='test-queue')
    
    # Get the name of the queue
    queue_url = response['QueueUrl']
    print(queue_url)
    
    # Connect to database
    cnx = db.connect_to_db(db_host,
        db_port,
        db_user,
        db_password,
        db_name)
    
    cursor = cnx.cursor()
    
    # Check for table in database
    db.create_tables(cursor,table_name)

    messages = []
    while True:
        # Retrieve messages from the queue
        response = get_messages_from_queue(sqs, queue_url)
        print('Getting messages from Queue')
        if 'Messages' not in response:
            print('no messages in queue')
            break

        for message in response['Messages']:
            print(message)
            # Process the message
            try:
                transformed_message = tm.transform_message(json.loads(message['Body']))
            except Exception as e:
                print(f"Error transforming message {message['MessageId']}: {e}")
                continue

            messages.append(transformed_message)
            print('Transformation Finished')

            # Delete the message from the queue
            delete_message_from_queue(sqs, queue_url, message)
            print('messages have been deleted from queue')

            # Upload messages in batches
            if len(messages) >= 100:
                print('Upload in progress')
                upload_messages_in_batches(cnx,cursor, table_name, messages)
                messages = []

    # Upload any remaining messages
    if messages:
        print('Remaining messages being uploaded')
        upload_messages_in_batches(cnx, cursor, table_name, messages)

    close_database_connection(cursor, cnx)


def get_messages_from_queue(sqs, queue_url):
    return sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=num_messages,
        VisibilityTimeout=30,
        WaitTimeSeconds=20
    )


def delete_message_from_queue(sqs, queue_url, message):
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])


def upload_messages_in_batches(cnx ,cursor, table_name, messages):
    um.upload_messages(cnx, cursor, table_name, messages)


def close_database_connection(cursor, cnx):
    cursor.close()
    cnx.close()
    
if __name__ == '__main__':
   
    # Path to the .env file
    env_path = './.env'

    # Load the environment variables from the .env file
    load_dotenv(dotenv_path=env_path)

    # Access the environment variables
    queue_url = os.getenv('QUEUE_URL')
    queue_access_key = os.getenv('QUEUE_ACCESS_KEY')
    queue_secret = os.getenv('QUEUE_SECRET')
    queue_token = os.getenv('QUEUE_TOKEN')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    table_name = os.getenv('TABLE_NAME')
    num_messages = 10


    process_messages(queue_url, num_messages, queue_access_key, queue_secret, queue_token,
                     db_host, db_port, db_user, db_password, db_name, table_name)

