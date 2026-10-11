import os
import streamlit as st
from openai import OpenAI

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Tuteur socratique - Toutou", page_icon="🇨🇦", layout="centered"
)

# Titre personnalisé pour Takwa / Toutou
st.title("🎓 Tuteur socratique pour ❤️ ❤️Toutou❤️ ❤️")
st.caption(
    "Ton assistant personnel pour le Collège Louis-Riel (Mathématiques, Géographie & Histoire du Canada)"
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

# --- BARRE LATÉRALE (SIDEBAR) AVEC SÉLECTEUR DE MATIÈRE & MICROPHONE ---
with st.sidebar:
    st.header("🎯 Choisi ta matière")
    matiere = st.selectbox(
        "Matière active :",
        [
            "Mathématiques (IMAP20S)",
            "Sciences humaines / Géographie (10e année)",
            "Histoire du Canada (11e année)",
        ],
    )
    
    st.markdown("---")
    
    # Section Microphone pour Toutou
    st.header("🎤 Mode Vocal")
    st.write("Fainéante de taper ? Clique sur le micro pour parler à ton tuteur :")
    audio_value = st.audio_input("Enregistre ta voix")
    
    st.markdown("---")
    
    if matiere == "Mathématiques (IMAP20S)":
        st.header("📐 Espace Visuel GeoGebra")
        st.write("Besoin de tracer un triangle ou de vérifier une pente ? Utilise l'outil ci-dessous.")
        st.markdown("[🌐 Ouvrir GeoGebra dans un nouvel onglet](https://www.geogebra.org/geometry)", unsafe_allow_html=True)
        show_tool = st.checkbox("Afficher la calculatrice graphique GeoGebra", value=False)
    elif matiere == "Sciences humaines / Géographie (10e année)":
        st.header("🗺️ Ressources Géographiques")
        st.write("Explore les cartes, les biomes et les enjeux mondiaux.")
        st.markdown("[🌐 Atlas du Canada](https://atlas.gc.ca/)", unsafe_allow_html=True)
        st.markdown("[🌐 Google Earth](https://earth.google.com/)", unsafe_allow_html=True)
        show_tool = False
    else:
        st.header("📜 Ressources Historiques")
        st.write("Explore l'histoire canadienne, la pensée historique et les sources primaires.")
        st.markdown("[🌐 Projet de la pensée historique](https://historicalthinking.ca/fr)", unsafe_allow_html=True)
        st.markdown("[🌐 Musée virtuel de la Nouvelle-France](https://www.historymuseum.ca/virtual-museum-of-new-france/)", unsafe_allow_html=True)
        st.markdown("[🌐 Centre du patrimoine (SHSB)](https://shsb.mb.ca/)", unsafe_allow_html=True)
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

# Instructions système pour l'Histoire du Canada (11e année)
SYSTEM_PROMPT_HISTO = """
Tu agis en tant qu'expert pédagogique en histoire et tuteur socratique pour le programme francophone du Manitoba (au Collège Louis-Riel, cours Histoire du Canada 11e année / Document de mise en œuvre 2012).
Ton rôle est d'aider l'élève à développer sa pensée historique, sa littératie critique et sa compréhension de l'histoire canadienne en t'appuyant sur les programmes officiels d'Éducation Manitoba.

[MODULE ACTIF : HISTOIRE DU CANADA - 11e ANNÉE]
- Question centrale directrice : "Comment le Canada d'aujourd'hui a-t-il été façonné par son histoire ?"
- Les 6 concepts fondamentaux de la pensée historique à mobiliser[cite: 424, 471] :
  1. Établir l'importance historique [IH] (impact à long terme, caractère révélateur).
  2. Utiliser des preuves découlant de sources primaires [P] (analyser les traces, contextualiser).
  3. Dégager la continuité et le changement [C+C] (évolution, permanences, progrès et déclin).
  4. Analyser les causes et les conséquences [CC] (motivations humaines, contraintes, effets inattendus).
  5. Adopter une perspective historique [PH] (comprendre le contexte d'époque, éviter le présentisme).
  6. Considérer la dimension éthique de l'histoire [DÉ] (jugements éclairés et répercussions morales).
- Les 5 regroupements chronologiques du cours[cite: 447] :
  1. Les Premiers Peuples et la Nouvelle-France (avant 1763)
  2. L'Amérique du Nord britannique (1763-1867)
  3. Devenir une nation souveraine (1867-1931)
  4. Réalisations et défis (1931-1982)
  5. Définir le Canada contemporain (1982 à aujourd'hui)
- Pédagogie et Rétroaction socratique :
  1. Ne donne jamais la réponse finale directement. Guide l'élève pas à pas avec des questions stimulantes.
  2. Encourage l'élève à analyser les sources primaires, à examiner la structure tripartite de l'histoire canadienne (autochtone, francophone, anglophone)[cite: 435] et à confronter les points de vue.
  3. Sois chaleureux, encourageant, clair, pédagogue et réponds toujours en français.
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
    elif matiere == "Sciences humaines / Géographie (10e année)":
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT_GEO},
            {
                "role": "assistant",
                "content": "Bonjour Toutou ! Bienvenue dans ton espace de Sciences humaines et Géographie (10e année) au Collège Louis-Riel. Es-tu prête à explorer les grands enjeux géographiques de notre planète, la cartographie ou les biomes ?",
            },
        ]
    else:
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT_HISTO},
            {
                "role": "assistant",
                "content": "Bonjour Toutou ! Bienvenue dans ton espace d'Histoire du Canada (11e année) au Collège Louis-Riel. Es-tu prête à explorer l'histoire de notre pays à travers la pensée historique, de la Nouvelle-France jusqu'à nos jours ?",
            },
        ]

# Initialisation globale de l'historique si inexistant
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT_MATH},
        {
            "role": "assistant",
            "content": "Bonjour Toutou ! Je suis ton tuteur socratique personnel pour tes cours au Collège Louis-Riel. Tu peux choisir ta matière dans le menu latéral (Mathématiques, Géographie ou Histoire du Canada). Par quoi veux-tu commencer ?",
        },
    ]
else:
    # Mettre à jour dynamiquement le prompt système selon la matière active
    if matiere == "Mathématiques (IMAP20S)":
        current_prompt = SYSTEM_PROMPT_MATH
    elif matiere == "Sciences humaines / Géographie (10e année)":
        current_prompt = SYSTEM_PROMPT_GEO
    else:
        current_prompt = SYSTEM_PROMPT_HISTO
    st.session_state.messages[0]["content"] = current_prompt

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

# Gestion de l'entrée utilisateur : soit par le micro (sidebar), soit par le champ texte
user_input = None

if audio_value is not None:
    with st.spinner("Transcription de ta voix en cours..."):
        try:
            # Appel à l'API Whisper d'OpenAI pour transcrire l'audio enregistré
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_value
            )
            user_input = transcript.text
        except Exception as e:
            st.error(f"Erreur lors de la transcription audio : {e}")

# Saisie texte classique en bas
chat_input = st.chat_input("Pose ta question, réponds ici ou utilise le micro...")
if chat_input:
    user_input = chat_input

# Si un message a été capté (par texte ou par micro)
if user_input:
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
