"""
Small util to fix reinvent models vocabulary in windows os.
"""

import os

root = os.path.join(os.environ["CONDA_PREFIX"])

path_to_reinvent = os.path.join(root, "Lib", "site-packages", "reinvent")
path_to_vocabulary = os.path.join(
    path_to_reinvent, "models", "mol2mol", "models", "vocabulary.py"
)
path_to_transformer = os.path.join(
    path_to_reinvent, "models", "transformer", "core", "vocabulary.py"
)

v = ""
with open(path_to_transformer) as reader:
    v = reader.read()

with open(path_to_vocabulary, "w") as writer:
    writer.write(v)
