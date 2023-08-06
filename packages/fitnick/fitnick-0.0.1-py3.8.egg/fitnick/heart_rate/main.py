from fitnick.heart_rate.time_series import HeartRateTimeSeries
from fitnick.heart_rate.models import heart_intraday_table


def main():
    # HeartRateZone(config={
    #    'base_date': '2020-09-17',
    #    'period': '1d',
    #    'database': 'fitbit'}).insert_heart_rate_time_series_data()

    load_historical_hrz_data()


def load_historical_hrz_data():
    HeartRateTimeSeries(config={
        'database': 'fitbit'}).backfill(period=7)


if __name__ == '__main__':
    load_historical_hrz_data()
