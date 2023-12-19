# To work on dataframe and read data from csv
import pandas as pd
# To get the data through API
import requests
# To work on JSON data
import json
# to convert data from xml to json
import xmltodict
# To delete the already available file, where I will write my output
import os


# to read csv file
df = pd.read_csv("C:\Rishabh_Drive\python\chembl.csv")
# to filter data in coloumn value antioxidant and again keeping data into same df variable
df = df[df['ACTIVITY']=='Antioxidant']
# to get top 10 records from df dataframe and storing it in a new dataframe just to check code functionality
# df1 = df.head(10)

# Removing duplicates from "COMPOUND" column to reduce the runtime 
df.drop_duplicates(subset="COMPOUND", keep=False, inplace=True)
# creating an empty list 
lst = []

# to iterate all data from df dataframe
for i in df['COMPOUND']:
    # creating payload where q as a key is already given in chembl webservices and i is the value (value will
    #  change with every iteration of i)
    payload = {"q":i}  
    # get is the method in API (already mentioned in chmbl)
    # request is a python library to get data from API 
    # params is a payload to provide keys and values(which defined in row 29)       
    response = requests.get("https://www.ebi.ac.uk/chembl/api/data/activity/search", params = payload)
    # to convert output(respose) of row 33 from xml to json (we converted it into json bcz getting data from json is quite easy)
    data_dict = xmltodict.parse(response.content)
    # getting "assay_chembl_id" from nested json 
    # We will check if given payload ("Activity") is having any data or not, if it doesn't hold any data then append NULL to 
    # list else append chembl_id into list
    # appending "assay_chembl_id" into list (lst)
    if data_dict['response']['activities'] == None:
        print(i)
        lst.append('Null')
    # if there is no nested list after "activity" (which states only one chembl_id is available for that compound then
    # it will be acting like dictionary else as a list) then below code will work. because in nested list data type will be
    # as list only
    elif isinstance(data_dict['response']['activities']['activity'], dict):
        lst.append(data_dict['response']['activities']['activity']['assay_chembl_id'])
    else:
        lst.append(data_dict['response']['activities']['activity'][0]['assay_chembl_id'])
    
# inserting list data in protein column in df1 dataframe
df['Protein'] = lst

# checking if output.csv is alredy present in current directoruy then delete that fiile and create 
# new ouput.csv with data present in df1 dataframe
if os.path.exists("output.csv"):
    os.remove("output.csv")
    df.to_csv('Output.csv', index=False)
# if file is not avialable then create new ouput.csv with data present in df1 dataframe
else:
    df.to_csv('Output.csv', index=False)