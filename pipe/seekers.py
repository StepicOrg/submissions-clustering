class Seeker:
    def __init__(self, *, insider_cluster=False, start_from_center=False, only_centroids=False,
                 max_c=200, dist_c=1., cmax_c=20, cdist_c=.1,
                 parralel=False, leaf_size=30):
        self.inside_cluster = insider_cluster
        self.start_from_center = start_from_center
        self.only_centroids = only_centroids
        self.max_c = max_c
        self.dist_c = dist_c
        self.cmax_c = cmax_c
        self.cdist_c = cdist_c
        self.parralel = parralel
        self.leaf_size = leaf_size

    @staticmethod
    def from_predefined(seeker):
        if seeker == "nn":
            return Seeker()
        else:
            raise ValueError("No such seeker supported yet")

    def nn_map(self, data, X, y, c):
        pass
