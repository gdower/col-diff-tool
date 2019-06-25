# CoL Diff Tool

The col-diff-tool is a web crawler that compares Global Species Database (GSD) statistics and taxon pages between different versions of the Catalogue of Life (CoL). The col-diff-tool uses [GNParser](https://github.com/GlobalNamesArchitecture/gnparser) to break scientific names down into their name componenets.

# Installation

```
git clone https://github.com/gdower/col-diff-tool.git
cd col-diff-tool
pip3 install -r requirements.txt
```

After [installing GNParser](https://github.com/GlobalNamesArchitecture/gnparser#command-line-tool-and-socket-server), run:

```
docker run -p 0.0.0.0:9797:8080 gnames/gognparser -w 8080
```

# Usage

```
python3 diff_gsd_stats.py
python3 diff_taxon_pages.py
```
