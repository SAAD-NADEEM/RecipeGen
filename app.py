import streamlit as st
from google import genai
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv



if "recipe" not in st.session_state:
    st.session_state.recipe = None


# ------------------------------------------------------------------------ 
# Pydantic Model for Structure Output 
# ------------------------------------------------------------------------

class RecipeFormat(BaseModel):
    ingredients: list[str]
    method: str = Field(description="Step-by-step instructions without extra headings. but i do want sub headings with '##' like what step is being performed and for each sub steps dotn use number instead use bullet points( - )")

# ------------------------------------------------------------------------ 
# OpenAI Structured Response
# ------------------------------------------------------------------------

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def getRecipe(query: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents='Write a detailed recipe for {recipe_name}.',
        config={
        'response_mime_type': 'application/json',
        'response_schema': RecipeFormat,
        },
    )
    return response.parsed






# ------------------------------------------------------------------------ 
# Streamlit full App design
# ------------------------------------------------------------------------

st.set_page_config(page_title="RecipeGen")

# ----------------------------- Header -----------------------------

st.image("https://recipegen-ai.netlify.app/Logo.jpg", width=64)

# ----------------------------- Header -----------------------------
st.divider()


st.markdown(
    """
    <style>
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            background-color: transparent;
            border-radius: 10px;
        }
        .container h1 {
            color: red;
            font-size: 2rem;
            text-align: center; 
        }
        .container p {
            text-align: center;
            font-size: clamp(0.8rem, 1.3vw, 1rem);
            padding: 10px 5px;
        }
    </style>

    <div class="container">
        <h1>Recipe Generator</h1>
        <p>Introducing RecipeGen, the ultimate app for personalized recipes! Simply input your preferences, and our AI-powered engine creates delicious, tailored meal ideas just for you. Powered by OpenAI, your perfect dish is just a tap away!</p>
    </div>
    """,
    unsafe_allow_html=True
)


user_input = st.text_input("", placeholder='"Brownie" or "Aloo Paratha"')
submit = st.button("Generate Recipe")

if submit and user_input:
    st.session_state.recipe = getRecipe(user_input)
    st.session_state.recipe_title = user_input

upload_image = st.file_uploader("Upload An Image For Your Recipe Card", type=["jpg", "png", "jpeg"], key="recipe_image")
if upload_image:
    st.image(upload_image)
    st.markdown("<style> div[data-testid='stFileUploader'] {display: none;} </style>", unsafe_allow_html=True)  # Hide File Upload Metadata


if st.session_state.recipe:
    res = st.session_state.recipe

    st.divider()
    st.header(st.session_state.recipe_title.upper())
    columns = st.columns(3)
    for idx, ingredient in enumerate(res.ingredients):
        with columns[idx % 3]:
            st.write(f"- {ingredient}")
    st.write(res.method)
