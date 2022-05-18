import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup

# headers = {
#     'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36',
#     'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
# }

def get_data(url):
    cur_date = datetime.now().strftime('%m_%d_%Y')
    response = requests.get(url=url, headers=headers)
    r = response.text

    # with open(file="index.html", mode='w',encoding="utf-8") as file:
    #     file.write(response.text)

    with open(file='index.html') as file:
        src = file.read()
    
    soup = BeautifulSoup(src, 'lxml')
    table = soup.find('table', id='eag_tx')
    data_th = table.find('thead').find_all('th')

    table_headers = ['Area']

    for dth in data_th:
        dth = dth.text.strip()
        
        table_headers.append(dth)

    with open(file=f'data_{cur_date}.csv', mode='w') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                table_headers
            )
        )

    data = []
    tbody_trs = table.find('tbody').find_all('tr')
    for tr in tbody_trs:
        area = tr.find('th').text.strip()

        data_by_month = tr.find_all('td')
        data = [area]
        for dbm in data_by_month:
            if dbm.find('a'):
                area_data = dbm.find('a').get('href')
            elif dbm.find('span'):
                area_data = dbm.find('span').text.strip()
            else:
                area_data = 'None'
            data.append(area_data)

        with open(file=f'data_{cur_date}.csv', mode='a') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    data
                )
            )
    return 'work is done!'
url='https://www.bls.gov/regions/southwest/texas.htm#eag'


def main():
    print(get_data('https://www.bls.gov/regions/southwest/texas.htm#eag'))

if __name__ == '__main__':
    main()
