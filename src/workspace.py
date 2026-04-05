import streamlit as st
import pandas as pd # for dataframe creation
import numpy as np # for pooled std calculation
import plotly.express as px # for histogram figures
import plotly.graph_objects as go # for visual data displays (in general)

def header(workspace_name: str) -> None:
    st.markdown(f'# {workspace_name}', unsafe_allow_html=True)

def check_header(workspace_name: str, workspace_id: str) -> None:
    if workspace_name != st.session_state.workspaces[workspace_id]['name']:
        st.rerun() # to show matching header/workspace name

def file_upload_and_preview(workspace_id: str) -> None:
    with st.container(border=True):
        col_1, col_2 = st.columns([2, 3])
        with col_1:
            with st.container(border=True):
                st.markdown('#### **Expectations & Exceptions**:', unsafe_allow_html=True)
                st.markdown(
                    '''
                    The :grey-background[first three columns] must be ordered:
                    student, pre-test score, and post-test score.

                    Note that the *name* of each heading, *number* of headings, and *order* of the headings
                    (past the first three) :grey-background[does not matter].
                    ''',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '''
                    In the event that you do not have a student column, make a column in place of where the student
                    name column should be and fill it with random values. Student names are
                    :grey-background[*not* needed for functionality].
                    ''',
                    unsafe_allow_html=True,
                )

        with col_2:
            if st.button('Delete dataset', type='primary', width='stretch', icon=':material/do_not_disturb_on:'):
                st.session_state.workspaces[workspace_id]['dataframe'] = None
                st.session_state['uploader_key'] += 1  # forces uploader wdiget to reset
                st.rerun()

            if 'uploader_key' not in st.session_state:
                st.session_state['uploader_key'] = 0

            dataset = st.file_uploader(
                label='Upload dataset. (csv, xlsx, or ods)',
                type=['csv', 'xlsx', 'ods'], # 3 most common dataset types
                accept_multiple_files=False,
                width='stretch',
                key=st.session_state['uploader_key'], # changing this resets the widget
            )

            dataframe = st.session_state.workspaces[workspace_id]['dataframe']
            dummyframe = {'Student': [], 'Pre-test Scores': [], 'Post-test Scores': []}

            # redundant conditionals are purely to adjust dataframe's height
            if dataset is not None:
                try:
                    if dataset.type == 'text/csv':
                        dataframe = pd.read_csv(dataset)
                    elif dataset.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        dataframe = pd.read_excel(dataset)
                    elif dataset.type == 'application/vnd.oasis.opendocument.spreadsheet':
                        dataframe = pd.read_excel(dataset, engine='odf')

                    if dataframe is None: # meaning first upload
                        st.dataframe(dataframe, width=400, height=361, hide_index=True)
                    else: # meaning another upload
                        st.dataframe(dataframe, width=400, height=304, hide_index=True)
                    st.session_state.workspaces[workspace_id]['dataframe'] = dataframe

                except:
                    st.error('**RUNTIME ERROR**: Dataframe creation error.')
                    st.dataframe(dummyframe, width=400, height=361, hide_index=True)

            elif dataset is None and dataframe is not None: # meaning previously uploaded (either switched pages or deleted)
                st.dataframe(dataframe, width=400, height=361, hide_index=True)
            elif dataset is None and dataframe is None: # meaning no action or re-uploaded and deleted
                st.dataframe(dummyframe, width=400, height=361, hide_index=True)

