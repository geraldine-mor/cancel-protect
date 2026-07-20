import streamlit as st
import pandas as pd
import joblib

@st.cache_data
def load_data():
    df = pd.read_csv("outputs/datasets/cleaned/HotelBookingsValid.csv")
    return df


@st.cache_resource
def load_pipeline(pipeline_path):
    return joblib.load(filename=pipeline_path)