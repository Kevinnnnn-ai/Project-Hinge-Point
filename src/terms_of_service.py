import streamlit as st

# ============================
# page setup
# ============================

st.set_page_config(
    layout='centered',
    page_title='Terms of Service - Project Hinge Point',
    page_icon='res/placeholder_image.png',
)

def separator() -> None:
    st.markdown('---', unsafe_allow_html=True)

def spacer() -> None:
    st.markdown('#####', unsafe_allow_html=True)

# ============================
# page sections
# ============================

def header() -> None:
    st.markdown(
        '''
        # Terms of :red[Service]
        Please read these terms carefully before using Project Hinge Point.
        ''',
        unsafe_allow_html=True,
    )
    st.caption('Last updated: March 2025')

def acceptance_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[1.] Acceptance of Terms', unsafe_allow_html=True)
        st.markdown(
            '''
            By accessing or using Project Hinge Point (the "Application"), you agree to be bound by
            these Terms of Service. If you do not agree with any part of these terms, you may not use
            the Application.

            These terms apply to all users of the Application, including educators, administrators,
            researchers, and any other individuals who upload or interact with data through the platform.
            ''',
            unsafe_allow_html=True,
        )

def description_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[2.] Description of Service', unsafe_allow_html=True)
        st.markdown(
            '''
            Project Hinge Point is a statistical analysis tool designed to help educators calculate
            and interpret effect sizes from pre- and post-test classroom data. The Application provides:
            ''',
            unsafe_allow_html=True,
        )

        col_1, col_2 = st.columns(2)
        with col_1:
            with st.container(border=True):
                st.markdown(
                    '''
                    ##### What the Application Does
                    - Calculates descriptive statistics from uploaded datasets
                    - Computes Cohen's *d* effect size
                    - Benchmarks results against Hattie's 0.40 hinge point
                    - Renders interactive visualizations of score distributions
                    ''',
                    unsafe_allow_html=True,
                )
        with col_2:
            with st.container(border=True):
                st.markdown(
                    '''
                    ##### What the Application Does Not Do
                    - Store, transmit, or retain any uploaded data
                    - Provide professional pedagogical or legal advice
                    - Guarantee outcomes or instructional recommendations
                    - Access or share data with third parties
                    ''',
                    unsafe_allow_html=True,
                )

def data_privacy_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[3.] Data & Privacy', unsafe_allow_html=True)

        st.info(
            '**All data processing occurs locally within your browser session. '
            'No data is transmitted to external servers or retained after your session ends.**',
        )

        spacer()

        col_1, col_2 = st.columns(2, vertical_alignment='top')

        with col_1:
            st.markdown(
                '''
                #### Your Responsibility
                You are solely responsible for the data you upload. Before uploading any dataset,
                you must ensure that:

                - You have the legal right to use and process the data
                - Any personally identifiable information (PII) has been removed or anonymized
                - Your use complies with applicable data protection laws (e.g. FERPA, GDPR)
                - You have obtained any necessary institutional or parental consent
                ''',
                unsafe_allow_html=True,
            )

        with col_2:
            st.markdown(
                '''
                #### Student Data
                Project Hinge Point is not designed to process, store, or transmit student PII.
                Student names are not required for any calculation. If your dataset includes
                student names or other identifying information, **anonymize it before uploading**.

                The Application bears no liability for any data uploaded in violation of
                applicable privacy laws or institutional policies.
                ''',
                unsafe_allow_html=True,
            )

def disclaimer_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[4.] Disclaimer of Warranties', unsafe_allow_html=True)

        st.warning(
            'Project Hinge Point is provided **"as is"** without warranties of any kind, '
            'either express or implied.',
        )

        st.markdown(
            '''
            The Application makes no representations or warranties regarding:

            - **Accuracy** — Statistical outputs depend entirely on the quality and correctness
              of data you supply. The Application cannot validate whether your dataset is
              accurate, complete, or appropriate for the calculations performed.
            - **Fitness for purpose** — Results are intended as analytical aids, not as
              definitive assessments of teaching quality or student ability.
            - **Availability** — Uninterrupted or error-free operation of the Application
              is not guaranteed.
            - **Interpretation** — Effect sizes are one of many lenses through which
              instructional impact can be understood. They should not be used as the sole
              basis for personnel, curriculum, or policy decisions.
            ''',
            unsafe_allow_html=True,
        )

def limitation_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[5.] Limitation of Liability', unsafe_allow_html=True)
        st.markdown(
            '''
            To the fullest extent permitted by law, Project Hinge Point and its creator shall not
            be liable for any direct, indirect, incidental, consequential, or punitive damages
            arising from your use of the Application, including but not limited to:

            - Decisions made on the basis of results generated by the Application
            - Data loss, corruption, or unauthorized access to data you upload
            - Errors or inaccuracies in statistical outputs
            - Any reliance placed on the Application's calculations or visualizations

            Use of the Application is entirely at your own risk.
            ''',
            unsafe_allow_html=True,
        )

def acceptable_use_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[6.] Acceptable Use', unsafe_allow_html=True)

        col_1, col_2 = st.columns(2, vertical_alignment='top')

        with col_1:
            with st.container(border=True):
                st.markdown(
                    '''
                    ##### Permitted Uses
                    - Analyzing pre- and post-test data for instructional reflection
                    - Academic or educational research purposes
                    - Professional development and training contexts
                    - Personal evaluation of classroom practices
                    ''',
                    unsafe_allow_html=True,
                )

        with col_2:
            with st.container(border=True):
                st.markdown(
                    '''
                    ##### Prohibited Uses
                    - Uploading datasets containing unredacted student PII
                    - Using outputs to make binding employment or grading decisions
                    - Reverse-engineering or tampering with the Application's source
                    - Any use that violates applicable law or institutional policy
                    ''',
                    unsafe_allow_html=True,
                )

def intellectual_property_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[7.] Intellectual Property', unsafe_allow_html=True)
        st.markdown(
            '''
            All source code, design, and content within Project Hinge Point are the intellectual
            property of the Application's creator. You may not reproduce, distribute, or create
            derivative works without explicit written permission.

            The statistical methodologies implemented (Cohen's *d*, Hattie's hinge point) are
            based on published academic research and are not proprietary to this Application.
            ''',
            unsafe_allow_html=True,
        )

def changes_section() -> None:
    with st.container(border=True):
        st.markdown('## :red[8.] Changes to These Terms', unsafe_allow_html=True)
        st.markdown(
            '''
            These Terms of Service may be updated at any time. Continued use of the Application
            after changes are posted constitutes your acceptance of the revised terms. The date
            of the most recent revision is shown at the top of this page.
            ''',
            unsafe_allow_html=True,
        )

def contact_section() -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns([3, 2], vertical_alignment='center')

        with col_1:
            st.markdown(
                '''
                ## :red[Questions?]

                If you have questions about these terms or the Application's data practices,
                visit the About page or reach out directly through the project's repository.
                ''',
                unsafe_allow_html=True,
            )

        with col_2:
            if st.button('Go to About', icon=':material/error:', width='stretch'):
                st.switch_page('about.py')

# ============================
# execution logic
# ============================

if __name__ == '__main__':
    header()
    separator()

    acceptance_section()
    spacer()

    description_section()
    spacer()

    data_privacy_section()
    separator()

    disclaimer_section()
    spacer()

    limitation_section()
    spacer()

    acceptable_use_section()
    spacer()

    intellectual_property_section()
    spacer()

    changes_section()
    separator()

    contact_section()