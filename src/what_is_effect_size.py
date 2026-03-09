import streamlit as st
import plotly.graph_objects as go
import main # main.py

st.warning('THIS PAGE IS CURRENTLY UNDER DEVELOPMENT. YOU MAY ENCOUNTER ERRORS.')

# ============================
# page setup
# ============================

st.set_page_config(
    layout='centered',
    page_title='What Is Effect Size? - Project Hinge Point',
    page_icon='assets/project_hinge_point_logo.png',
)

def separator() -> None:
    st.markdown('---', unsafe_allow_html=True)

def spacer() -> None:
    st.markdown('#####', unsafe_allow_html=True)

# ============================
# page sections
# ============================

def hero_section() -> None:
    st.markdown(
        '''
        # What Is :red[Effect Size]?
        Understanding the numbers behind your instructional impact.
        ''',
        unsafe_allow_html=True,
    )

def effect_size_intro_section() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns([3, 2], vertical_alignment='center')

        with col_1:
            st.markdown(
                '''
                ## The Core :red[Idea]

                An **effect size** is a standardized measure of the magnitude of a difference between
                two groups or two points in time. Unlike raw score changes, effect sizes are
                scale-independent — they account for the natural spread of scores in your class,
                making results comparable across different assessments, grade levels, and subjects. <br>

                In the context of pre- and post-test data, effect size answers one question:

                > *How meaningful was the change in student performance,
                > relative to how spread out scores already were?*
                ''',
                unsafe_allow_html=True,
            )

        with col_2:
            with st.container(border=True):
                st.markdown(
                    '''
                    #### Why Not Just Use Score Change?

                    A 10-point gain means something different when scores range
                    from 90–100 versus 40–100. Effect size normalizes that gain
                    against the variability in your data, producing a number
                    that is directly comparable and interpretable.
                    ''',
                    unsafe_allow_html=True,
                )

def cohens_d_section() -> None:
    st.markdown("## Cohen's :red[d] — The Formula", unsafe_allow_html=True)

    col_1, col_2 = st.columns(2, vertical_alignment='top')

    with col_1:
        with st.container(border=True):
            st.markdown(
                r'''
                #### The Formula

                $$d = \frac{\bar{x}_2 - \bar{x}_1}{s_p}$$

                Where:
                - $\bar{x}_1$ = Pre-test mean
                - $\bar{x}_2$ = Post-test mean
                - $s_p$ = Pooled standard deviation
                ''',
                unsafe_allow_html=True,
            )

    with col_2:
        with st.container(border=True):
            st.markdown(
                r'''
                #### Pooled Standard Deviation

                $$s_p = \sqrt{\frac{(n-1)s_1^2 + (n-1)s_2^2}{2n - 2}}$$

                The pooled standard deviation combines the variability
                of both the pre- and post-test distributions into a
                single representative spread. It ensures the effect
                size is not distorted if one distribution is unusually
                tight or wide.
                ''',
                unsafe_allow_html=True,
            )

    st.markdown(
        '''
        The result, *d*, expresses how many **standard deviations** the post-test mean
        sits above the pre-test mean. A *d* of 1.0 means the post-test average exceeded
        the pre-test average by one full standard deviation — a substantial shift.
        ''',
        unsafe_allow_html=True,
    )

def hinge_point_section() -> None:
    st.markdown("## Hattie's :red[Hinge Point]", unsafe_allow_html=True)

    with st.container(border=True):
        col_1, col_2 = st.columns([2, 3], vertical_alignment='center')

        with col_1:
            st.markdown(
                '''
                > *"An effect size of 0.40 sets the standard from which we can judge
                > the success of an influence."*
                > — John Hattie, *Visible Learning* (2009)
                ''',
                unsafe_allow_html=True,
            )

        with col_2:
            st.markdown(
                '''
                John Hattie synthesized more than 800 meta-analyses covering over 80 million students
                to identify what instructional practices drive learning most effectively.
                His central benchmark — the **0.40 hinge point** — represents the average
                growth a student is expected to make in one academic year through typical schooling. <br>

                Interventions that exceed *d* = 0.40 are producing learning gains
                **above and beyond** what students would achieve on their own. This is the threshold
                that Project Hinge Point measures every result against.
                ''',
                unsafe_allow_html=True,
            )

