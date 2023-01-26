import sqlite3
import pandas as pd

# Function to create a database and save data
def savedb(list1, list2, list3, list4, list5):
    # Creating a dataframe
    all = {'Quantity': list1, 'Title': list2, 'Company': list3, 'City': list4, 'State': list5}
    df = pd.DataFrame.from_dict(all, orient='index')
    df = df.transpose()

    # Creating a database connection
    connection = sqlite3.connect('../database/databasejobs.db')

    # Creating a cursor
    cursor = connection.cursor()

    # Create a table if not exist
    def create_table():
        connection.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Quantity INT, ' \
                        'Title TEXT,  Company TEXT, City TEXT, State TEXT)')

    create_table()

    # Function 'to_sql' transforming a dataframe to a sql table and saving in database
    df.to_sql(name='jobs', con=connection, if_exists='append', index=False)

    # Recording the transaction
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()
