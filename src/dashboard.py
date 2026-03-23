import streamlit as st
import pandas as pd
import numpy as np # used for calculation and aggregation
import plotly.graph_objects as go

st.set_page_config(
    layout='centered',
    page_title='Dashboard - Project Hinge Point',
    page_icon='res/placeholder_image.png',
)

def get_workspaces() -> None:
    if 'workspaces' not in st.session_state:
        st.session_state.workspaces = {}

def get_active_workspaces() -> list[dict]:
    active_workspaces = []
    for workspace_id, workspace_data in st.session_state.workspaces.items():
        dataframe_statistics = workspace_data.get('dataframe_statistics', {})
        cohens_d = dataframe_statistics.get('cohens_d')

        if cohens_d is not None: # if calculations have been done, then the workspace is active
            active_workspaces.append({'workspace_id': workspace_id, 'workspace_data': workspace_data})

    return active_workspaces

def get_aggregate_statistics(workspaces: list[dict]) -> dict:
    total_students, total_improved, total_unchanged, total_regressed = 0, 0, 0, 0
    cohens_d_values, above_hinge_count = [], 0
    for workspace in workspaces:
        total_students   += workspace['workspace_data']['dataframe_statistics']['sample_size']
        total_improved   += workspace['workspace_data']['dataframe_statistics']['students_improved']
        total_unchanged  += workspace['workspace_data']['dataframe_statistics']['students_unchanged']
        total_regressed  += workspace['workspace_data']['dataframe_statistics']['students_regressed']
        cohens_d_values.append(workspace['workspace_data']['dataframe_statistics']['cohens_d'])

        if workspace['workspace_data']['dataframe_statistics']['is_above_hinge']:
            above_hinge_count += 1

    mean_cohens_d = float(np.mean(cohens_d_values))

    return {
        'total_students':    total_students,
        'total_improved':    total_improved,
        'total_unchanged':   total_unchanged,
        'total_regressed':   total_regressed,
        'mean_cohens_d':     mean_cohens_d,
        'above_hinge_count': above_hinge_count,
        'workspace_count':   len(workspaces),
    }

def header() -> None:
    st.markdown('# Dashboard', unsafe_allow_html=True)
    st.markdown('Aggregate view across all workspaces with loaded datasets.', unsafe_allow_html=True)

def no_data_guard(workspaces: list[dict]) -> bool:
    if not st.session_state.get('workspaces'):
        st.info('**INFORMATION**: No workspaces exist yet. Create one from the sidebar to get started.')
        return True
    if not workspaces:
        st.warning('**WARNING**: No workspaces have loaded or detected datasets.')
        return True
    return False

def delta_zero_color(delta_zero_color: str, inverse: bool, value, zero) -> str: # the color of delta at 0
    if delta_zero_color == 'green':
        if value == zero: return 'green'
    elif delta_zero_color == 'red':
        if value == zero: return 'red'
    else:
        if value == zero: return 'off'
    if inverse: return 'inverse'
    else:       return 'normal'

