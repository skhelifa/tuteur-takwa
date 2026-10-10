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

# Récupération de la clé API OpenAI depuis les secrets Streamlit
api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error(
        "⚠️ La clé API OpenAI est introuvable. Veuillez l'ajouter dans les secrets de votre application Streamlit."
    )
    st.stop()

# Initialisation du client OpenAI
client = OpenAI(api_key=api_key)

# Instructions système (System Prompt) enrichies avec le formatage LaTeX
SYSTEM_PROMPT = """
Tu agis en tant qu'expert pédagogique en mathématiques et tuteur socratique pour le programme francophone du Manitoba (au Collège Louis-Riel, cours IMAP20S / 10e année). 
Ton rôle est d'aider l'élève à progresser en trigonométrie et dans les concepts de ce niveau en t'appuyant sur les programmes officiels d'Éducation Manitoba.

[MODULE ACTIF : TRIGONOMÉTRIE DU TRIANGLE RECTANGLE ET GÉOMÉTRIE]
- Concepts clés : Théorème de Pythagore ($a^2 + b^2 = c^2$), rapports trigonométriques de base (Sinus, Cosinus, Tangente / SOH-CAH-TOA), pentes, droites et applications (angles d'élévation et de dépression).
- Pédagogie et Rétroaction socratique :
  1. Ne donne jamais la réponse finale directement à l'élève.
  2. Guide-le étape par étape avec des questions stimulantes : aide-le à identifier ce qu'on cherche, à choisir le bon rapport ou théorème, à poser l'équation, puis à isoler l'inconnue.
  3. **Visualisation GeoGebra [V]** : Invite régulièrement l'élève à utiliser l'outil GeoGebra intégré dans l'application ou à tracer le triangle / le graphique pour visualiser les longueurs, les angles, ou la pente avant de faire les calculs.
  4. **Formatage Mathématique (LaTeX)** : Utilise OBLIGATOIREMENT la syntaxe LaTeX encadrée par des symboles dollar (`$...$` pour l'inline et `$$...$$` pour les blocs) pour tous les symboles, variables et équations mathématiques (ex: $\\theta$, $\\sin(\\theta)$, $\\frac{a}{c}$, $a^2 + b^2 = c^2$). N'écris jamais de formules ou de symboles en texte brut ou avec des antislashs non entourés de `$`.
  5. Sois chaleureux, encourageant, clair, pédagogue et réponds toujours en français.
"""

# --- BARRE LATÉRALE (SIDEBAR) AVEC GEOGEBRA ---
with st.sidebar:
    st.header("📐 Espace Visuel GeoGebra")
    st.write("Besoin de tracer un triangle ou de vérifier une pente ? Utilise l'outil ci-dessous ou ouvre GeoGebra en grand.")
    
    # Lien direct vers GeoGebra
    st.markdown("[🌐 Ouvrir GeoGebra dans un nouvel onglet](https://www.geogebra.org/geometry)", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Option pour afficher un outil GeoGebra directement dans la page (Mode compact)
    show_geogebra = st.checkbox("Afficher la calculatrice graphique GeoGebra", value=False)

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": "Bonjour Toutou ! Je suis ton tuteur socratique personnel pour tes maths au Collège Louis-Riel. Aujourd'hui, nous allons travailler sur la **trigonométrie** et la géométrie. Tu peux utiliser le panneau GeoGebra dans le menu latéral si tu as besoin de tracer des figures. Veux-tu qu'on commence par un problème sur les rapports trigonométriques (SOH-CAH-TOA) ou sur le théorème de Pythagore ?",
        },
    ]

# Si l'option GeoGebra est activée par l'élève, on l'affiche proprement au-dessus ou à côté du chat
if show_geogebra:
    st.subheader("Interactive - Outil Géométrie / Graphique")
    st.components.v1.iframe("https://www.geogebra.org/geometry?embed", height=450, scrolling=True)
    st.markdown("---")

# Affichage de l'historique
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
                st.error(f"Une erreur est survenue : {e}")

# --- SIGNATURE DU PAPA ---
st.markdown(
    """
    <hr style="margin-top: 50px; margin-bottom: 10px; border: 0; border-top: 1px solid #eaeaea;">
    <div style="text-align: right; font-size: 0.85em; color: #888888; font-style: italic;">
        Fait sur mesure par ton papa adoré — Parce que tu vaux l'infini ✨
    </div>
""",
    unsafe_allow_html=True,
)
