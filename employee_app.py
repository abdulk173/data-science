import streamlit as st
import pandas as pd
import plotly.express as px

#page configuration 

st.set_page_config(page_title="employee Dashboard", page_icon ="👥", layout= "wide")

@st.cache_data
def load_data():
    #load employee dataset
    df = pd.read_csv("clean_employee_dataset.csv")
    return df

def create_sidebar_filter(df):
    """Create sidebar filter and return filter"""
    st.sidebar.header("filter")
    department = st.sidebar.multiselect(
        "selecte department(s)",
        options=df["department"].unique(),
        default=df["department"].unique()
    )

    location = st.sidebar.multiselect(
        "select office location(s)",
        options=df["office_location"].unique(),
        default=df["office_location"].unique()
    )

    remote_filter = st.sidebar.radio(
        "remote work status(s)",
        options=["All", "Yes", "No"],
        index=0
    )

    return department, location, remote_filter

def filter_data(df , department , location , remote_filter):

    """apply filter to the dataframe"""
    filtered_df = df[df["department"].isin(department) & df["office_location"].isin(location)]
    if remote_filter != "All":
      filtered_df = filtered_df[filtered_df["remote"] == remote_filter]   
    return filtered_df   

def display_metrics(filtered_df):

    """display key metrics"""

    col1, col2,col3,col4 = st.columns(4)

    with col1:
        st.metric("👤 Total employee", len(filtered_df))   

    with col2:
        avg_salary = filtered_df["salary"].mean() if len(filtered_df) > 0 else 0
        st.metric("average salary" , f"${avg_salary:,.2f}")   

    with col3:
        avg_performance = filtered_df["performance"].mean() if len(filtered_df) > 0 else 0
        st.metric("average performance" , f"{avg_performance :.1f}")

    with col4:
        remote_pct = (filtered_df["remote"] == "Yes").sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric("Remote worker" , f"{remote_pct:.1f}") 

def display_cahrt(filtered_df):
    """create vidualization chart"""
    if len(filtered_df) == 0:
        st.warning("No available data for selectered filter. Please adjust your filter selection")
        return

    col1 , col2 = st.columns(2)

    with col1:
        st.subheader("Employee by department")
        dept_count = filtered_df["department"].value_counts()
        fig1 = px.pie(values= dept_count.values, names= dept_count.index, hole=0.5)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Average salary by department")
        dept_salary = filtered_df.groupby("department")["salary"].mean().sort_values(ascending =True)    
        fig2 = px.bar(
            x=dept_salary.values,
            y=dept_salary.index,
            orientation="h"
        )      
        fig2.update_layout(xaxis_title="salary",yaxis_title="Department")
        st.plotly_chart(fig2 , use_container_width=True) 

    col3 , col4 = st.columns(2)     

    with col3:
        st.subheader("performance distribution")
        fig3= px.histogram(filtered_df, x="performance" , nbins=6)
        fig3.update_layout(xaxis_title="performance score",yaxis_title="count")
        fig3.update_traces(marker_line_color="white", marker_line_width=1.5)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Employee by location")
        location_counts = filtered_df["office_location"].value_counts()
        fig4 =px.bar(x = location_counts.index, y= location_counts.values)    
        fig4.update_layout(xaxis_title="office location" , yaxis_title= "count")
        st.plotly_chart(fig4, use_container_width=True)

def display_table_data(filtered_df):
    """display employee table data"""
    if len(filtered_df) > 0:
        st.dataframe(filtered_df, use_container_width=True , height=300)
        st.success("data successfully displayed")
    else:
        st.info("no employee data to display")
                




def main():
    """main function to run the dashboard"""
    df=load_data()

    # """Create side bar filter"""

    department , location, remote_filter = create_sidebar_filter(df)

    filtered_df = filter_data(df, department, location, remote_filter)

    #display metrics 
    display_metrics(filtered_df)

    #markdowm
    st.markdown("---")

    display_cahrt(filtered_df)

    display_table_data(filtered_df)

if __name__ == "__main__":
    main()