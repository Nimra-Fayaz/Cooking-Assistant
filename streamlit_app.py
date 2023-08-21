import streamlit as st
st.write("Cooking-Assistant")
import clarifai 
import llama2
import nutritionix
import pandas as pd
import numpy as np

@st.cache
def get_ingredients(image):
   # Clarifai API call
   return ingredients

@st.cache 
def get_recipes(ingredients):
   # LLama2 API call
   return recipes

@st.cache
def get_nutrition(recipe):
   # Nutritionix API call
   return nutrition_data

st.title("Cooking Assistant")

uploaded_file = st.file_uploader(...)
if clicked submit:
   ing = get_ingredients(file)
   rec = get_recipes(ing)
   nutr = get_nutrition(rec)

   st.success("Found recipes:")
   st.json(rec)
