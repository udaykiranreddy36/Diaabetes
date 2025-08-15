import streamlit as st
import ollama
import base64

# Set page config with a unique title
st.set_page_config(
    page_title="Diabetic ChatBot",  # Set the page title
    layout="wide",  # Use wide layout
    page_icon="🤖"  # Optional: Add an icon
)

# Navigation menu
#st.sidebar.title("Navigation")
#page = st.sidebar.radio("Go to", ["Diabetes Prediction", "Chatbot"])



# Load background image
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("background.png")

# Custom CSS for styling
st.markdown(f"""
    <style>
        .main {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
st.session_state.setdefault('conversation_history', [])

# Function to generate AI response
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(model="llama2", messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']
    except Exception as e:
        st.error(f"Error generating response: {e}")
        ai_response = "Sorry, I couldn't generate a response. Please try again."

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Main app
st.title("Diabetic Chat Bot 🤖")  # Add an emoji for better UI

# Display chat history
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# Use a form to handle text input and submission
with st.form(key="chat_form"):
    user_message = st.text_input("How can I help you today?", key="user_input")
    submit_button = st.form_submit_button("Submit")

# Process the user's message
if submit_button and user_message:
    with st.spinner("Thinking....."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")
elif submit_button and not user_message:
    st.warning("Please enter a message before submitting.")