import pandas as pd
import pymysql
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Function to execute SQL query and return DataFrame
def execute_query(query):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1234',
        db='phonepe'
    )
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# to create plots
def create_plot(df, plot_type, **kwargs):
    if plot_type == 'pie':
        fig = px.pie(df, **kwargs)
    elif plot_type == 'sunburst':
        fig = px.sunburst(df, **kwargs)
    elif plot_type == 'bar':
        fig = px.bar(df, **kwargs)
    elif plot_type == 'line':
        fig = px.line(df, **kwargs)
    elif plot_type == 'scatter':
        fig = px.scatter(df, **kwargs)
    else:
        fig = None
    if fig:
        fig.update_layout(title_x=0.3)
        st.plotly_chart(fig)


state_list = ["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
"Uttar Pradesh","Uttarakhand","West Bengal"]
year_list = [2018,2019,2020,2021,2022,2023,2024]
quarter_list = [1,2,3,4]

# streamlit page
st.set_page_config(layout="wide")

# Option menu in Streamlit
with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Home","Countrywide TRAN","Statewide TRAN","Countrywide USER","Statewide USER","Top Charts", "Questions"],
        icons = ["house-door","globe2","globe-central-south-asia","globe2","globe-central-south-asia","reception-4","patch-question"],
        menu_icon = "emoji-smile",
        default_index = 0
    )

# Home menu of Streamlit
if selected == "Home":
    st.title(":violet[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]") 
    st.write("")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader(':blue[PHONEPE]')
        st.write("""
    - India’s leading fintech company headquartered in Bengaluru, Karnataka was launched in Aug 2016.
    - From the largest towns to the remotest villages, phonepe exists.
    - **Vision**: To offer every Indian an equal opportunity to accelerate their progress by unlocking the flow of money and access to services.
    """)
    with col2:
        st.image(Image.open("C:/Users/Incognito/Desktop/vscode/PHONEPE/pulse/phonepe.jpg"), width=400)
    
    st.subheader(':blue[PHONEPE PULSE]')
    st.write("""
             PhonePe Pulse is offered by PhonePe to analyze how digital payments have evolved over years in India.
             It helps to understand the interesting trends, deep insights and in-depth analysis of phonepe data in an interactive geo visualization that helps to make important business decisions.
             """)

if selected == "Countrywide TRAN":
    st.subheader(":blue[**GEO VISUALIZATION OF TRANSACTION AMOUNT IN INDIA**]")
    df = execute_query("select State,sum(Tran_amount) as Transaction_Amount from tran_agg group by State;")

    # Plotly Choropleth map
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",  
        locations="State",
        color="Transaction_Amount",
        featureidkey="properties.ST_NM", 
        hover_data=["State","Transaction_Amount"],
        color_continuous_scale="emrld",
        title="Choropleth Map of Transaction Details in India"
    )
       
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    title_text="Choropleth Map of Transaction Details in India",
    title_x=0.2
  )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(":blue[**STATE WISE TRANSACTION TYPE ANALYSIS**]")
    selected_state =  st.selectbox("Select any state",state_list,key="st_5")
    col1,col2=st.columns(2)
    with col1:
        tran_agg = execute_query(f"""select * from(select State,Year,Tran_type,sum(Tran_count) as Transaction_count,sum(Tran_amount) as Transaction_amount from tran_agg
                                    group by State,Year,Tran_type) as a where a.state='{selected_state}' """)
        create_plot(tran_agg,"bar",x="Year",y="Transaction_amount",title="TRANSACTION AMOUNT ANALYSIS BY TYPE AND AMOUNT",hover_name="Transaction_amount",color="Tran_type",barmode="group")
        
        tran_agg_quarters = execute_query(f"""select * from(Select state,Year,Quarter,sum(Tran_amount) as Transaction_amount FROM tran_agg  group by state,year,quarter) as a where a.state='{selected_state}' """)
        create_plot(tran_agg_quarters,"line",x="Quarter",y="Transaction_amount",title="YEARWISE TRANSACTION AMOUNT ANALYSIS BY QUARTER",markers=True,hover_data=["Year","Quarter","Transaction_amount"],color="Year")
        
    with col2:       
        tran_agg_states = execute_query(f"""select * from(select State,Year,sum(Tran_amount) as Transaction_amount from tran_agg group by State,Year) as a where a.state='{selected_state}' """)
        create_plot(tran_agg_states,"line",x="Year",y="Transaction_amount",title="TRANSACTION AMOUNT ANALYSIS",markers=True,hover_data=["Year","Transaction_amount"])

        tran_agg_quarter = execute_query(f"""select * from(select State,Quarter,sum(Tran_amount) as Transaction_amount from tran_agg group by State,Quarter) as a where a.state='{selected_state}' """)
        create_plot(tran_agg_quarter,"pie",names="Quarter",values="Transaction_amount",title="TRANSACTION AMOUNT ANALYSIS BY QUARTER",hover_name="Transaction_amount",hole=0.5)

    st.subheader(":blue[**COUNTRYWIDE TRANSACTION ANALYSIS**]")
    col1,col2=st.columns(2)
    with col1:
        tran_agg = execute_query("SELECT Year,sum(Tran_amount) as Transaction_amount FROM tran_agg group by Year;")
        create_plot(tran_agg,"bar",x="Year",y="Transaction_amount",title="TRANSACTION AMOUNT ANALYSIS BY YEAR",hover_name="Transaction_amount")
        
    with col2:       
        tran_agg_q = execute_query("SELECT quarter as Quarter,sum(Tran_amount) as Transaction_amount FROM tran_agg group by quarter;")
        create_plot(tran_agg_q,"pie",names="Quarter",values="Transaction_amount",title="TRANSACTION AMOUNT ANALYSIS BY QUARTER",hover_name="Transaction_amount",hole=0.5)

    st.subheader(":blue[**INSIGHT**]")
    st.write("""
    - Transaction amount is higher for the states **Telangana,Maharashtra and Karnataka**.
    - Transaction value is higher in the year **2023** which may be associated with higher **Peer-to-Peer Transactions** for all the states.
    - In maximum number of states, **Quarter 4 and Quarter 1** has the highest transaction value. Quarter 1 result includes Q1 of 2024.
    """)


