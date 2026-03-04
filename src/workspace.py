import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def divider() -> None:
    st.markdown('---', unsafe_allow_html=True)

def spacer() -> None:
    st.markdown('#####', unsafe_allow_html=True)

def make_workspace_page(workspace_id: str) -> callable:
    def workspace_page(): # convert workspace_id to a callable that can be used as a page
        workspace_name = st.session_state.workspaces[workspace_id]['name']
        workspace_description = st.session_state.workspaces[workspace_id]['data']['description']

        # workspace header section
        st.markdown(f'# {workspace_name}')

        # workspace description
        st.session_state.workspaces[workspace_id]['data']['description'] = st.text_area(
            label='Enter workspace description here:',
            height='content', width='stretch',
            placeholder='Enter description here...',
            value=workspace_description,
        )

        divider()

        # dataset upload section
        st.markdown('# File :red[Upload]', unsafe_allow_html=True)

        # dataset upload instructions
        st.markdown('### :red[Instructions] and Exceptions:', unsafe_allow_html=True)
        upload_col_1, upload_col_2 = st.columns(2)
        upload_col_1.markdown(
            '''
            > ##### **:red[Required heading order]:**
            > 1. Name
            > 2. Pre-test grade
            > 3. Post-test grade

            > Note that :red[they do not] have to be named as such.
            ''',
            unsafe_allow_html=True,
        )
        upload_col_2.markdown(
            '''
            > ##### No :red[student name column]:
            > 1. Make a **column** :red[in place of where the **student name column** should be]. 
            > 2. Fill it with random strings.

            > :red[Student names] are not needed for calculation, simply just the :red[quantity of students].
            ''',
            unsafe_allow_html=True,
        )

        # dataset upload area
        st.markdown('### :red[File] Upload:', unsafe_allow_html=True)

        dataset = st.file_uploader(
            label='Upload dataset.',
            type=['csv', 'xlsx', 'ods'], # 3 most common dataset types
            accept_multiple_files=False,
            width='stretch',
        )

        st.warning('Your dataset must follow the correct heading orders, as explained above.')

        # dataset upload status and data frame creation
        if dataset:
            try:
                if dataset.type == 'text/csv':
                    dataframe = pd.read_csv(dataset)
                elif dataset.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    dataframe = pd.read_excel(dataset)
                elif dataset.type == 'application/vnd.oasis.opendocument.spreadsheet':
                    dataframe = pd.read_excel(dataset, engine='odf')
                st.success('Dataset has been loaded.')
            except:
                st.error('Data frame creation error.')
            st.session_state.workspaces[workspace_id]['data']['dataset'] = dataframe
        dataframe = st.session_state.workspaces[workspace_id]['data']['dataset']

        st.markdown('### :red[Dataset] Preview:', unsafe_allow_html=True)

        if dataframe is not None:
            st.dataframe(dataframe)
        else:
            st.warning('Upload a dataset to continue.')

        # dataset scope definition
        try:
            pre_heading = dataframe.columns[1] # columns could be named differently, so define it as a numerical location
            post_heading = dataframe.columns[2]
            pre_scores = dataframe[pre_heading]
            post_scores = dataframe[post_heading]
            sample_size = len(dataframe.columns[0])
        except:
            st.error('Dataset scope definition error.')

        # pre-test statistical calculations
        try:
            pre_min = pre_scores.min()
            pre_max = pre_scores.max()
            pre_range = pre_max - pre_min
            pre_mean = pre_scores.mean()
            pre_q1 = pre_scores.quantile(0.25)
            pre_q3 = pre_scores.quantile(0.75)
            pre_iqr = pre_q3 - pre_q1
            pre_std = pre_scores.std()
        except:
            st.error('Pre-test statistical calculation error.')

        # post-test statistical calculations
        try:
            post_min = post_scores.min()
            post_max = post_scores.max()
            post_range = post_max - post_min
            post_mean = post_scores.mean()
            post_q1 = post_scores.quantile(0.25)
            post_q3 = post_scores.quantile(0.75)
            post_iqr = post_q3 - post_q1
            post_std = post_scores.std()
        except:
            st.error('Post-test statistical calculations error.')

        # primary calculations used in calculation effect size (Cohen's d)
        try:
            mean_diff = post_mean - pre_mean

            pooled_std_numerator = ((sample_size - 1) * pre_std ** 2) + ((sample_size - 1) * post_std ** 2)
            pooled_std_denominator = sample_size * 2 - 2
            pooled_std = np.sqrt(pooled_std_numerator / pooled_std_denominator)

            if pooled_std > 0:
                cohens_d = mean_diff / pooled_std 
            else:
                cohens_d = 0
            hinge_point = 0.40
            is_above_hinge = cohens_d >= hinge_point

        except:
            st.error("Effect size (Cohen's d) calculation error.")

        divider()

        # metric summary section
        st.markdown('# Metric :red[Summary]', unsafe_allow_html=True)

        # pre-test measurements display
        metric_summary_col_1, metric_summary_col_2 = st.columns(2)

        metric_summary_col_1.markdown('### :red[Pre-test] Measurements:', unsafe_allow_html=True)
            
        try:
            metric_summary_col_1.table(
                data={
                    'Metric': [
                        'Pre-test Minimum',
                        'Pre-test Maximum',
                        'Pre-test Range',
                        'Pre-test Mean (x̄1)',
                        'Pre-test 1st Quartile (Q1 1)',
                        'Pre-test 3rd Quartile (Q3 1)',
                        'Pre-test Interquartile Range (IQR1)',
                        'Pre-test Standard Deviation (s1)',
                    ],
                    'Value': [
                        f'{pre_min:.2f}',
                        f'{pre_max:.2f}',
                        f'{pre_range:.2f}',
                        f'{pre_mean:.2f}',
                        f'{pre_q1:.2f}',
                        f'{pre_q3:.2f}',
                        f'{pre_iqr:.2f}',
                        f'{pre_std:.2f}',
                    ],
                }
            )

        except:
            st.error('Pre-test measurements display error.')

        # post-test measurements display
        metric_summary_col_2.markdown('### :red[Post-test] Measurements:', unsafe_allow_html=True)

        try:
            metric_summary_col_2.table(
                data={
                    'Metric': [
                        'Post-test Minimum',
                        'Post-test Maximum',
                        'Post-test Range',
                        'Post-test Mean (x̄2)',
                        'Post-test 1st Quartile (Q1 2)',
                        'Post-test 3rd Quartile (Q3 2)',
                        'Post-test Interquartile Range (IQR2)',
                        'Post-test Standard Deviation (s2)',
                    ],
                    'Value': [
                        f'{post_min:.2f}',
                        f'{post_max:.2f}',
                        f'{post_range:.2f}',
                        f'{post_mean:.2f}',
                        f'{post_q1:.2f}',
                        f'{post_q3:.2f}',
                        f'{post_iqr:.2f}',
                        f'{post_std:.2f}',
                    ],
                }
            )

        except:
            st.error('Post-test measurements display error.')

        # effect size measurements display
        st.markdown('### :red[Effect Size] Measurements:', unsafe_allow_html=True)

        try:
            st.table(
                data={
                    'Metric': [
                        "Effect Size (Cohen's d)",
                        'Hinge Point',
                        'Is Above Hinge Point',
                    ],
                    'Value': [
                        f'{cohens_d:.2f}',
                        f'{hinge_point:.2f}',
                        is_above_hinge,
                    ],
                }
            )

        except:
            st.error('Effect size measurements display error.')

        # key metrics display
        st.markdown('### :red[Key] Metrics:', unsafe_allow_html=True)

        try:
            key_metrics_col_1, key_metrics_col_2, key_metrics_col_3, key_metrics_col_4 = st.columns(4)
            key_metrics_col_1.metric(label='Pre-test Mean (x̄1)', value=f'{pre_mean:.2f}')
            key_metrics_col_2.metric(label='Post-test Mean (x̄2)', value=f'{post_mean:.2f}')
            key_metrics_col_3.metric(label='Mean Improvement (Δx̄)', value=f'{mean_diff:.2f}')
            key_metrics_col_4.metric(label="Effect Size (d)", value=f'{cohens_d:.2f}')

            key_metrics_col_5, key_metrics_col_6, key_metrics_col_7 = st.columns(3)
            key_metrics_col_5.metric(label='Pre-test Standard Deviation (s1)', value=f'{pre_std:.2f}')
            key_metrics_col_6.metric(label='Post-test Standard Deviation (s2)', value=f'{post_std:.2f}')
            key_metrics_col_7.metric(label='Pooled Standard Deviation (sp)', value=f'{pooled_std:.2f}')

        except:
            st.error('Key metrics display error.')

        # effect size (Cohen's d) interpretation display
        try:
            if cohens_d < 0.2:
                st.info(f'Impact Category: Small Effect')
            elif cohens_d < 0.4:
                st.info(f'Impact Category: Below Hinge Point')
            elif cohens_d < 0.8:
                st.info(f'Impact Category: Moderate Effect')
            else:
                st.info(f'Impact Category: Large Effect')
        except:
            st.error("Effect size (Cohen's d) interpretation display error.")
        
        # hinge point check display
        try:
            if is_above_hinge:
                st.info("This intervention exceeds Hattie's 0.40 hinge point.")
            else:
                st.info('This intervention falls below the 0.40 hinge point.')
        except:
            st.error('Hinge point check display error.')

        divider()

        # pre-/post-test visualization section
        st.markdown('# :red[Pre-/Post-test] Visualization', unsafe_allow_html=True)

        # layered comparison histogram description
        st.markdown('### :red[Comparison] Histogram:', unsafe_allow_html=True)
        st.warning(
            '''
            White represents pre-test scores, and red represents post-test scores.\n
            Use the "Assessment Type" legend to view each histogram respectively.
            '''
        )

        # comparison histogram
        comp_hist = go.Figure()

        try:
            comp_hist.add_trace(
                go.Histogram(
                    x=pre_scores, name='Pre-test Scores',
                    opacity=0.5,
                    histnorm=None,
                    marker=dict(color='white'),
                    xbins=dict(start=0, end=100, size=5),
                )
            )
            comp_hist.add_trace(
                go.Histogram(
                    x=post_scores, name='Post-test Scores',
                    opacity=0.5,
                    histnorm=None,
                    marker=dict(color='red'),
                    xbins=dict(start=0, end=100, size=5),
                )
            )
        except:
            st.error('Comparison histogram set up error.')

        try:
            comp_hist.update_layout(
                barmode='overlay',
                xaxis_title='Test Score (%)', yaxis_title='Number of Students',
                legend_title_text='Assessment Type',
            )
            st.plotly_chart(comp_hist)
        except:
            st.error('Comparison histogram generation error.')

        spacer()

        # baseline histograms
        st.markdown('### :red[Baseline] Histograms:', unsafe_allow_html=True)
        st.warning(
            '''
            White represents pre-test scores, and red represents post-test scores.\n
            Adjust a desired baseline using the sliders.
            '''
        )

        base_hist_col_1, base_hist_col_2 = st.columns(2)
        try:
            pre_baseline = base_hist_col_1.slider(
                label='Set Desired Score Baseline',
                min_value=0, max_value=100,
                value=0, step=1,
                key=0,
            )
        except:
            st.error('Pre-test baseline slider generation error.')

        try:
            pre_base_hist = px.histogram(
                dataframe,
                x=pre_scores,
                nbins=10,
                labels={
                    'x': 'Pre-Test Score',
                    'count': 'Number of Students'
                },
                color_discrete_sequence=['white'],
            )
            pre_base_hist.update_layout(
                xaxis_title='Pre-Test Score (%)',
                yaxis_title='Number of Students',
            )
            pre_base_hist.add_vline(
                x=pre_baseline,
                line_dash='dash',
                annotation_text=f'Baseline = {pre_baseline}',
                annotation_position='top'
            )
            base_hist_col_1.plotly_chart(pre_base_hist, width='stretch')
        except:
            st.error('Pre-test histogram generation error.')

        try:
            post_baseline = base_hist_col_2.slider(
                label='Set Desired Score Baseline',
                min_value=0, max_value=100,
                value=0, step=1,
                key=1,
            )
        except:
            st.error('Post-test baseline slider generation error.')

        try:
            post_base_hist = px.histogram(
                dataframe,
                x=post_scores,
                nbins=10,
                labels={
                    'x': 'Post-Test Score',
                    'count': 'Number of Students'
                },
                color_discrete_sequence=['red'],
            )
            post_base_hist.update_layout(
                xaxis_title='Post-Test Score (%)',
                yaxis_title='Number of Students',
            )
            post_base_hist.add_vline(
                x=post_baseline,
                line_dash='dash',
                annotation_text=f'Baseline = {post_baseline}',
                annotation_position='top'
            )
            base_hist_col_2.plotly_chart(post_base_hist, width='stretch')
        except:
            st.error('Post-test histogram generation error.')

        spacer()


        try:
            st.warning('Section is in development.')
        except:
            st.error('Pre-test baseline statistic calculation error.')

        try:
            st.warning('Section is in development')
        except:
            st.error('Post-test baseline statistic calculation error.')

    return workspace_page