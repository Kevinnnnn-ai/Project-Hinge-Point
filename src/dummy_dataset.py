import streamlit as st
import pandas as pd # for dummy dataframe
import numpy as np # for dummy dataset calculations

def set_dummy_dataset(dummy_dataset: str) -> None:
    dummy_dataframe = pd.read_csv(dummy_dataset) # for simplicity, keep dummy datasets as .csv

    st.session_state.dummy_dataset = {
        'file':      dummy_dataset,
        'dataframe': dummy_dataframe,
        
        # facilitates cross script statistic accessibility (notably, for dashboard.py)
        'dataframe_statistics': {
            'sample_size':        None, 'mean_diff':      None, 'pooled_std':        None, 'cohens_d':           None,
            'hinge_point':        None, 'is_above_hinge': None, 'students_improved': None, 'students_unchanged': None,
            'students_regressed': None,
        },
        'pre_score_statistics': {
            'pre_min': None, 'pre_max': None, 'pre_range': None, 'pre_mean': None,
            'pre_q1':  None, 'pre_q3':  None, 'pre_iqr':   None, 'pre_std':  None,
        },
        'post_score_statistics': {
            'post_min': None, 'post_max': None, 'post_range': None, 'post_mean': None,
            'post_q1':  None, 'post_q3':  None, 'post_iqr':   None, 'post_std':  None,
        },
    }

def calculate() -> None: # no error handling: dummy dataset remains static and is controlled by me
    dataframe = st.session_state.dummy_dataset['dataframe']

    # preliminary
    pre_heading        = dataframe.columns[1] # columns could be named differently, so define it as a numerical location
    post_heading       = dataframe.columns[2]
    pre_scores         = dataframe[pre_heading]
    post_scores        = dataframe[post_heading]
    sample_size        = len(dataframe)
    students_improved  = int((post_scores > pre_scores).sum())
    students_unchanged = int((post_scores == pre_scores).sum())
    students_regressed = int((post_scores < pre_scores).sum())

    # pre-
    pre_min   = pre_scores.min()
    pre_max   = pre_scores.max()
    pre_range = pre_max - pre_min
    pre_mean  = pre_scores.mean()
    pre_q1    = pre_scores.quantile(0.25)
    pre_q3    = pre_scores.quantile(0.75)
    pre_iqr   = pre_q3 - pre_q1
    pre_std   = pre_scores.std()

    # post-
    post_min   = post_scores.min()
    post_max   = post_scores.max()
    post_range = post_max - post_min
    post_mean  = post_scores.mean()
    post_q1    = post_scores.quantile(0.25)
    post_q3    = post_scores.quantile(0.75)
    post_iqr   = post_q3 - post_q1
    post_std   = post_scores.std()

    # primary
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

    # update
    st.session_state.dummy_dataset['dataframe_statistics'].update(
        {
            'students_improved':  students_improved,
            'students_unchanged': students_unchanged,
            'students_regressed': students_regressed,
            'sample_size':        sample_size,
            'mean_diff':          mean_diff,
            'pooled_std':         pooled_std,
            'cohens_d':           cohens_d,
            'hinge_point':        hinge_point,
            'is_above_hinge':     is_above_hinge,
        }
    )

    st.session_state.dummy_dataset['pre_score_statistics'].update(
        {
            'pre_min': pre_max, 'pre_max': pre_max, 'pre_range': pre_range, 'pre_mean': pre_mean,
            'pre_q1':  pre_q1,  'pre_q3':  pre_q3,  'pre_iqr':   pre_iqr,   'pre_std':  pre_std,
        }
    )

    st.session_state.dummy_dataset['post_score_statistics'].update(
        {
            'post_min': post_min, 'post_max': post_max, 'post_range': post_range, 'post_mean': post_mean,
            'post_q1':  post_q1,  'post_q3':  post_q3,  'post_iqr':   post_iqr,   'post_std':  post_std,
        }
    )