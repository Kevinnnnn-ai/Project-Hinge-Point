import streamlit as st
import uuid # for workspace IDs
import workspace

def dashboard() -> None:
    st.set_page_config(
        layout='centered',
        page_title='Dashboard - Project Hinge Point',
        page_icon='assets/placeholder_image.png',
    )

    st.markdown(
        '''
        # :red[Dash]board
        '''
    )

def get_pages() -> dict:
    pages = {
        'Navigation': [
            st.Page('home.py', title='Home', default=True),
            st.Page(dashboard, title='Dashboard'),
            st.Page('about.py', title='About'),
        ],
        'Workspaces': [],
    }

    for workspace_id, workspace_data in st.session_state.workspaces.items():
        workspace_name = workspace_data['name']
        pages['Workspaces'].append(
            st.Page(
                make_workspace_page(workspace_id), # all workspaces refer to the workspace_page() callable
                title=workspace_name,
                url_path=f'workspace_{workspace_id}', # thus, workspaces need cutsom URLs
            )
        )
    return pages

def get_workspaces() -> None:
    if 'workspaces' not in st.session_state:
        st.session_state.workspaces = {} # if workspaces don't exist, initialize workspace functionality

def make_workspace_page(id: str) -> callable:
    return workspace.make_workspace_page(id)

def workspace_sidebar() -> None:
    with st.sidebar:
        if st.button('Create New Workspace'):
            id = str(uuid.uuid4())
            name = f'Workspace {len(st.session_state.workspaces) + 1}'

            st.session_state.workspaces[id] = {
                'name': name,
                'data': {
                    'description': '',
                },
            }
            st.success(f'Created {name}')

def get_started() -> None:
    id = str(uuid.uuid4())
    name = f'Workspace {len(st.session_state.workspaces) + 1}'

    st.session_state.workspaces[id] = {
        'name': name,
        'data': {
            'description': '',
        },
    }
    st.success(f'Created {name}')

if __name__ == '__main__':
    get_workspaces()
    workspace_sidebar()
    
    pages = get_pages()
    navigation = st.navigation(pages=pages, position='sidebar', expanded=True)
    navigation.run()