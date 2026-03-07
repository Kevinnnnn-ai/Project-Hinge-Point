import streamlit as st

st.warning('THIS PAGE IS CURRENTLY UNDER DEVELOPMENT. YOU MAY ENCOUNTER ERRORS.')

st.set_page_config(
    layout='centered',
    page_title='About - Project Hinge Point',
    page_icon='assets/placeholder_image.png',
)

def separator() -> None:
    st.markdown('---', unsafe_allow_html=True)

def spacer() -> None:
    st.markdown('#####', unsafe_allow_html=True)

def hero_section() -> None:
    st.markdown(
        '''
        # About :red[Project Hinge Point]

        Turning :grey[educational data] into :grey[meaningful insight].
        ''',
        unsafe_allow_html=True,
    )

def mission_section() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns(2, vertical_alignment='center')

        col_1.image('assets/placeholder_image.png', width='stretch')

        col_2.markdown(
            '''
            ## Our :red[Mission]

            **Project Hinge Point** exists to make educational data **accessible, interpretable,
            and actionable** for educators.

            Teachers and researchers constantly collect valuable data, but interpreting
            that data often requires statistical tools that are difficult to access
            or understand.

            This project simplifies the process by allowing educators to **quickly compute
            Hattie effect sizes** and evaluate the impact of their instructional strategies.
            ''',
            unsafe_allow_html=True
        )

def platform_section() -> None:
    st.markdown(
        '''
        ## What does Project :red[Hinge Point] do?

        Project Hinge Point provides a simple interface for analyzing classroom data
        using **Hattie effect sizes**, a widely recognized metric for evaluating
        educational impact.

        With this platform, you can:

        + Input classroom performance data
        + Instantly calculate **effect sizes**
        + Visualize the impact of instructional decisions
        + Compare different teaching strategies
        + Support **data-driven educational improvement**

        The goal is not just to calculate numbers — but to help educators
        **interpret and apply those insights in meaningful ways**.
        ''',
        unsafe_allow_html=True
    )

def research_section() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns(2, vertical_alignment='center')

        col_1.markdown(
            '''
            ## The Idea of a :red[Hinge Point]

            Educational researcher **John Hattie** introduced the concept
            of a **hinge point** when analyzing the impact of different
            educational practices.

            In his research, an **effect size of 0.40** represents the
            average yearly learning growth for students.

            Practices that exceed this hinge point can be considered
            **above-average contributors to student learning**.

            Project Hinge Point helps educators measure where their
            strategies fall relative to this benchmark.
            ''',
            unsafe_allow_html=True
        )

        col_2.image('assets/placeholder_image.png', width='stretch')

def creator_section() -> None:
    st.markdown(
        '''
        ## About the :red[Creator]

        Project Hinge Point was developed as an effort to make
        **statistical analysis tools more accessible** to educators.

        Many powerful research metrics remain confined to academic papers
        or specialized statistical software. This project aims to bring
        those tools into a **simple and intuitive interface**.

        By combining **data analysis, visualization, and accessible design**,
        Project Hinge Point bridges the gap between educational research
        and classroom practice.
        ''',
        unsafe_allow_html=True
    )

def vision_section() -> None:
    with st.container(border=True):
        st.markdown(
            '''
            ## Looking :red[Forward]

            Future development of Project Hinge Point may include:

            + Expanded statistical tools for educational analysis
            + Classroom data visualization dashboards
            + Research comparison tools
            + Collaboration features for educators and researchers

            The long-term vision is to build a platform that helps
            educators **turn evidence into action** and improve learning outcomes
            through **data-informed decisions**.
            ''',
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    hero_section()
    separator()
    mission_section()
    spacer()
    platform_section()
    spacer()
    research_section()
    spacer()
    creator_section()
    separator()
    vision_section()