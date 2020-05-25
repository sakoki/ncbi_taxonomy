# Python tool for interacting with the NCBI Taxonomy data

_Author: Koki Sasagawa_

File Structure

    .
    ├── data
    │  └── taxdump
    │     ├── citations.dmp
    │     ├── delnodes.dmp
    │     ├── division.dmp
    │     ├── gc.prt
    │     ├── gencode.dmp
    │     ├── merged.dmp
    │     ├── names.dmp  # Only using  #
    │     ├── nodes.dmp  # these files #
    │     └── readme.txt
    ├── data_exploration.ipynb
    ├── dev.ipynb
    └── ncbi_taxonomy
      ├── __init__.py
      ├── IO.py
      └── taxonomy.py

Download the ncbi data from: (https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz)

# Getting the lowest common ancestor

1.  Import taxonomy.py
2.  To start interacting with the ncbi taxonomy data, load it into the environment  by calling. We then assign that object to variable `session`.

```python
session = taxonomy.ncbi_taxonomy(file_path="<insert_file_path>")
```

3.  Prepare your input (a list of names or tax_id's) as a list of TaxonomyNode objects. Here we pass in the acronyms MERS and SARS.

```python
nodes = session.create_node_objects(['MERS', 'SARS'])
```

4.  Get the lowest common ancestor by calling 

```python
session.get_LCA(node_list=nodes)
```
