import sqlite3
conn = sqlite3.connect('MovieFinder.db')
c= conn.cursor()

c.execute("""CREATE TABLE Customers(
                firstName text,
                lastname text,
                DateofBirth text,
                EmailAddress text,
                Password text,
                PhoneNumber integer,
                Banlist text,
                Wishlist text,
                UserID integer
                )""")


c.execute("""CREATE TABLE Movies(
Id integer,
MovieName text,
ReleasedDate text,
WebsiteName text,
Cast text,
Director text,
Genre text,
Rating integer,
Reviews text,
Region text
)""")




c.execute("""CREATE TABLE Client(
Movie text,
Website text
)""")

c.execute("""CREATE TABLE Actor(
Name text,
PopularityStats text,
PID integer
)""")



conn.commit()
conn.close()
