# for extracting massive big Neo4j-style PharMeBINet TSVs
import os
from pathlib import Path
import pandas as pd

PWD = Path().resolve()
EDGES_PATH = PWD / "data/raw/pharmebinet_tsv_2022_08_19_v2/edges.tsv"
NODES_PATH = PWD / "data/raw/pharmebinet_tsv_2022_08_19_v2/nodes.tsv"
OUT_DIR = PWD / "data/processed/pharmebinet"
OUT_DIR.mkdir(parents=True, exist_ok=True) # shouldn't blow up?

TRIPLES_OUT = OUT_DIR / "triples.tsv"
ENTITY2ID_OUT = OUT_DIR / "entity2id.csv"
RELATION2ID_OUT = OUT_DIR / "relation2id.csv"
ENTITY_TYPES_OUT= OUT_DIR / "entity_types.csv"

NODE_CHUNKSIZE = 250_000   # rows per chunk for nodes.tsv
EDGE_CHUNKSIZE = 1_000_000 # rows per chunk for edges.tsv
PRINT_EVERY = 1_000_000 # print every N processed rows

# helpers
def _norm_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def _strip_str(df: pd.DataFrame) -> pd.DataFrame:
    # applymap on huge frames is slow; vectorize on object cols only
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].str.strip()
    return df

def main():
    # Validate files first
    if not EDGES_PATH.exists():
        raise FileNotFoundError(f"Missing edges file: {EDGES_PATH}")
    if not NODES_PATH.exists():
        raise FileNotFoundError(f"Missing nodes file:  {NODES_PATH}")

    # stream NODES to build entity_types.csv ----------
    print(f"[nodes] reading: {NODES_PATH}")
    node_rows = 0
    wrote_header_entity_types = False

    # read only needed columns to save RAM
    node_usecols = ["node_id", "labels"]
    for chunk in pd.read_csv(
        NODES_PATH, sep="\t", dtype=str, keep_default_na=False, na_filter=False,
        usecols=node_usecols, chunksize=NODE_CHUNKSIZE, encoding="utf-8"
    ):
        _norm_cols(chunk)
        _strip_str(chunk)

        # Validate required columns once
        if node_rows == 0:
            required_node_cols = {"node_id", "labels"}
            if not required_node_cols.issubset(chunk.columns):
                raise ValueError(f"nodes.tsv doesn't contain {required_node_cols}, got {set(chunk.columns)}")
            # init output file
            if ENTITY_TYPES_OUT.exists():
                ENTITY_TYPES_OUT.unlink()
            # write header first time
            chunk.rename(columns={"node_id":"entity_id","labels":"label"}) \
                 .drop_duplicates() \
                 .to_csv(ENTITY_TYPES_OUT, index=False, header=True, mode="w")
            wrote_header_entity_types = True
            node_rows += len(chunk)
            print(f"[nodes] wrote {len(chunk):,} rows to {ENTITY_TYPES_OUT} (header)")

        else:
            # append without header
            chunk.rename(columns={"node_id":"entity_id","labels":"label"}) \
                 .drop_duplicates() \
                 .to_csv(ENTITY_TYPES_OUT, index=False, header=False, mode="a")
            node_rows += len(chunk)

        if node_rows % PRINT_EVERY < NODE_CHUNKSIZE:
            print(f"[nodes] processed ~{node_rows:,} rows")

    if not wrote_header_entity_types:
        # If nodes was empty
        pd.DataFrame(columns=["entity_id","label"]).to_csv(ENTITY_TYPES_OUT, index=False)
    print(f"[nodes] done. total rows seen: {node_rows:,}")
    print(f"[nodes] entity types at: {ENTITY_TYPES_OUT}")

    # stream EDGES to produce triples.tsv and collect sets --------
    print(f"[edges] reading: {EDGES_PATH}")
    if TRIPLES_OUT.exists():
        TRIPLES_OUT.unlink()

    # Unique sets for final ID maps
    entities = set()
    relations = set()

    edge_rows = 0
    wrote_header_triples = False
    edge_usecols = ["start_id", "type", "end_id"]

    for chunk in pd.read_csv(
        EDGES_PATH, sep="\t", dtype=str, keep_default_na=False, na_filter=False,
        usecols=edge_usecols, chunksize=EDGE_CHUNKSIZE, encoding="utf-8"
    ):
        _norm_cols(chunk)
        _strip_str(chunk)

        # Validate expected columns
        if not {"type","start_id","end_id"}.issubset(chunk.columns):
            raise ValueError(f"edges.tsv must contain columns {{'type','start_id','end_id'}}, got {set(chunk.columns)}")

        # Rename and basic cleaning
        chunk = chunk.rename(columns={"start_id":"head", "type":"relation", "end_id":"tail"})
        # drop empties
        chunk = chunk[(chunk["head"]!="") & (chunk["relation"]!="") & (chunk["tail"]!="")]
        # drop self-loops
        chunk = chunk[chunk["head"] != chunk["tail"]]
        # normalize relation case
        chunk["relation"] = chunk["relation"].str.lower()
        # Drop exact duplicates within chunk
        chunk = chunk.drop_duplicates()

        # Update sets
        entities.update(chunk["head"].tolist())
        entities.update(chunk["tail"].tolist())
        relations.update(chunk["relation"].tolist())

        # Append to triples.tsv (FIXME: heavy operation)
        if not wrote_header_triples:
            chunk.to_csv(TRIPLES_OUT, sep="\t", index=False, header=True, mode="w")
            wrote_header_triples = True
        else:
            chunk.to_csv(TRIPLES_OUT, sep="\t", index=False, header=False, mode="a")

        edge_rows += len(chunk)
        if edge_rows % PRINT_EVERY < EDGE_CHUNKSIZE:
            print(f"[edges] appended ~{edge_rows:,} cleaned rows to {TRIPLES_OUT}")

    print(f"[edges] done streaming. total cleaned rows written (approx): {edge_rows:,}")

    # write ID maps
    print("[maps] writing entity2id / relation2id")
    entity2id = pd.DataFrame({"entity_id": sorted(entities)})
    entity2id["idx"] = range(len(entity2id))
    relation2id = pd.DataFrame({"relation": sorted(relations)})
    relation2id["idx"] = range(len(relation2id))

    entity2id.to_csv(ENTITY2ID_OUT, index=False)
    relation2id.to_csv(RELATION2ID_OUT, index=False)

    print(f"[done] triples:\t\t{TRIPLES_OUT}")
    print(f"[done] entity2id:\t\t{ENTITY2ID_OUT}\t({len(entity2id):,} entities)")
    print(f"[done] relation2id:\t\t{RELATION2ID_OUT}\t({len(relation2id):,} relations)")
    print(f"[done] entity_types:\t\t{ENTITY_TYPES_OUT}")

if __name__ == "__main__":
    main()
