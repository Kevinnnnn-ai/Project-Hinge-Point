import streamlit as st
import uuid                               # for workspace identification
from workspace import make_workspace_page # for making workspace pages
from dummy_dataset import (               # to set session state variables for dummy dataset
    set_dummy_dataset,
    calculate,
)

def get_pages() -> dict:
    pages = {
        'Project Hinge Point': [
            st.Page('home.py',      title='Home',      icon=':material/home:', default=True),
            st.Page('dashboard.py', title='Dashboard', icon=':material/dashboard:'),
            st.Page('about.py',     title='About',     icon=':material/error:'),
        ],
        'Using Project Hinge Point': [
            st.Page('how_to_use.py',          title='How To Use',          icon=':material/table:'),
            st.Page('what_is_effect_size.py', title='What Is Effect Size', icon=':material/insert_chart:'),
            st.Page('terms_of_service.py',    title='Terms of Service',    icon=':material/article:'),
        ],
        'Your Workspaces': [],
    }

    for workspace_id, workspace_data in st.session_state.workspaces.items():
        workspace_name = workspace_data['name']
        pages['Your Workspaces'].append(
            st.Page(
                make_workspace_page(workspace_id),
                title=workspace_name,
                url_path=f'workspace_{workspace_id}', # because all workspaces reference workspace_page() callable
                icon=':material/widgets:',
            )
        )

    return pages

def get_workspaces() -> None:
    if 'workspaces' not in st.session_state: # if user has no workspace history
        st.session_state.workspaces = {}

def get_new_workspace() -> None:
    workspace_id    = str(uuid.uuid4()) # effectively infinite workspaces
    workspace_name  = f'Workspace {len(st.session_state.workspaces) + 1}'

    st.session_state.workspaces[workspace_id] = {
        'name':        workspace_name,
        'description': '',
        'dataframe':   None,
        
        # for cross script statistic accessibility (notably, for dashboard.py)
        'dataframe_statistics': {
            'sample_size':        None,
            'mean_diff':          None,
            'pooled_std':         None,
            'cohens_d':           None,
            'hinge_point':        None,
            'is_above_hinge':     None,
            'students_improved':  None,
            'students_unchanged': None,
            'students_regressed': None,
        },
        'pre_score_statistics': {
            'pre_min':   None,
            'pre_max':   None,
            'pre_range': None,
            'pre_mean':  None,
            'pre_q1':    None,
            'pre_q3':    None,
            'pre_iqr':   None,
            'pre_std':   None,
        },
        'post_score_statistics': {
            'post_min':   None,
            'post_max':   None,
            'post_range': None,
            'post_mean':  None,
            'post_q1':    None,
            'post_q3':    None,
            'post_iqr':   None,
            'post_std':   None,
        },
    }

def get_dummy_dataset() -> None:
    set_dummy_dataset(dummy_dataset='./res/dummy_dataset.csv')
    calculate()

def sidebar_funtionality() -> None:
    with st.sidebar:
        if st.button('Create Workspace', icon=':material/add_circle:'):
            get_new_workspace()

if __name__ == '__main__':
    get_dummy_dataset()
    get_workspaces()
    sidebar_funtionality()
    
    pages = get_pages()
    navigation = st.navigation(pages=pages, position='sidebar', expanded=True)
    navigation.run()