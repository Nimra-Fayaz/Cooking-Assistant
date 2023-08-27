import base64
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

def get_ingredients(image):
    PAT = 'ea604e81c34544c5b477cdec8f05eb85'  # Your Personal Access Token from Clarifai
    USER_ID = 'clarifai'  # Your user ID
    APP_ID = 'main'  # Your app ID
    MODEL_ID = 'food-item-v1-recognition'  # The model ID for food recognition
    MODEL_VERSION_ID = 'dfebc169854e429086aceb8368662641'  # Optional: Specify a model version ID

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image  # Pass the image content as bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
    
    predicted_ingredients = [concept.name for concept in post_model_outputs_response.outputs[0].data.concepts]
    return predicted_ingredients


import requests
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc, status_code_pb2

# Your PAT (Personal Access Token) from Clarifai
PAT = '10d7dbdf99ec4129be8d5df61fa323ef'
USER_ID = 'meta'
APP_ID = 'Llama-2'
MODEL_ID = 'llama2-13b-chat'
MODEL_VERSION_ID = '79a1af31aa8249a99602fc05687e8f40'
TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'

def get_recipes(predicted_ingredients):
    # Convert the predicted ingredients into a single string
    ingredients_text = ', '.join(predicted_ingredients)

    # Set up Clarifai channel and stub
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    # Post model outputs request for Clarifai
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            content=ingredients_text  # Pass the ingredients as text content
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    print("Completion:\n")
    print(output.data.text.raw)

    response = requests.get(llama2_api_url, headers=headers, params=params)
    if response.status_code == 200:
        recipes_data = response.json()
        recipes = []
        for recipe in recipes_data:
            title = recipe.get('title', 'Unknown Recipe')
            instructions = recipe.get('instructions', 'No instructions available')
            recipes.append(f"{title}: {instructions}")
        return recipes
    else:
        return ["Unable to fetch recipes at the moment. Please try again later."]
        


# Streamlit UI
import streamlit as st

def main():
    st.set_page_config(page_title="Your Cooking Assistant", layout="centered")
    st.title("Your Cooking Assistant")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        predicted_ingredients = get_ingredients(uploaded_file.read())
        recipes = get_recipes(predicted_ingredients)

        st.success("Here are some recipe ideas:")
        for recipe in recipes:
            st.write(recipe)
        st.write(predicted_ingredients)

if __name__ == "__main__":
    main()
