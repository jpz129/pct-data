import pandas as pd
from gpx_converter import Converter
from haversine import haversine, Unit
import glob


def _get_filenames(update_dir):
    update_dir = update_dir + '/*.gpx'
    filenames = glob.glob(update_dir)
    return filenames


def _transform_gpx_data(filenames):
    df_list = []
    for filename in filenames:
        # Load the GPX data from the file into a dataframe
        df = (Converter(input_file=filename)
              .gpx_to_dataframe())

        # Convert the 'time' column to the Pacific timezone
        df['time'] = df['time'].apply(lambda x: x.tz_convert('US/Pacific'))

        # Calculate the time difference between consecutive rows
        df['seconds_delta'] = (((df['time'].shift(-1)-df['time'])
                                .fillna(pd.Timedelta(seconds=0))
                                .astype(int)/1000000000)
                               .astype(int))

        # Extract human-readable date and time from the 'time' column
        df['human_date'] = df['time'].dt.strftime('%Y-%m-%d')
        df['human_time'] = df['time'].dt.strftime('%I:%M:%S %p')

        # Convert altitude from meters to feet and round to an integer
        df['altitude_feet'] = round(df['altitude'] * 3.280839895).astype('int')

        # Calculate the distance and altitude change between consecutive rows
        for i in range(df.shape[0]-1):
            start = df.at[i, 'latitude'], df.at[i, 'longitude']
            end = df.at[i+1, 'latitude'], df.at[i+1, 'longitude']
            distance = round(haversine(start, end, unit=Unit.FEET), 1)
            df.at[i, 'distance_feet'] = distance

            altitude_change = df.at[i+1,
                                    'altitude_feet'] - df.at[i, 'altitude_feet']
            df.at[i, 'altitude_change'] = altitude_change

        # Calculate speed in mph
        df['speed_mph'] = (
            (df['distance_feet'] / df['seconds_delta']) * (3600/5280)).round(1)

        # Select columns to return in the final dataframe
        df = df[['time', 'human_date', 'human_time', 'seconds_delta',
                'latitude', 'longitude', 'altitude_feet',
                 'distance_feet', 'speed_mph',
                 'altitude_change']].copy()

        df_list.append(df)

    return pd.concat(df_list)


def _save_data_name(data, update_dir):
    min_date = data['time'].min()
    max_date = data['time'].max()
    save_name = f'{min_date}---{max_date}.csv'
    save_name = f'{update_dir}/{save_name}'
    return save_name


def main(update_dir='data/update1'):
    filenames = _get_filenames(update_dir)
    df = _transform_gpx_data(filenames)
    save_name = _save_data_name(df, update_dir)
    df.to_csv(save_name, index=False)
    print(df.head())
    print('===============')
    print(df.info())


if __name__ == '__main__':
    main()