if selected == "Statewide TRAN":

    st.subheader(":blue[**TRANSACTION DETAILS OF EACH STATE**]")
    selected_state =  st.selectbox("Select any state",state_list,key="st_3")
    tran_states = execute_query(f"""select * from(select State,Year,District,sum(district_tran_count) as Transaction_count, sum(district_tran_amount) as Transaction_amount from tran_map
                                    group by State,Year,District) as a where a.state='{selected_state}' """)
    create_plot(tran_states,"line",x="District",y="Transaction_amount",title=f'Transaction Amount By District for {selected_state}',color="Year",markers=True)
   
    tran_state = execute_query(f"""select * from(select state,District,sum(district_tran_count) as Transaction_count, sum(district_tran_amount) as Transaction_amount from tran_map
                                    group by state,district) as a where a.state='{selected_state}' """)

    create_plot(tran_state,"bar",x="District",y="Transaction_count",title="OVERALL TRANSACTION DETAILS IN EACH DISTRICT",color="Transaction_amount",hover_data=["District","Transaction_count","Transaction_amount"],color_continuous_scale="sunsetdark")
    
    st.subheader(":blue[**INSIGHT**]")
    st.write("**Top 5 districts of Higher Transaction Value**")
    result = execute_query(f"select * from tran_map where state = '{selected_state}' order by District_Tran_Amount desc limit 5;")
    result["Year"]=result["Year"].astype(str)
    st.write(result)

