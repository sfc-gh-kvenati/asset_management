import streamlit as st
import snowflake.connector
from snowflake.snowpark import DataFrame
from snowflake.snowpark.session import Session
from snowflake.snowpark import functions as F
from snowflake.snowpark.functions import col, lit, udf
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, date, timedelta
import random
import datetime
import time

########################################################################
# You can modify these for another airline. These are for Thai Airways
########################################################################

session = Session.builder.configs(st.secrets["snowflake"]).create()

st.set_page_config(layout="wide")

@st.cache_data
def get_aum_data():
    # st.write('Sample cluster data that shows the recency, frequency and monetary attributes of each customer')
    df = session.table('AUM')
    return df.to_pandas()

@st.cache_data
def get_opm_data():
    # st.write('Sample cluster data that shows the recency, frequency and monetary attributes of each customer')
    df = session.table('OPM')
    return df.to_pandas()

@st.cache_data
def get_roa_data():
    # st.write('Sample cluster data that shows the recency, frequency and monetary attributes of each customer')
    df = session.table('ROA')
    return df.to_pandas()

@st.cache_data
def get_der_data():
    # st.write('Sample cluster data that shows the recency, frequency and monetary attributes of each customer')
    df = session.table('DER')
    return df.to_pandas()

@st.cache_data
def get_bench_data():
    # st.write('Sample cluster data that shows the recency, frequency and monetary attributes of each customer')
    df = session.table('BENCHMARK')
    return df.to_pandas()

