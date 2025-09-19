import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "checklist_data.xlsx"

@st.cache_data(ttl=60)
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=['Unnamed:_0', 'Unnamed:_1', 'Unnamed:_2', 'Unnamed:_3', 'Unnamed:_4', 'Unnamed:_5', 'Unnamed:_6', 'Unnamed:_7', 'Unnamed:_8', 'Unnamed:_9', 'Unnamed:_10', 'Unnamed:_11', 'Unnamed:_12'])
    df = pd.read_excel(DATA_FILE)
    return df

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

st.set_page_config(page_title="Checklist Data Entry", layout="wide")

st.title("✅ Checklist — Data Entry & Dashboard")

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("Filters & Actions")
status_filter = st.sidebar.multiselect("Filter by Status", options=df['Status'].dropna().unique() if 'Status' in df.columns else [], default=None)
responsible_filter = st.sidebar.multiselect("Filter by Responsible", options=df['Responsible'].dropna().unique() if 'Responsible' in df.columns else [], default=None)

# Data entry form
st.subheader("Add / Update Checklist Item")
with st.form("entry_form", clear_on_submit=True):
    cols = st.columns(3)
    task = cols[0].text_input("Task Name")
    resp = cols[1].text_input("Responsible")
    target = cols[2].date_input("Target Date", value=datetime.today())
    status = st.selectbox("Status", options=["Pending", "In Progress", "Done", "On Hold"], index=0)
    remarks = st.text_area("Remarks")
    submitted = st.form_submit_button("Save")

    if submitted:
        new = {k: None for k in df.columns}
        # populate known columns
        if 'Task_Name' in df.columns:
            new['Task_Name'] = task
        else:
            first_text = df.columns[0] if len(df.columns)>0 else 'Task'
            new[first_text] = task
        if 'Responsible' in df.columns:
            new['Responsible'] = resp
        if 'Target_Date' in df.columns:
            new['Target_Date'] = pd.to_datetime(target)
        if 'Status' in df.columns:
            new['Status'] = status
        if 'Remarks' in df.columns:
            new['Remarks'] = remarks
        df2 = df.append(new, ignore_index=True)
        save_data(df2)
        st.success("Saved ✅ — the checklist has been updated. Refresh below to see changes.")

st.write("---")
# Display & edit table
st.subheader("Checklist Table")
df = load_data()  # reload
display_df = df.copy()

# Apply filters if selected
if status_filter:
    display_df = display_df[display_df['Status'].isin(status_filter)]
if responsible_filter:
    display_df = display_df[display_df['Responsible'].isin(responsible_filter)]

st.dataframe(display_df, use_container_width=True)

# Simple KPIs
st.sidebar.header("KPIs")
total = len(df)
pending = len(df[df['Status']=='Pending']) if 'Status' in df.columns else 0
inprog = len(df[df['Status']=='In Progress']) if 'Status' in df.columns else 0
done = len(df[df['Status']=='Done']) if 'Status' in df.columns else 0
st.sidebar.metric("Total Items", total)
st.sidebar.metric("Pending", pending)
st.sidebar.metric("In Progress", inprog)
st.sidebar.metric("Done", done)

# Download button for current data
st.download_button("Download Excel", data=df.to_excel(index=False), file_name="checklist_data_export.xlsx")
