import streamlit as st
import pandas as pd
import joblib
import pefile
import os
from sklearn.preprocessing import MinMaxScaler

# Configuration de la page
st.set_page_config(
    page_title="MalwareScope - Analyse de Sécurité",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown('''
    <style>
        .header {padding: 20px; border-bottom: 2px solid #FF4B4B;}
        .prediction-box {padding: 20px; border-radius: 10px; margin-top: 20px;}
        .safe {background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;}
        .danger {background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;}
        .feature-table {margin-top: 20px; padding: 15px; border: 1px solid #eee; border-radius: 8px;}
    </style>
''', unsafe_allow_html=True)

# En-tête amélioré
st.markdown('''
    <div class="header">
        <h1 style="color: #FF4B4B">🛡️ MalwareScope</h1>
        <h3>Analyse Avancée de Fichiers Exécutables</h3>
    </div>
''', unsafe_allow_html=True)

# Section de téléversement dans une colonne
col1, col2 = st.columns([2, 3])
with col1:
    st.markdown("### 📤 Téléverser un Fichier")
    uploaded_file = st.file_uploader(" ", type=["exe"], label_visibility="hidden")

# Instructions dans l'autre colonne
with col2:
    st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h4>📌 Comment utiliser :</h4>
            <ol>
                <li>Téléversez un fichier .exe</li>
                <li>Attendez l'extraction des caractéristiques</li>
                <li>Consultez les résultats d'analyse</li>
            </ol>
        </div>
    ''', unsafe_allow_html=True)

# Fonction d'extraction inchangée
def extract_features(file_path):
    # ... (le code d'extraction existant reste identique) ...
    if uploaded_file:
        with st.spinner('🔍 Analyse en cours...'):
        # Enregistrement temporaire
         temp_file_path = "temp_file.exe"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            features_df = extract_features(temp_file_path)
            
            if features_df is not None:
                # Section des caractéristiques
                st.markdown("### 📊 Caractéristiques Extraites")
                st.dataframe(features_df.style.highlight_max(color='#fffdba'), use_container_width=True)

                # Prédiction
                scaler = joblib.load('scalerforest.pkl')
                features_df = scaler.transform(features_df)
                tree_clf = joblib.load('random_forest_model.pkl')
                prediction = tree_clf.predict(features_df)

                # Affichage des résultats
                st.markdown("### 📌 Résultat de l'Analyse")
                if prediction[0] == 0:
                    st.markdown('''
                        <div class="prediction-box safe">
                            <h2>✅ Fichier Sûr</h2>
                            <p>Aucune menace détectée</p>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('''
                        <div class="prediction-box danger">
                            <h2>🚨 Danger !</h2>
                            <p>Malware détecté - Ne pas exécuter ce fichier !</p>
                        </div>
                    ''', unsafe_allow_html=True)

                # Section d'informations supplémentaires
                with st.expander("📝 Afficher les détails techniques"):
                    st.markdown(f"""
                        - Nom du fichier: `{uploaded_file.name}`
                        - Taille du fichier: {uploaded_file.size // 1024} KB
                        - Nombre de caractéristiques analysées: {len(features_df.columns)}
                    """)

        except Exception as error:
            st.error(f"❌ Erreur lors de l'analyse : {str(error)}")
        else:
            st.markdown('''
        <div style="margin-top: 50px; text-align: center; color: #666;">
            <h4>⬆️ Veuillez téléverser un fichier pour commencer l'analyse</h4>
            <p>Formats supportés : .exe</p>
        </div>
    ''', unsafe_allow_html=True)
