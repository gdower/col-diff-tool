
# Running the taxon diff tool on a local docker testbenches hosting the same data is much faster,
#   but the prod servers can be used for diffing GSD statistics and viewing the taxon diff output

DIFF_URLS = {
    'dev_hostname1': 'localhost',  # CoL-
    'dev_hostname2': 'localhost',  # CoL+
    'dev_dir1': 'testcol',
    'dev_dir2': 'col_plus',
    'dev_port1': '2200',
    'dev_port2': '9191',
    'prod_hostname1': 'www.catalogueoflife.org',
    'prod_hostname2': 'workbench.catalogueoflife.org',
    'prod_dir1': 'annual-checklist/2019',
    'prod_dir2': 'col_plus',
}

GNPARSER = {
    'hostname': 'localhost',
    'port': '9797',
    'start_cmd': 'docker run -p 0.0.0.0:9797:8080 gnames/gognparser -w 8080'
}
