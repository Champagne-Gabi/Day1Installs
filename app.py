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
    all_questions = [
        {
            "q": "Where does the pressure come from in Cleaver LT?",
            "options": ["TE side", "Opposite TE", "Middle", "Boundary"],
            "answer": "Opposite TE",
            "position": "STAR",
            "image": None
        },
        {
            "q": "In Scissors, what happens if #3 is fast?",
            "options": ["Check Slingshot", "Check Thin", "Play Out", "Trap"],
            "answer": "Check Thin",
            "position": "Free Safety",
            "image": None
        },
        {
            "q": "What’s the DL's job in Shake RT?",
            "options": ["Slant into pressure", "Drop into coverage", "Hold gap", "Slant away from pressure"],
            "answer": "Slant away from pressure",
            "position": "Defensive End",
            "image": None
        },
        {
            "q": "What does STAR do when there's man motion?",
            "options": ["Check Lock", "Play Top Hat", "Call Slingshot", "Blitz"],
            "answer": "Call Slingshot",
            "position": "STAR",
            "image": None
        },
        {
            "q": "How does the defense handle Empty checks?",
            "options": ["Blitz STAR", "Play Out", "Push coverage", "Drop DE"],
            "answer": "Play Out",
            "position": "Mike LB",
            "image": None
        },
        {
            "q": "What’s the role of the boundary corner in Trap?",
            "options": ["Deep third", "Inside leverage", "Flat zone", "Man-to-man"],
            "answer": "Flat zone",
            "position": "Cornerback",
            "image": None
        },
        {
            "q": "In 3x1, what might the STAR be responsible for?",
            "options": ["Wall #2", "Middle third", "Seam-curl-flat", "Blitz"],
            "answer": "Seam-curl-flat",
            "position": "STAR",
            "image": None
        }
    ]

    filtered_questions = [q for q in all_questions if q["position"] == selected_position or selected_position == "General"]

    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.correct = None
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.submitted = False
        st.session_state.answered_questions = []
        st.session_state.do_rerun = False

    # rerun check must happen immediately
    if st.session_state.get("do_rerun"):
        st.session_state.do_rerun = False
        st.experimental_rerun()

    if filtered_questions:
        q = filtered_questions[st.session_state.quiz_index % len(filtered_questions)]
        st.markdown(f"**{q['q']}**")
        if q["image"]:
            st.image(q["image"], width=500)
        choice = st.radio("Choose one:", q["options"], key=st.session_state.quiz_index)

        if not st.session_state.submitted and st.button("Submit Answer"):
            st.session_state.correct = (choice == q["answer"])
            st.session_state.total += 1
            if st.session_state.correct:
                st.session_state.score += 1
            st.session_state.submitted = True
            st.session_state.answered_questions.append({"question": q["q"], "selected": choice, "correct": q["answer"]})

        if st.session_state.submitted:
            if st.session_state.correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect — the correct answer was: {q['answer']}")

            if st.button("Next Question", key="next"):
                st.session_state.quiz_index += 1
                st.session_state.correct = None
                st.session_state.submitted = False
                st.session_state.do_rerun = True

        st.info(f"Score: {st.session_state.score} / {st.session_state.total}")
    else:
        st.warning("No questions available for this position.")




