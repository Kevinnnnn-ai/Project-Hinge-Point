import streamlit as st
import plotly.graph_objects as go
from main import get_new_workspace # workspace creation in call-to-action section

st.set_page_config(
    layout='centered',
    page_title='What Is Effect Size? - Project Hinge Point',
    page_icon='assets/project_hinge_point_logo.png',
)

def header() -> None:
    st.markdown(
        '''
        # What Is Effect Size?
        Understanding the numbers behind your instructional impact.
        ''',
        unsafe_allow_html=True,
    )

def the_core_idea() -> None:
    with st.expander('The Core Idea', expanded=True):
        col_1, col_2 = st.columns([3, 2])
        with col_1:
            st.markdown(
                '''
                ## The Core Idea

                An effect size is a standardized :grey-background[measure of the *magnitude*] of a
                difference between :grey-background[two groups or two points in time].
                Unlike raw score changes, effect sizes are :grey-background[*scale-independent*];
                in other words, they account for the natural spread of scores in your class,
                making results :grey-background[comparable] across different assessments, grade levels, and subjects. 

                In the context of pre- and post-test data, effect size answers one question:
                ''',
                unsafe_allow_html=True,
            )

        with col_2:
            with st.container(border=True, height=320):
                st.markdown(
                    '''
                    #### **Why Not Just Use Score Change?**

                    A 10-point gain means something *different* when scores range
                    from 90 to 100 versus 40 to 100. Effect size :grey-background[normalizes]
                    that gain in your data, producing a number that is
                    :grey-background[directly comparable and interpretable].
                    ''',
                    unsafe_allow_html=True,
                )

        st.markdown(
            '''
            > *How meaningful was the change in student performance,
            > relative to how spread out scores already were?*
            ''',
            unsafe_allow_html=True,
        )

def cohens_d_and_the_formulas() -> None:
    with st.expander("Cohen's d and the Formulas"):
        st.markdown("## Cohen's d and the Formulas", unsafe_allow_html=True)

        col_1, col_2 = st.columns(2, vertical_alignment='top')
        with col_1:
            with st.container(border=True, height=300):
                st.markdown(
                    r'''
                    #### **1. Sample Size (*n*)**

                    $$n = \text{count of student records in dataset}$$

                    The :grey-background[number of students] with both a pre- and post-test
                    score. Effect size reliability increases with sample size, as
                    results from :grey-background[fewer than 10 students] should be interpreted
                    cautiously.
                    ''',
                    unsafe_allow_html=True,
                )
            
            with st.container(border=True, height=300):
                st.markdown(
                    r'''
                    #### **3. Pooled Standard Deviation (*sₚ*)**

                    $$sₚ = \sqrt{\frac{(n-1)s₁^2 + (n-1)s₂^2}{2n - 2}}$$

                    The pooled standard deviation :grey-background[combines the variability]
                    of both the pre- and post-test distributions into a
                    :grey-background[single representative spread].
                    ''',
                    unsafe_allow_html=True,
                )

        with col_2:
            with st.container(border=True, height=300):
                st.markdown(
                    r'''
                    #### **2. Assessment Means (*x̄₁*, *x̄₂*)**

                    $$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

                    The :grey-background[mean of all scores for a given assessment].
                    *x̄₁* is the pre-test mean and *x̄₂* is the post-test mean.
                    Their difference (*Δx̄*) is the raw score gain before
                    standardization by *sₚ*.
                    ''',
                    unsafe_allow_html=True,
                )

            with st.container(border=True, height=300):
                st.markdown(
                    r'''
                    #### **4. Cohen's d (*d*)**

                    $$d = \frac{x̄₁ - x̄₂}{sₚ}$$

                    The result, *d*, expresses :grey-background[how many standard deviations]
                    the post-test mean sits above the pre-test mean.
                    ''',
                    unsafe_allow_html=True,
                )

