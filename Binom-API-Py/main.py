import requests
import argparse
import csv
import calendar
import time

# args
parser = argparse.ArgumentParser()
parser.add_argument('--month', help='Month', type=int, required=True)
parser.add_argument('--year', help='Year', type=int, required=True)
parser.add_argument('--camp_from', help='Campaign from', type=int, required=True)
parser.add_argument('--camp_to', help='Campaign to', type=int, required=True)
parser.add_argument('--camp_add', help='Campaign additional', required=False)
parser.add_argument('--filename', help='File name', required=False)
args = parser.parse_args()

print('Run by params: Month {}, Year {}, Camp From {}, Camp To {}, Camp Add {}, Filename {}'
      .format(args.month, args.year, args.camp_from, args.camp_to, args.camp_add, args.filename))

# constants
SERVICE_LINK = 'https://jump-track.com/panel.php'
API_KEY = '$$$$$$$$$$$$$$$$$$$$'
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

CSV_DIRECTORY = 'csv'
CAMPS_SPLIT_COUNT = 200
FIRST_PAGE = 1
DATE_FILTER_TYPE = 12
INVALID_VALUES = ['tst', 'test', 'advertorial']


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

# makes api request TODO camp_id=
def make_request(date: str, camps: list) -> list:
    payload = {
        'page': 'Stats',
        'camps': ','.join("{0}".format(n) for n in camps),
        'group1': 33,  # by campaigns
        'group2': 19,  # by lands
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

# split all campaigns numbers to the little chunk
def split_camps() -> list:
    camp_from = args.camp_from
    camp_to = args.camp_to
    camp_add = args.camp_add
    if camp_from > camp_to:
        raise Exception('camp_from can not be more or equal then camp_to.')

    all_values = list(range(camp_from, camp_to + 1))

    # adds values from additional camps param
    if camp_add is not None and camp_add != "" and not camp_add:
        for t_num in camp_add.split(','):
            t = int(t_num.strip())
            if t not in all_values:
                all_values.append(t)

    return [all_values[i: i + CAMPS_SPLIT_COUNT] for i in range(0, len(all_values), CAMPS_SPLIT_COUNT)]


def get_traffic_source(name: str, mb: str) -> str:
    if mb == 'Internal':
        return 'BackButton Internal'

    return name.strip().partition("-")[0].partition("(")[0].strip()


def get_traffic_type(item_id: int, name: str, mb: str, split_name: list, traffic_source: str) -> str:
    if item_id == 7 or mb == 'Internal':
        return 'Internal'
    if traffic_source == 'Audience_serv':
        return 'Email'
    if traffic_source == 'Twitter':
        return 'Social'
    if 'Native' and not ('Fee' or 'Fees') in name:
        return 'Native'
    if 'Fee' or 'Fees' in name:
        return 'Fee'

    return split_name[0].strip().partition("(")[0].strip()

def get_mb(campaign_name: str):
    camp_name_split = campaign_name.split('-')
    mb = camp_name_split[len(camp_name_split) - 1].strip().replace('(upsell)', '').strip()  # MB

    if mb == 'General':
        return 'Internal'

    return mb


def format_data(data: list, date: str) -> list:
    result = []

    for item in data:
        level = item['level'].strip()

        if level == '1':
            split_name = list(map(str.strip, item['name'].split('-')))
            item_id = item['name'].strip().partition("(id:")[2].rstrip(')')  # ID
            campaign_name = item['name'].partition("(id")[0].strip()  # Campaign
            mb = get_mb(campaign_name)  # MB
            traffic_source = get_traffic_source(item['name'], mb)
            traffic_type = get_traffic_type(item_id, item['name'], mb, split_name, traffic_source)  # Traffic.Type

            continue

        if level == '2':
            country = item['name']  # Country
            top = get_top(country)
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

            if has_incorrect_values([mb, traffic_source, campaign_name], cost):
                print('Skipped - ' + 'MB:' + mb + ' | TS: ' + traffic_source + ' | Camp: ' + campaign_name + ' | Cost: '
                      + cost)
                continue

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


def has_incorrect_values(values: list, cost: str) -> bool:
    for invalid_value in INVALID_VALUES:
        for value in values:
            if invalid_value in value.lower() and float(cost) <= 0:
                return True

    return False


def get_filename() -> str:
    if len(args.filename) > 0:
        return './' + CSV_DIRECTORY + '/' + args.filename + '.csv'

    month_name = calendar.month_name[args.month]
    year = str(args.year)

    return './' + CSV_DIRECTORY + '/' + month_name + '_' + year + '.csv'


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
        camps = split_camps()
        count = len(camps)
        print('Day: ' + str(day+1)+' Expected queries count: '+str(count))

        # iterate every campaigns chunk [ [7,8,9], [10,11,12], ... ]
        for camp in camps:
            request_date = get_date(day+1)  # +1 because the range func returns range starts from 0
            data = make_request(request_date, camp)
            queries += 1
            if not data:
                count -= 1
                continue

            for item in format_data(data, request_date):
                file.writer.writerow(item)
            count -= 1

    file.close()

    print("... %s seconds" % (time.time() - start_time))
    print('Queries: '+str(queries))
    print('\n')


create_csv()