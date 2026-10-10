import streamlit as st
from openai import OpenAI

# Titre personnalisé pour Takwa
st.title("🧮 Tuteur socratique pour ❤️ ❤️Toutou❤️ ❤️")
st.caption("Ton assistant personnel pour les maths au Collège Louis-Riel (IMAP20S)")

# Récupération sécurisée de la clé API (configurée dans Streamlit Cloud)
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    # Option de secours si la clé n'est pas dans les Secrets
    with st.sidebar:
        api_key = st.text_input("Clé API OpenAI", type="password")

if not api_key:
    st.info("👋 Bienvenue Takwa ! Le tuteur est en cours de préparation...")
else:
    client = OpenAI(api_key=api_key)

    # Le Prompt Système (L'ADN socratique pour Takwa)
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "system",
            "content": (
                "Tu es un tuteur pédagogique bienveillant, expert du programme de mathématiques "
                "de 10e année (IMAP20S) de la Division scolaire franco-manitobaine au Manitoba. "
                "Tu t'adresses à Takwa (surnommée Toutou). Ton rôle n'est jamais de lui donner la réponse "
                "finale ou de faire les calculs à sa place, mais de la guider pas à pas par la méthode "
                "socratique : pose des questions ouvertes, vérifie ses étapes de calcul, félicite ses efforts "
                "et utilise le vocabulaire officiel enseigné au Manitoba."
            )
        }]

    # Affichage des messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Zone de question
    if prompt := st.chat_input("Pose ta question sur ton devoir de maths..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
