import streamlit as st
import pandas as pd
import plotly_express as px
st.set_page_config(layout="wide")
st.title("Cars In Poland")
df=pd.read_csv("polandcars.csv")
df=df.drop(columns=["Unnamed: 0","generation_name"])
df["price"]=df["price"]/4.5
df=df.set_index("mark")
marks=df.index
marks=list(marks.unique())
col1,col2=st.columns(2)
with col1:
    marksst=st.multiselect("Select Car Brands",marks)
    if marksst:
        df=df.loc[marksst]
    df=df.reset_index()
    df=df.set_index("model")
    modellist=df.index
    modellist=list(modellist.unique())
    modelst=st.multiselect("Select Model",modellist)
    if modelst:
        df=df.loc[modelst]
    df=df.reset_index()
yearsradio=st.radio("Select Option Year",["Specific","All"])
if yearsradio!="All":
    yearst2=st.number_input("Select Year",min_value=min(df["year"]),max_value=max(df["year"]),value=2021)
    if yearst2:
        df=df[df["year"]==yearst2]
with col2:
    fuellist=list(df["fuel"].unique())
    fuellist.insert(0,"All")
    fuelst=st.selectbox("Select Fuel",fuellist)
    df=df.set_index("city")
    citylist=df.index
    citylist=list(citylist.unique())
    cityst=st.multiselect("Select City",citylist)
    if cityst:
        df=df.loc[cityst]
    df=df.reset_index()
    if fuelst!="All":
        df=df[df["fuel"]==fuelst]

col1,col2=st.columns(2)
with col1:
    mileagest = st.slider("Max-Min Mileage", value=[min(df["mileage"]), max(df["mileage"])])
    doublest = st.slider("Max-Min Engine", value=[min(df["vol_engine"]),max(df["vol_engine"])])
    pricest2=st.slider("Max-Min Price",value=[min(df["price"]),max(df["price"])])
    if pricest2:
        df=df[df["price"]>=pricest2[0]]
        df=df[df["price"]<=pricest2[1]]
    if mileagest:
        df=df[df["mileage"]>=mileagest[0]]
        df=df[df["mileage"]<=mileagest[1]]
    if doublest:
        df = df[df["vol_engine"] >= doublest[0]]
        df = df[df["vol_engine"] <= doublest[1]]
with col2:
    st.dataframe(df)


    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='dflast.csv',
        mime='text/csv',
    )
selectgraph=st.radio("Select Option",["Model","Mean"])
if selectgraph=="Model":
    listcolumns=list(df.columns)
    listcolumnsst=st.selectbox("Choose Column",listcolumns,index=listcolumns.index("fuel"))
    if listcolumnsst:
        df=df[listcolumnsst]
        df=df.value_counts()
        xlast=df.index
        ylast=df.values
        fig=px.pie(df,values=ylast,names=xlast,title=listcolumnsst,height=800)
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.write("Not Found In Columns")
if selectgraph=="Mean":
    df2=pd.read_csv("polandcars.csv")
    df2=df2.set_index("mark")
    modelmulti=df2.index
    modelmulti=list(modelmulti.unique())
    modelmultist=st.multiselect("Select Mark",modelmulti)
    if modelmultist:
        df2=df2.loc[modelmultist]
        df2=df2.reset_index()
        x5=df2["model"]
        y5=df2["price"]
        fig=px.bar(df2,x=x5,y=y5)
        st.plotly_chart(fig,use_container_width=True)
