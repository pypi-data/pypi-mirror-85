from sqlalchemy.orm import sessionmaker
from fitnick.base.base import create_db_engine
from fitnick.heart_rate.heart_rate import get_today_heart_rate_time_series_data, insert_heart_rate_time_series_data


def main():
    get_today_heart_rate_time_series_data(database='fitbit')

    #load_historical_hrz_data()


def load_historical_hrz_data():
    insert_heart_rate_time_series_data(config={
        'base_date': '2020-08-26',
        'end_date': '2020-09-05',
        'database': 'fitbit'
    })


if __name__ == '__main__':
    #main()
    load_historical_hrz_data()
