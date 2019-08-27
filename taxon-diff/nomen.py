import urllib3
import urllib.parse
import json
import config

sp2000_status_ids = {1: 'accepted name',
                     2: 'ambiguous synonym',
                     3: 'misapplied name',
                     4: 'provisionally accepted name',
                     5: 'synonym'}


def split_name_status(scientific_name_string):

    status = 0
    for code, s in sp2000_status_ids.items():
        if '(' + s + ')' in scientific_name_string:
            status = code

    scientific_name = scientific_name_string.replace('  ', ' ').strip()
    for _, s in sp2000_status_ids.items():
        scientific_name = scientific_name.replace('(' + s + ')', '')

    return {'name': scientific_name, 'status': status}


def gnparser(name):
    url = 'http://' + config.GNPARSER['hostname'] + ':' + str(config.GNPARSER['port']) + '/api?q=' + \
          urllib.parse.quote(name)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    name = json.loads(response.data.decode('utf8'))
    return name


class Nomen:

    verbatim = ''
    canonical = ''
    normalized = ''
    parser_quality = 0
    parser_version = ''
    genus = ''
    subgenus = ''
    species = ''
    infraspecies = ''
    infraspecies_marker = ''
    author_string = ''
    status = ''

    def __init__(self, name):
        name_info = split_name_status(name)
        self.status = name_info['status']
        parsed_name = gnparser(name_info['name'])[0]
        if parsed_name['parsed']:

            if 'verbatim' in parsed_name:
                self.verbatim = parsed_name['verbatim']
            if 'canonicalName' in parsed_name:
                self.canonical = parsed_name['canonicalName']['simple']
            if 'normalized' in parsed_name:
                self.normalized = parsed_name['normalized']
            if 'parserVersion' in parsed_name:
                self.parser_version = parsed_name['parserVersion']

            self.parser_quality = parsed_name['quality']
            details = parsed_name['details'][0]
            if 'genus' in details:
                self.genus = details['genus']['value']
            if 'infragenericEpithet' in details:
                self.subgenus = details['infragenericEpithet']['value']
            if 'specificEpithet' in details:
                self.species = details['specificEpithet']['value']
                if 'authorship' in details['specificEpithet']:
                    self.author_string = details['specificEpithet']['authorship']['value']
            if 'infraspecificEpithets' in details:
                self.infraspecies = details['infraspecificEpithets'][0]['value']
                if 'authorship' in details['infraspecificEpithets'][0]:
                    self.author_string = details['infraspecificEpithets'][0]['authorship']['value']

    def __str__(self):
        return self.normalized

    def __eq__(self, other):
        if isinstance(other, Nomen):
            return self.canonical == other.canonical
        return False


if __name__ == '__main__':
    name = Nomen('Acipenser (Cus) baerii baerii Brandt, 1869 (accepted name)')
    print('GNParser: ' + name.parser_version)
    print(name.verbatim)
    print(name.canonical)
    print(name.normalized)
    print(name.genus)
    print(name.subgenus)
    print(name.species)
    print(name.infraspecies)
    print(name.author_string)
    print(name.status)
