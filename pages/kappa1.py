import streamlit as st
from webdav import WebDAVClient
from authentification import login, logout

if "client" not in st.session_state.keys():
    client = WebDAVClient(
        base_url= st.secrets["webdav"]["url"],
        username= st.secrets["webdav"]["email"],
        password= st.secrets["webdav"]["psw"]
    )
    st.session_state["client"] = client
else:
    client = st.session_state["client"]



if "current_user" not in st.session_state.keys() or st.session_state["current_user"] is None:
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        login("Login", "pages/kappa1.py")
    with col2:
        if st.button("Return to homepage"):
            st.switch_page("app.py")
    st.stop()

    
logout("Logout", "app.py")


if "data" not in st.session_state.keys() or st.session_state["data"] is None:
    data = st.session_state["client"].get_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['current_user']}.json")
    st.session_state["data"] = data
else:
    data = st.session_state["data"]


# Here we include the form to collect the data, streamlit display etc...
# Form fields
st.title("Formulaire Kappa")

data["somnambulisme_adulte"] = st.radio(
    "Avez-vous été sujet à du somnambulisme depuis que vous avez atteint l’âge adulte ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("somnambulisme_adulte", None)) if data.get("somnambulisme_adulte", None) is not None else None,
    key = "somnambulisme_adulte"
)

data["aisance_expression_sentiments"] = st.radio(
    "A l’adolescence, vous sentiez-vous à l’aise pour exprimer vos sentiments à l’une ou l’autre de vos figures parentales ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("aisance_expression_sentiments", None)) if data.get("aisance_expression_sentiments", None) is not None else None,
    key="aisance_expression_sentiments"
)

data["contact_visuel_proche"] = st.radio(
    "Avez-vous tendance à regarder directement les personnes dans les yeux et/ou vous approcher d’elles lorsque vous discutez d’un sujet intéressant ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("contact_visuel_proche", None)) if data.get("contact_visuel_proche", None) is not None else None,
    key="contact_visuel_proche"
)

data["perception_autrui_critique"] = st.radio(
    "Avez-vous l’impression que la plupart des gens que vous rencontrez pour la première fois ne sont pas critiques à l’égard de votre apparence ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("perception_autrui_critique", None)) if data.get("perception_autrui_critique", None) is not None else None,
    key="perception_autrui_critique"
)

data["aisance_conversation_groupe"] = st.radio(
    "Dans un groupe avec des personnes que vous venez de rencontrer, vous sentez-vous à l’aise d’attirer l’attention sur vous en lançant la conversation ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("aisance_conversation_groupe", None)) if data.get("aisance_conversation_groupe", None) is not None else None,
    key="aisance_conversation_groupe"
)

data["affection_publique"] = st.radio(
    "Vous sentez-vous confortable de tenir la main ou de prendre dans les bras la personne avec qui vous êtes en couple lorsque vous êtes en présence d’autres personnes ?", 
      ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("affection_publique", None)) if data.get("affection_publique", None) is not None else None,
    key="affection_publique"
)

data["empathie_chaleur_physique"] = st.radio(
    "Quand quelqu'un parle de se sentir au chaud physiquement, commencez-vous également à ressentir de la chaleur ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("empathie_chaleur_physique", None)) if data.get("empathie_chaleur_physique", None) is not None else None,
    key="empathie_chaleur_physique"
)

data["ecoute_attention"] = st.radio(
    "Vous arrive-t-il parfois de ne plus vraiment écouter lorsque quelqu’un vous parle, au point de ne même plus entendre ce que l’autre personne dit, parce que vous êtes anxieux(se) de préparer votre réponse ?",
    ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("ecoute_attention", None)) if data.get("ecoute_attention", None) is not None else None,
    key="ecoute_attention"
)

data["apprentissage_visuel"] = st.radio(
    "Avez-vous l’impression que vous apprenez et comprenez mieux en voyant et/ou en lisant que lorsque vous entendez l'information ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("apprentissage_visuel", None)) if data.get("apprentissage_visuel", None) is not None else None,
    key="apprentissage_visuel"
)

data["aisance_questions_public"] = st.radio(
    "Lors d’un nouveau cours ou de conférences, vous sentez-vous généralement à l’aise de poser des questions devant le groupe ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("aisance_questions_public", None)) if data.get("aisance_questions_public", None) is not None else None,
    key="aisance_questions_public"
)

data["importance_details_expression"] = st.radio(
    "Lorsque vous exprimez vos idées, trouvez-vous important de présenter tous les détails afin que l'autre personne puisse comprendre complètement ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("importance_details_expression", None)) if data.get("importance_details_expression", None) is not None else None,
    key="importance_details_expression"
)

data["interaction_enfants"] = st.radio(
    "Aimez-vous interagir avec les enfants ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("interaction_enfants", None)) if data.get("interaction_enfants", None) is not None else None,
    key="interaction_enfants"
)

data["aisance_mouvements_public"] = st.radio(
    "Trouvez-vous facile d’être à l’aise et détendu(e) dans vos mouvements corporels, même en présence de personnes inconnues ou dans des situations inhabituelles ?",
    ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("aisance_mouvements_public", None)) if data.get("aisance_mouvements_public", None) is not None else None,
    key="aisance_mouvements_public"
)

data["lecture_fiction_preference"] = st.radio(
    "Préférez-vous lire de la fiction plutôt que des ouvrages non fictifs ? ", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("lecture_fiction_preference", None)) if data.get("lecture_fiction_preference", None) is not None else None,
    key="lecture_fiction_preference"
)

data["reponse_salive_citron"] = st.radio(
    "Si vous deviez imaginer manger un citron jaune, juteux et acide, votre bouche se mettrait-elle à saliver ?", 
    ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("reponse_salive_citron", None)) if data.get("reponse_salive_citron", None) is not None else None,
    key="reponse_salive_citron"
)

data["aisance_reception_compliment"] = st.radio(
    "Si vous estimez mériter un compliment pour quelque chose de bien fait, vous sentez-vous à l’aise de recevoir ce compliment devant d’autres personnes ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("aisance_reception_compliment", None)) if data.get("aisance_reception_compliment", None) is not None else None,
    key="aisance_reception_compliment"
)

data["bon_interlocuteur"] = st.radio(
    "Pensez-vous être un bon interlocuteur ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("bon_interlocuteur", None)) if data.get("bon_interlocuteur", None) is not None else None,
    key="bon_interlocuteur"
)

data["aisance_attention_flatterie"] = st.radio(
    "Vous sentez-vous à l’aise lorsque l’on attire une attention flatteuse sur votre corps ou votre apparence physique ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("aisance_attention_flatterie", None)) if data.get("aisance_attention_flatterie", None) is not None else None,
    key="aisance_attention_flatterie"
)

# Submit button
st.session_state["data"] = data
# Continue and return button, saving the data to server
col1, col2 = st.columns(2)

with col2:
    if st.button("Continuer"):
        error = False
        for key, value in data.items():
            if value is None or value == "Selection":
                st.error(f"Veuillez remplir le champ: {key}")
                error = True
                break

        if not error:
            st.session_state["client"].put_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['current_user']}.json" , data)
            st.switch_page("pages/kappa2.py")

with col1:
    if st.button("Retour"):
        if data["hypnose_praticien"] == "Oui":
            st.switch_page("pages/hypnose_expert.py")
        else:
            st.switch_page("pages/hypnose_patient.py")