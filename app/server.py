import psycopg2


conn = psycopg2.connect(database="mydiarydb", user="postgres", password="trekab",
host="127.0.0.1", port="5432")


cur = conn.cursor()

 
cur.execute("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        	)
        """)


cur.execute(""" 
		CREATE TABLE entries (
			 user_id SERIAL NOT NULL,
			FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
		    entry_id SERIAL PRIMARY KEY,
		    entry_title VARCHAR(255) NOT NULL,
		    entry_date DATE NOT NULL,
		    entry_content VARCHAR(255) NOT NULL
		     )
         """)


def connect_to_db():
	connection_string = "database="mydiarydb", user="postgres", password="trekab",host="127.0.0.1", port="5432""
	print(connection_string)

	try:
		return pycopg2.connect(connection_string)
	except:
		print("Can't connect to database")

# conn = psycopg2.connect(database="testdb", user="postgres", password="trekab",
# host="127.0.0.1", port="5432")

# print ("Opened database successfully")


# cur = conn.cursor()
# cur.execute("SELECT id, name, address, salary from COMPANY")
# rows = cur.fetchall()
# for row in rows:
# 	print ("ID = ", row[0])
# 	print ("NAME = ", row[1])
# 	print ("ADDRESS = ", row[2])
# 	print ("SALARY = ", row[3], "\n")
# print ("Operation done successfully");
# conn.close()