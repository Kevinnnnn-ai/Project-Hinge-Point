import streamlit as st
import pandas as pd

st.warning('THIS PAGE IS CURRENTLY UNDER DEVELOPMENT. YOU MAY ENCOUNTER ERRORS.')

st.set_page_config(
    layout='centered',
    page_title='Dashboard - Project Hinge Point',
    page_icon='assets/placeholder_image.png',
)

datasets = []

def separator() -> None:
    st.markdown('---', unsafe_allow_html=True)

def header() -> None:
    st.markdown('# :red[Dash]board')
    separator()

def get_all_dataframes() -> None:
    global datasets
    for id, data in st.session_state.workspaces.items():
        dataframe = st.session_state.workspaces[id]['dataset']
        if dataframe is not None:
            datasets.append(dataframe)

    if datasets:
        combined_dataframe = pd.concat(datasets, ignore_index=True)
        st.dataframe(combined_dataframe)

if __name__ == '__main__':
    header()
    
    get_all_dataframes()