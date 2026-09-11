# app.py
import streamlit as st

st.title("My Python App")
name = st.text_input("Your name")

if st.button("Say hello"):
    st.write(f"Hello, {name}!")