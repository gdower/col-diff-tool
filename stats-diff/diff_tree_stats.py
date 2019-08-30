from get_tree_stats import recurse_children
import config

if __name__ == '__main__':

    # AG+
    ag_plus_url = 'http://' + config.DIFF_URLS['dev_hostname1'] + ':' + config.DIFF_URLS['dev_port1'] + '/' + \
               config.DIFF_URLS['dev_dir1'] + '/browse/tree/fetch/taxa'
    col_plus_url = 'http://' + config.DIFF_URLS['dev_hostname2'] + ':' + config.DIFF_URLS['dev_port2'] + '/' + \
               config.DIFF_URLS['dev_dir2'] + '/browse/tree/fetch/taxa'

    # crawl bacteria kingdom
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54773567, 'Biota-Plantae-Tracheophyta-Magnoliopsida-Fabales')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3901776, 'Biota-Plantae-Tracheophyta-Magnoliopsida-Fabales')

    # crawl animalia
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54772746, 'Biota-Animalia')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3893462, 'Biota-Animalia')

    # crawl archaea
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54775083, 'Biota-Archaea')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3899448, 'Biota-Archaea')

    # crawl bacteria
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54772802, 'Biota-Bacteria')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3893909, 'Biota-Bacteria')

    # crawl chromista
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54773344, 'Biota-Chromista')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3893507, 'Biota-Chromista')

    # crawl fungi
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54772769, 'Biota-Fungi')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3893520, 'Biota-Fungi')

    # # crawl plantae
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54772870, 'Biota-Plantae')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3893548, 'Biota-Plantae')

    # crawl protozoa
    # print(ag_plus_url)
    # ag_plus_tree = recurse_children(ag_plus_url, 54774392, 'Biota-Protozoa')
    # print(col_plus_url)
    # col_plus_tree = recurse_children(col_plus_url, 3893371, 'Biota-Protozoa')

    # crawl viruses
    print(ag_plus_url)
    ag_plus_tree = recurse_children(ag_plus_url, 54772796, 'Biota-Viruses')
    print(col_plus_url)
    col_plus_tree = recurse_children(col_plus_url, 3893380, 'Biota-Viruses')


    for taxon_code, taxon in ag_plus_tree.items():

        if taxon['extant'] != col_plus_tree[taxon_code]['extant'] or taxon['fossil'] != col_plus_tree[taxon_code]['fossil']:
            print(taxon)
            print(col_plus_tree[taxon_code])


