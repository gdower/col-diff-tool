from get_gsd_stats import get_gsds_statistics
import config

if __name__ == '__main__':

    base_url1 = 'http://' + config.DIFF_URLS['dev_hostname1'] + ':' + \
                     config.DIFF_URLS['dev_port1'] + '/' + config.DIFF_URLS['dev_dir1'] + \
                     '/details/database/id/'
    base_url2 = 'http://' + config.DIFF_URLS['dev_hostname2'] + ':' + \
                config.DIFF_URLS['dev_port2'] + '/' + config.DIFF_URLS['dev_dir2'] + \
                '/details/database/id/'

    # small CoL+ assembly
    gsds = [10, 76, 192, 168, 21, 86, 87, 181, 182, 152, 149]

    # full AC2019 CoL- assembly
    # gsds = ['5','6','8','9','10','11','12','14','15','18','19','20','21','22','23','24','25','26','27','28',
    # '29','30','31','32','33','34','36','37','38','39','40','42','44','45','46','47','48','49','50','51','52',
    # '53','54','55','57','58','59','61','62','63','65','66','67','68','69','70','73','74','76','78','79','80',
    # '81','82','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','103',
    # '104','105','106','107','108','109','110','112','113','115','118','119','120','122','123','124','125',
    # '126','127','128','129','130','131','132','133','134','138','139','140','141','142','143','144','146',
    # '148','149','150','152','153','154','157','158','161','162','163','164','166','167','168','169','170',
    # '171','172','173','174','175','176','177','178','179','180','181','182','183','184','185','186','188',
    # '189','190','191','192','193','194','195','196','197','198','199','200','201','202','203','204','500',
    # '501','502']

    # output headers
    print('gsd\tfull_name\tliving_species1\tliving_species2\textinct_species1\textinct_species2\tliving_infraspecies1\t'
          'living_infraspecies2\textinct_infraspecies1\textinct_infraspecies2\tsynonyms1\tsynonyms2\tcommon_names1\t'
          'common_names2\ttotal_names1\ttotal_names2')

    col1_stats = get_gsds_statistics(base_url1, gsds)
    col2_stats = get_gsds_statistics(base_url2, gsds)

    r = 0
    for col1 in col1_stats:

        col2 = col2_stats[r]

        print(str(col1['gsd']) + '\t' + col1['full_name'] + '\t' +
              str(col1['living_species']) + '\t' + str(col2['living_species']) + '\t' +
              str(col1['extinct_species']) + '\t' + str(col2['extinct_species']) + '\t' +
              str(col1['living_infraspecies']) + '\t' + str(col2['living_infraspecies']) + '\t' +
              str(col1['extinct_infraspecies']) + '\t' + str(col2['extinct_infraspecies']) + '\t' +
              str(col1['synonyms']) + '\t' + str(col2['synonyms']) + '\t' +
              str(col1['common_names']) + '\t' + str(col2['common_names']) + '\t' +
              str(col1['total_names'])+ '\t' + str(col2['total_names']))

        r += 1
