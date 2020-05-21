import pandas as pd

def read_nodes_dmp(fname):
    """Read taxonomy nodes.dmp file into pandas DataFrame

    Parameters 
    ----------
    fname : str
        Path/name to taxonomy node dmp file

    Returns
    -------
    DataFrame
    """
    df = pd.read_csv(fname, sep="|", header=None, index_col=False,
                     names=['tax_id', 
                            'parent_tax_id',
                            'rank', 
                            'embl_code',
                            'division_id', 
                            'inherited_div_flag',  # 1 or 0
                            'genetic_code_id', 
                            'inherited_GC_flag',  # 1 or 0
                            'mitochondrial_genetic_code_id', 
                            'inherited_MGC_flag',  # 1 or 0
                            'GenBank_hidden_flag',
                            'hidden_subtree_root_flag',  # 1 or 0 
                            'comments'])
    return df.assign(rank = lambda x: x['rank'].str.strip(),
                     embl_code = lambda x: x['embl_code'].str.strip(),
                     comments = lambda x: x['comments'].str.strip())

def read_names_dmp(fname):
    """Read taxonomy names.dmp file into pandas DataFrame

    Parameters
    ----------
    fname : str
        Path/name to taxonomy names.dmp file

    Returns
    -------
    DataFrame 
    """
    df = pd.read_csv(fname, sep="|", header=None, index_col=False,
                    names=["tax_id",
                           "name_txt",
                           "unique_name",
                           "name_class"])
    return df.assign(name_txt = lambda x: x['name_txt'].str.strip(),
                     unique_name = lambda x: x['unique_name'].str.strip(),
                     name_class = lambda x: x['name_class'].str.strip())