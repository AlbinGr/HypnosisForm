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
        login("Login", "pages/kappa2.py")
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
st.title("Formulaire Kappa 2")

data["paralysie_sommeil"] = st.radio(
    "Vous est-il déjà arrivé de vous réveiller au milieu de la nuit en ayant l'impression de ne pas pouvoir bouger votre corps et/ou de ne pas pouvoir parler ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("paralysie_sommeil", None)) if data.get("paralysie_sommeil", None) is not None else None,
    key="paralysie_sommeil"
)

data["sensibilite_ton_voix"] = st.radio(
    "Lorsque vous étiez enfant, vous sentiez-vous plus affecté(e) par le ton de voix de vos figures parentales que par ce qu’elles disaient réellement ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("sensibilite_ton_voix", None)) if data.get("sensibilite_ton_voix", None) is not None else None,
    key="sensibilite_ton_voix"
)

data["empathie_peur"] = st.radio(
    "Si une personne de votre entourage parle d'une peur que vous avez également vécue, avez-vous tendance à ressentir aussi de l’appréhension ou de la peur ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("empathie_peur", None)) if data.get("empathie_peur", None) is not None else None,
    key="empathie_peur"
)

data["ressassement_dispute"] = st.radio(
    "Si vous êtes impliqué dans une dispute avec quelqu'un, une fois celle-ci terminée, avez-vous tendance à ressasser ce que vous auriez pu ou dû dire ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("ressassement_dispute", None)) if data.get("ressassement_dispute", None) is not None else None,
    key="ressassement_dispute"
)

data["deconnexion_conversation"] = st.radio(
    "Vous arrive-t-il parfois de décrocher lorsque quelqu'un vous parle, au point de ne même plus entendre ce qui a été dit, parce que votre esprit a dérivé vers quelque chose de totalement différent ?", 
     ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("deconnexion_conversation", None)) if data.get("deconnexion_conversation", None) is not None else None,
    key="deconnexion_conversation"
)

data["desir_compliments"] = st.radio(
    "Désirez-vous parfois recevoir des compliments pour un travail bien fait, même si vous vous sentez gêné(e) ou mal à l’aise lorsque vous le recevez ?", ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("desir_compliments", None)) if data.get("desir_compliments", None) is not None else None,
    key="desir_compliments"
)

data["crainte_conversation_inconnus"] = st.radio(
    "Craignez-vous souvent de ne pas être capable de tenir une conversation avec quelqu’un que vous venez de rencontrer ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("crainte_conversation_inconnus", None)) if data.get("crainte_conversation_inconnus", None) is not None else None,
    key="crainte_conversation_inconnus"
)

data["gene_attention_apparence"] = st.radio(
    "Vous sentez-vous mal à l’aise ou gêné(e) lorsque l’attention est portée sur votre corps ou votre apparence physique ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("gene_attention_apparence", None)) if data.get("gene_attention_apparence", None) is not None else None,
    key="gene_attention_apparence"
)

data["evitement_enfants"] = st.radio(
    "Si vous aviez le choix, préféreriez-vous éviter d’être entouré(e) d’enfants la plupart du temps ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("evitement_enfants", None)) if data.get("evitement_enfants", None) is not None else None,
    key="evitement_enfants"
)

data["maladresse_mouvements_public"] = st.radio(
    "Avez-vous l’impression de ne pas être détendu(e) ou à l’aise dans vos mouvements corporels, surtout en présence de personnes inconnues ou dans des situations inhabituelles ?",
    ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("maladresse_mouvements_public", None)) if data.get("maladresse_mouvements_public", None) is not None else None,
    key="maladresse_mouvements_public"
)

data["preference_non_fiction"] = st.radio(
    "Préférez-vous lire des ouvrages non fictifs plutôt que des œuvres de fiction ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("preference_non_fiction", None)) if data.get("preference_non_fiction", None) is not None else None,
    key="preference_non_fiction"
)

data["sensation_amertume"] = st.radio(
    "Lorsque quelqu’un décrit un goût très amer, avez-vous du mal à ressentir cette sensation d’amertume ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("sensation_amertume", None)) if data.get("sensation_amertume", None) is not None else None,
    key="sensation_amertume"
)

data["auto_perception_negative"] = st.radio(
    "Avez-vous généralement l’impression de vous percevoir de manière moins favorable que la façon dont les autres vous perçoivent ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("auto_perception_negative", None)) if data.get("auto_perception_negative", None) is not None else None,
    key="auto_perception_negative"
)

data["gene_contact_physique_public"] = st.radio(
    "Avez-vous tendance à vous sentir maladroit(e) ou gêné(e) d’initier un contact physique (tenir la main, embrasser, etc.) avec une personne avec qui vous êtes en couple, en présence d'autres personnes ?",
    ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("gene_contact_physique_public", None)) if data.get("gene_contact_physique_public", None) is not None else None,
    key="gene_contact_physique_public"
)

data["gene_questions_public"] = st.radio(
    "Lors d’un cours ou d’une conférence, vous sentez-vous généralement mal à l’aise de poser des questions devant le groupe, même si vous souhaitez des explications supplémentaires ?", 
    ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("gene_questions_public", None)) if data.get("gene_questions_public", None) is not None else None,
    key="gene_questions_public"
)

data["gene_regard_direct"] = st.radio(
    "Ressentez-vous une gêne si une personne que vous venez de rencontrer vous regarde directement dans les yeux lorsqu'elle vous parle, surtout si la conversation porte sur vous ?", 
    ["Oui", "Non"],
    index= ["Oui", "Non"].index(data.get("gene_regard_direct", None)) if data.get("gene_regard_direct", None) is not None else None,
    key="gene_regard_direct"
)

data["gene_conversation_groupe"] = st.radio(
    "Dans un groupe de personnes que vous venez de rencontrer, vous sentiriez-vous mal à l’aise d’attirer l’attention sur vous en initiant la conversation ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("gene_conversation_groupe", None)) if data.get("gene_conversation_groupe", None) is not None else None,
    key="gene_conversation_groupe"
)

data["difficulte_exprimer_amour"] = st.radio(
    "Si vous êtes en couple ou très proche de quelqu’un, trouvez-vous difficile ou embarrassant d’exprimer verbalement votre amour pour cette personne ?", ["Oui", "Non"], 
    index= ["Oui", "Non"].index(data.get("difficulte_exprimer_amour", None)) if data.get("difficulte_exprimer_amour", None) is not None else None,
    key="difficulte_exprimer_amour"
)

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
            st.switch_page("pages/audiopage.py")

with col1:
    if st.button("Retour"):
        client.put_json(st.secrets["webdav"]["remote_path"]  + f"{st.session_state['CURRENT_USER']}.json", data)
        st.switch_page("pages/kappa1.py")