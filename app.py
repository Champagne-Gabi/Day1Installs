import streamlit as st
import openai

st.set_page_config(page_title="Day 1 Playbook Assistant", layout="wide")

st.title("🏈 Day 1 Defensive Playbook Assistant")
st.subheader("Ask anything about Day 1 install – alignments, assignments, or adjustments")

# Load OpenAI API key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Define expanded chunks from playbook
playbook_chunks = [
    {
        "title": "Cleaver LT",
        "tags": ["pressure", "nickel", "fire zone"],
        "content": "'Cleaver LT' is a Day 1 nickel pressure. Pressure comes from the left (opposite the TE). DL does not drop. STAR blitzes off edge. Fire zone coverage behind it."
    },
    {
        "title": "Scissors",
        "tags": ["mint front", "fire zone"],
        "content": "'Scissors' is a one-word fire zone pressure from a Mint front. No DL drops. STAR blitzes. If #3 is fast, check THIN. DBs rotate into fire zone shell with curl/flat, hook 3, and MOF."
    },
    {
        "title": "STAR Motion Rules",
        "tags": ["motion", "adjustments"],
        "content": "If STAR gets man motion, we check 'SLINGSHOT'. STAR tracks the motion across. In stacks, use FIRE CALLS like Tophat, Lock, or Push."
    },
    {
        "title": "Empty Checks",
        "tags": ["empty", "adjustments"],
        "content": "If the offense motions to Empty, the check is 'PLAY OUT'. Pressure is canceled. STAR becomes curl/flat or hook. MOF safety rotates."
    },
    {
        "title": "Shake LT",
        "tags": ["pressure", "boundary", "fire zone"],
        "content": "'Shake LT' is a pressure from the boundary side. STAR typically drops while the pressure comes from inside. The DL slants away from pressure. Fire zone principles apply with 3 under, 3 deep behind it."
    },
    {
        "title": "MULE Check",
        "tags": ["motion", "formation", "adjustment"],
        "content": "'MULE' is a check used when motion brings a TE or WR into a tight split near the box. It triggers a shift from nickel to a base alignment. STAR may bump out and safety spins down based on call."
    },
    {
        "title": "Red Zone Fire Zone",
        "tags": ["red zone", "pressure", "coverage"],
        "content": "In the red zone, fire zone pressures tighten. STAR or boundary corner may become primary flat defenders. Deep zones condense, and reads become quicker. Communication is critical pre-snap."
    },
    {
        "title": "3x1 Checks",
        "tags": ["coverage", "adjustments", "3x1"],
        "content": "Against 3x1 formations, safeties communicate and decide on MOF integrity. Typical check involves pushing coverage or rotating a safety down. STAR may play wall 3 or seam-curl-flat depending on coverage."
    }
]

# Simple retrieval + GPT wrapper
user_question = st.text_input("🗣️ Ask a question about the install (e.g. 'What does STAR do in Scissors?')")

if user_question:
    # Find relevant chunks
    matches = []
    for chunk in playbook_chunks:
        if any(word in user_question.lower() for word in chunk['title'].lower().split() + chunk['tags']):
            matches.append(chunk["content"])

    if not matches:
        matches = [chunk["content"] for chunk in playbook_chunks[:2]]  # fallback

    # Build prompt
    prompt = f"""
    You are a defensive football coach helping players understand a Day 1 playbook install.
    Based on the following notes:
    {chr(10).join(matches)}
    Answer this player question clearly and concisely:
    {user_question}
    """

    # GPT completion (new API format)
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

