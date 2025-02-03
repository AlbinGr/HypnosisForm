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

st.title("Évaluation d'écoute")

st.header("Pour information :")
st.write("L’état de transe hypnotique est un état modifié de conscience caractérisé par une focalisation intense sur\
		 une idée ou une sensation, une diminution de la perception de l’environnement extérieur et une ouverture\
		 accrue aux suggestions. Ce n’est pas une perte de contrôle ou de conscience, mais un état dans lequel on\
		 peut ressentir une relaxation profonde, une distorsion du temps, ou une concentration très spécifique.")
st.header("Tâche expérimentale")
st.write(
	"""Le but de cette tâche est que vous évaluez dans quelle mesure chaque enregistrement facilite l’accès à
l’état de transe hypnotique, en utilisant l’échelle proposée.""")

st.header("Qualité d'écoute")
st.write(""" Avant de commencer l'écoute, veuillez vérifier que votre volume est réglé de manière confortable sur vos
appareils (téléphone, tablette, ordinateur) pour que vous puissiez entendre clairement, sans gêne. Si le son
est trop faible ou trop fort, ajustez le volume en conséquence, en gardant une intensité agréable. Pour cela :
Cliquez ici pour écouter le test audio.""")

st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

result = st.slider("Sur une échelle de 0 à 10, à quel point considérez-vous cette voix comme hypnotique ?", min_value=0, max_value=10, key="hypnotique", step = 1, )
