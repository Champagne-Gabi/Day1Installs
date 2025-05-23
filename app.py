import streamlit as st
import random

st.set_page_config(page_title="Day 1 Playbook Assistant", layout="wide")

st.title("🏈 Day 1 Playbook Assistant")
st.subheader("Ask about your install, assignments, or quiz yourself")

# Sample knowledge base (simplified for demo)
knowledge_base = {
    "cleaver lt": "'Cleaver LT' is a nickel pressure call. LT means the pressure is coming from the left — opposite the tight end. DL does not drop; it's a fire zone structure.",
    "scissors": "'Scissors' is a one-word fire zone pressure from a Mint front. DL stays in, STAR often pressures. If #3 is fast, play THIN.",
    "star motion": "If STAR is in motion, check for SLINGSHOT adjustment. Realign based on motion rules and formation shifts.",
    "empty": "Empty checks you out of most pressures. 'PLAY OUT' = drop into coverage, STAR becomes curl/flat or hook defender."
}

# Chat interface
user_question = st.text_input("🗣️ Ask me anything from the Day 1 install:")

if user_question:
    key = user_question.lower().strip()
    matched = None
    for k in knowledge_base:
        if k in key:
            matched = k
            break
    if matched:
        st.success(knowledge_base[matched])
    else:
        st.warning("I don't know that one yet — ask about another Day 1 term like 'Cleaver LT' or 'Scissors'.")

# Quiz mode
with st.expander("🎯 Quiz Yourself", expanded=False):
    questions = [
        {
            "q": "Where does pressure come from in Cleaver LT?",
            "options": ["TE side", "Opposite TE", "Middle", "Off-ball LB"],
            "answer": "Opposite TE"
        },
        {
            "q": "What is the STAR's role in Scissors?",
            "options": ["Deep 1/3", "Blitz", "Play MOF", "Drop to weak hook"],
            "answer": "Blitz"
        },
        {
            "q": "What’s the empty check in most pressure calls?",
            "options": ["Check Flood", "Stay Blitz", "Play Out", "Banjo"],
            "answer": "Play Out"
        }
    ]

    q = random.choice(questions)
    st.markdown(f"**{q['q']}**")
    choice = st.radio("Choose one:", q["options"], key=q['q'])

    if st.button("Submit Answer"):
        if choice == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Not quite — the correct answer was: {q['answer']}")
