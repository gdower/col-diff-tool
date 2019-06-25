import urllib3
from bs4 import BeautifulSoup
import config

row_names = {'full_name': 'Full name',
             'living_species': 'Number of living species',
             'extinct_species': 'Number of extinct species',
             'living_infraspecies': 'Number of living infraspecific taxa',
             'extinct_infraspecies': 'Number of extinct infraspecific taxa',
             'synonyms': 'Number of synonyms',
             'common_names': 'Number of common names',
             'total_names': 'Total number of names'}


def clean_str(d):
    d = d.replace("UPDATED!", "")
    d = d.replace("NEW!", "")
    d = d.replace(",", "") # remove commas from stats
    d = d.replace("\t", " ")
    d = d.replace("\n", " ")
    d = d.replace("\r", " ")
    d = d.replace("&nbsp;", " ")
    d = d.replace(u'\xa0', u' ')
    d = d.replace("  ", " ")
    d = d.strip()
    return d


def get_statistic(name, table):
    statistic = ''
    for row in table.find_all('tr'):

        if name in row.get_text():
            statistic = clean_str(row.find_all('td')[0].get_text())
    return statistic


def get_gsd_statistics(base_url, gsd):
    url = base_url + str(gsd)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf8'), "html.parser")
    tables = soup.find_all('table')
    stats_table = tables[1]
    statistics = {'gsd': gsd}
    for var, stat in row_names.items():
        statistics[var] = get_statistic(stat, stats_table)
    return statistics


def get_gsds_statistics(url, gsds):
    gsds_statistics = []
    for gsd in gsds:
        gsds_statistics.append(get_gsd_statistics(url, gsd))
    return gsds_statistics


if __name__ == '__main__':

    # assemble the base URL
    base_url = 'http://' + config.DIFF_URLS['prod_hostname1'] + '/' + \
               config.DIFF_URLS['prod_dir1'] + '/details/database/id/'

    # output headers
    print('gsd\t'
          'full_name\t'
          'living_species\t'
          'living_infraspecies\t'
          'extinct_species\t'
          'extinct_infraspecies\t'
          'synonyms\t'
          'common_names\t'
          'total_names')

    # get stats for multiple GSDs
    gsds = [10, 76, 192, 168, 21, 86, 87, 181, 182, 152, 149]
    gsds_stats = get_gsds_statistics(base_url, gsds)
    for statistics in gsds_stats:

        print(str(statistics['gsd']) + '\t' + statistics['full_name'] + '\t' +
              str(statistics['living_species']) + '\t' +
              str(statistics['extinct_species']) + '\t' +
              str(statistics['living_infraspecies']) + '\t' +
              str(statistics['extinct_infraspecies']) + '\t' +
              str(statistics['synonyms']) + '\t' +
              str(statistics['common_names']) + '\t' +
              str(statistics['total_names']))
