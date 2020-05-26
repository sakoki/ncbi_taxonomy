import pandas as pd
from collections import deque
from ncbi_taxonomy.IO import read_nodes_dmp, read_names_dmp

class TaxonomyNode():
    """Taxonomy node"""
    
    def __init__(self, tax_id: str):
        self.tax_id = tax_id
        self.rank = None
        self.name_txt = None
        self.parent_tax_id = None
        
    def __repr__(self):
        return f"TaxonomyNode({self.tax_id})"
        
    def __str__(self):
        return "\n".join([f"tax_id: {self.tax_id}", 
                          f"rank: {self.rank}", 
                          f"name_txt: {self.name_txt}",
                          f"parent_txt_id: {self.parent_tax_id}"])

class NCBI_Taxonomy():
    """Interact with the NCBI taxonomy data"""
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_taxonomy_data(self):
        """Merge taxonomy files together"""
        
        self.nodes = read_nodes_dmp(self.file_path + 'nodes.dmp').set_index("tax_id")
        self.names = read_names_dmp(self.file_path + 'names.dmp')
    
    def get_tax_id(self, name):
        """Get the tax_id from names table
        
        Parameters
        ----------
        query : str
        
        Returns
        -------
        tax_id : int
        """
        
        hits = self.names.loc[lambda df: df["name_txt"] == name]
        if hits.shape[0] > 1:  # multiple matches
            msg = [f"Multiple matches to query found:",
                   f"{hits}",
                   "Please select tax_id: "]
            return int(input("\n".join(msg)))
        elif hits.shape[0] == 1:
            return hits.tax_id.values[0]
        else:
            raise IndexError("Invalid name - not found or possible typo")
            
    def get_name_txt(self, tax_id, name_class):
        """Given a tax_id, get the name_txt of specific name_class from the names table
        
        Parameters
        ----------
        tax_id : int
        name_class : str
        
        Returns
        -------
        name_txt : str
        """
        
        try:
            return self.names.loc[
                lambda df: (df["tax_id"] == tax_id) & (df["name_class"] == name_class)].name_txt.values[0]
        except IndexError:
            print("Invalid tax_id - not found or possible typo")
    
    def get_node_info(self, node):
        """Look up the tax_id in the nodes table for additional information
        
        Parameters
        ----------
        node : TaxonomyNode
        """
        
        result = self.nodes.loc[node.tax_id]
        node.rank = result['rank']
        node.parent_tax_id = result['parent_tax_id']
        node.name_txt = self.get_name_txt(node.tax_id, name_class="scientific name")
        return node
    
    def create_node_objects(self, name_list, from_tax_id=False):
        """Create node objects from a list of names or tax_id in the taxonomy database
        
        Parameters
        ----------
        names : list of str or int
            list of names (str) or tax_id (int)
        from_tax_id : bool
            True if name_list contains tax_ids
            
        Returns
        -------
        nodes : list of TaxonomyNode
        """
        
        nodes = []
        
        for name in name_list:
            tax_id = self.get_tax_id(name) if not from_tax_id else name
            nodes.append(self.get_node_info(TaxonomyNode(tax_id)))
        return nodes
      
    def get_LCA(self, node_list):
        """Get the lowest common ancestor of given nodes
        
        Parameters
        ----------
        node_list : list of TaxonomyNode
        
        Returns
        -------
        node : TaxonomyNode
            Lowest common ancestor
        """
        nodes_seen = {}
        node_count = len(node_list)
        
        queue = deque()
        for node in node_list:
            queue.append(node)
        
        while queue:
            node = queue.popleft()
            nodes_seen[node.tax_id] = nodes_seen.get(node.tax_id, 0) + 1 
            if nodes_seen[node.tax_id] == node_count:
                return node
            parent_node = self.get_node_info(TaxonomyNode(node.parent_tax_id))
            queue.append(parent_node)