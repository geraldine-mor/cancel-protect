import streamlit as st
import pandas as pd
import joblib

@st.cache_data
def load_data():
    df = pd.read_csv("outputs/datasets/cleaned/HotelBookingsValid.csv")
    return df


@st.cache_data
def load_raw():
    raw_df = pd.read_csv("outputs/datasets/collection/HotelBookings.csv")
    return raw_df


@st.cache_data
def load_clean():
    clean_df = pd.read_csv("outputs/datasets/cleaned/HotelBookingsClean.csv")
    return clean_df


@st.cache_resource
def load_pipeline(pipeline_path):
    return joblib.load(filename=pipeline_path)