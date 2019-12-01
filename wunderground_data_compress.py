import pandas
import glob
import os

station_array = ['KCLT', 'KLGA', 'KSFO', 'KMIA', 'KPHL', 'KATL', 'KLAX', 'KORD', 'KJFK', 'KDCA']


def compress_data(cur_station):
    path = os.path.dirname(__file__);
    all_files = glob.glob(path + "/" + cur_station + "_csv/*.csv")

    li = []

    for file_handle in all_files:
        df = pandas.read_csv(file_handle, index_col=None, header=0)
        li.append(df)
    frame = pandas.concat(li, axis=0, ignore_index=True)
    new_frame = pandas.DataFrame(frame)

    # new_frame['date'] = pandas.to_datetime(new_frame.date)
    sorted_frame = new_frame.sort_values(by=['year', 'month', 'day'])
    sorted_frame.to_csv('./' + cur_station + '_csv/' + cur_station + '.csv')


for station in station_array:
    print("Compressing station: " + station)
    compress_data(station)
print("Compression of data completed!")


