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
st.title("Formulaire Kappa 2")

data[st.session_state["CURRENT_USER"]]["paralysie_sommeil"] = st.radio(
    "Vous est-il déjà arrivé de vous réveiller au milieu de la nuit en ayant l'impression de ne pas pouvoir bouger votre corps et/ou de ne pas pouvoir parler ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["sensibilite_ton_voix"] = st.radio(
    "Lorsque vous étiez enfant, vous sentiez-vous plus affecté(e) par le ton de voix de vos figures parentales que par ce qu’elles disaient réellement ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["empathie_peur"] = st.radio(
    "Si une personne de votre entourage parle d'une peur que vous avez également vécue, avez-vous tendance à ressentir aussi de l’appréhension ou de la peur ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["ressassement_dispute"] = st.radio(
    "Si vous êtes impliqué dans une dispute avec quelqu'un, une fois celle-ci terminée, avez-vous tendance à ressasser ce que vous auriez pu ou dû dire ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["deconnexion_conversation"] = st.radio(
    "Vous arrive-t-il parfois de décrocher lorsque quelqu'un vous parle, au point de ne même plus entendre ce qui a été dit, parce que votre esprit a dérivé vers quelque chose de totalement différent ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["desir_compliments"] = st.radio(
    "Désirez-vous parfois recevoir des compliments pour un travail bien fait, même si vous vous sentez gêné(e) ou mal à l’aise lorsque vous le recevez ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["crainte_conversation_inconnus"] = st.radio(
    "Craignez-vous souvent de ne pas être capable de tenir une conversation avec quelqu’un que vous venez de rencontrer ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["gene_attention_apparence"] = st.radio(
    "Vous sentez-vous mal à l’aise ou gêné(e) lorsque l’attention est portée sur votre corps ou votre apparence physique ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["evitement_enfants"] = st.radio(
    "Si vous aviez le choix, préféreriez-vous éviter d’être entouré(e) d’enfants la plupart du temps ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["maladresse_mouvements_public"] = st.radio(
    "Avez-vous l’impression de ne pas être détendu(e) ou à l’aise dans vos mouvements corporels, surtout en présence de personnes inconnues ou dans des situations inhabituelles ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["preference_non_fiction"] = st.radio(
    "Préférez-vous lire des ouvrages non fictifs plutôt que des œuvres de fiction ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["sensation_amertume"] = st.radio(
    "Lorsque quelqu’un décrit un goût très amer, avez-vous du mal à ressentir cette sensation d’amertume ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["auto_perception_negative"] = st.radio(
    "Avez-vous généralement l’impression de vous percevoir de manière moins favorable que la façon dont les autres vous perçoivent ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["gene_contact_physique_public"] = st.radio(
    "Avez-vous tendance à vous sentir maladroit(e) ou gêné(e) d’initier un contact physique (tenir la main, embrasser, etc.) avec une personne avec qui vous êtes en couple, en présence d'autres personnes ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["gene_questions_public"] = st.radio(
    "Lors d’un cours ou d’une conférence, vous sentez-vous généralement mal à l’aise de poser des questions devant le groupe, même si vous souhaitez des explications supplémentaires ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["gene_regard_direct"] = st.radio(
    "Ressentez-vous une gêne si une personne que vous venez de rencontrer vous regarde directement dans les yeux lorsqu'elle vous parle, surtout si la conversation porte sur vous ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["gene_conversation_groupe"] = st.radio(
    "Dans un groupe de personnes que vous venez de rencontrer, vous sentiriez-vous mal à l’aise d’attirer l’attention sur vous en initiant la conversation ?", ["Oui", "Non"], index=None
)

data[st.session_state["CURRENT_USER"]]["difficulte_exprimer_amour"] = st.radio(
    "Si vous êtes en couple ou très proche de quelqu’un, trouvez-vous difficile ou embarrassant d’exprimer verbalement votre amour pour cette personne ?", ["Oui", "Non"], index=None
)

st.session_state["data"] = data
# Continue and return button, saving the data to server
col1, col2 = st.columns(2)

with col2:
	if st.button("Continuer"):
		client.put_json(st.secrets["webdav"]["remote_path"]  + f"{st.session_state['CURRENT_USER']}.json", data)
		st.switch_page("pages/audiopage.py")

with col1:
	if st.button("Retour"):
		client.put_json(st.secrets["webdav"]["remote_path"]  + f"{st.session_state['CURRENT_USER']}.json", data)
		st.switch_page("pages/kappa1.py")