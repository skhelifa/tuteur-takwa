import os
import streamlit as st
from openai import OpenAI

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Tuteur socratique - Toutou", page_icon="🌍", layout="centered"
)

# Titre personnalisé pour Takwa / Toutou
st.title("🎓 Tuteur socratique pour ❤️ ❤️Toutou❤️ ❤️")
st.caption(
    "Ton assistant personnel pour le Collège Louis-Riel (Mathématiques & Sciences humaines)"
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

# --- BARRE LATÉRALE (SIDEBAR) AVEC SÉLECTEUR DE MATIÈRE ---
with st.sidebar:
    st.header("🎯 Choisi ta matière")
    matiere = st.selectbox(
        "Matière active :",
        [
            "Mathématiques (IMAP20S)",
            "Sciences humaines / Géographie (10e année)",
        ],
    )
    
    st.markdown("---")
    
    if matiere == "Mathématiques (IMAP20S)":
        st.header("📐 Espace Visuel GeoGebra")
        st.write("Besoin de tracer un triangle ou de vérifier une pente ? Utilise l'outil ci-dessous.")
        st.markdown("[🌐 Ouvrir GeoGebra dans un nouvel onglet](https://www.geogebra.org/geometry)", unsafe_allow_html=True)
        show_tool = st.checkbox("Afficher la calculatrice graphique GeoGebra", value=False)
    else:
        st.header("🗺️ Ressources Géographiques")
        st.write("Explore les cartes, les biomes et les enjeux mondiaux.")
        st.markdown("[🌐 Atlas du Canada](https://atlas.gc.ca/)", unsafe_allow_html=True)
        st.markdown("[🌐 Google Earth](https://earth.google.com/)", unsafe_allow_html=True)
        show_tool = False

# Instructions système pour les Mathématiques
SYSTEM_PROMPT_MATH = """
Tu agis en tant qu'expert pédagogique en mathématiques et tuteur socratique pour le programme francophone du Manitoba (au Collège Louis-Riel, cours IMAP20S / 10e année). 
Ton rôle est d'aider l'élève à progresser en trigonométrie et dans les concepts de ce niveau en t'appuyant sur les programmes officiels d'Éducation Manitoba.

[MODULE ACTIF : TRIGONOMÉTRIE DU TRIANGLE RECTANGLE ET GÉOMÉTRIE]
- Concepts clés : Théorème de Pythagore ($a^2 + b^2 = c^2$), rapports trigonométriques de base (Sinus, Cosinus, Tangente / SOH-CAH-TOA), pentes, droites et applications (angles d'élévation et de dépression).
- Pédagogie et Rétroaction socratique :
  1. Ne donne jamais la réponse finale directement à l'élève.
  2. Guide-le étape par étape avec des questions stimulantes : aide-le à identifier ce qu'on cherche, à choisir le bon rapport ou théorème, à poser l'équation, puis à isoler l'inconnue.
  3. **Visualisation GeoGebra [V]** : Invite régulièrement l'élève à utiliser l'outil GeoGebra intégré ou à tracer le triangle / le graphique pour visualiser les longueurs, les angles, ou la pente avant de faire les calculs.
  4. **Formatage Mathématique (LaTeX)** : Utilise OBLIGATOIREMENT la syntaxe LaTeX encadrée par des symboles dollar (`$...$` pour l'inline et `$$...$$` pour les blocs) pour tous les symboles, variables et équations mathématiques.
  5. Sois chaleureux, encourageant, clair, pédagogue et réponds toujours en français.
"""

# Instructions système pour la Géographie / Sciences humaines (10e année)
SYSTEM_PROMPT_GEO = """
Tu agis en tant qu'expert pédagogique en sciences humaines et géographie et tuteur socratique pour le programme francophone du Manitoba (au Collège Louis-Riel, 10e année / Secondaire 2 — Cours : Les enjeux géographiques du XXIe siècle).
Ton rôle est d'aider l'élève à explorer la littératie géographique, les enjeux mondiaux et environnementaux en t'appuyant sur les programmes officiels d'Éducation Manitoba.

[MODULE ACTIF : GÉOGRAPHIE & SCIENCES HUMAINES - LITTÉRATIE GÉOGRAPHIQUE ET ENJEUX]
- Concepts clés : Géographie physique et humaine, répartition spatiale, systèmes d'information géographique (SIG), projections cartographiques (Mercator, Robinson, Peters), biomes mondiaux et du Manitoba (forêt boréale, prairie, toundra, etc.), développement durable, gestion responsable de l'environnement, et influence du lieu sur l'identité.
- Pédagogie et Rétroaction socratique :
  1. Ne donne jamais les réponses toutes faites. Pose des questions ouvertes pour amener l'élève à réfléchir de manière critique (pensée critique, perspective géographique, citoyenneté mondiale et environnementale).
  2. Aide l'élève à analyser l'interdépendance entre les humains et leur environnement, ainsi que les impacts des changements et des décisions géographiques au fil du temps.
  3. Encourage l'utilisation d'outils cartographiques (cartes, atlas, repérage spatial) pour illustrer et questionner les représentations du monde.
  4. Valorise la curiosité, la rigueur intellectuelle et la conscience écologique.
  5. Sois chaleureux, encourageant, clair, pédagogue et réponds toujours en français.
"""

# Gestion du changement de matière dans la session state
if "current_matiere" not in st.session_state:
    st.session_state.current_matiere = matiere

if st.session_state.current_matiere != matiere:
    st.session_state.current_matiere = matiere
    if matiere == "Mathématiques (IMAP20S)":
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT_MATH},
            {
                "role": "assistant",
                "content": "Bonjour Toutou ! Je suis ton tuteur socratique pour tes maths au Collège Louis-Riel. Prête pour un nouveau défi en trigonométrie ou géométrie ?",
            },
        ]
    else:
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT_GEO},
            {
                "role": "assistant",
                "content": "Bonjour Toutou ! Bienvenue dans ton espace de Sciences humaines et Géographie (10e année) au Collège Louis-Riel. Es-tu prête à explorer les grands enjeux géographiques de notre planète, la cartographie ou les biomes ?",
            },
        ]

# Initialisation globale de l'historique si inexistant
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT_MATH},
        {
            "role": "assistant",
            "content": "Bonjour Toutou ! Je suis ton tuteur socratique personnel pour tes cours au Collège Louis-Riel. Tu peux choisir ta matière dans le menu latéral (Mathématiques ou Géographie). Par quoi veux-tu commencer ?",
        },
    ]
else:
    # Mettre à jour dynamiquement le prompt système selon la matière active
    st.session_state.messages[0]["content"] = (
        SYSTEM_PROMPT_MATH if matiere == "Mathématiques (IMAP20S)" else SYSTEM_PROMPT_GEO
    )

# Affichage de l'outil GeoGebra si activé en maths
if show_tool and matiere == "Mathématiques (IMAP20S)":
    st.subheader("Interactive - Outil Géométrie / Graphique")
    st.components.v1.iframe("https://www.geogebra.org/geometry?embed", height=450, scrolling=True)
    st.markdown("---")

# Affichage de l'historique des messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Zone de saisie utilisateur
if user_input := st.chat_input("Pose ta question ou réponds ici..."):
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
        Fait sur mesure par ton papa adoré — Parce que ta réussite n'a pas de limites ✨
    </div>
""",
    unsafe_allow_html=True,
)
