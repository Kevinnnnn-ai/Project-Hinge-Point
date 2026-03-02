import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px

def make_workspace_page(workspace_id: str) -> callable:
    def workspace_page(): # convert workspace_id to a callable that can be used as a page
        workspace_name = st.session_state.workspaces[workspace_id]['name']
        workspace_data = st.session_state.workspaces[workspace_id]['data']
        workspace_description = st.session_state.workspaces[workspace_id]['data']['description']

        # workspace header and description
        st.markdown(f'# {workspace_name}')

        st.session_state.workspaces[workspace_id]['data']['description'] = st.text_area(
            label='Enter workspace description here:',
            height='content', width='stretch',
            placeholder='Enter description here...',
            value=workspace_description,
        )

        st.markdown('---')

        #  dataset upload and preview
        st.markdown('# File :red[Upload]')

        file_upload_col_1, file_upload_col_2 = st.columns(2)
        file_upload_col_1.markdown(
            '''
            :red[Required heading order]:
            > 1. Name
            > 2. Pre-test grade
            > 3. Post-test grade

            Note that :red[they do not] have to be named as such.
            '''
        )
        file_upload_col_2.markdown(
            '''
            If you do not have a :red[student name column]:

            > 1. Make a column :red[in place of where the student name column should be]. 
            > 2. Fill it with random strings.

            :red[Student names] are not needed for calculation, simply just the :red[quantity of students].
            '''
        )

        dataset = st.file_uploader(
            label='Upload dataset.',
            type=['csv', 'xlsx', 'ods'], # .csv, .xlsx, and .ods are 3 common dataset filetypes
            accept_multiple_files=False,
            width='stretch',
        )

        if dataset is not None:
            if dataset.type == 'text/csv':
                df = pd.read_csv(dataset)
            if dataset.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                df = pd.read_excel(dataset)
            if dataset.type == 'application/vnd.oasis.opendocument.spreadsheet':
                df = pd.read_excel(dataset, engine='odf')
            st.dataframe(df)
        else:
            df = pd.DataFrame()
            st.dataframe(df)

        # calculations
        pre_heading = df.columns[1] # columns could be named differently, so define it as a numerical location
        post_heading = df.columns[2]
        pre_scores = df[pre_heading]
        post_scores = df[post_heading]
        sample_size = len(df.columns[0])

        pre_min = pre_scores.min()
        pre_max = pre_scores.max()
        pre_range = pre_max - pre_min
        pre_mean = pre_scores.mean()
        pre_q1 = pre_scores.quantile(0.25)
        pre_q3 = pre_scores.quantile(0.75)
        pre_iqr = pre_q3 - pre_q1
        pre_std = pre_scores.std()

        post_min = post_scores.min()
        post_max = post_scores.max()
        post_range = post_max - post_min
        post_mean = post_scores.mean()
        post_q1 = post_scores.quantile(0.25)
        post_q3 = post_scores.quantile(0.75)
        post_iqr = post_q3 - post_q1
        post_std = post_scores.std()

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

        # dataset metric summary
        st.markdown('# Metric :red[Summary]')

        # pre-/post-test measurements
        metric_summary_col_1, metric_summary_col_2 = st.columns(2)
        metric_summary_col_1.markdown('### :red[Pre-test] Measurements')
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
        metric_summary_col_2.markdown('### :red[Post-test] Measurements')
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

        # effect size measurements
        st.markdown('### :red[Effect Size] Measurements')
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

        # key metrics
        st.markdown('### :red[Key] Metrics', unsafe_allow_html=True)

        # WIP:
        key_metrics_col_1, key_metrics_col_2, key_metrics_col_3, key_metrics_col_4 = st.columns(4)
        key_metrics_col_1.metric('Pre-test Mean (x̄1)', f'{pre_mean:.2f}')
        key_metrics_col_2.metric('Post-test Mean (x̄2)', f'{post_mean:.2f}')
        key_metrics_col_3.metric('Mean Improvement (Δx̄)', f'{mean_diff:.2f}')
        key_metrics_col_4.metric("Effect Size (d)", f'{cohens_d:.2f}')

        key_metrics_col_5, key_metrics_col_6, key_metrics_col_7 = st.columns(3)
        key_metrics_col_5.metric('Pre-test Standard Deviation (s1)', f'{pre_std:.2f}')
        key_metrics_col_6.metric('Post-test Standard Deviation (s2)', f'{post_std:.2f}')
        key_metrics_col_7.metric('', f'{pooled_std:.2f}')

        if cohens_d < 0.2:
            impact_label = 'Small Effect'
        elif cohens_d < 0.4:
            impact_label = 'Below Hinge Point'
        elif cohens_d < 0.8:
            impact_label = 'Moderate Effect'
        else:
            impact_label = 'Large Effect'
        st.success(f'Impact Category: {impact_label}')
        if above_hinge:
            st.success("This intervention exceeds Hattie's 0.40 hinge point.")
        else:
            st.warning('This intervention falls below the 0.40 hinge point.')

        st.markdown('### Score Distribution Comparison')
        comparison_histogram_labels = ['Pre-test', 'Post-test']
        comparison_histogram_data = [pre_test_scores, post_test_scores]
        comparison_histogram = ff.create_distplot(
            comparison_histogram_data,
            comparison_histogram_labels,
        )
        st.plotly_chart(comparison_histogram)

        '''
        st.markdown('### Score Distribution')
        histogram_baseline = st.slider(
            "Set Desired Score Baseline",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
        )
        histogram = px.histogram(
            example_dataframe,
            x="score_after",
            nbins=10,
        )
        histogram.add_vline(
            x=baseline,
            line_dash="dash",
            annotation_text=f"Baseline = {baseline}",
            annotation_position="top"
        )
        st.plotly_chart(fig, use_container_width=True)
        '''

    return workspace_page