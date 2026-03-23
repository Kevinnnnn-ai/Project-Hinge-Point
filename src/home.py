import streamlit as st
import plotly.graph_objects as go # for visual figures in each card
from main import get_pages, get_new_workspace # to redirect users via the buttons on each card

st.set_page_config(
    layout='centered',
    page_title='Home - Project Hinge Point',
    page_icon='res/placeholder_image.png',
)

def how_to_use_card() -> None:
    with st.container(border=True, height=315):
        if st.button('How To Use', type='primary', icon=':material/table:'):
            st.switch_page('how_to_use.py')

        st.markdown(
            '''
            Learn how to :grey-background[format] your data,
            :grey-background[navigate] your workspace,
            and :grey-background[interpret] your visualizations.
            ''',
            unsafe_allow_html=True,
        )

        dummy_dataframe = st.session_state.dummy_dataset['dataframe']
        st.dataframe(dummy_dataframe, height=135, hide_index=True)

def what_is_effect_size_card() -> None:
    with st.container(border=True, height=315):
        if st.button('What Is Effect Size', type='primary', icon=':material/insert_chart:'):
            st.switch_page('what_is_effect_size.py')

        st.markdown(
            '''
            Understand the meaning of :grey-background[effect size]
            and the reasons behind :grey-background[why it works].
            ''',
            unsafe_allow_html=True,
        )

        gauge = go.Figure(
            go.Indicator(
                mode='gauge+number+delta', value=st.session_state.dummy_dataset['dataframe_statistics']['cohens_d'],
                number={'prefix': 'Effect Size (d): ', 'font': {'size': 13}},
                delta={'reference': 0.4, 'suffix': ' from hinge'},
                gauge={
                    'axis': {
                        'range':    [0.0, 1.5],
                        'tickvals': [0.2, 0.4, 0.8, 1.2],
                        'ticktext': ['Small', 'Hinge Point', 'Moderate', 'Large'],
                    },
                    'bar': {'color': '#5ae086'},
                    'steps': [
                        {'range': [0.0, 0.2], 'color': '#000000'},
                        {'range': [0.2, 0.4], 'color': '#252525'},
                        {'range': [0.4, 0.8], 'color': '#444444'},
                        {'range': [0.8, 1.2], 'color': '#656565'},
                        {'range': [1.2, 1.5], 'color': '#7c7c7c'},
                    ],
                    'threshold': {
                        'line':      {'color': 'white', 'width': 2},
                        'thickness': 0.75,
                        'value':     0.4,
                    },
                },
            )
        )

        gauge.update_layout(height=250, margin=dict(t=60, b=0, l=40, r=40))

        st.plotly_chart(gauge, width='stretch', height=160)

def dashboard_card() -> None:
    with st.container(border=True, height=315):
        if st.button('Dashboard', type='primary', icon=':material/dashboard:'):
            st.switch_page('dashboard.py')

        st.markdown(
            '''
            Collectively and holisitically review all your workspaces in one place.
            ''',
            unsafe_allow_html=True,
        )

def workspaces_card() -> None:
    with st.container(border=True, height=315):
        if st.button('Workspaces', type='primary', icon=':material/widgets:'):
            get_new_workspace()
            pages = get_pages()
            last_workspace = len(pages['Your Workspaces']) - 1
            st.switch_page(pages['Your Workspaces'][last_workspace])

        st.markdown(
            '''
            Input your :grey-background[data], calculate :grey-background[metrics],
            and get your :grey-background[effect size].
            ''',
            unsafe_allow_html=True,
        )

        st.dataframe(
            data={
                'Metric': [
                    'Effect Size (d)',
                    'Hinge Point',
                    'Is Above Hinge Point',
                    'Sample Size (n)',
                    'Mean Difference (Δx̄)',
                    'Pooled Standard Deviation (sₚ)',
                ],
                'Value': [
                    f'{st.session_state.dummy_dataset['dataframe_statistics']['cohens_d']:.2f}',
                    f'{st.session_state.dummy_dataset['dataframe_statistics']['hinge_point']:.2f}',
                    f'{st.session_state.dummy_dataset['dataframe_statistics']['is_above_hinge']}',
                    f'{st.session_state.dummy_dataset['dataframe_statistics']['sample_size']}',
                    f'{st.session_state.dummy_dataset['dataframe_statistics']['mean_diff']:.2f}',
                    f'{st.session_state.dummy_dataset['dataframe_statistics']['pooled_std']:.2f}',
                ],
            },
            height=160,
        )

def terms_of_service_card() -> None:
    with st.container(border=True, height=315):
        if st.button('Terms of Service', type='primary', icon=':material/article:'):
            st.switch_page('terms_of_service.py')

        st.markdown(
            '''
            Review how Project Hinge Point should utilized in order to
            produce reliable results, make informed decisions,
            and help build Project Hinge Point into more than just an educational tool.
            ''',
            unsafe_allow_html=True,
        )

def about_card() -> None:
    with st.container(border=True, height=315):
        if st.button('About', type='primary', icon=':material/error:'):
            st.switch_page('about.py')

        st.markdown(
            '''
            Read about values of Project Hinge Point, the project's mission, and its developer.
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