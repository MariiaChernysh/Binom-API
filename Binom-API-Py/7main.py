import requests
import argparse
import csv
import calendar
import time

# args
parser = argparse.ArgumentParser()
parser.add_argument('--month', help='Month', type=int, required=True)
parser.add_argument('--year', help='Year', type=int, required=True)
parser.add_argument('--camp_id', help='Campaign from', type=int, required=True)
parser.add_argument('--filename', help='File name', required=False)
args = parser.parse_args()

print('Run by params: Month {}, Year {}, Camp ID {}, Filename {}'
      .format(args.month, args.year, args.camp_id, args.filename))

# constants
SERVICE_LINK = 'https://jump-track.com/panel.php'
API_KEY = '$$$$$$$$$$$$$$'
#old '$$$$$$$$$$$$$$'
CSV_NAMES = ['ID', 'Date', 'Campaign', 'Country', 'Visits', 'Clicks', 'Leads', 'Deposit', 'Revenue', 'Cost',
             'Profit', 'MB', 'Traffic.Source', 'Traffic.Type', 'Top']

# TODO: DACH, UK, LATAM, GCC
TOP1 = {'IE': 'Ireland', 'CH': 'Switzerland', 'DE': 'Germany', 'AT': 'Austria', 'NO': 'Norway', 'SE': 'Sweden',
        'FI': 'Finland', 'IS': 'Iceland', 'NL': 'Netherlands', 'LU': 'Luxembourg', 'LI': 'Liechtenstein',
        'BH': 'Bahrain', 'OM': 'Oman', 'SG': 'Singapore', 'HK': 'Hong Kong', 'ES': 'Spain',
        'AU': 'Australia', 'MY': 'Malaysia', 'QA': 'Qatar', 'AE': 'United Arab Emirates', 'KW': 'Kuwait',
        'NZ': 'New Zealand', 'DK': 'Denmark', 'GB': 'United Kingdom', 'UK': 'United Kingdom', 'GCC': 'GCC',
        'DACH': 'DACH'}
TOP2 = {'IT': 'Italy', 'PT': 'Portugal', 'HU': 'Hungary', 'CL': 'Chile', 'MT': 'Malta',
        'EC': 'Ecuador', 'SV': 'El Salvador', 'MC': 'Monaco', 'BN': 'Brunei Darussalam',
        'PE': 'Peru', 'GT': 'Guatemala', 'MX': 'Mexico', 'CA': 'Canada', 'EE': 'Estonia',
        'LT': 'Lithuania', 'LV': 'Latvia', 'TH': 'Thailand', 'BE': 'Belgium', 'HR': 'Croatia',
        'SA': 'Saudi Arabia', 'KR': 'Korea, Republic of'}
TOP3 = {'TR': 'Turkey', 'PA': 'Panama', 'UY': 'Uruguay', 'TW': 'Taiwan, Province of China', 'KZ': 'Kazakhstan',
        'ID': 'Indonesia', 'BR': 'Brazil', 'SI': 'Slovenia', 'SK': 'Slovakia', 'PL': 'Poland', 'ZA': 'South Africa',
        'CO': 'Colombia', 'CZ': 'Czechia', 'FR': 'France', 'VN': 'Viet Nam', 'SB': 'Solomon Islands', 'RO': 'Romania',
        'GR': 'Greece', 'BS': 'Bahamas', 'AR': 'Argentina', 'JP': 'Japan', 'RU': 'Russian Federation',
        'CR': 'Costa Rica', 'SM': 'San Marino', 'BO': 'Bolivia, Plurinational State of', 'PY': 'Paraguay',
        'KY': 'Cayman Islands', 'TT': 'Trinidad and Tobago', 'CN': 'China', 'BB': 'Barbados', 'BM': 'Bermuda',
        'PH': 'Philippines', 'IN': 'India', 'KE': 'Kenya', 'RS': 'Serbia', 'US': 'United States', 'UA': 'Ukraine',
        'LATAM': 'LATAM', 'LaTaM': 'LATAM', 'latam': 'LATAM', 'Latam': 'LATAM'}

MB_DICT = {'ap': 'AP', 'vy': 'VY', 'VY': 'VY', 'oz': 'OZ', 'at': 'AT', 'AT': 'AT', 'rs': 'RS', 'vg': 'VG', 'ss': 'SS'}

