import pandas as pd
import matplotlib.pyplot as plt

import pm4py
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.statistics.sojourn_time.log import get as soj_time_get
from pm4py.objects.log.util import interval_lifecycle
from pm4py.visualization.process_tree import visualizer as pt_visualizer


def mine_process(log):
    net, im, fm = pm4py.discover_petri_net_inductive(log, 0.2)
    pm4py.view_petri_net(net, im, fm)

    tree = pm4py.convert_to_process_tree(net, im, fm)
    pm4py.view_process_tree(tree, format='png')


def analyze_performance(log):

    # Gets durations of all traces in the log (in seconds). Then, we convert the times to days by dividing by 86400.
    all_case_durations = case_statistics.get_all_case_durations(log, parameters={
        case_statistics.Parameters.TIMESTAMP_KEY: "time:timestamp"})

    x = range(1, len(all_case_durations) + 1)
    d = {'Traces': x, 'Durations': all_case_durations}
    trace_df = pd.DataFrame(data=d)

    # trace_df now contains the traces of the log with their corresponding durations
    # dataframe statistics

    pm4py.view_performance_spectrum(log, ["transport_to_track_1", "transport_to_cell_1",
                                          "operation_on_cell_1", "transport_to_cell_2",
                                          "operation_on_cell_2", "transport_to_track_2"], format="png")

    print(trace_df['Durations'].describe())
    plot = trace_df.plot(x="Traces", y="Durations", kind="hist", legend=False, title="Histogram of trace durations",
                         bins=30)
    plot.set_ylabel("Number of traces")
    plot.set_xlabel("Duration (in days)")
    plt.savefig('traces_hist.png', facecolor='white')


def analyze_service_time(log):
    soj_time = soj_time_get.apply(log, parameters={soj_time_get.Parameters.TIMESTAMP_KEY: "time:timestamp",
                                                   soj_time_get.Parameters.START_TIMESTAMP_KEY: "start_timestamp"})
    plt.xticks(rotation=-10)
    plt.bar(soj_time.keys(), soj_time.values())
    # plt.savefig('service_hist.png', facecolor='white')
    # pm4py.view_dotted_chart(log, format="png")


def analyze_waiting_time(log):
    enriched_log = interval_lifecycle.assign_lead_cycle_time(log)
    print(enriched_log)


if __name__ == '__main__':
    dataframe = pd.read_csv('./event_log.csv', sep=',')
    dataframe = pm4py.format_dataframe(dataframe, case_id='case:concept:name', activity_key='concept:name',
                                       timestamp_key='time:timestamp')
    dataframe_start = dataframe[dataframe['start_timestamp'] == 'start'].drop(['start_timestamp'], axis=1)
    dataframe_start.rename(columns={'time:timestamp': 'start_timestamp'}, inplace=True)
    dataframe_end = dataframe[dataframe['start_timestamp'] == 'end'].drop(['start_timestamp'], axis=1)
    dataframe = pd.merge(dataframe_start, dataframe_end,  how='left',
                                         left_on=['case:concept:name', 'concept:name'],
                                         right_on=['case:concept:name', 'concept:name'])
    event_log = pm4py.convert_to_event_log(dataframe)
    mine_process(event_log)
    analyze_performance(event_log)
    analyze_service_time(event_log)
    analyze_waiting_time(event_log)
