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

# def add_user(user):
# 	cur.execute("INSERT INTO users (user) VALUES (%s)", % user)
# 	conn.close()

# def add_entry(entry):
# 	cur.execute("INSERT INTO entries (entry) VALUES (%s)", % entry)
# 	conn.close()

# def get_entries(user_id):
# 	cur.execute("SELECT * FROM entries WHERE user_id = user_id")
# 	conn.close()

# def get_entry(entry_id):
# 	cur.execute("SELECT * FROM entries WHERE entry_id = entry_id")
# 	conn.close()
