import streamlit as st
from main import get_new_workspace # for create workspace button

st.set_page_config(
    layout='centered',
    page_title='How To Use - Project Hinge Point',
    page_icon='assets/project_hinge_point_logo.png',
)

def header() -> None:
    st.markdown(
        '''
        # How To Project Hinge Point
        From scores to insight in three steps.
        ''',
        unsafe_allow_html=True,
    )

def workflow_overview() -> None:
    with st.expander('Workflow Overview', expanded=True):
        st.markdown('## Workflow Overview', unsafe_allow_html=True)

        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            with st.container(border=True):
                st.markdown(
                    '''
                    #### **1. Create a Workspace**
                    Each workspace holds *one* dataset. This means one pre-/post-assessment cycle.
                    :grey-background[Create as many workspaces as you need] from the sidebar or the
                    buttons on this page to manage multiple cycles.
                    ''',
                    unsafe_allow_html=True,
                )
                st.image('res/placeholder_image.png', width='stretch')

        with col_2:
            with st.container(border=True, height=507):
                st.markdown(
                    '''
                    #### **2. Upload Your Data**
                    Upload a `.csv`, `.xlsx`, or `.ods` file with your student scores.
                    The :grey-background[*first three* columns must follow the required order]
                    (which you can see below).
                    ''',
                    unsafe_allow_html=True,
                )
                st.image('res/placeholder_image.png', width='stretch')

        with col_3:
            with st.container(border=True, height=507):
                st.markdown(
                    '''
                    #### **3. Read Your Results**
                    Each workspace calculates
                    :grey-background[descriptive statistics, Cohen's d, and visualizations]
                    for your data.
                    ''',
                    unsafe_allow_html=True,
                )
                st.image('res/placeholder_image.png', width='stretch')

def data_format_requirements() -> None:
    with st.expander('Data Format Requirements'):
        st.markdown('## Data Format Requirements', unsafe_allow_html=True)

        col_1, col_2 = st.columns([3, 2])
        with col_1:
            with st.container(border=True):
                st.markdown(
                    '''
                    #### **Required Column Order**

                    Your file's :grey-background[*first three columns*] must be structured as follows.
                    Column names do *not* need to match exactly, as only their position matters
                    (they are not needed for calculation).

                    | Column 1                       | Column 2       | Column 3        |
                    |---                             |---             |---              |
                    | Student value (name, ID, etc.) | Pre-test score | Post-test score |

                    Additional columns beyond the third are ignored.
                    ''',
                    unsafe_allow_html=True,
                )

        with col_2:
            with st.container(border=True, height=374):
                st.markdown(
                    '''
                    #### **No Student Names?**

                    Student names are :grey-background[*not* required for any calculation].
                    If your dataset has no name column, create a :grey-background[placeholder column] in
                    position 1 and :grey-background[fill it with any values]
                    (e.g., participant IDs or random strings).
                    ''',
                    unsafe_allow_html=True,
                )

        with st.container(border=True):
            st.markdown(
                '''
                #### **Accepted File Types**
                `.csv` -- Comma-Separated Values  
                `.xlsx` -- Excel Workbook  
                `.ods` -- OpenDocument Spreadsheet
                ''',
                unsafe_allow_html=True,
            )

def reading_the_statistics() -> None:
    with st.expander('Reading the Statistics'):
        st.markdown('## Reading the Statistics', unsafe_allow_html=True)

        col_1, col_2 = st.columns(2)
        with col_1:
            with st.container(border=True, height=476):
                st.markdown(
                    '''
                    #### **Metric Summary**

                    The *Metric Summary* panel in each workspace summarizes descriptive statistics
                    for both the pre- and post-test score list. This includes
                    :grey-background[min, max, range, mean, quartiles, IQR, and standard deviation.]
                    ''',
                    unsafe_allow_html=True,
                )
                st.image('res/placeholder_image.png', width='stretch')

        with col_2:
            with st.container(border=True):
                st.markdown(
                    '''
                    #### **Key Metrics**

                    The *Key Metrics* panel displays the four most important numbers:
                    :grey-background[pre-test mean, post-test mean, mean improvement (*Δx̄*), and Cohen's *d*].
                    Below them are the :grey-background[pooled and individual standard deviations],
                    allowing you to verify spread.
                    ''',
                    unsafe_allow_html=True,
                )
                st.image('res/placeholder_image.png', width='stretch')

def reading_the_charts() -> None:
    with st.expander('Reading the Charts'):
        st.markdown('## Reading the Charts', unsafe_allow_html=True)

        with st.container(border=True):
            col_1, col_2 = st.columns(2)
            col_1.markdown(
                '''
                #### **Baseline Histograms**

                Two :grey-background[independent histograms] with 
                :grey-background[baseline sliders].
                The table beneath each charts count how many students (both raw counts and percentages) scored
                below, at, and above your chosen baseline.
                ''',
                unsafe_allow_html=True,
            )
            col_2.image('res/placeholder_image.png', width='stretch')

        with st.container(border=True):
            col_1, col_2 = st.columns(2)
            col_1.image('res/placeholder_image.png', width='stretch')
            col_2.markdown(
                '''
                #### **Box Plot Comparison**

                Side-by-side box plots that display the
                :grey-background[median, quartile spread, and individual score points]
                for both assessments.
                ''',
                unsafe_allow_html=True,
            )

        with st.container(border=True):
            col_1, col_2 = st.columns(2)
            col_1.markdown(
                '''
                #### **Comparison Histogram**

                Overlays :grey-background[pre-test and post-test] score distributions
                in 5-point bins.
                ''',
                unsafe_allow_html=True,
            )
            col_2.image('res/placeholder_image.png', width='stretch')

        with st.container(border=True):
            col_1, col_2 = st.columns(2)
            col_1.image('res/placeholder_image.png', width='stretch')
            col_2.markdown(
                '''
                #### **Pre- vs. Post-test Score Scatter Plot**

                Plots :grey-background[pre- versus post-test scores]
                alongside a linear representation of stagnating scores.
                Scores above the line improved, below regressed, and on it stayed the same.
                ''',
                unsafe_allow_html=True,
            )

def call_to_action() -> None:
    with st.expander('Ready to Begin?'):
        col_1, col_2 = st.columns(2, vertical_alignment='center')

        with col_1:
            st.markdown(
                '''
                ## Ready to Begin?

                Create a workspace, upload your dataset, and get your effect size in seconds.
                ''',
                unsafe_allow_html=True,
            )

        with col_2:
            st.markdown(
                '''
                > #### **Quick Checklist**
                > - [ ] Dataset has at least 3 columns
                > - [ ] Column 2 = pre-test scores
                > - [ ] Column 3 = post-test scores
                > - [ ] File is `.csv`, `.xlsx`, or `.ods`
                ''',
                unsafe_allow_html=True,
            )

        button = st.button('Create a Workspace', type='primary', width='stretch', icon=':material/add_circle:')
        if button:
            get_new_workspace()
            st.rerun()

if __name__ == '__main__':
    header()
    workflow_overview()
    data_format_requirements()
    reading_the_statistics()
    reading_the_charts()
    call_to_action()