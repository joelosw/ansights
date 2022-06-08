# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup
import unicodedata
from lxml import etree

# --------- Query: Structure Example --------------
# https://www.dnb.de/DE/Professionell/Metadatendienste/Datenbezug/SRU/sru_node.html#doc58294bodyText4
# Anfrage an SRU-Server der DNB: https://services.dnb.de/sru
# Festlegen des Kataloges (z. B. GND): authorities
# Angabe der SRU-Version, Standard: ?version=1.1
# Befehl an den Server: &operation=searchRetrieve
# Anfrage formulieren: &query=
# WOE ist die Indexbezeichnung, %3D ist die URL-Kodierung für =, Suchbegriff hier: Goethe: WOE%3DGoethe
# Sortierung der Ergebnismenge nach Titel aufsteigend von A-Z: %20sortby%20tit/sort.ascending
# gewünschtes Format der SRU-Antwort: &recordSchema=MARC21-xml

# https://github.com/deutsche-nationalbibliothek/dnblab/blob/main/DNB_SRU_Tutorial.ipynb
# https://wiki.dnb.de/pages/viewpage.action?pageId=134055670


def dnb_sru(query: str,
            sru_server='https://services.dnb.de/sru/',
            catalog='authorities',
            recordSchema='MARC21-xml',
            operation='searchRetrieve',
            version='1.1',
            maximumRecords=10
            ):

    base_url = sru_server + catalog
    params = {'recordSchema': recordSchema,
              'operation': operation,
              'version': version,
              'maximumRecords': str(maximumRecords),
              'query': query
              }

    r = requests.get(base_url, params=params)
    xml = soup(r.content, features="xml")

    records = xml.find_all('record', {'type': 'Bibliographic'})

    if len(records) < maximumRecords:

        return records

    else:

        num_results = maximumRecords
        i = maximumRecords + 1
        while num_results == maximumRecords:

            params.update({'startRecord': i})
            r = requests.get(base_url, params=params)
            xml = soup(r.content, features='xml')
            new_records = xml.find_all('record', {'type': 'Bibliographic'})
            records += new_records
            i += maximumRecords
            num_results = len(new_records)

        # TODO: recieve most important records
        records = records[-10:]

        return records


def parse_record(record):

    ns = {"marc": "http://www.loc.gov/MARC21/slim"}
    xml = etree.fromstring(unicodedata.normalize("NFC", str(record)))

    # idn
    idn = xml.xpath("marc:controlfield[@tag = '001']", namespaces=ns)
    try:
        idn = idn[0].text
    except:
        idn = 'fail'

    # titel
    titel = xml.xpath(
        "marc:datafield[@tag = '245']/marc:subfield[@code = 'a']", namespaces=ns)

    try:
        titel = titel[0].text
        #titel = unicodedata.normalize("NFC", titel)
    except:
        titel = "unkown"

    meta_dict = {"idn": idn,
                 "titel": titel}

    return meta_dict


def get_gnd_record(query: str,
                   sru_server='https://services.dnb.de/sru/',
                   catalog='authorities',
                   recordSchema='MARC21-xml',
                   operation='searchRetrieve',
                   version='1.1',
                   maximumRecords=10,
                   debug=False
                   ):

    records = dnb_sru(query=query,
                      sru_server=sru_server,
                      catalog=catalog,
                      recordSchema=recordSchema,
                      operation=operation,
                      version=version,
                      maximumRecords=maximumRecords
                      )

    output = [parse_record(record) for record in records]
    df = pd.DataFrame(output)

    if debug:
        print(len(records), 'Ergebnisse')
        print(df)

    df.to_csv("data/GND/"+query+".csv", index=False)

    return df


df = get_gnd_record(query='Streik%3D1919', # 'Goethe', 
                    sru_server='https://services.dnb.de/sru/',
                    catalog='dnb', # 'authorities', 'dnb'
                    recordSchema='MARC21-xml',
                    operation='searchRetrieve',
                    version='1.1',
                    maximumRecords=25,
                    debug=True)
print(df.head())

