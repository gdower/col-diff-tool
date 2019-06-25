import urllib3
from nomen import Nomen
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import config


def clean_str(d):
    d = d.replace("\t", " ")
    d = d.replace("\n", " ")
    d = d.replace("\r", " ")
    d = d.replace("&nbsp;", " ")
    d = d.replace(u'\xa0', u' ')
    d = d.replace("  ", " ")
    return d.strip()


class Taxon:

    def __init__(self, url):
        self.url = url
        self.scientific_name = ''
        self.scientific_name_references = ''
        self.synonyms = []
        self.synonym_references = []
        self.common_names = []
        self.common_names_references = []
        self.taxonomy = {}
        self.distribution = ''
        self.life_zone = ''
        self.scrutiny = ''
        self.source_url = ''
        self.source_db = {}
        self.comments = ''
        self.status = '200'
        self.scrape_taxon(url)

    def scrape_references(self, cell):
        # join the base url and relative reference url
        references = []
        if cell.find('a', href=True) is not None:
            ref_url = urljoin(self.url, cell.find('a', href=True)['href'])
            http = urllib3.PoolManager()
            response = http.request('GET', ref_url)
            soup = BeautifulSoup(response.data.decode('utf8'), "html.parser")
            tables = soup.find_all('table')
            for table in tables:
                reference = {}
                rows = table.find_all('tr')
                for row in rows:
                    th = clean_str(row.find('th').get_text().lower().replace(':', ' '))
                    td = clean_str(row.find('td').get_text())
                    reference[th] = td
                references.append(reference)
        return references

    def scrape_synonyms(self, rows):
        parsed_synonyms = []
        for row in rows:
            if clean_str(row.find_all('td')[0].get_text()) != '':
                parsed_synonyms.append(Nomen(clean_str(row.find_all('td')[0].get_text())))
        return parsed_synonyms

    def scrape_synonym_references(self, rows):
        parsed_synonym_references = []
        for row in rows:
            parsed_synonym_references.append(self.scrape_references(row.find_all('td')[1]))
        return parsed_synonym_references

    def scrape_taxonomy(self, rows):
        taxonomy = {}
        for row in rows:
            rank = clean_str(row.find_all('td')[0].get_text()).lower()
            nomen = clean_str(row.find_all('td')[1].get_text())
            taxonomy[rank] = nomen
        return taxonomy

    def scrape_common_names(self, rows):
        common_names = []
        headings = {}
        r = 0
        for row in rows:
            common_name = {}
            if r == 0:
                h = 0
                for heading in row.find_all('th'):
                    headings[h] = heading.get_text().replace(' ', '_').lower()
                    h += 1
            else:
                h = 0
                for h, heading in headings.items():
                    value = clean_str(row.find_all('td')[h].get_text())
                    if value != '-' and value != '':
                        common_name[heading] = value
                    h += 1
                common_names.append(common_name)
            r += 1
        return common_names

    def scrape_common_name_references(self, rows):
        common_names_references = []
        r = 0
        ref_col = 0
        for row in rows:
            if r == 0:
                ref_col = len(row.find_all('th')) - 1
            else:
                common_name_references = self.scrape_references(row.find_all('td')[ref_col])
                common_names_references.append(common_name_references)
            r += 1
        #print(common_names_references)
        return common_names_references

    def scrape_data(self, table, keyword):
        data = ''
        for th in table.find_all('th'):
            if keyword in th.get_text():
                tr = th.parent
                data = tr.find_all('td')[0].get_text()
                if data == '-':
                    data = ''
        return clean_str(data)

    # TODO: parse scrutiny date
    def scrape_scrutiny(self, table):
        scrutiny_info = {}
        data = self.scrape_data(table, 'Latest taxonomic scrutiny').replace(' 00:00:00', '')
        # expert = ''
        # date = ''
        # if ',' in data:
        #     data_split = data.split(',')
        #     scrutiny_info['expert']  = data_split[0]
        #     date = data_split[1]
        # if date != '':
        #     scrutiny_info['date'] = datetime.strptime(date, '%d-%b-%Y')
        # else:
        #     try:
        #         scrutiny_info['date'] = datetime.strptime(data, '%d-%b-%Y')
        #     except ValueError:
        #         scrutiny_info['expert'] = data
        return data


    def scrape_db(self, table):
        db_info = {}
        data = self.scrape_data(table, 'Source database')
        if re.search('([0-9]+\%)', data) is not None:
            db_info['completeness'] = re.search('([0-9]+\%)', data).group(1)
            data = clean_str(data.replace(db_info['completeness'], ''))
        if re.search('([A-Z]{1}[a-z]{2} [0-9]{4})', data) is not None:
            db_info['updated'] = re.search('([A-Z]{1}[a-z]{2} [0-9]{4})', data).group(1)
            data = clean_str(data.replace(', ' + db_info['updated'], ''))
        if re.search(', ([0-9\.]+)$', data) is not None:
            db_info['version'] = re.search(', ([0-9\.]+)$', data).group(1)
            data = clean_str(data.replace(', ' + db_info['version'], ''))
        db_info['name'] = data
        return db_info

    def scrape_taxon(self, url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data.decode('utf8'), "html.parser")

        if soup.find('p', text='Species not found') is None:
            tables = soup.find_all('table')
            sci_name_td = soup.find('th', text='Accepted scientific name:').find_next('td')
            if clean_str(sci_name_td.get_text()) != '-':
                self.scientific_name = Nomen(sci_name_td.find('table').find_all('td')[0].get_text())
                self.scientific_name_references = self.scrape_references(sci_name_td.find('table').find_all('td')[1])
            synonyms_td = soup.find('th', text='Synonyms:').find_next('td')
            if clean_str(synonyms_td.get_text()) != '-':
                self.synonyms = self.scrape_synonyms(synonyms_td.find('table').find_all('tr'))
                self.synonym_references = self.scrape_synonym_references(synonyms_td.find('table').find_all('tr'))
            common_name_td = soup.find('th', text='Common names:').find_next('td')
            if clean_str(common_name_td.get_text()) != '-':
                self.common_names = self.scrape_common_names(common_name_td.find('table').find_all('tr'))
                self.common_names_references = \
                    self.scrape_common_name_references(common_name_td.find('table').find_all('tr'))
            taxonomy_td = soup.find('th', text='Classification:').find_next('td')
            if clean_str(taxonomy_td.get_text()) != '-':
                self.taxonomy = self.scrape_taxonomy(taxonomy_td.find('table').find_all('tr'))
            self.distribution = self.scrape_data(tables[0], 'Distribution')
            self.life_zone = self.scrape_data(tables[0], 'Environment')
            self.scrutiny = self.scrape_scrutiny(tables[0])
            self.comments = self.scrape_data(tables[0], 'Additional data')
            self.source_url = self.scrape_data(tables[0], 'Online resource')
            self.source_db = self.scrape_db(tables[0])
        else:
            self.status = '404'

    def equal_sci_name(self, other):
        if self.scientific_name == other.scientific_name:
            return '+'
        else:
            return '-'

    def equal_taxonomy(self, other):
        if self.taxonomy == other.taxonomy:
            return '+'
        else:
            return '-'

    def equal_synonyms(self, other):
        if self.synonyms == other.synonyms:
            return '+'
        else:
            return '-'

    def equal_synonym_references(self, other):
        if self.synonym_references == other.synonym_references:
            return '+'
        else:
            return '-'

    def equal_common_names_references(self, other):
        if self.common_names_references == other.common_names_references:
            return '+'
        else:
            return '-'

    # array is a list of dictionaries
    def equal_dictionary_element(self, array1, array2, element):
        list1 = []
        list2 = []
        for item in array1:
            if element in item:
                list1.append(item[element])
            else:
                list1.append('-')
        for item in array2:
            if element in item:
                list2.append(item[element])
            else:
                list2.append('-')
        return list1 == list2

    def equal_common_names(self, other):
        if self.equal_dictionary_element(self.common_names, other.common_names, 'common_name'):
            return '+'
        else:
            return '-'

    def equal_common_names_transliteration(self, other):
        if self.equal_dictionary_element(self.common_names, other.common_names, 'transliteration'):
            return '+'
        else:
            return '-'

    def equal_common_names_languages(self, other):
        if self.equal_dictionary_element(self.common_names, other.common_names, 'languages'):
            return '+'
        else:
            return '-'

    def equal_common_names_countries(self, other):
        if self.equal_dictionary_element(self.common_names, other.common_names, 'countries'):
            return '+'
        else:
            return '-'

    def equal_references(self, other):
        if self.scientific_name_references == other.scientific_name_references:
            return '+'
        else:
            return '-'

    def equal_distribution(self, other):
        if self.distribution == other.distribution:
            return '+'
        else:
            return '-'

    def equal_life_zone(self, other):
        if self.life_zone == other.life_zone:
            return '+'
        else:
            return '-'

    def equal_scrutiny(self, other):
        if self.scrutiny == other.scrutiny:
            return '+'
        else:
            return '-'

    def equal_comments(self, other):
        if self.comments == other.comments:
            return '+'
        else:
            return '-'

    def equal_source_url(self, other):
        if self.source_url == other.source_url:
            return '+'
        else:
            return '-'

    def equal_source_db_completeness(self, other):
        if 'completeness' in self.source_db and 'completeness' in other.source_db:
            if self.source_db['completeness'] == other.source_db['completeness']:
                return '+'
            else:
                return '-'
        else:
            return '-'

    def equal_source_db_name(self, other):
        if 'name' in self.source_db and 'name' in other.source_db:
            if self.source_db['name'] == other.source_db['name']:
                return '+'
            else:
                return '-'
        else:
            return '-'

    def equal_source_db_version(self, other):
        if 'version' in self.source_db and 'version' in other.source_db:
            if self.source_db['version'] == other.source_db['version']:
                return '+'
            else:
                return '-'
        return ' '

    def equal_source_db_updated(self, other):
        if 'updated' in self.source_db and 'updated' in other.source_db:
            if self.source_db['updated'] == other.source_db['updated']:
                return '+'
            else:
                return '-'
        return ' '

    # __eq__ only tests the scientific name, synonyms, common names, and taxonomy
    def __eq__(self, other):
        if isinstance(other, Taxon):
            return self.equal_sci_name(other) == '+' and \
                   self.equal_synonyms(other) == '+' and \
                   self.equal_common_names(other) == '+' and \
                   self.equal_taxonomy(other) == '+'
        return False


if __name__ == '__main__':

    url = 'http://' + config.DIFF_URLS['prod_hostname2'] + '/' + \
          config.DIFF_URLS['prod_dir2'] + '/details/species/id/ac4311ffb93d067eeb47de08951a87ff'

    taxon = Taxon(url)
    taxon2 = Taxon(url)

    print('Scientific name: ' + str(taxon.scientific_name))

    print('Synonyms: ')
    for nom in taxon.synonyms:
        print(nom)

    print(taxon.common_names)

    print(taxon.taxonomy)

    print(taxon.distribution)

    print(taxon.life_zone)

    print(taxon.comments)

    print(taxon.scrutiny)

    print(taxon.source_url)

    print(taxon.source_db)

    print(taxon == taxon2)

    ac2018 = Taxon('http://' + config.DIFF_URLS['prod_hostname1'] + '/' + config.DIFF_URLS['prod_dir1'] +
                   '/details/species/id/ac4311ffb93d067eeb47de08951a87ff')
    ac2019 = Taxon('http://' + config.DIFF_URLS['prod_hostname2'] + '/' + config.DIFF_URLS['prod_dir2'] +
                   '/details/species/id/ac4311ffb93d067eeb47de08951a87ff')

    print(ac2018 == ac2019)
