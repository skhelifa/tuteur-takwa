import os
import streamlit as st
from openai import OpenAI

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Tuteur socratique - Toutou", page_icon="🧮", layout="centered"
)

# Titre personnalisé pour Takwa / Toutou
st.title("🧮 Tuteur socratique pour ❤️ ❤️Toutou❤️ ❤️")
st.caption(
    "Ton assistant personnel pour les maths au Collège Louis-Riel (IMAP20S)"
)

# Initialisation du client OpenAI (récupère la clé depuis les secrets Streamlit ou l'environnement)
api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error(
        "⚠️ La clé API OpenAI est introuvable. Veuillez l'ajouter dans les secrets de votre application Streamlit."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# Instructions système (System Prompt) intégrant le Collège Louis-Riel et la trigonométrie
SYSTEM_PROMPT = """
Tu agis en tant qu'expert pédagogique en mathématiques et tuteur socratique pour le programme francophone du Manitoba (au Collège Louis-Riel, cours IMAP20S / 10e année). 
Ton rôle est d'aider l'élève à progresser en trigonométrie et dans les concepts de ce niveau en t'appuyant sur les programmes officiels d'Éducation Manitoba.

[MODULE ACTIF : TRIGONOMÉTRIE DU TRIANGLE RECTANGLE]
- Concepts clés : Théorème de Pythagore (a² + b² = c²), rapports trigonométriques de base (Sinus, Cosinus, Tangente / SOH-CAH-TOA), et applications (angles d'élévation et de dépression).
- Pédagogie et Rétroaction socratique :
  1. Ne donne jamais la réponse finale directement à l'élève.
  2. Guide-le étape par étape avec des questions stimulantes : aide-le à identifier ce qu'on cherche, à choisir le bon rapport ou théorème, à poser l'équation, puis à isoler l'inconnue.
  3. Intègre les processus mathématiques du Manitoba (Visualisation [V], Résolution de problèmes [RP], Raisonnement [R]).
  4. Sois chaleureux, encourageant, clair, pédagogue et réponds toujours en français.
"""

# Initialisation de l'historique des messages dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": "Bonjour Toutou ! Je suis ton tuteur socratique personnel pour tes maths au Collège Louis-Riel. Aujourd'hui, nous allons travailler sur la **trigonométrie**. Veux-tu qu'on commence par un problème sur les rapports trigonométriques (SOH-CAH-TOA), le théorème de Pythagore, ou sur les angles d'élévation ?",
        },
    ]

# Affichage de l'historique des messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Zone de saisie utilisateur
if user_input := st.chat_input(
    "Pose ta question ou réponds au problème ici..."
):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                assistant_reply = response.choices[0].message.content
                st.markdown(assistant_reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_reply}
                )
            except Exception as e:
                st.error(f"Une erreur est survenue lors de la communication avec l'IA : {e}")
