import mysql.connector
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="PASSWORD",
)

#prepare cursor object
cursorObject = dataBase.cursor()

#create database
cursorObject.execute("CREATE DATABASE inventory")


print("All done")
