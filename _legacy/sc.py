# pre stage
self._add_submissions(submissions)
data = self._submissions

# vectorizer
X = self.vectorizer.fit_transform(data["code"]).toarray()
if "preprocessor" in self.vectorizer.named_steps:
    data = data.iloc[vectorizer.named_steps["preprocessor"].correct_index].reset_index(drop=True)

# clusterizer
if self.clusterizer is not None:
    y = self.clusterizer.fit_predict(X).astype(int)
else:
    y = -np.ones(X.shape[0], dtype=int)

# seeker
self.seeker.fit(X[data.status == "correct"], y[data.status == "correct"], find_centers(X, y))

def norm_submission(submission):
    if isinstance(submission, tuple) and len(submission) == 2:
        return submission
    elif isinstance(submission, str):
        return submission, "correct"
    elif hasattr(submission, "code"):
        return submission.code, submission.status if hasattr(submission, "status") else "correct"
    elif hasattr(submission, "__getitem__") and "code" in submission:
        return submission["code"], submission["status"] if "status" in submission else "correct"
    else:
        try:
            return str(submission), "correct"
        except Exception as e:
            raise ValueError("Wrong submission form") from e