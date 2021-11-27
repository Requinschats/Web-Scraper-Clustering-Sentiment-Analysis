import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
from k_means.selectors import select_ranked_terms_by_cluster


class K_means:
    EXCLUDED_CLUSTER_TITLES = ["concordia"]

    def __init__(self, html_documents, n_clusters=2):
        self.vectorizer = None
        self.vectorized_documents = None
        self.true_k = n_clusters
        self.model = self.select_model(html_documents)

    def select_model(self, html_documents):
        print("Initializing K-Means model...")
        vectorizer = TfidfVectorizer(stop_words='english')
        self.vectorized_documents = vectorizer.fit_transform(html_documents)
        self.vectorizer = vectorizer
        k2_model = KMeans(n_clusters=self.true_k, init='k-means++', max_iter=100, n_init=1)
        k2_model.fit(self.vectorized_documents)
        return k2_model

    def get_top_terms_per_cluster(self, term_per_cluster=50):
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names_out()
        return select_ranked_terms_by_cluster(order_centroids, terms, self.true_k, term_per_cluster)

    def get_clusters_title(self):
        top_terms_per_cluster = self.get_top_terms_per_cluster()
        cluster_titles = []
        for terms_per_cluster in top_terms_per_cluster:
            for term in terms_per_cluster:
                if term not in self.EXCLUDED_CLUSTER_TITLES and term not in cluster_titles:
                    cluster_titles.append(term)
                    break
        return cluster_titles

    def get_text_by_distance_from_center(self):
        from sklearn.metrics import pairwise_distances

        distances = pairwise_distances(self.vectorized_documents, self.model.cluster_centers_,metric='cosine')

        ranking = np.argsort(distances, axis=0)

        df = pd.DataFrame({'text': text})
        for i in range(self.model.n_clusters):
            df['cluster_{}'.format(i)] = ranking[:, i]

        top_n = 2

        for i in range(self.model.n_clusters):
            print('top_{} closest text to the cluster {} :'.format(top_n, i))
            print(df.nsmallest(top_n, 'cluster_{}'.format(i))[['text']].values)
