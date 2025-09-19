Streamlit Checklist App
=======================

Files:
- app.py                 : Streamlit app
- checklist_data.xlsx    : Initial data (editable by the app)
- requirements.txt       : Python dependencies

How to run locally:
1. Install dependencies: pip install -r requirements.txt
2. Run: streamlit run app.py
3. The app will open in your browser (http://localhost:8501).

Notes:
- The app writes updates to 'checklist_data.xlsx' in the same folder.
- If you want to deploy, use Streamlit Cloud, Heroku, or any server that can run Python apps.