def calculate(workspace_id: str) -> None:
    dataframe = st.session_state.workspaces[workspace_id]['dataframe']
    if dataframe is not None:
        try:
            pre_heading        = dataframe.columns[1] # columns could be named differently, so define it as a numerical location
            post_heading       = dataframe.columns[2]
            pre_scores         = dataframe[pre_heading]
            post_scores        = dataframe[post_heading]
            sample_size        = len(dataframe)
            students_improved  = int((post_scores > pre_scores).sum())
            students_unchanged = int((post_scores == pre_scores).sum())
            students_regressed = int((post_scores < pre_scores).sum())
        
            st.session_state.workspaces[workspace_id]['dataframe_statistics'].update(
                {
                    'students_improved':  students_improved,
                    'students_unchanged': students_unchanged,
                    'students_regressed': students_regressed,
                    'sample_size':        sample_size,
                }
            )

        except:
            st.error('**RUNTIME ERROR**: Dataframe scope error.')

        try:
            pre_min   = pre_scores.min()
            pre_max   = pre_scores.max()
            pre_range = pre_max - pre_min
            pre_mean  = pre_scores.mean()
            pre_q1    = pre_scores.quantile(0.25)
            pre_q3    = pre_scores.quantile(0.75)
            pre_iqr   = pre_q3 - pre_q1
            pre_std   = pre_scores.std()

            st.session_state.workspaces[workspace_id]['pre_score_statistics'].update(
                {
                    'pre_min': pre_max, 'pre_max': pre_max, 'pre_range': pre_range, 'pre_mean': pre_mean,
                    'pre_q1':  pre_q1,  'pre_q3':  pre_q3,  'pre_iqr':   pre_iqr,   'pre_std':  pre_std,
                }
            )

        except:
            st.error('**RUNTIME ERROR**: Pre-test calculation error.')

        try:
            post_min   = post_scores.min()
            post_max   = post_scores.max()
            post_range = post_max - post_min
            post_mean  = post_scores.mean()
            post_q1    = post_scores.quantile(0.25)
            post_q3    = post_scores.quantile(0.75)
            post_iqr   = post_q3 - post_q1
            post_std   = post_scores.std()

            st.session_state.workspaces[workspace_id]['post_score_statistics'].update(
                {
                    'post_min': post_min, 'post_max': post_max, 'post_range': post_range, 'post_mean': post_mean,
                    'post_q1':  post_q1,  'post_q3':  post_q3,  'post_iqr':   post_iqr,   'post_std':  post_std,
                }
            )

        except:
            st.error('**RUNTIME ERROR**: Post-test calculation error.')

        try:
            mean_diff              = post_mean - pre_mean
            pooled_std_numerator   = ((sample_size - 1) * pre_std ** 2) + ((sample_size - 1) * post_std ** 2)
            pooled_std_denominator = sample_size * 2 - 2
            pooled_std             = np.sqrt(pooled_std_numerator / pooled_std_denominator)

            if pooled_std > 0:
                cohens_d = mean_diff / pooled_std 
            else:
                cohens_d = 0
            hinge_point = 0.40
            is_above_hinge = cohens_d >= hinge_point

            st.session_state.workspaces[workspace_id]['dataframe_statistics'].update(
                {
                    'mean_diff':   mean_diff,   'pooled_std':     pooled_std,     'cohens_d': cohens_d,
                    'hinge_point': hinge_point, 'is_above_hinge': is_above_hinge,
                }
            )

        except:
            st.error("**RUNTIME ERROR**: Effect size (Cohen's d) calculation error.")
    else:
        st.warning('**WARNING**: Dataframe has not been detected.')

