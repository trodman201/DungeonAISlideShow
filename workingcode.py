import streamlit as st 
import openai
from openai import OpenAI
import random

# Set your OpenAI API key here
OPENAI_API_KEY = " "

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate AI Dungeon prompt
def generate_ai_dungeon_prompt(prompt):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500,
            n=1,
            stop=None
        )
        generated_text = response.choices[0].text.strip()
        return generated_text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to generate image from description
def generate_image_from_description(description):
    try:
        response = client.images.generate( 
            model='dall-e-2',
            prompt=description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None 

# Main function
def main():
    st.title("AI Storyteller")

    # AI Dungeon story generation
    st.subheader("AI Dungeon Story Generation")
    user_input = st.text_area("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        return
    prompts = [
        "You find yourself in a dark cave. ",
        "In front of you, there is a mysterious door. ",
        "A dragon appears on the horizon. ",
        "You are standing in a bustling marketplace. "
    ]
    random_prompt = random.choice(prompts)
    full_prompt = f"You are in a fantasy world. {user_input}\nAI: {random_prompt}"
    ai_response = generate_ai_dungeon_prompt(full_prompt)

    # Generate image from the AI Dungeon response
    if ai_response:
        st.write(f"AI: {ai_response}")
        image_url = generate_image_from_description(ai_response)
        if image_url:
            st.image(image_url, caption="Image generated from the AI Dungeon story", use_column_width=True)
        else:
            st.error("Failed to generate image.")
    else:
        st.error("Failed to generate AI Dungeon response.")

    # Star rating
    st.subheader("Rate This App")
    rating = st.slider("Rate this app:", min_value=0, max_value=5, step=1, value=0)
    st.write("You rated the app:", rating, "stars")

if __name__ == "__main__":
    main()



