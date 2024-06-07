import os
import pandas as pd
import json
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine

# Data has been cloned from github to local using the command "git clone github_link"

# aggregate_transactions
path = "path"
Agg_state_list = os.listdir(path)

clm = {'State':[], 'Year':[],'Quarter':[],'Tran_type':[], 'Tran_count':[], 'Tran_amount':[]}

for i in Agg_state_list:
    p_i = path+i+"/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j  = p_i+j+"/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['transactionData']:
              Name = z['name']
              count = z['paymentInstruments'][0]['count']
              amount = z['paymentInstruments'][0]['amount']
              clm['Tran_type'].append(Name)
              clm['Tran_count'].append(count)
              clm['Tran_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quarter'].append(int(k.strip('.json')))

Tran_Agg = pd.DataFrame(clm)


# aggregate_users
path_1 = "path"
Agg_state_list = os.listdir(path_1)

clm_1 = {'State':[], 'Year':[],'Quarter':[],'Registered_Users':[], 'App_Opened':[], 'Brand_Name':[],'Brand_Count':[],'Brand_Percentage':[]}

for i in Agg_state_list:
    p_i = path_1+i+"/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i+j+"/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j+k
            Data = open(p_k,'r')
            D = json.load(Data)
       
            Registered_Users = D['data']['aggregated']['registeredUsers']
            App_Opened = D['data']['aggregated']['appOpens']
            try:
                for user in D['data']['usersByDevice']:
                    Brand_name=user["brand"]
                    Brand_count=user["count"]
                    Brand_percentage=user["percentage"]
                    clm_1['Brand_Percentage'].append(Brand_percentage*100)
                    clm_1['Brand_Count'].append(Brand_count)
                    clm_1['Brand_Name'].append(Brand_name)
                    clm_1['App_Opened'].append(App_Opened)
                    clm_1['Registered_Users'].append(Registered_Users)
                    clm_1['State'].append(i)
                    clm_1['Year'].append(j)
                    clm_1['Quarter'].append(int(k.strip('.json')))
            except Exception:
                pass
                  
User_Agg = pd.DataFrame(clm_1)


# map_transactions
path_2 = "path"
Agg_state_list = os.listdir(path_2)

clm_2 = {'State':[], 'Year':[],'Quarter':[],'District':[],'District_Tran_Count':[],'District_Tran_Amount':[]}

for i in Agg_state_list:
    p_i = path_2+i+"/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i+j+"/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['hoverDataList']:
              District = z['name']
              District_tran_count = z['metric'][0]['count']
              District_tran_amount = z['metric'][0]['amount']
              clm_2['District'].append(District)
              clm_2['District_Tran_Count'].append(District_tran_count)
              clm_2['District_Tran_Amount'].append(District_tran_amount)
              clm_2['State'].append(i)
              clm_2['Year'].append(j)
              clm_2['Quarter'].append(int(k.strip('.json')))

Tran_Map = pd.DataFrame(clm_2)

# map_users
path_3 = "path"
Agg_state_list = os.listdir(path_3)

clm_3={'State':[], 'Year':[],'Quarter':[],'District':[],'Registered_Users':[], 'App_Opened':[]}

for i in Agg_state_list:
    p_i = path_3+i+"/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i+j+"/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['hoverData'].items():
                District_Name = z[0]
                Registered_Users = z[1]['registeredUsers']
                App_Opened =  z[1]['appOpens']
                clm_3['District'].append(District_Name)
                clm_3['Registered_Users'].append(Registered_Users)
                clm_3['App_Opened'].append(App_Opened)
                clm_3['State'].append(i)
                clm_3['Year'].append(j)
                clm_3['Quarter'].append(int(k.strip('.json')))

User_Map = pd.DataFrame(clm_3)


# top_transaction_states
path_4 = "path"
Agg_state_list = os.listdir(path_4)

clm_4 = {'State':[], 'Year':[],'Quarter':[],'Tran_Amount':[],'Tran_Count':[]}

for i in Agg_state_list:
    if i != "state":
        p_i = path_4+i+"/"
        top_tran_list = os.listdir(p_i)

        for k in top_tran_list:
            p_k = p_i+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['states']:
                State_Name = z['entityName']
                Tran_Count = z['metric']['count']
                Tran_Amount = z['metric']['amount']
                clm_4['Tran_Amount'].append(Tran_Amount)
                clm_4['Tran_Count'].append(Tran_Count)
                clm_4['State'].append(State_Name)
                clm_4['Year'].append(i)
                clm_4['Quarter'].append(int(k.strip('.json')))
                  
Tran_Top_States = pd.DataFrame(clm_4)

# top_transaction_district
clm_5 = {'District':[], 'Year':[],'Quarter':[],'Tran_Amount':[],'Tran_Count':[]}

