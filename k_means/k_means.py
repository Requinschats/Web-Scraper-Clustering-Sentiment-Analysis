import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
from k_means.selectors import select_ranked_terms_by_cluster, select_distance_to_cluster, \
    select_centroids_doc_id_center_distance
from sklearn.metrics import pairwise_distances


class K_means:
    EXCLUDED_CLUSTER_TITLES = ["concordia"]

    def __init__(self, html_documents, n_clusters=2):
        self.vectorizer = None
        self.vectorized_documents = None
        self.true_k = n_clusters
        self.corpus = html_documents
        self.model = self.select_model()

    def select_model(self):
        print("Initializing K-Means model...")
        vectorizer = TfidfVectorizer(stop_words='english')
        self.vectorized_documents = vectorizer.fit_transform(self.corpus)
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

    def get_centroids_doc_id_center_distance(self):
        labels = self.model.labels_
        distance_to_cluster = select_distance_to_cluster(self)
        return select_centroids_doc_id_center_distance(self.corpus, labels, distance_to_cluster)
