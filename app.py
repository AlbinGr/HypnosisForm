import streamlit as st
from authentification import login, logout



st.config.set_option("client.showSidebarNavigation", False)
if "has_rerun" not in st.session_state:
    st.session_state.has_rerun = True
    st.rerun()

st.title("Évaluation de la propension d’induction de l’état de transe hypnotique sur base d’une analyse perceptive d’enregistrements d’hypnothérapeutes")
with st.container(border=True, key=  "consent"):
    st.markdown("### Quel est le but de cette étude et qui la dirige ?")
    st.markdown(""" 
    <div>
           Nous vous demandons de prendre part à une étude de recherche dont l'objectif est d’étudier l’influence de la voix de l’hypnothérapeute dans l’induction de la transe hypnotique. Cette étude est menée par LORENZINI Leila (leila.lorenzini@ulb.be) et LIENARD Alice (alice.lienard@ulb.be) à l'Université Libre de Bruxelles, sous la supervision de la Professeure REMACLE Angélique (Faculté de Psychologie, des Sciences de l’Education et de Logopédie), et fait partie des travaux associés à un mémoire de fin d'études en logopédie. Cette recherche implique de : 
    </div>
    <ol style="padding-left: 20px;">
        <li>compléter deux questionnaires reprenant des informations vous concernant comme votre âge, votre genre, votre éventuelle expérience en hypnose, en méditation, ou en musique ;  </li>
        <li>réaliser une tâche consistant à écouter et donner votre avis concernant des enregistrements d'hypnothérapeutes lisant un texte. La durée totale de votre participation est d’environ une heure. </li>
    </ol>
""", unsafe_allow_html = True)
    
    st.markdown("### Participation et retrait")
    st.write("""
Votre participation à cette recherche est volontaire. Vous pouvez choisir de ne pas participer et si vous décidez de participer vous pouvez cesser de répondre aux questions ou la tâche à tout moment et fermer la fenêtre de votre navigateur sans aucun préjudice. Les investigatrices doivent vous fournir toutes les explications nécessaires concernant cette recherche. Vous avez le droit d’obtenir des réponses à vos questions sur les procédures avant ou après la passation en envoyant un mail à leila.lorenzini@ulb.be ou alice.lienard@ulb.be.
""")
    st.markdown("### Confidentialité et sécurité des données")
    st.write("""
Toutes les données recueillies dans cette étude sont anonymes et seront stockées en toute confidentialité. Ni les chercheurs, ni les tiers n’auront accès à votre identité, qui ne pourra pas être recoupée avec les réponses au questionnaire. Les données issues de votre participation à cette recherche peuvent être transmises dans le cadre d’une autre recherche en relation avec cette étude, et éventuellement compilées dans des bases de données accessibles à la communauté scientifique. Les données que nous partageons ne sont pas identifiables, de telle sorte que personne ne saura quelles données sont les vôtres ni même si vous avez participé.
""")
    st.markdown("### Droits des participant.e.s")
    st.write("""
L’ULB se conforme au Règlement général sur la protection des données (RGPD) et attache une grande importance à la protection de vos données à caractère personnel. Toutes vos questions sur la protection de vos données par l’ULB peuvent être envoyées au Délégué à la protection des données (rgpd@ulb.be).
""")
    st.markdown("### Qui a examiné cette étude ?")
    st.write("""
Cette étude a été évaluée par un Comité d'Ethique indépendant, à savoir le Comité d'Avis Ethique de la Faculté de Psychologie, des Sciences de l'Education et de Logopédie. En aucun cas vous ne devez prendre l'avis favorable du Comité d'Avis Ethique comme une incitation à participer à cette étude.
""")

st.markdown(""" 
    <div>
           En acceptant de cliquer sur le bouton «J'ai lu et compris», vous convenez que : 
    </div>
    <ol style="padding-left: 20px;">
        <li>Vous avez lu et compris les informations fournies ci-dessus  </li>
        <li>Vous consentez à la gestion et au traitement des données acquises telles que décrites ci-dessus  </li>
        <li>Vous avez 18 ans ou plus  </li>
        <li>Vous donnez votre consentement libre et éclairé pour participer à cette recherche</li>
    </ol>
""", unsafe_allow_html = True)

understood = st.checkbox("J'ai lu et compris", value=False)

if "data" in st.session_state.keys():
    del st.session_state.data
if "client" in st.session_state.keys():
    del st.session_state.client
if understood:
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        st.session_state.data = None
        login("Login", "pages/formulaire_sd.py")
    with col2:
        if "current_user" in st.session_state.keys() and st.session_state["current_user"] is not None:
            logout("Logout", "app.py")
        else:
            if st.button("Register"):
                st.session_state.target_page = "pages/formulaire_sd.py"
                st.switch_page("pages/register.py")






