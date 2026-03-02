import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import main

st.set_page_config(
    layout='centered',
    page_title='Home - Project Hinge Point',
    page_icon='assets/placeholder_image.png',
)

def spacer() -> None:
    st.markdown('---')

def hero_section() -> None:
        st.markdown(
            '''
            # Project :red[Hinge Point]
            Turn :grey[data] into :grey[impact].
            ''',
            unsafe_allow_html=True,
        )

def description() -> None:
    col_1, col_2 = st.columns(spec=2, vertical_alignment='center', border=True)
    col_1.image(image='assets/placeholder_image.png', width='stretch')
    col_2.markdown(
        '''
        ## What is Project :red[Hinge Point]?
        **Project Hinge Point** is your go-to tool for quickly calculating **Hattie effect sizes**. 
        Simply input your data and get instant insights to gauge your impactful decisions in education.
        ''',
        unsafe_allow_html=True,
    )

    st.markdown(
        '''
        ## Why do :red[Hattie effect sizes] matter?
        Hattie effect sizes help you understand the impact of your educational strategies. 
        With **Project Hinge Point**,
        you can easily calculate these metrics to make informed decisions and guide meaningful change.
        >  "The best thing you can do...
        > is reinforce something you have already learnt." <br>
        > -- John Hattie (regarding the effect size of specific practices)
        ''',
        unsafe_allow_html=True,
    )

def example_section() -> None:
    st.markdown(
        '''
        ## :red[Example] usage.
        '''
    )

    st.markdown('> Example Input', unsafe_allow_html=True)
    df = pd.DataFrame(
        {
            'student': [
                'Alice', 'Bob', 'Charlie', 'Daniel', 'Elena', 
                'Felix', 'Grace', 'Henry', 'Isla', 'Julian', 
                'Keira', 'Liam', 'Maya', 'Noah', 'Olivia', 
                'Peter', 'Quinn', 'Rachel', 'Samuel', 'Talia', 
                'Uriah', 'Violet', 'William', 'Xander', 'Yara',
            ],
            'pre_scores': [
                78, 82, 90, 60, 81,
                55, 70, 63, 77, 52,
                68, 85, 74, 61, 88,
                59, 73, 66, 50, 79,
                62, 71, 80, 54, 76,
            ],
            'post_scores': [
                85, 88, 93, 72, 91,
                66, 81, 74, 88, 64,
                79, 94, 85, 73, 97,
                70, 85, 77, 61, 89,
                73, 82, 91, 65, 87,
            ],
        }
    )
    st.dataframe(df)

    st.markdown('> Example Output', unsafe_allow_html=True)
    pre_scores = df['pre_scores']
    post_scores = df['post_scores']

    pre_mean = pre_scores.mean()
    post_mean = post_scores.mean()
    mean_diff = post_mean - pre_mean
    pre_std = pre_mean.std()
    post_std = post_scores.std()
    pooled_std = np.sqrt((pre_std ** 2 + post_std ** 2) / 2)
    if pooled_std > 0:
        cohens_d = mean_diff / pooled_std 
    else:
        cohens_d = 0
    hinge_point = 0.40
    is_above_hinge = cohens_d >= hinge_point

    st.markdown('### Key Metrics', unsafe_allow_html=True)
    col_1, col_2, col_3, col_4 = st.columns(4)
    col_1.metric(label='Pre-test Mean', value=f'{pre_mean:.2f}')
    col_2.metric(label='Post-test Mean', value=f'{post_mean:.2f}')
    col_3.metric(label='Mean Improvement', value=f'{mean_diff:.2f}')
    col_4.metric(label='Effect Size', value=f'{cohens_d:.2f}')
    col_5, col_6, col_7 = st.columns(3)
    col_5.metric(label='Pre-test Standard Deviation', value=f'{pre_std:.2f}')
    col_6.metric(label='Post-test Standard Deviation', value=f'{post_std:.2f}')
    col_7.metric(label='Pooled Standard Deviation', value=f'{pooled_std:.2f}')

    if cohens_d < 0.2:
        impact_label = 'Small Effect'
    elif cohens_d < 0.4:
        impact_label = 'Below Hinge Point'
    elif cohens_d < 0.8:
        impact_label = 'Moderate Effect'
    else:
        impact_label = 'Large Effect'
    st.success(f'Impact Category: {impact_label}')
    if is_above_hinge:
        st.success("This intervention exceeds Hattie's 0.40 hinge point.")
    else:
        st.warning('This intervention falls below the 0.40 hinge point.')

    st.markdown('### Score Distribution Comparison')
    comp_hist_labels = ['Pre-test', 'Post-test']
    comp_hist_data = [pre_scores, post_scores]
    comp_hist = ff.create_distplot(
        comp_hist_data,
        comp_hist_labels,
    )
    st.plotly_chart(comp_hist)

    st.markdown(
        '''
        > End of example...
        ...and get more data visualizations and tools with your own workspaces!
        '''
    )

def call_to_action() -> None:
    st.markdown(
        '''
        ## Get :red[started].
        Ready to see your data come to life? <br>
        Look at this example and click the button below to calculate your Hattie effect size instantly.
        ''',
        unsafe_allow_html=True,
    )
    if st.button('Create a Workspace'):
        main.get_started()
        st.rerun()

def benefits_section() -> None:
    st.markdown('## Why Use Project :red[Hinge Point]?', unsafe_allow_html=True)

    col_1, col_2, col_3, col_4 = st.columns(4)

    col_1.image(image='assets/placeholder_image.png', width='stretch')
    col_1.markdown('''
        **Instant Insights** <br>
        Calculate effect sizes in seconds.
        ''',
        unsafe_allow_html=True,
    )

    col_2.image(image='assets/placeholder_image.png', width='stretch')
    col_2.markdown('''
        **Data-Driven Decisions** <br>
        Make informed choices based on metrics.
        ''',
        unsafe_allow_html=True,
    )

    col_3.image(image='assets/placeholder_image.png', width='stretch')
    col_3.markdown('''
        **User-Friendly** <br>
        No prior statistics experience needed.
        ''',
        unsafe_allow_html=True,
    )

    col_4.image(image='assets/placeholder_image.png', width='stretch')
    col4.markdown('''
        **Reliable & Accurate** <br>
        Trustworthy calculations for research.
        ''',
        unsafe_allow_html=True,
    )

def contacts_section() -> None:
    st.markdown(
        '''
        ## :red[Connect] with me.
        Have questions or feedback? I'd love to hear from you!  
        + **Streamlit Profile:** [Kevin Jie](https://share.streamlit.io/user/kevinnnnn-ai)
        + **GitHub:** [Kevinnnnn-ai](https://github.com/Kevinnnnn-ai)
        + **LinkedIn:** [kevin-jie-21a477368](https://www.linkedin.com/in/kevin-jie-21a477368/)
        ''',
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    hero_section()
    spacer()
    description()
    spacer()
    call_to_action()
    spacer()
    example_section()
    spacer()
    benefits_section()
    spacer()
    contacts_section()