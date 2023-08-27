import base64
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, resources_pb2, service_pb2
def get_ingredients(image):
    # Create a Clarifai channel
    channel = ClarifaiChannel.get_grpc_channel()
    # Initialize the stub for the V2 API
    stub = service_pb2_grpc.V2Stub(channel)
    # Set up the request
    request = service_pb2.PostModelOutputsRequest(
        model_id='food-item-recognition',
        inputs=[resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(base64=image)))],
    )
    # Set up the authorization metadata
    metadata = (('authorization', 'Key ea604e81c34544c5b477cdec8f05eb85'),
            ('x-user-id', 'clarifai'),
            ('x-app-id', 'main'))
    # Make the gRPC call with the metadata
    response = stub.PostModelOutputs(request, metadata=metadata)
    # Print the entire response for debugging
    print(response)
    # Check if the response contains any outputs
    if response.outputs:
        # Extract predicted ingredients from the response
        predicted_ingredients = [concept.name for concept in response.outputs[0].data.concepts]
        return predicted_ingredients
    else:
        # Handle case where no concepts were found
        print("No predicted ingredients found in the response.")
        return []


import os   # importing os for accessing tokens
os.environ["REPLICATE_API_TOKEN"]="r8_1XFHddW7FUYSULo1Eii4s1GWDLPa8H10hgJDe"  # placing key
import replicate   # importing replicate
def get_recipes(predicted_ingredients):
    i_prompt = f"Suggest recipes using these ingredients: {', '.join(predicted_ingredients)}"
    output_prompt = replicate.run('replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf',
                                  input={"prompt": f"{i_prompt} Assistant:",
                                         "temperature": 0.7, "top_p": 0.8, "max_length": 200, "repetition_penalty": 1.2})
    recipes = "".join(output_prompt)
    return recipes


# Streamlit UI
import streamlit as st
     # Initialize session_state
if 'predicted_ingredients' not in st.session_state:
    st.session_state.predicted_ingredients = []
if 'recipes' not in st.session_state:
    st.session_state.recipes = ""

st.set_page_config(page_title="Your Cooking Assistant", page_icon="🍳", layout="centered", initial_sidebar_state="collapsed")
st.title("Your Cooking Assistant")
# File uploader widget
uploaded_file = st.file_uploader("Upload the Image", type=["jpg", "jpeg", "png"])
    # Check if an image has been uploaded
if uploaded_file is not None:
    # Call the get_ingredients function with the uploaded image
    predicted_ingredients = get_ingredients(image.read())
    if st.button("Get Recipes"):
       recipes = get_recipes(predicted_ingredients)
       st.success("Here are some recipe ideas:")
       st.write(recipes)
       st.write(predicted_ingredients)
