import time

import streamlit as st
import snowflake.connector
from snowflake.snowpark import DataFrame
from snowflake.snowpark.session import Session
from snowflake.snowpark import functions as F
from snowflake.snowpark.functions import col, lit, udf
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
from datetime import datetime, date, timedelta
import random

########################################################################
# You can modify these for another airline. These are for Thai Airways
########################################################################
sample_table = 'AUM'

session = Session.builder.configs(st.secrets["snowflake"]).create()

st.set_page_config(layout="wide")

@st.cache_data
def get_sample_data():
    # st.write('Sample cluster data that shows the recency, frequency and monetary attributes of each customer')
    df = session.table(sample_table)
    return df.to_pandas()


def main():

    df = get_sample_data()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(df, x="YEAR", y="AUM")
 

if __name__ == "__main__":
    main()


