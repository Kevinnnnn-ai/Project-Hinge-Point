import streamlit as st
from main import get_new_workspace # for workspace creation button

st.set_page_config(
    layout='centered',
    page_title='About - Project Hinge Point',
    page_icon='res/project_hinge_point_logo.png',
)

def value_proposition() -> None:
    st.markdown(
        '''
        # About Project Hinge Point
        Turning data about education into insight.
        ''',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.image('res/instant_analyses.png')
            st.markdown('#### **Instant Analyses**', unsafe_allow_html=True)
        with col_2:
            st.image('res/clear_comparisons.png')
            st.markdown('#### **Clear Comparisons**', unsafe_allow_html=True)
        with col_3:
            st.image('res/data_visualizations.png')
            st.markdown('#### **Data Visualizations**', unsafe_allow_html=True)

def the_why() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns([3, 4], vertical_alignment='center')
        with col_1:
            st.image('res/the_why_1.png', width='stretch')
            st.image('res/the_why_2.png', width='stretch')

        col_2.markdown(
            '''
            ## The Why

            Teachers often quickly accumulate massive amounts of classroom data,
            but transforming that data into clear, actionable insight is often more difficult
            than many think.

            Most educators don't have the time, training, or access to use the tools
            required to analyze their data. This in turn makes educators gauge actions
            based on instinct rather than evidence.

            Project Hinge Point was built to change that. It's an accessible interface that turns
            data into insight directly within the hands of the people who need it most.
            ''',
            unsafe_allow_html=True,
        )

def mission_statement() -> None: # mission statement
    with st.container(border=True):
        col_1, col_2 = st.columns(2, vertical_alignment='center')
        col_1.markdown(
            '''
            ## Mission & Values

            The mission is to make statistical analysis accessible, interpretable,
            and usable for every teacher.

            We believe that:
            + Data belongs to teachers
            + Good tools should be simple and accurate
            ''',
            unsafe_allow_html=True,
        )
        col_2.image('res/mission_statement.png', width='stretch')

def the_creator_and_developer() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns([7, 5], vertical_alignment='center')
        col_1.image('res/project_hinge_point_logo.png', width='stretch')

        col_2.markdown(
            '''
            ## The Creator & Developer

            My name is Kevin Jie, and I built Project Hinge Point to bridge the gap between
            education and classroom analysis. I want to focus on combining statistical analysis
            with easy-to-use graphical interfaces that facilitate the classroom decision-making.
            ''',
            unsafe_allow_html=True,
        )

def the_research_behind_it() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns([2, 1], vertical_alignment='center')
        col_1.markdown(
            '''
            ## The Research Behind It

            John Hattie's synthesis of over 800 meta-analyses, published in
            *Visible Learning* (2009), remains one of the most comprehensive
            investigations into what actually drives student achievement and learning.

            His central finding is an effect size of 0.40. It represents the average
            yearly learning growth expected of a student. Practices that exceed
            this threshold are considered above-average contributors to learning,
            and thus a effective teaching methodology.

            Project Hinge Point implements this point so educators can gauge and
            measure their own impact against a globally recognized standard, allowing
            for both methodology refinement and comparison.
            ''',
            unsafe_allow_html=True,
        )

        col_2.markdown(
            '''
            > *"The remarkable feature of the evidence is that the greatest effects
            > on student learning occur when teachers become learners of their
            > own teaching."*
            > -- John Hattie, *Visible Learning*
            ''',
            unsafe_allow_html=True,
        )

def call_to_action() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns(2, vertical_alignment='center')
        col_1.markdown(
            '''
            ## Ready to Get Started?

            Upload your pre- and post-test data and see your educational
            impact in seconds. No statistics background is required,
            so what are you waiting for?
            ''',
            unsafe_allow_html=True,
        )
        col_2.image('res/get_started.png', width='stretch')

        button = st.button('Create Workspace', type='primary', width='stretch', icon=':material/add_circle:')
        if button:
            get_new_workspace()
            st.rerun()

if __name__ == '__main__':
    value_proposition()
    the_why()
    mission_statement()
    the_creator_and_developer()
    the_research_behind_it()
    call_to_action()