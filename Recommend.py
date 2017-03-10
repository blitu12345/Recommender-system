import MySQLdb
import pandas.io.sql as sql

con = MySQLdb.connect("localhost","root","lnm@#$","Recommend")
cur = con.cursor()


cur.execute(''' set foreign_key_checks=0''')
cur.execute(''' drop table if exists Books ''')
cur.execute(''' drop table if exists UserBooks ''')
cur.execute(''' drop table if exists Users ''')

cur.execute("""
		create table Books(
			book_id int not null,
			genre_id int not null,
			genre_name char(30) not null,
			author char(30) not null,
			primary key (book_id))
		""")

cur.execute(''' 
		create table Users(
			user_id int not null,
			age int not null,
			gender char(1),
			profession char(10) not null,
			primary key (user_id))
	''')

cur.execute(''' 
		create table UserBooks(
			user_id int not null,
			book_id int not null,
			preference int,
			foreign key (user_id) references Users(user_id),
			foreign key (book_id) references Books(book_id))
	''')

#### insert values into Books table
fr=open('Books.csv')
fr.readline()
for line in fr.readlines():
	line=line.strip().split(',')
	line[:2]=map(int,line[:2])
	cur.execute('''insert into Books values('%d','%d','%s','%s')'''%(line[0],line[1],line[2],line[3]) )
	#print line[0],line[1],line[2],line[3]
fr.close()

#### insert values into Users table
fr=open('Users.csv')
fr.readline()
for line in fr.readlines():
	line=line.strip().split(',')
	line[:2]=map(int,line[:2])
	cur.execute('''insert into Users values('%d','%d','%s','%s')'''%(line[0],line[1],line[2],line[3]) )
	#print line[0],line[1],line[2],line[3]
fr.close()

#### insert values into UserBooks table
fr=open('UserBooks.csv')
fr.readline()
for line in fr.readlines():
	line=line.strip().split(',')
	line=map(int,line)
	cur.execute('''insert into UserBooks values('%d','%d','%d')'''%(line[0],line[1],line[2]) )
	#print line[0],line[1],line[2]
fr.close()

#### for train dataset for training content based recommendation system
table = sql.read_frame('select b.book_id,u.user_id,age,gender,profession,genre_name,author,preference from Books b,Users u,UserBooks ub where ub.user_id=u.user_id and ub.book_id=b.book_id;', con)
table.to_csv('train.csv')

#### user feature dataset
table1 = sql.read_frame('select *from Books b,Users u,UserBooks ub where ub.user_id=u.user_id and ub.book_id=b.book_id ;',con)
table1.to_csv('users.csv')
con.commit()

con.close()