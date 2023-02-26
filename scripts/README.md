# GPX Data Converter

This is a Python script that takes **GAIA GPS** GPX files and converts them to a CSV file that you can use to analyze you activity. The output CSV file will contain the following columns for each point in the GPX data:

- time (in Pacific timezone)
- human_date (YYYY-MM-DD format)
- human_time (HH:MM:SS AM/PM format)
- seconds_delta (time difference between consecutive points in seconds)
- latitude
- longitude
- altitude_feet (altitude in feet)
- distance_feet (distance to previous point in feet)
- speed_mph (speed to previous point in miles per hour)
- altitude_change (change in altitude to previous point in feet)

## Requirements

This script requires the following Python packages:

- pandas
- gpx_converter
- haversine

You can install these packages using pip:

```{python} 
pip install pandas gpx_converter haversine
```

## Usage

1. Place your GPX files in a directory.
2. Modify the update_dir variable in main() function of the gpx_data_converter.py file to point to the directory where your GPX files are located.
3. Run the script with the following command: 
```{python}
python gpx_data_converter.py.
```
The output CSV file will be created in the same directory as the GPX files.

## Note
This script only supports GPX files from **GAIA GPS**. It may work with others, but testing has not been done on other GPX data sources.