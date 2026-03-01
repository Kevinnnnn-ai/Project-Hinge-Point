import streamlit as st
import uuid # for workspace IDs

def get_workspaces() -> None: # check for existing workspaces in session state
    if 'workspaces' not in st.session_state:
        st.session_state.workspaces = {} # inside is: workspace_id: {name: str, data: dict}
    if 'active_workspace' not in st.session_state:
        st.session_state.active_workspace = None

def dashboard() -> None: # dashboard must be in the same script with workspace functionality
    st.title('Dashboard')

def workspace_sidebar() -> None:
    with st.sidebar:
        create_workspace_button = st.button('Create New Workspace')

        if create_workspace_button:
            workspace_id = str(uuid.uuid4())
            number_of_workspaces = len(st.session_state.workspaces)
            workspace_name = f'Workspace {number_of_workspaces + 1}'

            st.session_state.workspaces[workspace_id] = {
                'name': workspace_name,
                'data': {},
            }
            st.session_state.active_workspace = workspace_id
            st.success(f'Created {workspace_name} - ID: {workspace_id}')

def main() -> None:
    pages = (
        st.Page('home.py', title='Home', default=True,),
        st.Page(dashboard, title='Dashboard',),
        st.Page('about.py', title='About',),
    )
    navigation = st.navigation(pages, position='sidebar', expanded=True,)
    navigation.run()

if __name__ == '__main__':
    main()
    workspace_sidebar()
    get_workspaces()