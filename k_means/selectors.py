def select_ranked_terms_by_cluster(order_centroids, terms, true_k, term_per_cluster):
    ranked_terms_by_cluster = []
    for centroid_index in range(true_k):
        cluster_terms = []
        for ind in order_centroids[centroid_index, :term_per_cluster]:
            cluster_terms.append(terms[ind])
        ranked_terms_by_cluster.append(cluster_terms)
    return ranked_terms_by_cluster
