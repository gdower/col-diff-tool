from taxon import Taxon
import config

if __name__ == '__main__':

    ids = []
    input_ids = open("test.tsv", "r")
    for line in input_ids:
        ids.append(line.replace("\n", ""))

    diff_output = open('output/diff_taxon_output.html', 'w')
    diff_header = '<!DOCTYPE html><html lang="en-US"><head><title>CoL Diff Tool Output</title>' \
                  '<style type="text/css">body {margin-top:0;margin-bottom:0;padding:0;}</style></head><body><tt><pre>'
    diff_footer = '</pre></tt></body></html>'
    diff_output.write(diff_header)
    error_output = open('output/diff_taxon_error.html', 'w')
    error_header = '<!DOCTYPE html><html lang="en-US"><head><title>CoL Diff Tool Output</title>' \
                   '<style type="text/css">body {margin-top:0;margin-bottom:0;padding:0;}</style></head><body><tt><pre>'
    error_footer = '</pre></tt></body></html>'
    diff_output.write(error_header)

    not_found = []

    for id in ids:
        colplus = Taxon('http://' + config.DIFF_URLS['dev_hostname2'] + ':' +
                        config.DIFF_URLS['dev_port2'] + '/' + config.DIFF_URLS['dev_dir2'] +
                        '/details/species/id/' + id)
        colminus = Taxon('http://' + config.DIFF_URLS['dev_hostname1'] + ':' +
                        config.DIFF_URLS['dev_port1'] + '/' + config.DIFF_URLS['dev_dir1'] +
                         '/details/species/id/' + id)

        # A R S R I C R t l c T D E C S G V U % O
        print(colplus.status)
        print(colminus.status)
        if colplus.status == '200' and colminus.status == '200':
            line = colplus.equal_sci_name(colminus) + ' ' + \
                   colplus.equal_references(colminus) + ' ' + \
                   colplus.equal_synonyms(colminus) + ' ' + \
                   colplus.equal_synonym_references(colminus) + ' ' + \
                   colplus.equal_infraspecies(colminus) + ' ' + \
                   colplus.equal_common_names(colminus) + ' ' + \
                   colplus.equal_common_names_references(colminus) + ' ' + \
                   colplus.equal_common_names_transliteration(colminus) + ' ' + \
                   colplus.equal_common_names_languages(colminus) + ' ' + \
                   colplus.equal_common_names_countries(colminus) + ' ' + \
                   colplus.equal_taxonomy(colminus) + ' ' + \
                   colplus.equal_distribution(colminus) + ' ' + \
                   colplus.equal_life_zone(colminus) + ' ' + \
                   colplus.equal_comments(colminus) + ' ' + \
                   colplus.equal_scrutiny(colminus) + ' ' + \
                   colplus.equal_source_db_name(colminus) + ' ' + \
                   colplus.equal_source_db_version(colminus) + ' ' + \
                   colplus.equal_source_db_updated(colminus) + ' ' + \
                   colplus.equal_source_db_completeness(colminus) + ' ' + \
                   colplus.equal_source_url(colminus) + ' ' + \
                   '<a href="http://ower.org/col_diff/diff.php?id=' + id + '" target="_blank">' + id + '</a>\n'
            diff_output.write(line)
            diff_output.flush()
        else:
            error_output.write('col-: ' + colminus.status + ' http://' + config.DIFF_URLS['dev_hostname2'] + ':' +
                               config.DIFF_URLS['dev_port2'] + '/' + config.DIFF_URLS['dev_dir2'] +
                               '/details/species/id/' + id + '\n')
            error_output.write('col+: ' + colplus.status + ' http://' + config.DIFF_URLS['dev_hostname1'] + ':' +
                               config.DIFF_URLS['dev_port1'] + '/' + config.DIFF_URLS['dev_dir2'] +
                               '/details/species/id/' + id + '\n')
            error_output.flush()

    diff_output.write(diff_footer)
    error_output.write(error_footer)
    diff_output.close()
    error_output.close()

