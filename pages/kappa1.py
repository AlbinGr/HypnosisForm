import streamlit as st
from webdav import WebDAVClient
import hashlib

if "client" not in st.session_state.keys():
	client = WebDAVClient(
		base_url= st.secrets["webdav"]["url"],
		username= st.secrets["webdav"]["email"],
		password= st.secrets["webdav"]["psw"]
	)
	st.session_state["client"] = client
else:
	client = st.session_state["client"]

if "CURRENT_USER" not in st.session_state.keys():
	username = st.text_input("Nom d'utilisateur", key="USERNAME")
	if username:
		m = hashlib.sha256()
		m.update(username.encode())
		username = m.hexdigest()

		# Check if the user exists
		if not client.file_exists(st.secrets["webdav"]["remote_path"] + f"{username}.json"):
			st.error("Nom d'utilisateur inconnu. Retournez à la page d'accueil pour en créer un nouveau si besoin.")
			if st.button("Retour"):
				st.switch_page("app.py")
			st.stop()
		else:
			st.session_state["CURRENT_USER"] = username
			st.rerun()
	else:
		if st.button("Retour"):
			st.switch_page("app.py")
		st.stop()

if "data" not in st.session_state.keys():
	data = client.get_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['CURRENT_USER']}.json")
	st.session_state["data"] = data
else:
	data = st.session_state["data"]


# Here we include the form to collect the data, streamlit display etc...
# Form fields
# Form fields
st.title("Questionnaire de suggestibilité kappasien")

data[st.session_state["CURRENT_USER"]]["somnambulisme_adulte"] = st.radio(
    "Avez-vous été sujet à du somnambulisme depuis que vous avez atteint l’âge adulte ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["aisance_expression_sentiments"] = st.radio(
    "À l’adolescence, vous sentiez-vous à l’aise pour exprimer vos sentiments à l’un ou l’autre de vos figures maternelles ou paternelles ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["contact_visuel_proche"] = st.radio(
    "Avez-vous tendance à regarder directement les personnes dans les yeux et/ou vous approcher d’eux lorsque vous discutez d’un sujet intéressant ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["perception_autrui_critique"] = st.radio(
    "Avez-vous l’impression que la plupart des gens que vous rencontrez pour la première fois ne sont pas critiques à l’égard de votre apparence ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["aisance_conversation_groupe"] = st.radio(
    "Dans un groupe avec des personnes que vous venez de rencontrer, vous sentiriez-vous à l’aise d’attirer l’attention sur vous en lançant la conversation ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["affection_publique"] = st.radio(
    "Vous sentez-vous confortable de tenir la main ou de prendre dans les bras la personne avec qui vous êtes en couple lorsque vous êtes en présence d’autres personnes ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["empathie_chaleur_physique"] = st.radio(
    "Quand quelqu’un parle de se sentir au chaud physiquement, commencez-vous également à ressentir de la chaleur ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["ecoute_attention"] = st.radio(
    "Vous arrive-t-il parfois de ne plus vraiment écouter lorsque quelqu’un vous parle, au point de ne même plus entendre ce que l’autre personne dit, parce que vous êtes anxieux(se) de préparer votre réponse ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["apprentissage_visuel"] = st.radio(
    "Avez-vous l’impression que vous apprenez et comprenez mieux en voyant et/ou en lisant par rapport à lorsque vous l’entendez ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["aisance_questions_public"] = st.radio(
    "Lors d’un nouveau cours ou conférence, vous sentez-vous généralement à l’aise de poser des questions devant le groupe ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["importance_details_expression"] = st.radio(
    "Lorsque vous exprimez vos idées, trouvez-vous important de présenter tous les détails afin que l’autre personne puisse bien comprendre complètement ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["interaction_enfants"] = st.radio(
    "Aimez-vous interagir avec les enfants ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["aisance_mouvements_public"] = st.radio(
    "Trouvez-vous facile d’être à l’aise et détendu(e) dans vos mouvements corporels, même en présence de personnes inconnues ou dans des situations inhabituelles ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["lecture_fiction_preference"] = st.radio(
    "Préférez-vous lire de la fiction plutôt que des ouvrages non fictifs ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["reponse_salive_citron"] = st.radio(
    "Si vous deviez imaginer manger un citron jaune, juteux et acide, votre bouche se mettrait-elle à saliver ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["aisance_reception_compliment"] = st.radio(
    "Si vous estimez mériter un compliment pour quelque chose de bien fait, vous sentez-vous à l’aise de recevoir ce compliment devant d’autres personnes ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["bon_interlocuteur"] = st.radio(
    "Pensez-vous être un bon interlocuteur ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["aisance_attention_flatterie"] = st.radio(
    "Vous sentez-vous à l’aise lorsque l’on attire une attention flatteuse sur votre corps ou votre apparence physique ?", ["Oui", "Non"], index=None
)

st.session_state["data"] = data
# Continue and return button, saving the data to server
col1, col2 = st.columns(2)

with col2:
	if st.button("Continuer"):
		# Check if any of the radio buttons is None
		error = False
		for key, value in data[st.session_state["CURRENT_USER"]].items():
			if value is None:
				st.error("Veuillez répondre à toutes les questions avant de continuer.")
				error = True
				break
		if not error:
			client.put_json(st.secrets["webdav"]["remote_path"]  + f"{st.session_state['CURRENT_USER']}.json", data)
			st.switch_page("pages/kappa2.py")

with col1:
	if st.button("Retour"):
		if data[st.session_state["CURRENT_USER"]]["hypnose_praticien"] == "Oui":
			st.switch_page("pages/hypnose_expert.py")
		elif data[st.session_state["CURRENT_USER"]]["hypnose_patient"] == "Oui":
			st.switch_page("pages/hypnose_patient.py")
		else:
			st.switch_page("pages/formulaire_sd.py")