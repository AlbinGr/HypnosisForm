import streamlit as st
from webdav import WebDAVClient
import hashlib

if "CURRENT_USER" not in st.session_state.keys():
	m = hashlib.sha256()
	m.update(st.experimental_user.email.encode())
	st.session_state["CURRENT_USER"] = m.hexdigest()

	client = WebDAVClient(
		base_url=st.secrets["webdav"]["url"],
		username=st.secrets["webdav"]["email"],
		password=st.secrets["webdav"]["psw"]
	)

	data = client.get_json(st.secrets["webdav"]["remote_path"])
if not st.session_state["CURRENT_USER"] in data.keys():
	# Create new user entry
	data[st.session_state["CURRENT_USER"]] = {}
	client.put_json(st.secrets["webdav"]["remote_path"], data)

# Here we include the form to collect the data, streamlit display etc...
# Form fields
st.title("Formulaire Kappa")

data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_a_lecole_primaire"] = st.radio(
	"Avez-vous été victime d'intimidation à l'école primaire ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_a_lecole_primaire", "Non"))
)
data[st.session_state["CURRENT_USER"]]["aLadolescence_avezvous_ete_victime_dintimidation"] = st.radio(
	"A l'adolescence, avez-vous été victime d'intimidation ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("aLadolescence_avezvous_ete_victime_dintimidation", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_au_travail"] = st.radio(
	"Avez-vous été victime d'intimidation au travail ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_au_travail", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousLimpression_que_lintimidation_a_affecte_votre_vie"] = st.radio(
	"Avez-vous l'impression que l'intimidation a affecté votre vie ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousLimpression_que_lintimidation_a_affecte_votre_vie", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_votre_quartier"] = st.radio(
	"Avez-vous été victime d'intimidation dans votre quartier ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_votre_quartier", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_sur_les_reseaux_sociaux"] = st.radio(
	"Avez-vous été victime d'intimidation sur les réseaux sociaux ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_sur_les_reseaux_sociaux", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_club_ou_une_organisation"] = st.radio(
	"Avez-vous été victime d'intimidation dans un club ou une organisation ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_club_ou_une_organisation", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_une_relation_amoureuse"] = st.radio(
	"Avez-vous été victime d'intimidation dans une relation amoureuse ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_une_relation_amoureuse", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousLimpression_que_lintimidation_a_affecte_votre_sante_mentale"] = st.radio(
	"Avez-vous l'impression que l'intimidation a affecté votre santé mentale ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousLimpression_que_lintimidation_a_affecte_votre_sante_mentale", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_par_un_membre_de_votre_famille"] = st.radio(
	"Avez-vous été victime d'intimidation par un membre de votre famille ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_par_un_membre_de_votre_famille", "Non"))
)
data[st.session_state["CURRENT_USER"]]["lorsqueVous_etes_victime_dintimidation_comment_reagissezvous"] = st.radio(
	"Lorsque vous êtes victime d'intimidation, comment réagissez-vous ?", ["Je me défends", "Je me tais", "Je demande de l'aide"], 
	index=["Je me défends", "Je me tais", "Je demande de l'aide"].index(data[st.session_state["CURRENT_USER"]].get("lorsqueVous_etes_victime_dintimidation_comment_reagissezvous", "Je me tais"))
)
data[st.session_state["CURRENT_USER"]]["aimezvous_interagir_avec_les_autres"] = st.radio(
	"Aimez-vous interagir avec les autres ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("aimezvous_interagir_avec_les_autres", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_en_ligne"] = st.radio(
	"Avez-vous été victime d'intimidation en ligne ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_en_ligne", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_lieu_public"] = st.radio(
	"Avez-vous été victime d'intimidation dans un lieu public ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_lieu_public", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_par_un_inconnu"] = st.radio(
	"Avez-vous été victime d'intimidation par un inconnu ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_par_un_inconnu", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_par_un_collegue"] = st.radio(
	"Avez-vous été victime d'intimidation par un collègue ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_par_un_collegue", "Non"))
)
data[st.session_state["CURRENT_USER"]]["pensezvous_etre_une_personne_intimidante"] = st.radio(
	"Pensez-vous être une personne intimidante ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("pensezvous_etre_une_personne_intimidante", "Non"))
)
data[st.session_state["CURRENT_USER"]]["vousSentez_vous_en_securite_dans_votre_environnement_actuel"] = st.radio(
	"Vous sentez-vous en sécurité dans votre environnement actuel ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("vousSentez_vous_en_securite_dans_votre_environnement_actuel", "Non"))
)

# Continue and return button, saving the data to server
col1, col2 = st.columns(2)

with col2:
	if st.button("Continuer"):
		client.put_json(st.secrets["webdav"]["remote_path"], data)
		st.switch_page("pages/kappa2.py")

with col1:
	if st.button("Retour"):
		if data[st.session_state["CURRENT_USER"]]["hypnose_praticien"] == "Oui":
			st.switch_page("pages/hypnose_expert.py")
		elif data[st.session_state["CURRENT_USER"]]["hypnose_patient"] == "Oui":
			st.switch_page("pages/hypnose_patient.py")
		else:
			st.switch_page("pages/formulaire_sd.py")