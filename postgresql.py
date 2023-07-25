import psycopg2

# Connection parameters
host = 'localhost'
database = 'masters'
user = 'postgres'
password = 'Jolano268'

# Establish a connection
connection = psycopg2.connect(host=host, database=database, user=user, password=password)

# Create a cursor
cursor = connection.cursor()

# Execute a SELECT query
query = "SELECT * FROM sd_pas_bmi;"
cursor.execute(query)

# Fetch all rows from the cursor
rows = cursor.fetchall()

print(rows[0][2])

# # Process the fetched data
# for row in rows:
#     print(row)



    # # Access individual columns of each row
    # column1 = row[0]
    # column2 = row[1]
    # # Process the data further as needed
    # # ...

# Close the cursor and connection
cursor.close()
connection.close()
