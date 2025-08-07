import mysql.connector
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Aditi@279",
)

#prepare cursor object
cursorObject = dataBase.cursor()

#create database
cursorObject.execute("CREATE DATABASE elderco")

print("All done")