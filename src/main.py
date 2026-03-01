import streamlit as st
import uuid

def dashboard() -> None:
    st.title('Dashboard')

def get_pages() -> dict:
    pages = {
        'Navigation': [
            st.Page('home.py', title='Home', default=True),
            st.Page(dashboard, title='Dashboard'),
            st.Page('about.py', title='About'),
        ],
        'Workspaces': []
    }

    for workspace_id, workspace_data in st.session_state.workspaces.items():
        workspace_name = workspace_data['name']
        pages['Workspaces'].append(
            st.Page(
                make_workspace_page(workspace_id),
                title=workspace_name,
                url_path=f'workspace_{workspace_id}',
            )
        )
    return pages

def get_workspaces() -> None:
    if 'workspaces' not in st.session_state:
        st.session_state.workspaces = {}

def make_workspace_page(workspace_id: str) -> callable:
    def workspace_page():
        workspace = st.session_state.workspaces[workspace_id]
        st.title(workspace['name'])
    return workspace_page

def workspace_sidebar() -> None:
    with st.sidebar:
        if st.button('Create New Workspace'):
            workspace_id = str(uuid.uuid4())
            workspace_name = f'Workspace {len(st.session_state.workspaces) + 1}'

            st.session_state.workspaces[workspace_id] = {
                'name': workspace_name,
                'data': {},
            }
            st.success(f'Created {workspace_name}')

if __name__ == '__main__':
    get_workspaces()
    workspace_sidebar()
    
    pages = get_pages()
    navigation = st.navigation(pages, position='sidebar', expanded=True)
    navigation.run()