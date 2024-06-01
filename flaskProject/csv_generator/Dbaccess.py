import schedule
import time
import mysql.connector
import csv


def generate_csv():
    # Database connection parameters
    hostname = '127.0.0.1'
    port = 3306
    username = 'root'
    password = ''  # Enter your MySQL root password here
    database_name = 'ERP_project'

    try:
        # Connect to the MySQL database
        mydb = mysql.connector.connect(
            host=hostname,
            port=port,
            user=username,
            password=password,
            database=database_name
        )

        # Create a cursor object to execute SQL queries
        cursor = mydb.cursor()

        # Define the SQL query to retrieve data from the 'products' table
        query = "SELECT * FROM products"

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the result set
        result = cursor.fetchall()

        # Specify the file path for the CSV file
        csv_file_path = 'products.csv'

        # Open the CSV file in write mode
        with open(csv_file_path, 'w', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)

            # Write the header row
            csv_writer.writerow(
                ['id', 'name', 'category', 'brand', 'quantity', 'price', 'total_price', 'updated_at', 'customer_id',
                 'created_at', 'updated_at'])

            # Write each row of data to the CSV file
            for row in result:
                csv_writer.writerow(row)

        print(f"CSV file '{csv_file_path}' created successfully.")

    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)

    finally:
        # Close the cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()


# Define the job and schedule it to run daily at 2 AM
schedule.every().day.at("02:01").do(generate_csv)

# Loop to continuously check for scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)