def hatties_hinge_point() -> None:
    with st.expander("Hattie's Hinge Point"):
        st.markdown("## Hattie's Hinge Point", unsafe_allow_html=True)

        col_1, col_2 = st.columns([1, 3])
        with col_1:
            with st.container(border=True, height=304):
                st.markdown(
                    '''
                    > *"An effect size of 0.40 sets the standard from which we can judge
                    > the success of an influence."*
                    > John Hattie, *Visible Learning* (2009)
                    ''',
                    unsafe_allow_html=True,
                )

        with col_2:
            with st.container(border=True):
                st.markdown(
                    '''
                    John Hattie synthesized more than :grey-background[800 meta-analyses] covering over
                    :grey-background[80 million students] to identify what instructional practices
                    drive learning most effectively.
                    His central benchmark, the :grey-background[*0.40 hinge point*] represents the average
                    growth a student is expected to make in one academic year through typical schooling. 

                    Interventions that exceed *d* = 0.40 are producing learning gains
                    :grey-background[above and beyond what students would achieve on their own].
                    This is the threshold that Project Hinge Point measures every result against.
                    ''',
                    unsafe_allow_html=True,
                )

def interpreting_your_results() -> None:
    with st.expander("Interpreting Your Results"):
        st.markdown('## Interpreting Your Results', unsafe_allow_html=True)

        st.markdown(
            '''
            Project Hinge Point :grey-background[classifies every result] into one of four
            impact categories. Each maps to a range of Cohen's *d* values and carries a
            :grey-background[distinct instructional implication].
            ''',
            unsafe_allow_html=True,
        )

        gauge = go.Figure(
            go.Indicator(
                mode='gauge+number',
                value=0.40,
                number={'suffix': ' (Hinge Point)', 'font': {'size': 25}},
                gauge={
                    'axis': {'range': [0, 1.2], 'tickwidth': 1},
                    'bar': {'color': '#a3d1fe', 'thickness': 0.50},
                    'steps': [
                        {'range': [0.0, 0.2], 'color': '#2a2a2a', 'name': 'Small'},
                        {'range': [0.2, 0.4], 'color': '#3d3d3d', 'name': 'Below Hinge'},
                        {'range': [0.4, 0.8], 'color': '#555555', 'name': 'Moderate'},
                        {'range': [0.8, 1.2], 'color': '#737373', 'name': 'Large'},
                    ],
                    'threshold': {
                        'thickness': 0.75,
                        'value':     0.40,
                    },
                },
                title={'text': "Cohen's d Scale", 'font': {'size': 20}},
            )
        )

        gauge.update_layout(height=280, margin=dict(t=60, b=20, l=40, r=40))
        st.plotly_chart(gauge, width='stretch')

        st.dataframe(
            data={
                'Category': [
                    'Small Effect',
                    'Below Hinge Point',
                    'Moderate Effect',
                    'Large Effect',
                ],
                "Cohen's d Range": [
                    'd < 0.20',
                    '0.20 ≤ d < 0.40',
                    '0.40 ≤ d < 0.80',
                    'd ≥ 0.80',
                ],
                'Instructional Implication': [
                    'Minimal measurable impact on learning.',
                    'Some growth, but below expected yearly progress.',
                    'Above-average growth; intervention is working.',
                    'Exceptional impact; consider sharing the approach.',
                ],
            }
        )

def important_caveats() -> None:
    with st.expander('Important Caveats'):
        st.markdown('## Important Caveats', unsafe_allow_html=True)
        st.markdown(
            '''
            A few things to keep in mind:

            + **Sample size matters**: Effect sizes calculated on very small groups (fewer than 10 students)
              carry wide uncertainty and should be interpreted cautiously.
            + **Effect size does not imply causation**: A high *d* means scores improved significantly;
              it does not prove the intervention alone caused the improvement.
            + **Context is everything**: A *d* of 0.35 in a high-performing group of students may reflect
              a plateau effect, not a weak intervention.
            + **This tool assumes equal group sizes**: Pre- and post-test data should come from the same
              students. Mismatched datasets will produce misleading results.
            ''',
            unsafe_allow_html=True,
        )

def call_to_action() -> None:
    with st.expander('Ready to Calculate?', expanded=True):
        st.markdown(
            '''
            ## Ready to Calculate?

            Upload your pre- and post-test scores and get your effect size in seconds.
            No statistics background required.
            ''',
            unsafe_allow_html=True,
        )

        button = st.button('Create a Workspace', type='primary', width='stretch', icon=':material/add_circle:')
        if button:
            get_new_workspace()
            st.rerun()

if __name__ == '__main__':
    header()
    the_core_idea()
    cohens_d_and_the_formulas()
    hatties_hinge_point()
    interpreting_your_results()
    important_caveats()
    call_to_action()