if selected == "Countrywide USER":

    st.subheader(":blue[**GEO VISUALIZATION OF REGISTERED USERS IN INDIA**]")
    df = execute_query("select distinct State,sum(Registered_Users) as Registered_Users from user_map group by State")

    # Plotly Choropleth map
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",  
        locations="State",
        featureidkey="properties.ST_NM", 
        color="Registered_Users",
        color_continuous_scale="pinkyl",
        title="Choropleth Map of Phonepe Users in India",
        hover_data=["State","Registered_Users"]
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    title_text="Choropleth Map of Phonepe Users in India",
    title_x=0.3 
)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(":blue[**BRAND COUNT ANALYSIS IN EACH STATE**]")
    selected_state =  st.selectbox("Select any state",state_list,key="st_2")
    user_agg = execute_query(f"""select * from (select state,Brand_Name as Brand,sum(Brand_Count) as Brand_count from user_agg group by state,Brand_Name)
                             as a where a.state='{selected_state}' """)
    create_plot(user_agg,"bar",x="Brand",y="Brand_count",title="BRAND COUNT OF EACH BRANDS",color="Brand",color_discrete_sequence=[
                px.colors.qualitative.Plotly[5],
                px.colors.qualitative.D3[6],
                px.colors.qualitative.Antique[1],
                px.colors.qualitative.Plotly[2],
                px.colors.qualitative.Plotly[7],
                px.colors.qualitative.G10[5]])

    st.subheader(":blue[**BRANDS AND ITS COUNT IN INDIA**]")
    user_agg_india = execute_query("select Brand_Name as Brand, sum(Brand_Count) as Brand_count from user_agg  group by Brand_Name LIMIT 10")
    create_plot(user_agg_india,"pie",names="Brand",values="Brand_count",title="TOP 10 BRANDS AND THEIR COUNTS")

    res = execute_query(f"""select * from (select state,Brand_Name as Brand,sum(Brand_Count) as Brand_count from user_agg group by state,Brand_Name)
                             as a where a.state='{selected_state}' order by Brand_count desc limit 1 """)
    Brand_res = res.iloc[0,1]

    st.subheader(":blue[**INSIGHT**]")
    st.write(f"""
    - **Maharashtra,Uttar Pradesh and Karnataka** have higher number of Registered Users.
    - Among all the Brands, **{Brand_res}** is the top Brand used by phonepe users in {selected_state}.
    - **Xiamoi** is the top Brand in India.
    """)
    

if selected == "Statewide USER":

    st.subheader(":blue[**ANALYSIS OF REGISTERED USERS FOR THE SPECIFIC YEAR**]")
    selected_state =  st.selectbox("Select any state",state_list,key="st")
    selected_year = st.selectbox("Select any year",year_list)

    user_map = execute_query(f"SELECT * FROM phonepe.user_map where State='{selected_state}' and Year={selected_year} ")
    create_plot(user_map,"line",x="District",y="Registered_Users",title="REGISTERED USERS IN EACH DISTRICT",hover_data=["District","Registered_Users"],color="Quarter",markers=True)
    
    st.subheader(":blue[**REGISTERED USERS YEAR WISE COUNT**]")
    user_map_year = execute_query(f"""select * from(select State,Year,sum(Registered_Users) as Registered_Users from user_map
                                    group by State,Year) as a where a.State='{selected_state}' """)
    user_map_year["Year"] = user_map_year["Year"].astype(str)
    fig1 = px.bar(user_map_year,x="Year",y="Registered_Users",title="REGISTERED USERS IN EACH YEAR",hover_data=["Year","Registered_Users"],color="Year",color_discrete_sequence=[
                px.colors.qualitative.Plotly[5],
                px.colors.qualitative.D3[6],
                px.colors.qualitative.Antique[1],
                px.colors.qualitative.Plotly[2],
                px.colors.qualitative.Plotly[7],
                px.colors.qualitative.G10[5]])
    fig1.update_layout(bargap=0.5,title_x=0.4) 
    st.plotly_chart(fig1)

    res_1 = execute_query(f"select * from user_map where state = '{selected_state}' and year='{selected_year}' order by Registered_Users desc limit 1;")
    dstrct = res_1.iloc[0,3]
    Qrtr = res_1.iloc[0,2]

    res_2 = execute_query(f"select * from(select State,Year,sum(Registered_Users) as Registered_Users from user_map group by State,Year) as a where a.State='{selected_state}' order by Registered_Users desc limit 1;")
    yr = res_2.iloc[0,1]

    st.subheader(":blue[**INSIGHT**]")
    st.write(f"""
    - In {selected_year} for the state {selected_state}, **{dstrct}**  has more number of registered users in **Quarter {Qrtr}**.
    - From 2018 to 2024, **{selected_state}** has more number of Users Registered in the year **{yr}**.
    """)


