# -*- coding: utf-8 -*-
"""
Chemistry Utilities

"""

# Imports

try:
    from rdkit import Chem
    from rdkit.Chem.Draw import IPythonConsole
except:
    print('rdkit not installed.')

from IPython import display
from urllib.request import urlopen

# Convert from chemical name or nickname to smiles

def name_to_smiles(name):
    """Convert from chemical name to SMILES string using chemical identifier resolver.
    
    Parameters
    ----------
    name : str 
        Name or nickname of compound.
    
    Returns
    ----------
    str 
        SMILES string corresponding to chemical name.
    """
    
    name = name.replace(' ', '%20')
    
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + name + '/smiles'
        smiles = urlopen(url).read().decode('utf8')
        smiles = str(smiles)
        if '</div>' in smiles:
            return 'FAILED'
        else:
            return smiles
    except:
        return 'FAILED'

# 2D SMILES visualizations

class ChemDraw:
    """Class for chemical structure visualization."""
    
    def __init__(self, SMILES_list, row_size='auto', legends=None, 
                 ipython_svg=True):
        """        
        Parameters
        ----------
        SMILES_list : list 
            List of SMILES strings to be visualized.
        row_size : 'auto', int 
            Number of structures to include per row.
        legends : None, list
            Structure legends to include below representations.
        ipython_svg :bool 
            If true print SVG in ipython console.
        
        Returns
        ----------
        None
        """
        
        self.SMILES_list = list(SMILES_list)
        self.legends = legends
        self.mols = [Chem.MolFromSmiles(s) for s in self.SMILES_list]
        
        if row_size == 'auto':
            self.molsPerRow = len(self.mols)
        else:
            self.molsPerRow = row_size  
            
        # SVGs look nicer
        IPythonConsole.ipython_useSVG = ipython_svg
        self.SVG = ipython_svg
        
    def show(self):
        """Show 2D representation of SMILES strings.
        
        Returns
        ----------
        image 
            Visualization of chemical structures.
        """
        
        img = Chem.Draw.MolsToGridImage(self.mols, 
                    molsPerRow=self.molsPerRow, 
                    subImgSize=(200, 200), 
                    legends=self.legends, 
                    highlightAtomLists=None, 
                    highlightBondLists=None, 
                    useSVG=self.SVG)
        
        display.display(img)
    
    def export(self, path):
        """Export 2D representation of SMILES strings.
        
        Parameters
        ----------
        path : 'str'
            Export a PNG image of chemical structures to path.
        
        Returns
        ----------
        None
        """
        
        img = Chem.Draw.MolsToGridImage(self.mols, 
                    molsPerRow=self.molsPerRow, 
                    subImgSize=(500, 500), 
                    legends=self.legends, 
                    highlightAtomLists=None, 
                    highlightBondLists=None, 
                    useSVG=False)
        
        img.save(path + '.png')




