import numpy as np
import polars as pl
from sklearn.metrics.pairwise import cosine_similarity


def get_car_representation(make_model: str) -> np.array:
    # read clustering data
    cls_data = pl.read_csv("app/data/ClusteringData/data.csv")

    general_repr = (
        cls_data.filter(pl.col("make_model") == make_model)
        .drop(["modelId", "make_model", "segment"])
        .mean()
        .to_numpy()
    )
    general_repr = general_repr.reshape(1, -1)
    general_repr = np.nan_to_num(general_repr, nan=0)

    return general_repr


def get_scores(make_model: str, veh_repr: np.array) -> list:
    # read clustering data
    cls_data = pl.read_csv("app/data/ClusteringData/data.csv")
    # get the segments the vehicle in question shows up
    segments = (
        cls_data.filter(pl.col("make_model") == make_model)["segment"]
        .unique()
        .to_list()
    )
    # compute the scores for all other vehicles in the same segments as out 'make_model'
    scores = []
    filtered_dt = cls_data.filter(pl.col("segment").is_in(segments)).filter(
        pl.col("make_model") != make_model
    )
    for i in range(filtered_dt.shape[0]):
        pair = filtered_dt.drop(["modelId", "make_model", "segment"]).to_numpy()[i]
        # some values may be NaN so we impute the with 0
        pair = np.nan_to_num(pair, nan=0).reshape(1, -1)
        scores.append(cosine_similarity(veh_repr, pair).item())

    return scores


def get_recommendation(make_model: str, scores: list) -> list:
    # read clustering data
    cls_data = pl.read_csv("app/data/ClusteringData/data.csv")
    # get the segments the vehicle in question shows up
    segments = (
        cls_data.filter(pl.col("make_model") == make_model)["segment"]
        .unique()
        .to_list()
    )
    # dataset with required segments, but selected 'make_model' filtered out
    filtered_dt = cls_data.filter(pl.col("segment").is_in(segments)).filter(
        pl.col("make_model") != make_model
    )

    final_dt = pl.concat(
        [filtered_dt.select("make_model"), pl.DataFrame(scores, schema=["scores"])],
        how="horizontal",
    ).sort("scores", descending=True)

    recs = []
    for i in range(len(final_dt["make_model"].to_list())):
        if final_dt["make_model"].to_list()[i] not in recs:
            recs.append(final_dt["make_model"].to_list()[i])
        if len(recs) == 5:
            break

    return recs