def standard_statistics(workspace_id: str) -> None:
    with st.container(border=True):
        st.markdown('## Standard Statistics', unsafe_allow_html=True)

        dataframe = st.session_state.workspaces[workspace_id]['dataframe']
        col_1, col_2 = st.columns(2)
        if dataframe is not None:
            with col_1:
                st.markdown('#### **Pre-test**:')

                try:
                    st.dataframe(
                        data={
                            'Metric': [
                                'Min',
                                'Max',
                                'Range',
                                'Mean (x̄₁)',
                                '1st Quartile (Q1₁)',
                                '3rd Quartile (Q3₁)',
                                'Interquartile Range (IQR₁)',
                                'Standard Deviation (s₁)',
                            ],
                            'Value': [
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_min']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_max']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_range']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_mean']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_q1']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_q3']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_iqr']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_std']:.2f}',
                            ],
                        }
                    )
                except:
                    st.error('**RUNTIME ERROR**: Pre-test metric summary display error.')

            with col_2:
                st.markdown('#### **Post-test**:')

                try:
                    st.dataframe(
                        data={
                            'Metric': [
                                'Min',
                                'Max',
                                'Range',
                                'Mean (x̄₂)',
                                '1st Quartile (Q1₂)',
                                '3rd Quartile (Q3₂)',
                                'Interquartile Range (IQR₂)',
                                'Standard Deviation (s₂)',
                            ],
                            'Value': [
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_min']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_max']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_range']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_mean']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_q1']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_q3']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_iqr']:.2f}',
                                f'{st.session_state.workspaces[workspace_id]['post_score_statistics']['post_std']:.2f}',
                            ],
                        }
                    )
                except:
                    st.error('**RUNTIME ERROR**: Post-test metric summary display error.')

            st.markdown('#### **Effect Size**:')

            try:
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
                            f'{st.session_state.workspaces[workspace_id]['dataframe_statistics']['cohens_d']:.2f}',
                            f'{st.session_state.workspaces[workspace_id]['dataframe_statistics']['hinge_point']:.2f}',
                            f'{st.session_state.workspaces[workspace_id]['dataframe_statistics']['is_above_hinge']}',
                            f'{st.session_state.workspaces[workspace_id]['dataframe_statistics']['sample_size']}',
                            f'{st.session_state.workspaces[workspace_id]['dataframe_statistics']['mean_diff']:.2f}',
                            f'{st.session_state.workspaces[workspace_id]['dataframe_statistics']['pooled_std']:.2f}',
                        ],
                    }
                )
            except:
                st.error('**RUNTIME ERROR**: Effect size metric summary display error.')

        else:
            with col_1:
                st.markdown('#### **Pre-test**:')
                st.dataframe({'Metric': [], 'Value': []}, hide_index=True)
            with col_2:
                st.markdown('#### **Post-test**:')
                st.dataframe({'Metric': [], 'Value': []}, hide_index=True)
            st.markdown('#### **Effect Size**:')
            st.dataframe({'Metric': [], 'Value': []}, hide_index=True)

def delta_zero_color(delta_zero_color: str, inverse: bool, value) -> str: # the color of delta at 0
    if delta_zero_color == 'green':
        if value == 0.0: return 'green'
    elif delta_zero_color == 'red':
        if value == 0.0: return 'red'
    else:
        if value == 0.0: return 'off'
    if inverse: return 'inverse'
    else:       return 'normal'