CSV_DIRECTORY = 'csv'
CAMPS_SPLIT_COUNT = 200
FIRST_PAGE = 1
DATE_FILTER_TYPE = 12

# receives number of a day and returns the date, format: 2020-10-20
def get_date(day: int,) -> str:
    if day <= 9:
        day = '0' + str(day)
    return str(args.year) + '-' + str(args.month) + '-' + str(day)

def get_top(country: str) -> str:
    if country in TOP1.values():
        return 'Top1'
    if country in TOP2.values():
        return 'Top2'
    if country in TOP3.values():
        return 'Top3'
    return 'false'

def get_mb(split: str) -> str:
    mediab = {*MB_DICT.values()}
    mdb = {**MB_DICT}

    if split in MB_DICT.keys():
        return MB_DICT[split]
    if split not in MB_DICT.keys():
        return 'Internal'

# makes api request TODO camp_id=
def make_request(date: str) -> list:
    payload = {
        'page': 'Stats',
        'camp_id': 7,
        'group1': 19,  # by campaigns
        'group2': 27,  # by lands
        'group3': 1,  # by offers
        'date': DATE_FILTER_TYPE,  # for date_s and date_e with an additional query, format [YYYY]-[MM]-[DD]
        'date_s': date,  # start date
        'date_e': date,  # end date
        'timezone': '0:00',  # UTC
        'num_page': FIRST_PAGE,
        'val_page': 'All',  # pagination, means get all data from all pages in one time
        'api_key': API_KEY
    }

    # request
    response = requests.get(SERVICE_LINK, params=payload)
    response_content = response.json()
    if response.status_code != 200:
        return []

    if response_content == 'null' or response_content == 'no_clicks' or response_content is None:
        return []

    if 'status' in response_content and response_content['status'] == 'error':
        return []

    return response_content

def format_data(data: list, date: str) -> list:
    result = []

    for item in data:
        level = item['level'].strip()

        if level == '1':
            country = item['name']  # Country
            top = get_top(country)
            item_id = '7'  # ID
            campaign_name = 'Back Button - 10247 - Bitcoin Era - General'  # Campaign
            traffic_type = 'Internal'  # Traffic.Type
            traffic_source = 'BackButton Internal'

            continue

        if level == '2':
            split=item['name']
            mb = get_mb(split)  # MB
            clicks = item['clicks']
            lp_clicks = item['lp_clicks']  # LP_Clicks
            leads = item['leads']  # Leads
            cost = item['cost']  # Cost
            revenue = item['revenue']  # Revenue
            a_leads = item['a_leads']  # FTDs

            try:
                profit = float(revenue) - float(cost)
            except IndexError:
                print('Calculation error, values: revenue' + revenue + ' cost' + cost)

            result.append([
                item_id,
                date,
                campaign_name,
                country,
                clicks,
                lp_clicks,
                leads,
                a_leads,
                revenue,
                cost,
                profit,
                mb,
                traffic_source,
                traffic_type,
                top
            ])

    return result

def get_filename() -> str:
    if len(args.filename) > 0:
        return './' + CSV_DIRECTORY + '/' + args.filename + '_7.csv'

    month_name = calendar.month_name[args.month]
    year = str(args.year)

    return './' + CSV_DIRECTORY + '/' + month_name + '_' + year + '_7.csv'

def create_csv():
    start_time = time.time()
    queries = 0

    days_number = calendar.monthrange(args.year, args.month)[1]  # it's like 28 or 31

    # create csv file
    file = open(get_filename(), "w", newline='', encoding='utf-8')
    file.writer = csv.writer(file, delimiter=',')
    file.writer.writerow(CSV_NAMES)

    # iterate every day in month
    for day in range(days_number):
        print('Request: '+ str(args.year) + '-' + str(args.month)+ '-' + str(day+1))
        request_date = get_date(day+1)  # +1 because the range func returns range starts from 0
        data = make_request(request_date)
        queries += 1

        if not data:
            continue

        for item in format_data(data, request_date):
            file.writer.writerow(item)

    file.close()

    print("... %s seconds" % (time.time() - start_time))
    print('Queries: '+str(queries))
    print('\n')

create_csv()


