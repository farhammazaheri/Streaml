import streamlit as st
import datetime
import pymongo
import requests
import pandas as pd

st.write("Hello World")

options = ["Create", "Read", "blog","Delete"]

username = "MyAdmin"
password = "1275679684"
host = "localhost"
port = "27017"

connection_url = f"mongodb://{username}:{password}@{host}:{port}"

date = datetime.datetime.now()

url = 'https://jsonplaceholder.typicode.com/posts' 
response = requests.get(url) 
data = response.json()

csv_file = 'data.csv' 
df = pd.DataFrame(data) 
df.to_csv(csv_file, index=False)

client = pymongo.MongoClient(connection_url)
db = client["My_family"]


b = st.radio("select option :", options)


if b:
    if b == "Create":

        a = st.text_input("input your task name in here:")
        

        if a:
            op_1 = ["create", "write"]
            c = st.radio("select option :", op_1)
            if c == "create":
                if st.button("create:"):
                    db.create_collection(a)
            if c == "write":
                ui = st.text_area("write your task")
                collection = db[a]
                if ui:
                    if st.button("save a text"):
                        result = collection.insert_one({"text": ui, "Date" : date})
    if b == "Read":
        a = st.text_input("input your task name in here:")      
        if a:
            collection = db[a]  
            if st.button("Read"):
                    documents = collection.find({})
                    for doc in documents: 
                        text = doc.get('text', 'No text available') 
                        st.write(text)
    if b == "Delete":
        a = st.text_input("input your task name in here:")
        if a:
            collection = db[a]
            order = st.text_input("wich text do you want to delet ? :")
            if order:
                if st.button("delete") :
                    result = collection.delete_one({"text": order})
                    if result:
                        st.write("text deleted succssefully")

    if b == "blog":
        st.title('Download Data from URL')
        op_2 = ["show the data", "download data as csv file:"]
        option_2 = st.radio("option", op_2)
        if option_2 == "show the data":
            st.write('Data fetched from the URL:') 
            st.write(df)    
        if option_2 == "download data as csv file:":
            st.download_button( label='Download CSV', data=open(csv_file, 'rb').read(), file_name=csv_file, mime='text/csv' )


                


    
        
