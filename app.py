import streamlit as st
import openai
import random

st.set_page_config(page_title="Day 1 Playbook Assistant", layout="wide")

st.title("🏈 Day 1 Defensive Playbook Assistant")
st.subheader("Ask anything about Day 1 install – alignments, assignments, or adjustments")

# Load OpenAI API key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Position selection
positions = ["General", "STAR", "Cornerback", "Free Safety", "Strong Safety", "Mike LB", "Will LB", "Defensive End", "Defensive Tackle"]
selected_position = st.selectbox("👤 Select your position (optional):", positions)

# Toggle between assistant and quiz mode
mode = st.radio("Select Mode:", ["Ask the Assistant", "Quiz Me"], horizontal=True)

# Define expanded chunks from playbook
playbook_chunks = [
    {
        "title": "DL Contain Rules",
        "tags": ["defensive line", "contain", "rules"],
        "content": "Contain rules for DEs: play wide 5 or 9-tech. Maintain outside leverage unless inside stunt is tagged. DE must recognize boot, naked, or orbit motion."
    }
]

if mode == "Ask the Assistant":
    user_question = st.text_input("🗣️ Ask a question about the install (e.g. 'What does STAR do in Scissors?')")

    if user_question:
        matches = []
        for chunk in playbook_chunks:
            if any(word in user_question.lower() for word in chunk['title'].lower().split() + chunk['tags']):
                matches.append(chunk["content"])

        if not matches:
            matches = [chunk["content"] for chunk in playbook_chunks[:2]]  # fallback

        position_context = f"You are responding to a {selected_position} player. " if selected_position != "General" else ""
        prompt = f"""
        You are a defensive football coach helping players understand a Day 1 playbook install.
        {position_context}Based on the following notes:
        {chr(10).join(matches)}
        Answer this player question clearly and concisely:
        {user_question}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a defensive football coach assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif mode == "Quiz Me":
    questions = [
        {
            "q": "Where does the pressure come from in Cleaver LT?",
            "options": ["TE side", "Opposite TE", "Middle", "Boundary"],
            "answer": "Opposite TE"
        },
        {
            "q": "In Scissors, what happens if #3 is fast?",
            "options": ["Check Slingshot", "Check Thin", "Play Out", "Trap"],
            "answer": "Check Thin"
        },
        {
            "q": "What’s the DL's job in Shake RT?",
            "options": ["Slant into pressure", "Drop into coverage", "Hold gap", "Slant away from pressure"],
            "answer": "Slant away from pressure"
        }
    ]

    q = random.choice(questions)
    st.markdown(f"**{q['q']}**")
    choice = st.radio("Choose one:", q["options"], key=q['q'])

    if st.button("Submit Answer"):
        if choice == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect — the correct answer was: {q['answer']}")
