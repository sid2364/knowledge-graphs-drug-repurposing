# knowledge-graphs-drug-repurposing

PharMeBINet data: https://zenodo.org/records/7011027 although the paper links to https://zenodo.org/records/6578218 (https://doi.org/10.5281/zenodo.6578218).

PyKeen cannot directly use Neo4j export files directly, it expects (one way) a TriplesFactory which can be fed (head, tail, relation) style data. https://pykeen.readthedocs.io/en/latest/api/pykeen.triples.TriplesFactory.html
Hence, we have the src/extract/pharmebinet.py actually processing the "raw" TSV data into a triples.tsv (among other files).

