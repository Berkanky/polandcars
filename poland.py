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
    mileagest = st.slider("Max-Min Mileage", value=[min(df["mileage"]), max(df["mileage"])],min_value=min(df["mileage"]),max_value=max(df["mileage"]))
    doublest = st.slider("Max-Min Engine", value=[min(df["vol_engine"]),max(df["vol_engine"])])
    pricest2=st.slider("Max-Min Price",value=[min(df["price"]),max(df["price"])],min_value=min(df["price"]),max_value=max(df["price"]))
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
    newdf=pd.read_csv("polandcars.csv")
    newdf["price"]=newdf["price"]/4.5
    newdf=newdf.groupby("mark").describe()
    newdf = newdf[["vol_engine", "price"]]
    newdf.columns = ["Vcount", "Vmean", "Vstd", "Vmin", "V25%", "V50%", "V75%", "Vmax", "Pcount", "Pmean", "Pstd",
                     "Pmin", "P25%", "P50%", "P75%", "Pmax"]
    newdf = newdf.reset_index()
    newdf=newdf.set_index("mark")
    newdfcolumns=list(newdf.columns)
    defaultix=newdfcolumns.index("Pmean")
    newdfst=st.selectbox("Select Second Column",newdfcolumns,index=defaultix)
    if newdfst:
        newdf=newdf[[newdfst]]
        newdf[newdfst]=newdf[newdfst].apply(int)
        newdf=newdf.reset_index()
        listgraph=["Pie","Bar"]
        defaultix2=listgraph.index("Pie")
        listgraphst=st.selectbox("Select Graph",listgraph,index=defaultix2)
        if listgraphst=="Bar":
            fig = px.bar(newdf, x="mark", y=newdfst, title=newdfst)
        if listgraphst=="Pie":
            fig=px.pie(newdf,values=newdfst,names="mark",title=newdfst,height=700)
        st.plotly_chart(fig,use_container_width=True)
        @st.cache
        def convert_df(newdf):
            return newdf.to_csv().encode('utf-8')
        csv = convert_df(newdf)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='dflast2.csv',
            mime='text/csv',
        )
    #st.dataframe(newdf)