def aggregate_metrics_panel(aggregate_metrics: dict) -> None:
    with st.container(border=True):
        st.markdown('## Aggregate Overview', unsafe_allow_html=True)

        col_1, col_2 = st.columns(2)
        col_3, col_4 = st. columns(2)
        try:
            col_1.metric(
                label='Number of Active Workspaces',
                value=aggregate_metrics['workspace_count'],
                border=True,
            )
        except:
            st.error('**RUNTIME ERROR**: Workspace count metric error.')

        try:
            col_2.metric(
                label='Total Number of Students (NET x)', # SYMBOL NEEDED ===================================================
                value=aggregate_metrics['total_students'],
                border=True,
            )
        except:
            st.error('**RUNTIME ERROR**: Total students metric error.')

        try:
            col_3.metric(
                label='Mean Effect Size (d̄)',
                value=f'{aggregate_metrics['mean_cohens_d']:.2f}',
                delta=f'{aggregate_metrics['mean_cohens_d'] - 0.40:.2f} from hinge',
                delta_color=delta_zero_color(
                    delta_zero_color='green',
                    inverse=False,
                    value=aggregate_metrics['mean_cohens_d'],
                    zero=0.40,
                ),
                border=True,
            )
        except:
            st.error('**RUNTIME ERROR**: Average effect size metric error.')

        try:
            workspaces_above_hinge = aggregate_metrics['above_hinge_count']
            total_workspaces = aggregate_metrics['workspace_count']
            col_4.metric(
                label='Number of Workspaces Above Hinge Point',
                value=workspaces_above_hinge,
                delta=f'{workspaces_above_hinge} / {total_workspaces} ({workspaces_above_hinge / total_workspaces * 100:.2f}%)',
                delta_color=delta_zero_color(
                    delta_zero_color='green',
                    inverse=False,
                    value=workspaces_above_hinge,
                    zero=0,
                ),
                border=True,
            )
        except:
            st.error('**RUNTIME ERROR**: Above hinge metric error.')

        col_5, col_6, col_7 = st.columns(3)
        try:
            students_improved = aggregate_metrics['total_improved']
            students_total = aggregate_metrics['total_students']
            col_5.metric(
                label='Students that Improved',
                value=students_improved,
                delta=f'{students_improved} / {students_total} ({students_improved / students_total * 100:.2f}%)',
                delta_color=delta_zero_color(
                    delta_zero_color='red',
                    inverse=False,
                    value=students_improved,
                    zero=0,
                ),
                border=True,
            )
        except:
            st.error('**RUNTIME ERROR**: Students improved metric error.')

        try:
            students_unchanged = aggregate_metrics['total_unchanged']
            col_6.metric(
                label='Students Unchanged',
                value=students_unchanged,
                delta=f'{students_unchanged} / {students_total} ({students_unchanged / students_total * 100:.2f}%)',
                delta_color=delta_zero_color(
                    delta_zero_color='green',
                    inverse=True,
                    value=students_unchanged,
                    zero=0,
                ),
                border=True,
            )
        except:
            st.error('**RUNTIME ERROR**: Students unchanged metric error.')

        try:
            students_regressed = aggregate_metrics['total_regressed']
            col_7.metric(
                label='Students that Regressed',
                value=students_regressed,
                delta=f'{students_regressed} / {students_total} ({students_regressed / students_total * 100:.2f}%)',
                delta_color=delta_zero_color(
                    delta_zero_color='green',
                    inverse=True,
                    value=students_regressed,
                    zero=0,
                ),
                border=True,
            )
        except:
            st.error('**RUNTIME ERROR**: Students regressed metric error.')

def effect_size_comparison_panel(workspaces: list[dict]) -> None:
    with st.container(border=True):
        st.markdown('## Effect Size Comparison', unsafe_allow_html=True)
        st.markdown("Effect size per workspace. The dashed line marks Hattie's 0.40 hinge point.", unsafe_allow_html=True)

        try:
            workspace_names = []
            cohens_d_values = []
            for workspace in workspaces:
                workspace_names.append(workspace['workspace_data']['name'])
                cohens_d_values.append(workspace['workspace_data']['dataframe_statistics']['cohens_d'])

            colors = []
            for cohens_d in cohens_d_values:
                if cohens_d >= 0.4:
                    colors.append('#83a2c2')
                else:
                    colors.append('#a3d1fe')

            figure_text = []
            for cohens_d in cohens_d_values:
                figure_text.append(f'{cohens_d:.2f}')

            figure = go.Figure()
            figure.add_trace(
                go.Bar(
                    x=workspace_names, y=cohens_d_values,
                    marker_color=colors,
                    text=figure_text,
                    textposition='outside',
                    name='Effect Size',
                )
            )

            figure.add_hline(
                y=0.40,
                line_dash='dash', line_color='white',
                annotation_text='Hinge Point (0.40)',
                annotation_position='top right',
            )

            figure.update_layout(
                xaxis_title='Workspace', yaxis_title='Effect Size',
                height=350,
                showlegend=False,
                yaxis=dict(gridcolor='#3a3a3a'),
            )

            st.plotly_chart(figure, width='stretch')
        except:
            st.error('**RUNTIME ERROR**: Effect size comparison chart error.')

def pre_post_mean_panel(workspaces: list[dict]) -> None:
    with st.container(border=True):
        st.markdown('## Pre- vs. Post-test Means', unsafe_allow_html=True)
        st.markdown('Grouped bar chart showing the mean score shift per workspace.', unsafe_allow_html=True)

        try:
            workspace_names, pre_means, post_means = [], [], []
            for workspace in workspaces:
                workspace_names.append(workspace['workspace_data']['name'])
                pre_means.append(workspace['workspace_data']['pre_score_statistics']['pre_mean'])
                post_means.append(workspace['workspace_data']['post_score_statistics']['post_mean'])

            figure = go.Figure()

            figure_text_list_1 = []
            for pre_mean in pre_means:
                figure_text_list_1.append(f'{pre_mean:.2f}')

            figure.add_trace(
                go.Bar(
                    name='Pre-',
                    x=workspace_names, y=pre_means,
                    marker_color='#a3d1fe',
                    text=figure_text_list_1,
                    textposition='outside',
                )
            )

            figure_text_list_2 = []
            for post_mean in post_means:
                figure_text_list_2.append(f'{post_mean:.2f}')

            figure.add_trace(
                go.Bar(
                    name='Post-',
                    x=workspace_names, y=post_means,
                    marker_color='#005cb8',
                    text=figure_text_list_2,
                    textposition='outside',
                )
            )

            figure.update_layout(
                barmode='group',
                xaxis_title='Workspace',
                yaxis_title='Mean Score',
                height=350,
                legend_title_text='Assessment',
                yaxis=dict(gridcolor='#3a3a3a'),
            )

            st.plotly_chart(figure, width='stretch', height=375)
        except:
            st.error('**RUNTIME ERROR**: Pre/post mean comparison chart error.')

