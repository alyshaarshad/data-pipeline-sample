# Overview:
The main program in main.py is designed to process messages from an AWS SQS queue, transform them, and insert them into a MySQL database. This is achieved through the integration of four modules - main.py, database_connection.py, transform_messages.py, and upload_message.py.

### [Main](src/main.py)
The main.py module serves as the primary entry point for the message processing application. Specifically, it contains the process_messages function which coordinates the various operations involved in message processing. process_messages connects to the SQS queue using provided access keys and endpoint URL, and to the MySQL database using provided credentials.

### [MySQL database connection](src/database_connection.py)
The database_connection.py module provides database connectivity functionality. Specifically, it checks if the required database or table exists and creates it if it does not exist.The schema for the table in mySQL is as follows:

Table

| Field              | Type         | Null | Key | Default | Extra          |
|--------------------|--------------|------|-----|---------|----------------|
| id                 | int(11)      | NO   | PRI | NULL    | auto_increment|
| title              | varchar(255) | YES  |     | NULL    |                |
| user               | varchar(255) | YES  |     | NULL    |                |
| repository_name    | varchar(255) | YES  |     | NULL    |                |
| repository_owner   | varchar(255) | YES  |     | NULL    |                |
| created_at         | datetime     | YES  |     | NULL    |                |
| merged_at          | datetime     | YES  |     | NULL    |                |
| tags               | varchar(255) | YES  |     | NULL    |                |
| state              | varchar(255) | YES  |     | NULL    |                |
| body               | text         | YES  |     | NULL    |                |


### [Message transformation](src/transform_messages.py)
The transform_messages.py module contains the transform_message function. This function takes a JSON object as input and returns a dictionary, with the data assigned to the corresponding fields that are in the MySQL Table schema (above)

### [Uploading messages](src/upload_message.py)
The upload_message.py module provides the upload_messages function. This function takes a list of dictionaries and inserts them into the specified MySQL table in batches. If a batch fails to upload, the script automatically retries three times unless it has been successfully inserted before moving on to the next batch.

# Python Notebooks (RUN USING LOCAL SETUP ONLY(NOT DOCKER)):

In addition to the modules mentioned above, two Python notebooks are included in the repository. One notebook allows users to execute SQL queries according to the requirements, while the other is used for experimentation and temporary changes to the code.

### [SQL queries notebook](src/notebooks/sql_queries.ipynb) 

This notebook allows you to run the SQL queries as per the requirements:
1. List the most active users

    "
SELECT user, COUNT(*) AS event_count
FROM {TABLE_NAME}
GROUP BY user
ORDER BY event_count DESC
LIMIT 10;
    "

2. List longest open event (for Issue from started_at to closed_at for PullRequest from created_at to merged_at )

    "
SELECT id, title, user, repository_name, repository_owner,created_at, merged_at, TIMESTAMPDIFF(day, created_at, COALESCE(merged_at, NOW())) AS days_open 
FROM {TABLE_NAME}
WHERE state = 'open' OR (state = 'closed' AND merged_at BETWEEN 'start_date' AND 'end_date')
ORDER BY days_open DESC
LIMIT 5;
    "

3. List the most popular five tags for all repositories (or label for Issue)

    "
SELECT tags, COUNT(*) AS tag_count
FROM {TABLE_NAME}
WHERE tags IS NOT NULL
GROUP BY tags
ORDER BY tag_count DESC
LIMIT 5;
"
4. List the total completed event count per repository for a given period

    "
SELECT repository_name, COUNT(*) AS completed_event_count
FROM {TABLE_NAME}
WHERE state = 'closed' AND merged_at BETWEEN '{start_date}' AND '{end_date}'
GROUP BY repository_name;
"

5. List top users based on number of repositories they contributed
    
    "
SELECT user, COUNT(DISTINCT repository_name) AS repository_count
FROM {TABLE_NAME}
GROUP BY user
ORDER BY repository_count DESC
LIMIT 10;
"

### [Locally run notebook](src/notebooks/local_run.ipynb)
This notebook allows the user to run the main.py process_messages function using environment variables manually.

# How to run the program

## Prerequisites

You need to have:
1. VScode
2. Docker 
3. A MySQL account

### 1. Install VScode
1. Go to the Visual Studio Code website (https://code.visualstudio.com/) and click on the "Download for Windows" button.
2. Once the download is complete, run the installer.
3. Follow the installation wizard to install VSCode on your machine. You can accept the default installation settings, or choose custom settings as desired.
4. Once the installation is complete, open VSCode by clicking on the VSCode icon in the Start menu or on the desktop.

### 2. Make sure docker is installed on your account

1. Go to the Docker website (https://www.docker.com/) and download the version of Docker that is appropriate for your operating system.
2. Follow the installation instructions for your operating system. The installation process may differ depending on whether you're using Windows, Mac, or Linux.
3. Run 'docker run hello-world' to check it is working on your terminal

### 3. Getting a MySQL account

1. Download and install MySQL Installer for Windows from the official MySQL website (https://dev.mysql.com/downloads/mysql/).
2. Once the installation is complete, make sure you make a note of the root username and passwork as well as the port and database name. You can accept the default installation settings, or choose custom settings as desired.
3. You will need these details for your .env file :
    - Root username and password
    - User name and password
    - Database name

## Running the program

1. Make a copy of sample.env renaming the copied file to .env and fill in with all the variables that need filling in. This .env file is not saved into the repo in order to keep secrets hidden
2. In the terminal run 'docker-compose up -d' in the main directory.
3. Then run 'make run' in the terminal. This should run the program and upload the messages into the table you have defined MySQL.

NOTE: If like me, when you run this you get an error that looks like this 'caused by: Post "http://localhost:4566/": read tcp [::1]:54649->[::1]:4566: wsarecv: An existing connection was forcibly closed by the remote host.' after the make command. Restart your computer and make sure all instances of MySQL on port 3306 are killed before running again.

# Open-source alternative

I would recommend using Apache Nifi for your ETL pipeline that involves taking messages from an SQS queue, transforming them, and uploading them to MySQL. Here are some reasons why I think Nifi is a great tool:

- It's easy to use and has a drag-and-drop interface to design and manage data flows.
- Nifi is scalable and can handle large volumes of data efficiently.
- It has built-in support for SQS and MySQL, so you don't need to write any custom code to integrate with these systems.
- Nifi is highly extensible, allowing you to write custom processors or connect to external systems using Nifi's APIs.
- Nifi has a large and active community, so you can easily find help and support online.

Overall, Nifi provides a powerful and flexible platform for building ETL pipelines. With its user-friendly interface, built-in support for SQS and MySQL, and active community, it's a great choice for your ETL needs.




