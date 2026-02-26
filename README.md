# logiciels-malveillants
# MalwareScope – Malware Detection using Machine Learning

## Overview
This project implements a machine learning-based malware detection system using static analysis of Portable Executable (PE) files.

## Methodology
- Feature extraction using `pefile`
- Data preprocessing and MinMax scaling
- Random Forest classification
- Model evaluation using accuracy, confusion matrix and ROC-AUC

## Deployment
The trained model is deployed using Streamlit for real-time executable file analysis.

## Technologies
- Python
- Scikit-learn
- Pandas
- Streamlit
- Joblib
- PEFile