def student_outcome_panel(workspaces: list[dict]) -> None:
    with st.container(border=True):
        st.markdown('## Student Outcome Breakdown', unsafe_allow_html=True)
        st.markdown('Proportion of students who improved, unchanged, or regressed per workspace.', unsafe_allow_html=True)

        try:
            students_improved, students_unchanged, students_regressed = [], [], []
            workspace_names, sample_sizes = [], []
            for workspace in workspaces:
                workspace_names.append(workspace['workspace_data']['name'])
                students_improved.append(workspace['workspace_data']['dataframe_statistics']['students_improved'])
                students_unchanged.append(workspace['workspace_data']['dataframe_statistics']['students_unchanged'])
                students_regressed.append(workspace['workspace_data']['dataframe_statistics']['students_regressed'])
                sample_sizes.append(workspace['workspace_data']['dataframe_statistics']['sample_size'])

            imp_pct = [i / n * 100 for i, n in zip(students_improved, sample_sizes)]
            unc_pct = [u / n * 100 for u, n in zip(students_unchanged, sample_sizes)]
            reg_pct = [r / n * 100 for r, n in zip(students_regressed, sample_sizes)]

            fig = go.Figure()

            fig.add_trace(go.Bar(
                name='Improved',
                x=workspace_names, y=imp_pct,
                marker_color='#5ae086',
                text=[f'{v:.0f}%' for v in imp_pct],
                textposition='inside',
            ))

            fig.add_trace(go.Bar(
                name='Unchanged',
                x=workspace_names, y=unc_pct,
                marker_color='#7c7c7c',
                text=[f'{v:.0f}%' for v in unc_pct],
                textposition='inside',
            ))

            fig.add_trace(go.Bar(
                name='Regressed',
                x=workspace_names, y=reg_pct,
                marker_color='#ff6c6c',
                text=[f'{v:.0f}%' for v in reg_pct],
                textposition='inside',
            ))

            fig.update_layout(
                barmode='stack',
                xaxis_title='Workspace',
                yaxis_title='% of Students',
                yaxis=dict(range=[0, 100], ticksuffix='%', gridcolor='#3a3a3a'),
                height=320,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend_title_text='Outcome',
            )

            st.plotly_chart(fig, use_container_width=True)

        except:
            st.error('**RUNTIME ERROR**: Student outcome chart error.')

def workspace_summary_table(workspaces: list[dict]) -> None:
    with st.container(border=True):
        st.markdown('## Workspace Summary Table', unsafe_allow_html=True)

        try:
            rows = []
            for w in workspaces:
                ds  = w['workspace_data']['dataframe_statistics']
                pre = w['workspace_data']['pre_score_statistics']
                pst = w['workspace_data']['post_score_statistics']
                rows.append({
                    'Workspace':        w['workspace_data']['name'],
                    'n':                ds.get('sample_size'),
                    'Pre Mean':         f"{pre.get('pre_mean', 0):.2f}",
                    'Post Mean':        f"{pst.get('post_mean', 0):.2f}",
                    'Δ Mean':           f"{ds.get('mean_diff', 0):.2f}",
                    'Pre SD':           f"{pre.get('pre_std', 0):.2f}",
                    'Post SD':          f"{pst.get('post_std', 0):.2f}",
                    'Pooled SD':        f"{ds.get('pooled_std', 0):.2f}",
                    "Cohen's d":        f"{ds.get('cohens_d', 0):.2f}",
                    '≥ Hinge (0.40)':   '✓' if ds.get('is_above_hinge') else '✗',
                    'Improved':         ds.get('students_improved'),
                    'Unchanged':        ds.get('students_unchanged'),
                    'Regressed':        ds.get('students_regressed'),
                })

            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

        except:
            st.error('**RUNTIME ERROR**: Workspace summary table error.')

if __name__ == '__main__':
    get_workspaces()
    header()

    active_workspaces = get_active_workspaces()
    if not no_data_guard(active_workspaces):
        aggregate_metrics = get_aggregate_statistics(active_workspaces)
        aggregate_metrics_panel(aggregate_metrics)

        col_left, col_right = st.columns([3, 4])
        with col_left:
            effect_size_comparison_panel(active_workspaces)
        with col_right:
            pre_post_mean_panel(active_workspaces)

        student_outcome_panel(active_workspaces)
        workspace_summary_table(active_workspaces)