if selected == "Top Charts":

    tab1, tab2 = st.tabs(["Transaction", "User"])
    with tab1:
        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; color: blue; font-weight: bold;">
                TOP 10 STATES
            </div>
            """,
            unsafe_allow_html=True
        )
        tran_top_states = execute_query("SELECT * FROM phonepe.tran_top_states")
        create_plot(tran_top_states,"sunburst",path=["Year","Quarter","State"],values="Tran_Amount",color="Tran_Amount",color_continuous_scale='RdBu',hover_name="Tran_Amount",height=700,title=" ")
        
        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; color: blue; font-weight: bold;">
                TOP 10 DISTRICT
            </div>
            """,
            unsafe_allow_html=True
        )
        tran_top_district = execute_query("SELECT * FROM phonepe.tran_top_district")
        create_plot(tran_top_district,"sunburst",path=["Year","Quarter","District"],values="Tran_Amount",color="Tran_Amount",color_continuous_scale='rdpu',hover_name="Tran_Amount",height=700,title=" ")

        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; color: blue; font-weight: bold;">
                TOP 10 PINCODE
            </div>
            """,
            unsafe_allow_html=True
        )
        
        tran_top_pincode = execute_query("SELECT * FROM phonepe.tran_top_pincode")
        create_plot(tran_top_pincode,"sunburst",path=["Year","Quarter","Pincode"],values="Tran_Amount",color="Tran_Amount",color_continuous_scale='armyrose',height=700,hover_name="Tran_Amount",title=" ")
    
    with tab2:
        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; color: blue; font-weight: bold;">
                TOP 10 STATES
            </div>
            """,
            unsafe_allow_html=True
        )
        user_top_states = execute_query("SELECT * FROM phonepe.user_top_state")
        create_plot(user_top_states,"sunburst",path=["Year","Quarter","State"],values="Registered_Users",color="Registered_Users",color_continuous_scale='RdBu',height=700,hover_name="Registered_Users",title=" ")
        
        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; color: blue; font-weight: bold;">
                TOP 10 DISTRICT
            </div>
            """,
            unsafe_allow_html=True
        )
        user_top_district = execute_query("SELECT * FROM phonepe.user_top_district")
        create_plot(user_top_district,"sunburst",path=["Year","Quarter","District"],values="Registered_Users",color="Registered_Users",color_continuous_scale='rdpu',height=700,hover_name="Registered_Users",title=" ")
        
        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; color: blue; font-weight: bold;">
                TOP 10 PINCODE
            </div>
            """,
            unsafe_allow_html=True
        )
        user_top_pincode = execute_query("SELECT * FROM phonepe.user_top_pincode")
        create_plot(user_top_pincode,"sunburst",path=["Year","Quarter","Pincode"],values="Registered_Users",color="Registered_Users",color_continuous_scale='armyrose',height=700,hover_name="Registered_Users",title=" ")

