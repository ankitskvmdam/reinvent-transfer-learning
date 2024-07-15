import numpy as np

from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
from scipy.spatial import distance_matrix


def get_mol(smiles: str):
    return Chem.MolFromSmiles(smiles)

def compute_fingerprint(smiles: str):
    mol = get_mol(smiles)
    return AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)

def extract_features(smiles_list: "list[str]"):
    features = []
    for smiles in smiles_list:
        fp = compute_fingerprint(smiles)
        arr = np.zeros((1,))
        DataStructs.ConvertToNumpyArray(fp, arr)
        features.append(arr)
    return np.array(features)

def compute_3d_similarity(smiles1: str, smiles2: str) -> "tuple[bool, float]":
    ''' Compute 3d similarity of given smiles.

    It will return the RMSD (Root Mean Square Deviation). Here is the interpretation:

    1. 0.0 - 1.0 -> Very similar.
    2. 1.0 - 2.0 -> Close similar.
    3. > 2.0 -> Low similarity.
    '''
    mol1 = get_mol(smiles1)
    mol2 = get_mol(smiles2)

    mol1 = Chem.AddHs(mol1)
    mol2 = Chem.AddHs(mol2)

    num_atoms_mol1 = mol1.GetNumAtoms()
    num_atoms_mol2 = mol2.GetNumAtoms()

    if num_atoms_mol1 < num_atoms_mol2:
        # swapping
        mol2, mol1 = mol1, mol2
    
    status1= AllChem.EmbedMolecule(mol1, randomSeed=42)
    status2 = AllChem.EmbedMolecule(mol2, randomSeed=42)


    if status1 == -1 or status2 == -1:
        # If status is -1 then `EmbedMolecule` function 
        # failed to generate conformers. Hence we cannot
        # proceed.
        return (False, float('inf'))

    # Convert to numpy arrays for manual alignment
    conf1 = mol1.GetConformer().GetPositions()
    conf2 = mol2.GetConformer().GetPositions()
  
    # If molecules have different numbers of atoms, align based on atom types and positions
    if conf1.shape[0] != conf2.shape[0]:
        # Compute distance matrix between atom positions
        dist_matrix = distance_matrix(conf1, conf2)
        
        # Find the best match for each atom in mol1 to an atom in mol2
        min_dist_indices = np.argmin(dist_matrix, axis=1)
        
        # Align using the best matches
        aligned_conf1 = conf1
        aligned_conf2 = conf2[min_dist_indices]
    else:
        # Align using centroids for molecules with the same number of atoms
        centroid1 = np.mean(conf1, axis=0)
        centroid2 = np.mean(conf2, axis=0)
        aligned_conf1 = conf1 - centroid1
        aligned_conf2 = conf2 - centroid2

    # Compute RMSD
    rmsd = np.sqrt(np.mean(np.sum((aligned_conf1 - aligned_conf2) ** 2, axis=1)))

    return (True, rmsd)