for i in Agg_state_list:
    if i != "state":
        p_i = path_4+i+"/"
        top_tran_list = os.listdir(p_i)

        for k in top_tran_list:
            p_k = p_i+k
            Data = open(p_k,'r')
            D=json.load(Data)

            for z in D['data']['districts']:
                District = z['entityName']
                Tran_Count = z['metric']['count']
                Tran_Amount = z['metric']['amount']
                clm_5['Tran_Amount'].append(Tran_Amount)
                clm_5['Tran_Count'].append(Tran_Count)
                clm_5['District'].append(District)
                clm_5['Year'].append(i)
                clm_5['Quarter'].append(int(k.strip('.json')))
                  
Tran_Top_District = pd.DataFrame(clm_5)


# top_transaction_pincode
clm_6 = {'Pincode':[], 'Year':[],'Quarter':[],'Tran_Amount':[],'Tran_Count':[]}

for i in Agg_state_list:
    if i != "state":
        p_i = path_4+i+"/"
        top_tran_list = os.listdir(p_i)
        
        for k in top_tran_list:
            p_k = p_i+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['pincodes']:
                Pincode = z['entityName']
                Tran_Count = z['metric']['count']
                Tran_Amount = z['metric']['amount']
                clm_6['Tran_Amount'].append(Tran_Amount)
                clm_6['Tran_Count'].append(Tran_Count)
                clm_6['Pincode'].append(Pincode)
                clm_6['Year'].append(i)
                clm_6['Quarter'].append(int(k.strip('.json')))
                  
Tran_Top_Pincode = pd.DataFrame(clm_6)


# top_user_state
path_5 = "path"
Agg_state_list = os.listdir(path_4)

clm_7 = {'State':[], 'Year':[],'Quarter':[],'Registered_Users':[]}

for i in Agg_state_list:
    if i != "state":
        p_i = path_5+i+"/"
        top_tran_list = os.listdir(p_i)

        for k in top_tran_list:
            p_k = p_i+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['states']:
                State = z['name']
                Registered_Users = z['registeredUsers']
                clm_7['Registered_Users'].append(Registered_Users)
                clm_7['State'].append(State)
                clm_7['Year'].append(i)
                clm_7['Quarter'].append(int(k.strip('.json')))
                  
User_Top_State = pd.DataFrame(clm_7)

# top_user_district   
clm_8 = {'District':[], 'Year':[],'Quarter':[],'Registered_Users':[]}

for i in Agg_state_list:
    if i != "state":
        p_i = path_5+i+"/"
        top_tran_list = os.listdir(p_i)

        for k in top_tran_list:
            p_k = p_i+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['districts']:
                District = z['name']
                Registered_Users = z['registeredUsers']
                clm_8['Registered_Users'].append(Registered_Users)
                clm_8['District'].append(District)
                clm_8['Year'].append(i)
                clm_8['Quarter'].append(int(k.strip('.json')))

User_Top_District = pd.DataFrame(clm_8)


# top_user_pincode 
clm_9 = {'Pincode':[], 'Year':[],'Quarter':[],'Registered_Users':[]}

for i in Agg_state_list:
    if i != "state":
        p_i = path_5+i+"/"
        top_tran_list = os.listdir(p_i)

        for k in top_tran_list:
            p_k = p_i+k
            Data = open(p_k,'r')
            D = json.load(Data)

            for z in D['data']['pincodes']:
                Pincode = z['name']
                Registered_Users = z['registeredUsers']
                clm_9['Registered_Users'].append(Registered_Users)
                clm_9['Pincode'].append(Pincode)
                clm_9['Year'].append(i)
                clm_9['Quarter'].append(int(k.strip('.json')))
                  
User_Top_Pincode = pd.DataFrame(clm_9)


