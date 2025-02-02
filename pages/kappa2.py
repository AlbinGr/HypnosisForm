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
st.title("Formulaire Kappa 2")

data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_votre_famille"] = st.radio(
	"Avez-vous été victime d'intimidation dans votre famille ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_votre_famille", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_par_vos_amis"] = st.radio(
	"Avez-vous été victime d'intimidation par vos amis ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_par_vos_amis", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_votre_communauté"] = st.radio(
	"Avez-vous été victime d'intimidation dans votre communauté ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_votre_communauté", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_par_un_superieur"] = st.radio(
	"Avez-vous été victime d'intimidation par un supérieur ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_par_un_superieur", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_une_activité_sportive"] = st.radio(
	"Avez-vous été victime d'intimidation dans une activité sportive ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_une_activité_sportive", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_lieu_de_loisir"] = st.radio(
	"Avez-vous été victime d'intimidation dans un lieu de loisir ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_lieu_de_loisir", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_par_un_inconnu_dans_la_rue"] = st.radio(
	"Avez-vous été victime d'intimidation par un inconnu dans la rue ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_par_un_inconnu_dans_la_rue", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_transport_public"] = st.radio(
	"Avez-vous été victime d'intimidation dans un transport public ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_transport_public", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_magasin"] = st.radio(
	"Avez-vous été victime d'intimidation dans un magasin ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_magasin", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_restaurant"] = st.radio(
	"Avez-vous été victime d'intimidation dans un restaurant ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_restaurant", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_bar"] = st.radio(
	"Avez-vous été victime d'intimidation dans un bar ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_bar", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_centre_commercial"] = st.radio(
	"Avez-vous été victime d'intimidation dans un centre commercial ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_centre_commercial", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_parc"] = st.radio(
	"Avez-vous été victime d'intimidation dans un parc ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_parc", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_lieu_de_culte"] = st.radio(
	"Avez-vous été victime d'intimidation dans un lieu de culte ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_lieu_de_culte", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_hopital"] = st.radio(
	"Avez-vous été victime d'intimidation dans un hôpital ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_hopital", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_lieu_de_travail"] = st.radio(
	"Avez-vous été victime d'intimidation dans un lieu de travail ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_lieu_de_travail", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_lieu_public"] = st.radio(
	"Avez-vous été victime d'intimidation dans un lieu public ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_lieu_public", "Non"))
)
data[st.session_state["CURRENT_USER"]]["avezvousEte_victime_dintimidation_dans_un_lieu_prive"] = st.radio(
	"Avez-vous été victime d'intimidation dans un lieu privé ?", ["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("avezvousEte_victime_dintimidation_dans_un_lieu_prive", "Non"))
)

# Continue and return button, saving the data to server
col1, col2 = st.columns(2)

with col2:
	if st.button("Continuer"):
		client.put_json(st.secrets["webdav"]["remote_path"], data)
		st.switch_page("pages/audiopage.py")

with col1:
	if st.button("Retour"):
		client.put_json(st.secrets["webdav"]["remote_path"], data)
		st.switch_page("pages/kappa1.py")