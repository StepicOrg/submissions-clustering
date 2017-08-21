import os

import pandas as pd

from subsclu.utils.read import split_into_lists


def _make_best_scores(submissions, scnn, scorrer):
    best_scores = []
    for code, status in submissions:
        if status == "correct":
            best_scores.append(None)
        else:
            return 0


def make_error(metric):
    def error(sc, submissions, presaved_best_metric_path=None):
        sc.fit(submissions)
        codes, statuses = split_into_lists(submissions)
        codes, statuses = pd.Series(codes), pd.Series(statuses)
        correct_codes, wrong_codes = codes[statuses == "correct"], codes[statuses != "correct"]

        def neighbors_codes(neighbors_inds):
            return codes.iloc[neighbors_inds].tolist()

        if presaved_best_metric_path is not None and os.path.exists(presaved_best_metric_path):
            best_scores = default_load(presaved_best_metric_path)
        else:
            best_scores = _make_best_scores(submissions, scnn, scorrer)
        if presaved_best_metric_path is not None:
            default_save(best_scores, presaved_best_metric_path)

        wrong_codes = codes[statuses != "correct"]
        tsum = 0
        for code, neighbors_inds in zip(wrong_codes, sc.neighbors(wrong_codes)):
            if neighbors_inds.size:  # because we aint consider bad cases - such as wrong indentation
                tsum += metric.best_score(code, neighbors_codes(neighbors_inds))

        return tsum

        """
        codes, _ = split_into_lists(submissions)
        codes = pd.Series(codes)
        
        def neighbors_codes(neighbors_inds):
            return codes.iloc[neighbors_inds].tolist() 
        """

        """
        codes, statuses = split_into_lists(submissions)
        correct_indicies, _ = preprocessor.fit_sanitize(codes)
        codes = pd.Series(codes).iloc[correct_indicies].reset_index(drop=True).tolist()
        statuses = pd.Series(statuses).iloc[correct_indicies].reset_index(drop=True).tolist()

        sc.fit(submissions)
        """

        """
        codes, statuses = split_into_lists(submissions)
        correct_indicies, structs = preprocessor.fit_sanitize(codes)
        statuses = pd.Series(statuses).iloc[correct_indicies].reset_index(drop=True)
        correct_structs = structs[statuses == "correct"]
        wrong_structs = structs[statuses != "correct"]

        if best_scores_path is not None and os.path.exists(best_scores_path):
            best_scores = default_load(best_scores_path)
        else:
            best_scores = _make_best_scores(submissions, scnn, scorrer)
        if best_scores_path is not None:
            default_save(best_scores, best_scores_path)

        return 0
        """

    return error
