import streamlit as st
from datetime import date
import pandas as pd


today = date.today()
end_date = date(2026, 1, 1)
days_left = (end_date - today).days
days_past = (today - date(2025, 1, 1)).days
target_distance = days_past*2740

run_data = pd.read_csv('run_tracker.csv')
total_completed = run_data['distance_ran'].sum()
total_target = 1000000
distance_left = total_target - total_completed
daily_average = round(distance_left / days_left)
distance_delta = total_completed - target_distance
perc_complete = (total_completed/total_target)*100


def input_run(run_data, distance, pace, dt=today):
    '''
    '''
    new_row = pd.DataFrame({'distance_ran': distance,
                            'date_ran': dt,
                            'pace': pace},
                           index=[0])

    run_data = pd.concat([run_data, new_row], ignore_index=True)
    run_data.to_csv('run_tracker.csv', index=False)
    st.rerun()


@st.dialog('Input your Run', width='large')
def input_runs():

    distance = st.pills('Distance', ['3km', '5km', '6km',
                                     '7km', '10km', 'custom'],
                        label_visibility='visible')

    if distance == 'custom':
        distance = st.number_input('Custom Distance (m)',
                                   step=1)

    run_date = st.date_input('Run Date', label_visibility='visible')
    pace = st.text_input("Pace (eg: 6'50'')", label_visibility='visible')

    if st.button('Submit', use_container_width=True):
        input_run(run_data,
                  int(str(distance).replace('km', '000')),
                  pace,
                  run_date)


st.title('Toby\'s 2025 NY Resolution Tracker')

st.success('I aim to run 1 million meters in 2025')

left, middle, right = st.columns(3)

left.metric('Days Left', '{:,}'.format(days_left),
            border=True)
middle.metric('Distance Left', '{:,} m'.format(distance_left),
              border=True)
right.metric('Daily Average Left', '{:,} m'.format(daily_average),
             border=True)

left, middle, right = st.columns(3)

left.metric('Distance Ran', '{:,} m'.format(total_completed),
            border=True)
right.metric('Expected Distance', '{:,} m'.format(target_distance),
             border=True)
middle.metric('Distance Delta', '{:,} m'.format(distance_delta),
              border=True)

st.progress(perc_complete/100, 'Distance Ran')

distance = None
if st.button('Input Run', use_container_width=True):
    input_runs()
