from clarifai import rest
from clarifai.rest import ClarifaiApp
import base64
def get_ingredients(image):
# Initialize Clarifai API with your PAT
    clarifai_app = ClarifaiApp(api_key='c104074359ea40a0a22fab914c2caee2')
    USER_ID = 'clarifai'
    APP_ID = 'main'
    # Model details and version
    MODEL_ID = 'food-item-recognition'
    MODEL_VERSION_ID = '1d5fd481e0cf4826aa72ec3ff049e044'
    # Convert image bytes to base64-encoded image data
    base64_image = base64.b64encode(image).decode('utf-8')
    model = clarifai_app.models.get(MODEL_ID, MODEL_VERSION_ID)
    response = model.predict_by_base64(base64_image)
    predicted_ingredients = [concept.name for concept in response['outputs'][0]['data']['concepts']]
    return predicted_ingredients


import os   # importing os for accessing tokens
os.environ["REPLICATE_API_TOKEN"]="r8_9V0jsom0JgBxih0h9oKIm7SkTMlEh5G43WxfH"  # placing key
import replicate   # importing replicate
def get_recipes(predicted_ingredients):
  i_prompt = f"Suggest recipes using these ingredients: {predicted_ingredients}" #updated part
  output_propmt=replicate.run('replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781',input={"prompt":f"{pre} {i_prompt} Assistant:",#prompts
  "temperature":0.1,"top_p":0.9 , "max_length":128,"repetition_penalty":1})#model parameters
  recipes=" "
  for i in output_propmt:
         recipes+=i
  return recipes


# Nutritionix nutrition data function
from nutritionix import Nutritionix
def get_nutrition(recipes):
    APP_ID = '9de75d97'
    API_KEY ='28229e90a39a85f8c8e1ec39d6a17418'
    nutritionix_client = Nutritionix(app_id=APP_ID, api_key=API_KEY)
    nutrition_data = nutritionix_client.natural.nutrients(recipes)
    calories = nutrition_data['calories']
    protein = nutrition_data['protein']
    carbs = nutrition_data['carbs']
    return calories, protein, carbs


# Streamlit UI
import streamlit as st
st.title("Food Ingredient Identifier")
# File uploader widget
uploaded_file = st.file_uploader("Upload an ingredient photo", type=["jpg", "jpeg", "png"])
# Check if an image has been uploaded
if uploaded_file is not None:
    # Call the get_ingredients function with the uploaded image
    predicted_ingredients = get_ingredients(uploaded_file.read())
if st.button("Get Recommendations"):
  recipes = get_recipes(predicted_ingredients)
  calories, protein, carbs = get_nutrition(recipes[0])
  st.success("Here are some recipe ideas:")
  st.write(recipes)
  st.write(f"Calories: {calories}")
  st.write(f"Protein: {protein}")
  st.write(f"Carbs: {carbs}")