def interpretation_section() -> None:
    st.markdown('## Interpreting :red[Your Results]', unsafe_allow_html=True)

    st.markdown(
        '''
        Project Hinge Point classifies every result into one of four impact categories.
        Each maps to a range of Cohen's *d* values and carries a distinct instructional implication.
        ''',
        unsafe_allow_html=True,
    )

    # ============================
    # visual gauge chart
    # ============================

    try:
        gauge = go.Figure(go.Indicator(
            mode='gauge+number',
            value=0.40,
            number={'suffix': ' (Hinge Point)', 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 1.2], 'tickwidth': 1},
                'bar': {'color': '#FF4B4B', 'thickness': 0.25},
                'steps': [
                    {'range': [0.0, 0.2],  'color': '#2a2a2a', 'name': 'Small'},
                    {'range': [0.2, 0.4],  'color': '#3d3d3d', 'name': 'Below Hinge'},
                    {'range': [0.4, 0.8],  'color': '#555555', 'name': 'Moderate'},
                    {'range': [0.8, 1.2],  'color': '#737373', 'name': 'Large'},
                ],
                'threshold': {
                    'line': {'color': '#FF4B4B', 'width': 4},
                    'thickness': 0.75,
                    'value': 0.40,
                },
            },
            title={'text': "Cohen's d Scale", 'font': {'size': 18}},
        ))

        gauge.update_layout(height=280, margin=dict(t=60, b=20, l=40, r=40))
        st.plotly_chart(gauge, use_container_width=True)

    except:
        st.error('Effect size gauge chart generation error.')

    # ============================
    # category breakdown table
    # ============================

    try:
        st.table(
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
                'Hinge Point Status': [
                    'Below',
                    'Below',
                    'At or Above ✓',
                    'Well Above ✓',
                ],
                'Instructional Implication': [
                    'Minimal measurable impact on learning.',
                    'Some growth, but below expected yearly progress.',
                    'Above-average growth — intervention is working.',
                    'Exceptional impact; consider sharing the approach.',
                ],
            }
        )
    except:
        st.error('Interpretation table display error.')

def reading_the_app_section() -> None:
    st.markdown('## Reading the :red[App Output]', unsafe_allow_html=True)

    col_1, col_2 = st.columns(2, vertical_alignment='top')

    with col_1:
        with st.container(border=True):
            st.markdown(
                '''
                #### Metric Summary

                The **Metric Summary** panel in each workspace reports descriptive statistics
                for both the pre- and post-test distributions — min, max, range, mean,
                quartiles, IQR, and standard deviation. These give you a complete picture of
                how scores were distributed before and after instruction.
                ''',
                unsafe_allow_html=True,
            )

        with st.container(border=True):
            st.markdown(
                '''
                #### Key Metrics

                The **Key Metrics** panel surfaces the four most actionable numbers:
                pre-test mean, post-test mean, mean improvement (Δx̄), and Cohen's *d*.
                Below them, the pooled and individual standard deviations allow you to
                verify the spread used in the calculation.
                ''',
                unsafe_allow_html=True,
            )

    with col_2:
        with st.container(border=True):
            st.markdown(
                '''
                #### Visualizations

                Three chart types are provided per workspace:

                **Comparison Histogram** — Overlays pre- and post-test score distributions
                so you can see where gains occurred across the score range.

                **Baseline Histograms** — Let you set a custom score threshold and instantly
                see how many students fall below, at, or above it — useful for proficiency
                cut-point analysis.

                **Box Plot Comparison** — Summarizes both distributions side by side with
                quartiles and individual data points, making outliers and median shifts
                immediately visible.
                ''',
                unsafe_allow_html=True,
            )

def caveats_section() -> None:
    with st.container(border=True):
        st.markdown('### :red[Important] Caveats', unsafe_allow_html=True)
        st.markdown(
            '''
            Effect size is a powerful tool, but it is not the whole picture. A few things to keep in mind:

            + **Sample size matters.** Effect sizes calculated on very small groups (fewer than 10 students)
              carry wide uncertainty and should be interpreted cautiously.
            + **Effect size does not imply causation.** A high *d* means scores improved significantly;
              it does not prove the intervention alone caused the improvement.
            + **Context is everything.** A *d* of 0.35 in a high-performing cohort may reflect
              a ceiling effect, not a weak intervention.
            + **This tool assumes equal group sizes.** Pre- and post-test data should come from the same
              students. Mismatched datasets will produce misleading results.
            ''',
            unsafe_allow_html=True,
        )

def call_to_action_section() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns(2, vertical_alignment='center')

        with col_1:
            st.markdown(
                '''
                ## Ready to :red[Calculate]?

                Upload your pre- and post-test scores and get your effect size in seconds.
                No statistics background required.
                ''',
                unsafe_allow_html=True,
            )

        with col_2:
            button = st.button('Create a Workspace', width='stretch')
            if button:
                main.get_new_workspace()
                st.rerun()

# ============================
# execution logic
# ============================

if __name__ == '__main__':
    hero_section()
    separator()

    effect_size_intro_section()
    spacer()

    cohens_d_section()
    separator()

    hinge_point_section()
    spacer()

    interpretation_section()
    separator()

    reading_the_app_section()
    spacer()

    caveats_section()
    separator()

    call_to_action_section()