#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Nick Waters
"""
# Import bioservices module, to run remote UniProt queries
from bioservices import UniProt


service = UniProt()
gene = "TufB"
organism = "Escherichia coli"
query = '{gene} reviewed:yes organism:"{organism}" limit:1 '.format(**locals())
query = '{gene} reviewed:yes limit:1 '.format(**locals())
print(query)
result = service.search(query)

print(result)

def get_arganism_peptide_legnth():
    pass
