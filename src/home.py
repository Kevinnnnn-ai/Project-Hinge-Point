import streamlit as st
from main import get_pages, get_new_workspace

st.set_page_config(
    layout='centered',
    page_title='Home - Project Hinge Point',
    page_icon='res/placeholder_image.png',
)

def how_to_use_card() -> None:
    with st.container(border=True):
        if st.button('How To Use', icon=':material/table:'):
            st.switch_page('how_to_use.py')

        st.markdown(
            '''
            
            ''',
            unsafe_allow_html=True,
        )

def what_is_effect_size_card() -> None:
    with st.container(border=True):
        if st.button('What Is Effect Size', icon=':material/insert_chart:'):
            st.switch_page('what_is_effect_size.py')

        st.markdown(
            '''
            
            ''',
            unsafe_allow_html=True,
        )

def dashboard_card() -> None:
    with st.container(border=True):
        if st.button('Dashboard', icon=':material/dashboard:'):
            st.switch_page('dashboard.py')

        st.markdown(
            '''
            
            ''',
            unsafe_allow_html=True,
        )

def workspaces_card() -> None:
    with st.container(border=True):
        if st.button('Workspaces', icon=':material/widgets:'):
            get_new_workspace()
            pages = get_pages()
            last_workspace = len(pages['Your Workspaces']) - 1
            st.switch_page(pages['Your Workspaces'][last_workspace])

        st.markdown(
            '''
            
            ''',
            unsafe_allow_html=True,
        )

def terms_of_service_card() -> None:
    with st.container(border=True):
        if st.button('Terms of Service', icon=':material/article:'):
            st.switch_page('terms_of_service.py')

        st.markdown(
            '''
            
            ''',
            unsafe_allow_html=True,
        )

def about_card() -> None:
    with st.container(border=True):
        if st.button('About', icon=':material/error:'):
            st.switch_page('about.py')

        st.markdown(
            '''
            
            ''',
            unsafe_allow_html=True,
        )

def header() -> None:
    st.markdown(
        '''
        # Project Hinge Point

        You go-to tool for calculating your teaching efficacy.
        ''',
        unsafe_allow_html=True,
    )

def cards() -> None:
    col_1, col_2 = st.columns(2)
    with col_1:
        how_to_use_card()
        dashboard_card()
        terms_of_service_card()

    with col_2:
        what_is_effect_size_card()
        workspaces_card()
        about_card()

if __name__ == '__main__':
    header()
    cards()