if selected == "Questions":
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "Least 10 states based on year and amount of transaction",
               "Top 10 States and Districts based on Registered Users",
               "Least 10 States and Districts based on Registered Users",
               "Top 10 Districts based on the Transaction Amount",
               "Least 10 Districts based on the Transaction Amount",
               "Top 10 Districts based on the Transaction count",
               "Least 10 Districts based on the Transaction count",
               "Top Transaction types based on the Transaction Amount"]
    select = st.selectbox("**:blue[Choose any Question]**",options)

    col1,col2 = st.columns(2)
    # Question 1
    if select == options[1]:
        q1 = execute_query("""select Year,State,Transaction_amount from(select *,dense_rank() over(partition by Year order by Transaction_amount desc) rk from (select Year,State,round(sum(Tran_amount)) as Transaction_amount from tran_agg
                group by Year,State) as a) as b where b.rk<=10""")
        q1["Year"] = q1["Year"].astype(str)
        with col1:  
            st.write(q1)
        with col2:
            fig_q1 = px.sunburst(q1,path=["Year","State"],values="Transaction_amount",color="Transaction_amount",hover_name="Transaction_amount",color_continuous_scale="pinkyl",title="Top 10 states based on Year & Transaction Amount")
            st.plotly_chart(fig_q1)

    # Question 2
    if select == options[2]:
        q2 = execute_query("""select Year,State,Transaction_amount from(select *,dense_rank() over(partition by Year order by Transaction_amount asc) rk from (select Year,State,round(sum(Tran_amount)) as Transaction_amount from tran_agg
                group by Year,State) as a) as b where b.rk<=10""")
        q2["Year"] = q2["Year"].astype(str)
        with col1:  
            st.write(q2)
        with col2:
            fig_q2 = px.sunburst(q2,path=["Year","State"],values="Transaction_amount",color="Transaction_amount",hover_name="Transaction_amount",color_continuous_scale="brbg",title="Least 10 states based on Year & Transaction Amount")
            st.plotly_chart(fig_q2)

    # Question 3
    if select == options[3]:
        q3_st = execute_query("""select State,sum(Registered_Users) as Registered_Users from user_map
                group by State order by sum(Registered_Users) desc limit 10;""")
        with col1:  
            st.write(q3_st)
        with col2:
           create_plot(q3_st,"bar",x="State",y="Registered_Users",color="Registered_Users",hover_name="Registered_Users",title="Top 10 States based on Registered_Users")
     
        q3_dt = execute_query("""select District,State,sum(Registered_Users) as Registered_Users from user_map
                group by District,State order by sum(Registered_Users) desc limit 10;""")
        with col1:  
            st.write(q3_dt)
        with col2:
           create_plot(q3_dt,"bar",x="District",y="Registered_Users",color="Registered_Users",hover_name="Registered_Users",title="Top 10 Districts based on Registered_Users")

    # Question 4
    if select == options[4]:
        q4_st = execute_query("""select State,sum(Registered_Users) as Registered_Users from user_map
                group by State order by sum(Registered_Users) asc limit 10;""")
        with col1:  
            st.write(q4_st)
        with col2:
           create_plot(q4_st,"bar",x="State",y="Registered_Users",color="Registered_Users",hover_name="Registered_Users",title="Least 10 States based on Registered_Users")
     
        q4_dt = execute_query("""select District,State,sum(Registered_Users) as Registered_Users from user_map
                group by District,State order by sum(Registered_Users) asc limit 10;""")
        with col1:  
            st.write(q4_dt)
        with col2:
           create_plot(q4_dt,"bar",x="District",y="Registered_Users",color="Registered_Users",hover_name="Registered_Users",title="Least 10 Districts based on Registered_Users")
    
    # Question 5
    if select == options[5]:
        q5 = execute_query("""select District,State,sum(District_Tran_Amount) as Transaction_amount from tran_map 
                group by District,State order by sum(District_Tran_Amount) desc limit 10;""")
        with col1:  
            st.write(q5)
        with col2:
            create_plot(q5,"line",x="District",y="Transaction_amount",hover_data=["District","Transaction_amount","State"],markers=True,title="Top 10 Districts based on Transaction Amount")

    # Question 6
    if select == options[6]:
        q6 = execute_query("""select District,State,sum(District_Tran_Amount) as Transaction_Amount from tran_map 
                group by District,State order by sum(District_Tran_Amount) asc limit 10;""")
        with col1:  
            st.write(q6)
        with col2:
            create_plot(q6,"line",x="District",y="Transaction_Amount",hover_data=["District","Transaction_Amount","State"],markers=True,title="Least 10 Districts based on Transaction Amount")        
    
    # Question 7
    if select == options[7]:
        q7 = execute_query("""select District,State,sum(District_Tran_Count) as Transaction_Count from tran_map 
                group by District,State order by sum(District_Tran_Count) desc limit 10;""")
        with col1:  
            st.write(q7)
        with col2:
            create_plot(q7,"line",x="District",y="Transaction_Count",hover_data=["District","Transaction_Count","State"],markers=True,title="Top 10 Districts based on Transaction Count")

    # Question 8
    if select == options[8]:
        q8 = execute_query("""select District,State,sum(District_Tran_Count) as Transaction_Count from tran_map 
                group by District,State order by sum(District_Tran_Count) asc limit 10;""")
        with col1:  
            st.write(q8)
        with col2:
            create_plot(q8,"line",x="District",y="Transaction_Count",hover_data=["District","Transaction_Count","State"],markers=True,title="Least 10 Districts based on Transaction Count")        
    
     # Question 9
    if select == options[9]:
        q9 = execute_query("select Tran_type as Transaction_Type,round(sum(Tran_amount)) as Transaction_Amount from tran_agg group by Tran_type;")
        with col1:  
            st.write(q9)
        with col2:
            create_plot(q9,"pie",names="Transaction_Type",values="Transaction_Amount",hover_data=["Transaction_Type","Transaction_Amount"],hole=0.5,title="Top Transaction types based on Transaction Amount")        