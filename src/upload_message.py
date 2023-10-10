import datetime

def upload_messages(cnx, cursor, table_name, messages):
    query = f"INSERT INTO {table_name} (title, user, repository_name, repository_owner, created_at, merged_at, tags, state, body) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    # Convert datetime objects to strings
    messages = [{k: str(v) if isinstance(v, datetime.datetime) else v for k, v in message.items()} for message in messages]
    for i in range(3):
        try:
            print('uploading the batches in upload_messages.py')
            cursor.executemany(query,  [tuple(message.values()) for message in messages])
            result = cursor.fetchall()
            affected_rows = cursor.rowcount
            print(f"{affected_rows} rows inserted into table {table_name}")
            cnx.commit()
            break  # exit loop if insertion is successful
        except Exception as e:
            print(f"Error inserting messages into table: {e}")
            cnx.rollback()
            print("Retrying...")
    else:
        print(f"Failed to insert messages after {i+1} attempts")
        return  # exit function if all attempts fail
    print("Moving on to next batch")
    
