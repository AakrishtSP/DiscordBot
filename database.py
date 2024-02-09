import asyncio
import aiosqlite


async def main():
    # Connect to the database (or create it if it doesn't exist)
    conn = await aiosqlite.connect('Main.db')

    # Create a table if it doesn't exist
    await conn.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    userid INTEGER,
                    rollno INTEGER
                    );""")

    # # Data to be inserted into the table
    # data = [
    #     ("Aabartan Man Karmacharya", None, 1),
    #     ("Aagav Ojha", None, 2),
    #     ("Aakrisht Sharma Paudel", None, 3),
    #     ("Aayush Dhungana", None, 4),
    #     ("Aayush Subedi", None, 5),
    #     ("Abhaya Shrestha", None, 6),
    #     ("Abhinav Karn", None, 7),
    #     ("Abhishek Tharu", None, 8),
    #     ("Abhishu Panthi", None, 9),
    #     ("Abisekh Pandey", None, 10),
    #     ("Aditya Kumar Shah", None, 11),
    #     ("Alex Shrestha", None, 12),
    #     ("Aman Ranabhat", None, 13),
    #     ("Anup Kumar Jha", None, 14),
    #     ("Arya Dangol", None, 15),
    #     ("Aryan Dahal", None, 16),
    #     ("Asmit Khanal", None, 17),
    #     ("Avinash Kumar Yadav", None, 18),
    #     ("Bhim Prasad Upadhyaya", None, 19),
    #     ("Bibek Gautam", None, 20),
    #     ("Bibidh Subedi", None, 21),
    #     ("Biprash Pandey", None, 22),
    #     ("Chandan Kumar Shah", None, 23),
    #     ("Darpan Giri", None, 24),
    #     ("Dinesh Bhatta", None, 25),
    #     ("Dipesh S. Saud", None, 26),
    #     ("Diwas Pantha", None, 27),
    #     ("Diwas Shrestha", None, 28),
    #     ("Dumajal Malla", None, 29),
    #     ("Gagan Kumar Dahal", None, 30),
    #     ("Gaurab Khatry", None, 31),
    #     ("Homraj KC", None, 32),
    #     ("Hridan Bhattarai", None, 33),
    #     ("Ishan Gautam", None, 34),
    #     ("Janak Singh Pujara", None, 35),
    #     ("Jenif Khadka", None, 36),
    #     ("Kajal Kumari Chaudhary", None, 37),
    #     ("Kapil Pokhrel", None, 38),
    #     ("Krish Bansal", None, 39),
    #     ("Kushal Gautam", None, 40),
    #     ("Kushal KC", None, 41),
    #     ("Kushal Regmi", None, 42),
    #     ("Lav Raj Karn", None, 43),
    #     ("Laxmi Kumari", None, 44),
    #     ("Mahesh Bhandari", None, 45),
    #     ("Mission Baraily", None, 46),
    #     ("Nabina Thapa", None, 47),
    #     ("Nayan Khussu", None, 48)
    # ]

    # # Insert data into the table
    # await conn.executemany(
    #     "INSERT INTO users (username, userid, rollno) VALUES (?, ?, ?)", data)

    # Retrieve data from the table
    await conn.execute("UPDATE users SET userid = ? WHERE rollno = ?", (532592703192432650, 3))
    cursor = await conn.execute("SELECT * FROM users")
    rows = await cursor.fetchall()
    for row in rows:
        print(row)

    # Close the connection
    await conn.commit()
    await conn.close()

# Run the coroutine

asyncio.run(main())
