import json
import urllib3
import config

http = urllib3.PoolManager()


def parse_int(statistic):
    return int(statistic.replace(',', ''))


def parse_taxon(taxon, hierarchy):
    id = taxon['id']
    name = taxon['name']
    hierarchy = '-'.join([hierarchy, name])
    rank = taxon['type']
    extant = parse_int(taxon['nr_extant'])
    fossil = parse_int(taxon['nr_fossil'])
    total = parse_int(taxon['total'])
    estimate = -1
    if taxon['estimation'] != '?':
        estimate = parse_int(taxon['estimation'])
    return {'id': id,
            'hierarchy': hierarchy,
            'name': name,
            'rank': rank,
            'extant': extant,
            'fossil': fossil,
            'total': total,
            'estimate': estimate}


def crawl_tree(url):
    tree = {}
    data = json.loads(http.request('GET', url).data)
    parent_name = 'Biota'
    taxa = data['items']
    for taxon in taxa:
        leaf = parse_taxon(taxon, parent_name)
        hierarchy = leaf['hierarchy']
        tree[hierarchy] = leaf
        recurse_children(url, leaf['id'], leaf['name'])
    return tree


def recurse_children(url, id, parent_name=''):
    tree = {}
    data = json.loads(http.request('GET', url + '?id=' + str(id)).data)
    taxa = data['items']
    for taxon in taxa:
        leaf = parse_taxon(taxon, parent_name)
        #print(leaf)
        hierarchy = leaf['hierarchy']
        tree[hierarchy] = leaf
        if leaf['rank'] != 'genus':
            recurse_children(url, leaf['id'], leaf['hierarchy'])
    return tree


if __name__ == '__main__':

    # assemble the base URL
    base_url = 'http://' + config.DIFF_URLS['prod_hostname1'] + '/' + \
               config.DIFF_URLS['prod_dir1'] + '/browse/tree/fetch/taxa'

    #crawl_tree(base_url)

    # crawl bacteria kingdom
    tree = recurse_children(base_url, 54767800, 'Biota')
    print(tree)