def main():

    colors = [
        "#aa423a",
        "#f6b404",
        "#327a88",
        "#303e55",
        "#c7ab84",
        "#b1dbaa",
        "#feeea5",
        "#3e9a14",
        "#6e4e92",
        "#c98149",
        "#d1b844",
        "#8db6d8",
    ]

    with st.columns(3)[1]:
        st.title('AUM Dashboard')

    df = get_aum_data()
    df_opm = get_opm_data()
    df_roa = get_roa_data()
    df_der = get_der_data()
    df_bench = get_bench_data()


    col1, col2, col3 = st.columns([1,2,3])

    with st.container(border=True):

        with col1:

            col4, col5 = st.columns([1,5])
            with st.container():
                with col4:
                    st.markdown('\n  ')
                    st.image('user.svg',use_column_width=True)

                with col5:
                    st.subheader('92%\n  Client Retention Rate')

            col6, col7 = st.columns([1,5])
            with st.container():
                with col6:
                    st.markdown('\n  ')
                    st.image('growth.svg',use_column_width=True)

                with col7:
                    st.subheader('7%\n  New Client Acquisition Rate')

            col8, col9 = st.columns([1,5])
            with st.container():
                with col8:
                    st.markdown('\n  ')
                    st.image('aum.svg',use_column_width=True)

                with col9:
                    st.subheader('527%\n  AUM Growth YTD')
        with col2:
            # Donut Chart
            st.subheader('$' +str(df[df.YEAR==2024]['AUM'].values[0]*1000000))
            st.markdown("AUM (USD) YTD")
            cat_names = df.CATEGORY.values.tolist()
            cat_select = alt.selection_single(fields=["CATEGORY"], empty="all")
            cat_pie_clicks = (
                (
                    alt.Chart(df)
                    .mark_arc(innerRadius=80)
                    .encode(
                        theta=alt.Theta(
                            "AUM",
                            type="quantitative",
                            aggregate="sum",
                            title="Total AUM",
                        ),
                        color=alt.Color(
                            field="CATEGORY",
                            type="nominal",
                            scale=alt.Scale(domain=cat_names),
                            title="Category",
                        ),
                        opacity=alt.condition(cat_select, alt.value(1), alt.value(0.25)),
                    )
                )
                .add_selection(cat_select)
                .properties(height=250)
            )

            st.altair_chart(cat_pie_clicks, use_container_width=True)

        with col3:
            st.subheader('$' +str(df['AUM'].sum()*1000000))
            st.markdown("AUM Growth over time")
            st.bar_chart(df, x="YEAR", y="AUM", height=250)


    col20, col21 = st.columns([6,2])

    with st.container():

        with col20:
            col1, col2, col3 = st.columns([1,3,2])
            # Row 1
            with st.container():
                with col2:
                    st.subheader("Finance")
                with col3:
                    st.subheader("Investments")

            # Row 2
            col4, col5, col6 = st.columns([1,3,2])
            with st.container():
                with col4:
                    opm_total = df_opm['VALUE'].mean()
                    st.subheader("{:.0%}".format(opm_total) +'\n  Operating Profit Margin')
                with col5:
                    #df_opm['VALUE'] = df_opm['VALUE'].map('{:.1%}'.format)
                    #st.area_chart(df_opm, x="MONTH", y="VALUE", height=150)
                    #Line chart
                    opm_chart = (
                        (
                            alt.Chart(df_opm)
                            .mark_area()
                            .encode(
                                x=alt.X(
                                    "month(MONTH)",
                                    type="temporal",
                                    title=""
                                ),
                                y=alt.Y(
                                    field="VALUE",
                                    type="quantitative",
                                    title="",
                                    axis=alt.Axis(format='%')
                                )
                            )
                        )
                        .properties(height=150)

                    )
                    st.altair_chart(opm_chart, use_container_width=True)
                with col6:
                    df_bench['MONTH'] = pd.to_datetime(df_bench['MONTH'])
                    st.title("{:.0%}".format(df_bench[df_bench.MONTH==datetime.datetime(2023,12,1)]['VALUE'].values[0]))
         

            # Row 3
            col8, col9, col10 = st.columns([1,3,2])
            with st.container():
                with col8:
                    roa_total = df_roa['VALUE'].mean()
                    st.subheader("{:.0%}".format(roa_total) +'\n  ROA')
                with col9:
                    roa_chart = (
                        (
                            alt.Chart(df_roa)
                            .mark_line()
                            .encode(
                                x=alt.X(
                                    "month(MONTH)",
                                    type="temporal",
                                    title=""
                                ),
                                y=alt.Y(
                                    field="VALUE",
                                    type="quantitative",
                                    title="",
                                    axis=alt.Axis(format='%')
                                )
                            )
                        )
                        .properties(height=150)

                    )
                    st.altair_chart(roa_chart, use_container_width=True)
                with col10:
                    bench_chart = (
                        (
                            alt.Chart(df_bench)
                            .mark_bar()
                            .encode(
                                x=alt.X(
                                    "month(MONTH)",
                                    type="ordinal",
                                    title=""
                                ),
                                y=alt.Y(
                                    field="VALUE",
                                    type="quantitative",
                                    title="",
                                    axis=alt.Axis(format='.1%')
                                )
                            )
                        )
                        .properties(height=150, title="Porfolio Performance vs Benchmark")

                    )
                    st.altair_chart(bench_chart, use_container_width=True)        

          

        with col21:
            # Pie Chart
            st.subheader("ESG")
            df_esg = pd.DataFrame([['Carbon Footprint',0.33],['Social Impact Score',0.33],['Governance Score',0.33]],columns=('ESG','Score'))
            esg_chart = (
                (
                    alt.Chart(df_esg)
                    .mark_arc()
                    .encode(
                        theta=alt.Theta(
                            "Score",
                            type="quantitative",
                            aggregate="sum",
                            title="Score",
                        ),
                        color=alt.Color(
                            field="ESG",
                            type="nominal",
                            title="",
                            legend=alt.Legend(orient='bottom', direction='vertical', labelFontSize=14)
                        ),
                    )
                )
                .properties(height=350)
            )

            st.altair_chart(esg_chart, use_container_width=True)


    # Row 4
    col1, col2, col3, col4 = st.columns([1,3,2,2])
    with st.container():
        with col1:
            der_total = df_der['VALUE'].mean()
            st.subheader("{:.0%}".format(der_total) +'\n  Debt to Equity Ratio')
        with col2:
            #st.bar_chart(df_der, x="MONTH", y="VALUE", height=150)
            der_chart = (
                (
                    alt.Chart(df_der)
                    .mark_bar()
                    .encode(
                        x=alt.X(
                            "month(MONTH)",
                            type="ordinal",
                            title=""
                        ),
                        y=alt.Y(
                            field="VALUE",
                            type="quantitative",
                            title="",
                            axis=alt.Axis(format='%')
                        )
                    )
                )
                .properties(height=150)

            )
            st.altair_chart(der_chart, use_container_width=True)
        with col3:
            col4, col5 = st.columns(2)
            with st.container():
                with col4:
                    st.header("60%")
                with col5:
                    st.header("Beta = 0.85")
            col6, col7 = st.columns(2)
            with st.container():
                with col6:
                    st.markdown("Active Share")
                with col7:
                    st.markdown("Portfolio Risk") 



if __name__ == "__main__":
    main()
    
