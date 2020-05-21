import pandas as pd
from IO import read_nodes_dmp, read_names_dmp

class NCBI_Taxonomy():
    """Taxonomy node
    
    Contains tax_id, parent_tax_id, rank, name_txt
    """
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_taxonomy_data(self):
        """Merge nodes.dmp and names.dmp files together"""
        nodes = read_nodes_dmp(self.file_path + 'nodes.dmp')
        names = read_names_dmp(self.file_path + 'names.dmp').loc[names['name_class'] == 'scientific name']
        self.taxonomy_db = nodes.merge(names, on="tax_id")
        
    def get_LCA(self, query_nodes):
        pass

    

