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


import os   # importing os for accessing tokens
os.environ["REPLICATE_API_TOKEN"]="r8_HqkPlODUgGWvyCPv46RMYYyzPOb7ejO2KZ03o"  # placing key
import replicate   # importing replicate
def get_recipes(predicted_ingredients):
    i_prompt = f"Suggest recipes using these ingredients: {', '.join(predicted_ingredients)}"
    output_prompt = replicate.run('replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf',
                                  input={"prompt": f"{i_prompt} Assistant:",
                                         "temperature": 1, "top_p": 0.8, "max_length": 200, "repetition_penalty": 1})
    recipes = "".join(output_prompt)
    return recipes


# Streamlit UI
import streamlit as st

def main():
    # Initialize session_state
    if 'predicted_ingredients' not in st.session_state:
        st.session_state.predicted_ingredients = []
    if 'recipes' not in st.session_state:
        st.session_state.recipes = ""

    st.set_page_config(page_title="Your Cooking Assistant", page_icon="🍳", layout="centered", initial_sidebar_state="collapsed")
    st.title("Your Cooking Assistant")
    
    # Check if an image has been uploaded
    uploaded_file = st.file_uploader("Upload the Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
       predicted_ingredients = get_ingredients(uploaded_file.read())
        
    if st.button("Get Recipes"):
            recipes = get_recipes(predicted_ingredients)
            st.success("Here are some recipe ideas:")
            st.write(recipes)
            # st.write(predicted_ingredients)

if __name__ == "__main__":
    main()