# Data cleaning
Tran_Agg["State"] = Tran_Agg["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
Tran_Agg["State"] = Tran_Agg["State"].str.replace("-"," ")
Tran_Agg["State"] = Tran_Agg["State"].str.title()
Tran_Agg["State"] = Tran_Agg["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")

User_Agg["State"] = User_Agg["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
User_Agg["State"] = User_Agg["State"].str.replace("-"," ")
User_Agg["State"] = User_Agg["State"].str.title()
User_Agg["State"] = User_Agg["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")

Tran_Map["State"] = Tran_Map["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
Tran_Map["State"] = Tran_Map["State"].str.replace("-"," ")
Tran_Map["State"] = Tran_Map["State"].str.title()
Tran_Map["State"] = Tran_Map["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Tran_Map["District"] = Tran_Map["District"].str.replace(" district","")
Tran_Map["District"] = Tran_Map["District"].str.title()


User_Map["State"] = User_Map["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
User_Map["State"] = User_Map["State"].str.replace("-"," ")
User_Map["State"] = User_Map["State"].str.title()
User_Map["State"] = User_Map["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
User_Map["District"] = User_Map["District"].str.replace(" district","")
User_Map["District"] = User_Map["District"].str.title()

Tran_Top_States["State"] = Tran_Top_States["State"].str.title()
Tran_Top_District["District"] = Tran_Top_District["District"].str.title()
User_Top_State["State"] = User_Top_State["State"].str.title()
User_Top_District["District"] = User_Top_District["District"].str.title()

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host = "host",
  user = "user",
  password = "password",
  auth_plugin = "mysql_native_password"
)

# Create a new database and use
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepe")

# Close the cursor and database connection
mycursor.close()
mydb.close()

# Connect to the newly created database
engine = create_engine('mysql+mysqlconnector://user:password@host/db', echo=False)

# Insert the DataFrames datas to the SQL Database 

# 1
Tran_Agg.to_sql('tran_agg', engine, if_exists = 'replace', index=False,
                                 dtype={'State': sqlalchemy.types.VARCHAR(length=100),
                                       'Year': sqlalchemy.types.Integer,
                                       'Quarter': sqlalchemy.types.Integer,
                                       'Tran_type': sqlalchemy.types.VARCHAR(length=100),
                                       'Tran_count': sqlalchemy.types.BigInteger,
                                       'Tran_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
# 2
User_Agg.to_sql('user_agg', engine, if_exists = 'replace', index=False,
                          dtype={'State': sqlalchemy.types.VARCHAR(length=100),
                                 'Year': sqlalchemy.types.Integer,
                                 'Quarter': sqlalchemy.types.Integer,
                                 'Registered_Users': sqlalchemy.types.BigInteger,
                                 'App_Opened': sqlalchemy.types.BigInteger,
                                 'Brand_Name': sqlalchemy.types.VARCHAR(length=100),
                                 'Brand_Count': sqlalchemy.types.BigInteger,
                                 'Brand_Percentage': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
# 3
Tran_Map.to_sql('tran_map', engine, if_exists = 'replace', index=False,
                          dtype={'State': sqlalchemy.types.VARCHAR(length=100),
                                 'Year': sqlalchemy.types.Integer,
                                 'Quarter': sqlalchemy.types.Integer,
                                 'District': sqlalchemy.types.VARCHAR(length=100),
                                 'District_Tran_Count': sqlalchemy.types.BigInteger,
                                 'District_Tran_Amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
# 4
User_Map.to_sql('user_map', engine, if_exists = 'replace', index=False,
                   dtype={'State': sqlalchemy.types.VARCHAR(length=100),
                          'Year': sqlalchemy.types.Integer,
                          'Quarter': sqlalchemy.types.Integer,
                          'District': sqlalchemy.types.VARCHAR(length=100),
                          'Registered_Users': sqlalchemy.types.BigInteger,
                          'App_Opened': sqlalchemy.types.BigInteger })
# 5
Tran_Top_States.to_sql('tran_top_states', engine, if_exists = 'replace', index=False,
                         dtype={'State': sqlalchemy.types.VARCHAR(length=100),
                                'Year': sqlalchemy.types.Integer,
                                'Quarter': sqlalchemy.types.Integer,
                                'Tran_Amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True),
                                'Tran_Count': sqlalchemy.types.BigInteger
                               })
# 6
Tran_Top_District.to_sql('tran_top_district', engine, if_exists = 'replace', index=False,
                         dtype={'District': sqlalchemy.types.VARCHAR(length=100),
                                'Year': sqlalchemy.types.Integer,
                                'Quarter': sqlalchemy.types.Integer,
                                'Tran_Amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True),
                                'Tran_Count': sqlalchemy.types.BigInteger
                               })
# 7
Tran_Top_Pincode.to_sql('tran_top_pincode', engine, if_exists = 'replace', index=False,
                         dtype={'Pincode': sqlalchemy.types.Integer,
                                'Year': sqlalchemy.types.Integer,
                                'Quarter': sqlalchemy.types.Integer,
                                'Tran_Amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True),
                                'Tran_Count': sqlalchemy.types.BigInteger
                               })
# 8
User_Top_State.to_sql('user_top_state', engine, if_exists = 'replace', index=False,
                   dtype={'State': sqlalchemy.types.VARCHAR(length=100),
                          'Year': sqlalchemy.types.Integer,
                          'Quarter': sqlalchemy.types.Integer,
                          'Registered_Users': sqlalchemy.types.BigInteger})
# 9
User_Top_District.to_sql('user_top_district', engine, if_exists = 'replace', index=False,
                   dtype={'District': sqlalchemy.types.VARCHAR(length=100),
                          'Year': sqlalchemy.types.Integer,
                          'Quarter': sqlalchemy.types.Integer,
                          'Registered_Users': sqlalchemy.types.BigInteger})
# 10
User_Top_Pincode.to_sql('user_top_pincode', engine, if_exists = 'replace', index=False,
                   dtype={'Pincode': sqlalchemy.types.Integer,
                          'Year': sqlalchemy.types.Integer,
                          'Quarter': sqlalchemy.types.Integer,
                          'Registered_Users': sqlalchemy.types.BigInteger})















