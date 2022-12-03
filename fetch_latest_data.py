import datetime
import os

import pandas as pd


'''
Common args for reading this data
into a pandas df across scripts and notebooks

The state's numbered agency codes would contain duplicates
if cast to integers -- e.g. `010` is the governor's
office and `10` is the Department of Labor and
Regulation -- so always need to import agency codes as strings
'''
csv_read_settings = {
    'parse_dates': ['document_date', 'ap_payment_date'],
    'infer_datetime_format': True,
    'encoding': 'utf-8',
    'dtype': {'agency': str}
}


def get_latest():

    this_year = datetime.date.today().year
    base_url = 'http://bfm.sd.gov/ledger'

    urls = {
        this_year: f'{base_url}/CheckbookDetailCurrentYear.csv',
        this_year-1: f'{base_url}/CheckbookDetailPriorYear1.csv',
        this_year-2: f'{base_url}/CheckbookDetailPriorYear2.csv'
    }

    cumulative_file = 'sd-vendor-checkbook.csv'

    print('Fetching data from state website ...')

    # read data from three remote files into a df
    df_new = pd.concat([pd.read_csv(urls[x], **csv_read_settings) for x in urls])  # noqa

    print(f'New file: {len(df_new):,} records')

    # create local cumulative file if it doesn't exist
    if not os.path.exists(cumulative_file):
        df_new.to_csv(cumulative_file, index=False)

    # load cumulative file
    df_cumulative = pd.read_csv(cumulative_file, **csv_read_settings)
    print(f'Existing cumulative file: {len(df_cumulative):,} records')

    # merge the two data frames
    df = pd.concat([df_cumulative, df_new])

    # drop duplicates
    df.drop_duplicates(inplace=True)

    # per 2022-12-02 email from a state accountant,
    # 032 used to be ag and 20 was environment, and
    # the combined agency is now DANR, 03
    def fix_danr_codes(row):
        if row['agency'] in ['032', '20']:
            return '03'
        else:
            return row['agency']

    df['agency'] = df.apply(fix_danr_codes, axis=1)
    
    print(f'New cumulative file: {len(df):,} records')

    # write back out to file
    df.to_csv(cumulative_file, index=False)

    print()
    print('Done!')


if __name__ == '__main__':
    get_latest()
