#!/usr/bin/env python3

table_bins = table_bins[
    [
        ("Unnamed: 1_level_1", "bin_id"),
        ("chr", "count"),
        ("length", "sum"),
        ("length", "min"),
        ("length", "max"),
        ("length", "std"),
        ("length", "N50"),
    ]
]
table_bins.columns = [
    "user_genome",
    "contig_number",
    "contig_length_sum",
    "contig_length_min",
    "contig_length_max",
    "contig_length_std",
    "N50",
]
table_bins["user_genome"] = table_bins.apply(lambda x: x["user_genome"] + ".fa", axis=1)

table_gtdb = pd.read_csv(output.table_gtdb, sep="\t").rename(
    columns={"classification": "GTDB classification"}
)

table_ncbi = pd.read_csv(output.table_ncbi, sep="\t")

table_checkm = pd.read_csv(input.table_checkm, sep="\t").rename(
    columns={"bin_id": "user_genome"}
)
table_checkm["user_genome"] = table_checkm.apply(
    lambda x: x["user_genome"] + ".fa", axis=1
)

table_gtdb.join(
    table_ncbi.set_index(["user_genome", "GTDB classification"]),
    on=["user_gneome", "GTDB classification"],
).join(table_checkm.set_index("user_genome"), on="user_genome").join(
    table_bins.set_index("user_genome"), on="user_genome"
).loc[
    :,
    [
        "user_genome",
        "GTDB classification",
        "NCBI classification",
        "completeness",
        "contamination",
        "strain_heterogeneity",
        "MIMAG_quality_level",
        "SGB_quality_level",
        "quality_score",
        "contig_number",
        "contig_length_sum",
        "contig_length_min",
        "contig_length_max",
        "contig_length_std",
        "N50",
    ],
].to_csv(
    output.table_all, sep="\t", index=False
)