def key_metrics(workspace_id: str) -> None:
    dataframe = st.session_state.workspaces[workspace_id]['dataframe']
    with st.container(border=True):
        st.markdown('## Key Metrics', unsafe_allow_html=True)
        
        col_1, col_2 = st.columns([1, 3])
        if dataframe is not None:
            sample_size    = st.session_state.workspaces[workspace_id]['dataframe_statistics']['sample_size']
            post_mean      = st.session_state.workspaces[workspace_id]['post_score_statistics']['post_mean']
            pre_mean       = st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_mean']
            mean_diff      = st.session_state.workspaces[workspace_id]['dataframe_statistics']['mean_diff']
            cohens_d       = st.session_state.workspaces[workspace_id]['dataframe_statistics']['cohens_d']
            hinge_point    = st.session_state.workspaces[workspace_id]['dataframe_statistics']['hinge_point']
            is_above_hinge = st.session_state.workspaces[workspace_id]['dataframe_statistics']['is_above_hinge']
            pre_std        = st.session_state.workspaces[workspace_id]['pre_score_statistics']['pre_std']
            post_std       = st.session_state.workspaces[workspace_id]['post_score_statistics']['post_std']
            pooled_std     = st.session_state.workspaces[workspace_id]['dataframe_statistics']['pooled_std']

            try:
                with col_1:
                    st.metric(
                        label='Post-test Mean (x̄₂)',
                        border=True, value=f'{post_mean:.2f}', delta_color=delta_zero_color('red', False, mean_diff),
                        delta=f'{mean_diff:.2f} ({mean_diff / pre_mean * 100:.2f}%)',
                    )

                    std_diff = post_std - pre_std
                    st.metric(
                        label='Post-test SD (s₂)',
                        border=True, value=f'{post_std:.2f}', delta_color=delta_zero_color('off', True, std_diff),
                        delta=f'{std_diff:-.2f} ({std_diff / pre_std * 100:.2f}%)',
                    )

            except:
                st.error('**RUNTIME ERROR**: Key metrics display 1 error.')
            
            try:
                with col_2:
                    if is_above_hinge:
                        color = '#5ae086'
                    else:
                        color = '#ff6c6c'

                    gauge = go.Figure(
                        go.Indicator(
                            mode='gauge+number+delta',
                            value=cohens_d,
                            number={'prefix': 'Effect Size (d): ', 'font': {'size': 25}},
                            delta={'reference': hinge_point, 'suffix': ' from hinge'},
                            gauge={
                                'axis': {
                                    'range':    [0.0, 1.5],
                                    'tickvals': [0.2, 0.4, 0.8, 1.2],
                                    'ticktext': ['Small', 'Hinge Point', 'Moderate', 'Large'],
                                },
                                'bar': {'color': color},
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
                                    'value':     hinge_point,
                                },
                            },
                        )
                    )

                    gauge.update_layout(height=250, margin=dict(t=60, b=0, l=40, r=40))

                    with st.container(border=True):
                        st.plotly_chart(gauge, width='stretch', height=255)

            except:
                st.error('**RUNTIME ERROR**: Key metrics display 2 error.')
    
        else:
            with col_1:
                st.metric(
                    label='Post-test Mean (x̄₂)',
                    border=True, value=f'{0:.2f}', delta_color='off',
                    delta=f'{0:-.2f} ({0:.2f}%)',
                )

                st.metric(
                    label='Post-test SD (s₂)',
                    border=True, value=f'{0:.2f}', delta_color='off',
                    delta=f'{0:-.2f} ({0:.2f}%)', 
                )

            with col_2:
                gauge = go.Figure(
                    go.Indicator(
                        mode='gauge+number+delta', value=0.00,
                        number={'prefix': 'Effect Size (d): ', 'font': {'size': 25}},
                        delta={'reference': 0.4, 'suffix': ' from hinge'},
                        gauge={
                            'axis': {
                                'range': [0, 1.5],
                                'tickvals': [0.2, 0.4, 0.8, 1.2],
                                'ticktext': ['Small Effect', 'Hinge Point', 'Moderate Effect', 'Large Effect'],
                            },
                            'bar': {'color': '#464646'},
                            'steps': [
                                {'range': [0, 0.2],  'color': '#000000'},
                                {'range': [0.2, 0.4], 'color': '#252525'},
                                {'range': [0.4, 0.8], 'color': '#444444'},
                                {'range': [0.8, 1.2], 'color': '#656565'},
                                {'range': [1.2, 1.5], 'color': '#7c7c7c'},
                            ],
                            'threshold': {
                                'line': {'color': 'white', 'width': 2},
                                'thickness': 0.75,
                                'value': 0.4,
                            },
                        },
                    )
                )

                gauge.update_layout(
                    height=250, margin=dict(t=60, b=0, l=40, r=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                with st.container(border=True):
                    st.plotly_chart(gauge, width='stretch', height=255)

        col_5, col_6, col_7 = st.columns(3)
        if dataframe is not None:
            sample_size = st.session_state.workspaces[workspace_id]['dataframe_statistics']['sample_size']
            improved    = st.session_state.workspaces[workspace_id]['dataframe_statistics']['students_improved']
            unchanged   = st.session_state.workspaces[workspace_id]['dataframe_statistics']['students_unchanged']
            regressed   = st.session_state.workspaces[workspace_id]['dataframe_statistics']['students_regressed']

            try:
                col_5.metric(
                    label='Students that Improved',
                    value=improved, border=True, delta_color=delta_zero_color('red', False, improved),
                    delta=f'{improved} ({improved / sample_size * 100:.2f}%)',
                )

                col_6.metric(
                    label='Students Unchanged',
                    value=unchanged, border=True, delta_color=delta_zero_color('green', True, unchanged),
                    delta=f'{unchanged} ({unchanged / sample_size * 100:.2f}%)',
                )

                col_7.metric(
                    label='Students that Regressed',
                    value=regressed, border=True, delta_color=delta_zero_color('green', True, regressed),
                    delta=f'{regressed} ({regressed / sample_size * 100:.2f}%)',
                )
                
            except:
                st.error('**RUNTIME ERROR**: Key metrics display 3 error.')

        else:
            col_5.metric(
                label='Students that Improved', 
                value=0, border=True, delta_color='off',
                delta=f'{0} ({0:.2f}%)',
            )

            col_6.metric(
                label='Students Unchanged',
                value=0, border=True, delta_color='off',
                delta=f'{0} ({0:.2f}%)',
            )

            col_7.metric(
                label='Students that Regressed',
                value=0, border=True, delta_color='off',
                delta=f'{0} ({0:.2f}%)',
            )

def comparison_histogram(workspace_id: str) -> None:
    dataframe = st.session_state.workspaces[workspace_id]['dataframe']
    with st.container(border=True):
        st.markdown('## Comparison Histogram', unsafe_allow_html=True)

        if dataframe is not None:
            try:
                pre_scores  = dataframe[dataframe.columns[1]]
                post_scores = dataframe[dataframe.columns[2]]

                figure = go.Figure()
                figure.add_trace(
                    go.Histogram(
                        x=pre_scores, name='Pre-test',
                        opacity=0.5, marker=dict(color='#a3d1fe'),
                        xbins=dict(start=0, end=101, size=5), # end at 101 to show scores at 100
                    )
                )
            
                figure.add_trace(
                    go.Histogram(
                        x=post_scores, name='Post-test',
                        opacity=0.5, marker=dict(color='#005cb8'),
                        xbins=dict(start=0, end=101, size=5), # end at 101 to show scores at 100
                    )
                )

                figure.update_layout(
                    barmode='overlay',
                    xaxis_title='Score', yaxis_title='Number of Students',
                    legend_title_text='Assessment',
                )

                st.plotly_chart(figure, width='stretch')
            except:
                st.error('**RUNTIME ERROR**: Comparison histogram generation error.')
        else:
            figure = go.Figure()
            figure.add_trace(
                go.Histogram(
                    x=[0], name='Pre-test',
                    opacity=0.5, marker=dict(color='#3d4c5b'),
                    xbins=dict(start=0, end=101, size=5), # end at 101 to show scores at 100
                )
            )
        
            figure.add_trace(
                go.Histogram(
                    x=[0], name='Post-test',
                    opacity=0.5, marker=dict(color='#2a2a2a'),
                    xbins=dict(start=0, end=101, size=5), # end at 101 to show scores at 100
                )
            )

            figure.update_layout(
                barmode='overlay',
                xaxis_title='Score', yaxis_title='Number of Students',
                legend_title_text='Assessment',
            )

            st.plotly_chart(figure, width='stretch')
               
def baseline_histograms(workspace_id: str) -> None:
    dataframe = st.session_state.workspaces[workspace_id]['dataframe']
    with st.container(border=True):
        st.markdown('## Baseline Histograms', unsafe_allow_html=True)

        col_1, col_2 = st.columns(2)
        try:
            pre_baseline = col_1.slider(
                'Pre-test Baseline', min_value=0, max_value=100,
                value=0, step=1, key=f'pre_baseline_{workspace_id}',
            )

            post_baseline = col_2.slider(
                'Post-test Baseline', min_value=0, max_value=100,
                value=0, step=1, key=f'post_baseline_{workspace_id}',
            )

        except:
                st.error('**RUNTIME ERROR**: Baseline slider creation error.')

        if dataframe is not None:
            pre_scores  = dataframe[dataframe.columns[1]]
            post_scores = dataframe[dataframe.columns[2]]
            sample_size = st.session_state.workspaces[workspace_id]['dataframe_statistics']['sample_size']

            try:
                pre_figure = px.histogram(
                    dataframe, x=pre_scores, nbins=10,
                    color_discrete_sequence=['#a3d1fe'],
                    labels={'x': 'Pre-test Score'},
                )

                pre_figure.add_vline(
                    x=pre_baseline, line_dash='dash',
                    annotation_text=f'Baseline = {pre_baseline}',
                    annotation_position='top',
                )

                pre_figure.update_layout(
                    xaxis_title='Pre-test Score', yaxis_title='Students',
                )

                col_1.plotly_chart(pre_figure, width='stretch', height=350)

                post_figure = px.histogram(
                    dataframe, x=post_scores, nbins=10,
                    color_discrete_sequence=['#005cb8'],
                    labels={'x': 'Post-test Score'},
                )

                post_figure.add_vline(
                    x=post_baseline, line_dash='dash',
                    annotation_text=f'Baseline = {post_baseline}',
                    annotation_position='top',
                )

                post_figure.update_layout(
                    xaxis_title='Post-test Score', yaxis_title='Students',
                )

                col_2.plotly_chart(post_figure, width='stretch', height=350)
            except:
                st.error('**RUNTIME ERROR**: Baseline histogram generation error.')

            def baseline_counts(scores, baseline):
                below, at, above = 0, 0, 0
                for score in scores:
                    if score > baseline: below += 1
                    elif score < baseline: above += 1
                    else: at += 1
                return below, at, above

            pre_below, pre_at, pre_above    = baseline_counts(pre_scores, pre_baseline)
            post_below, post_at, post_above = baseline_counts(post_scores, post_baseline)

            col_1.dataframe(
                {
                    'Metric': [
                        'Students below baseline',
                        'Students at baseline',
                        'Students above baseline',
                    ],
                    'Count': [pre_below, pre_at, pre_above],
                    'Percent': [
                        f'{pre_below / sample_size * 100:.2f}%',
                        f'{pre_at / sample_size * 100:.2f}%',
                        f'{pre_above / sample_size * 100:.2f}%',
                    ],
                }
            )

            col_2.dataframe(
                {
                    'Metric': [
                        'Students below baseline',
                        'Students at baseline',
                        'Students above baseline',
                    ],
                    'Count': [post_below, post_at, post_above],
                    'Percent': [
                        f'{post_below / sample_size * 100:.2f}%',
                        f'{post_at / sample_size * 100:.2f}%',
                        f'{post_above / sample_size * 100:.2f}%',
                    ],
                }
            )

            st.caption('Set a score baseline to reveal where you students stand compared to the baseline.')

        else:
            pre_figure = px.histogram(
                dataframe, x=[0], nbins=10,
                color_discrete_sequence=['#3d4c5b'],
                labels={'x': 'Pre-test Score'},
            )

            pre_figure.add_vline(
                x=pre_baseline, line_dash='dash',
                annotation_text=f'Baseline = {pre_baseline}',
                annotation_position='top',
            )

            pre_figure.update_layout(
                xaxis_title='Pre-test Score', yaxis_title='Students',
            )

            col_1.plotly_chart(pre_figure, width='stretch', height=350)

            post_figure = px.histogram(
                dataframe, x=[0], nbins=10,
                color_discrete_sequence=['#2a2a3a'],
                labels={'x': 'Post-test Score'},
            )

            post_figure.add_vline(
                x=post_baseline, line_dash='dash',
                annotation_text=f'Baseline = {post_baseline}',
                annotation_position='top',
            )

            post_figure.update_layout(
                xaxis_title='Post-test Score', yaxis_title='Students',
            )

            col_2.plotly_chart(post_figure, width='stretch', height=350)

            col_1.dataframe(
                {
                    'Metric': [
                        'Students below baseline',
                        'Students at baseline',
                        'Students above baseline',
                    ],
                    'Count': ['', '', ''],
                    'Percent': ['', '', ''],
                }
            )

            col_2.dataframe(
                {
                    'Metric': [
                        'Students below baseline',
                        'Students at baseline',
                        'Students above baseline',
                    ],
                    'Count': ['', '', ''],
                    'Percent': ['', '', ''],
                }
            )

            st.caption('Set a score baseline to reveal where you students stand compared to the baseline.')
            
def box_plot(workspace_id: str) -> None:
    dataframe = st.session_state.workspaces[workspace_id]['dataframe']
    with st.container(border=True):
        st.markdown('## Box Plot Comparison', unsafe_allow_html=True)

        if dataframe is not None:
            try:
                pre_scores  = dataframe[dataframe.columns[1]]
                post_scores = dataframe[dataframe.columns[2]]

                fig = go.Figure()
                fig.add_trace(
                    go.Box(
                        y=pre_scores, name='Pre-test',
                        marker=dict(color='#a3d1fe'), line=dict(color='#a3d1fe'),
                        boxpoints='all', jitter=0.05, pointpos=-1.5,
                    )
                )
                
                fig.add_trace(
                    go.Box(
                        y=post_scores, name='Post-test',
                        marker=dict(color='#005cb8'), line=dict(color='#005cb8'),
                        boxpoints='all', jitter=0.05, pointpos=-1.5,
                    )
                )

                fig.update_layout(
                    yaxis_title='Score', xaxis_title='Assessment',
                    showlegend=False,
                )

                st.plotly_chart(fig, width='stretch', height=400)
            except:
                st.error('**RUNTIME ERROR**: Box plot error.')
        else:
            fig = go.Figure()
            fig.add_trace(
                go.Box(
                    y=[0], name='Pre-test',
                    marker=dict(color='#a3d1fe'), line=dict(color='#a3d1fe'),
                    boxpoints='all', jitter=0.05, pointpos=-1.5,
                )
            )
            
            fig.add_trace(
                go.Box(
                    y=[100], name='Post-test',
                    marker=dict(color='#005cb8'), line=dict(color='#005cb8'),
                    boxpoints='all', jitter=0.05, pointpos=-1.5,
                )
            )

            fig.update_layout(
                yaxis_title='Score', xaxis_title='Assessment',
                showlegend=False,
            )

            st.plotly_chart(fig, width='stretch', height=400)

def scatter_plot(workspace_id: str) -> None:
    dataframe = st.session_state.workspaces[workspace_id]['dataframe']
    with st.container(border=True):
        st.markdown('## Pre- vs. Post-test Score Scatter Plot', unsafe_allow_html=True)

        if dataframe is not None:
            try:
                student_heading = dataframe.columns[0]
                pre_scores      = dataframe[dataframe.columns[1]]
                post_scores     = dataframe[dataframe.columns[2]]
                score_min       = int(min(pre_scores.min(), post_scores.min())) - 5
                score_max       = int(max(pre_scores.max(), post_scores.max())) + 5

                figure = go.Figure()
                figure.add_trace(
                    go.Scatter(
                        x=[score_min, score_max], y=[score_min, score_max],
                        mode='lines',
                        line=dict(color='white', dash='dash', width=1),
                        name='No Change',
                    )
                )

                figure.add_trace(
                    go.Scatter(
                        x=pre_scores, y=post_scores,
                        mode='markers',
                        marker=dict(color='#a3d1fe', size=8, opacity=1),
                        text=dataframe[student_heading],
                        hovertemplate='<b>%{text}</b><br>Pre-test score: %{x}<br>Post-test score: %{y}<extra></extra>',
                        name='Students',
                    )
                )

                figure.update_layout(
                    xaxis_title='Pre-test Score',
                    yaxis_title='Post-test Score',
                    xaxis=dict(range=[score_min, score_max + 1]), # add 1 to show the max label
                    yaxis=dict(range=[score_min, score_max + 1]), # add 1 to show the max label
                )

                st.plotly_chart(figure, width='stretch', height=400)
                st.caption('Points above the dashed line improved; below regressed.')

            except:
                st.error('**RUNTIME ERROR**: Scatter plot generation error.')
        else:
            figure = go.Figure()
            figure.add_trace(
                go.Scatter(
                    x=[0, 100], y=[0, 100],
                    mode='lines',
                    line=dict(color='white', dash='dash', width=1),
                    name='No Change',
                )
            )

            figure.add_trace(
                go.Scatter(
                    x=[0], y=[100],
                    mode='markers',
                    marker=dict(color='#a3d1fe', size=8, opacity=1),
                    text='student',
                    hovertemplate='<b>%{text}</b><br>Pre-test score: %{x}<br>Post-test score: %{y}<extra></extra>',
                    name='Students',
                )
            )

            figure.update_layout(
                xaxis_title='Pre-test Score',
                yaxis_title='Post-test Score',
                xaxis=dict(range=[0, 101]), # add 1 to show the max label
                yaxis=dict(range=[0, 101]), # add 1 to show the max label
            )

            st.plotly_chart(figure, width='stretch', height=400)
            st.caption('Points above the dashed line improved; below regressed.')

def make_workspace_page(workspace_id: str) -> callable:
    def workspace_page(): # convert workspace_id to a callable that can be used as a page
        workspace_name = st.session_state.workspaces[workspace_id]['name']
        workspace_description  = st.session_state.workspaces[workspace_id]['description']

        st.set_page_config(
            layout='centered',
            page_title=f'{workspace_name} - Project Hinge Point',
            page_icon='res/placeholder_image.png',
        )

        header(workspace_name)

        tabs = st.tabs(
            [
                'Name & Description',
                'File Upload',
                'Metric Summary',
                'Histograms',
                'Box Plot',
                'Scatter Plot',
                'File Export',
            ]
        )

        with tabs[0]:
            st.session_state.workspaces[workspace_id]['name'] = st.text_area(
                label='Enter workspace name here:',
                height=100, width='stretch',
                placeholder='Enter name here...',
                value=workspace_name,
            )

            st.session_state.workspaces[workspace_id]['description'] = st.text_area(
                label='Enter workspace description here:',
                height='content', width='stretch',
                placeholder='Enter description here...',
                value=workspace_description,
            )

        check_header(workspace_name=workspace_name, workspace_id=workspace_id)

        with tabs[1]:
            st.markdown('# File Upload', unsafe_allow_html=True)
            file_upload_and_preview(workspace_id=workspace_id)

        calculate(workspace_id=workspace_id)

        with tabs[2]:
            st.markdown('# Metric Summary', unsafe_allow_html=True)
            key_metrics(workspace_id=workspace_id)
            standard_statistics(workspace_id=workspace_id)

        with tabs[3]:
            st.markdown('# Histograms', unsafe_allow_html=True)
            baseline_histograms(workspace_id=workspace_id)
            comparison_histogram(workspace_id=workspace_id)
        
        with tabs[4]:
            st.markdown('# Box Plot', unsafe_allow_html=True)
            box_plot(workspace_id=workspace_id)

        with tabs[5]:
            st.markdown('# Scatter Plot', unsafe_allow_html=True)
            scatter_plot(workspace_id=workspace_id)

    return workspace_page