from sklearn.metrics import pairwise_distances

from common.common import sort_by_second_tuple_element


def select_tf_idf_ranked_terms_by_cluster(order_centroids, terms, true_k, term_per_cluster):
    ranked_terms_by_cluster = []
    for centroid_index in range(true_k):
        cluster_terms = []
        for ind in order_centroids[centroid_index, :term_per_cluster]:
            cluster_terms.append(terms[ind])
        ranked_terms_by_cluster.append(cluster_terms)
    return ranked_terms_by_cluster


def select_distance_to_cluster(k_means):
    return list(map(lambda distances: min(distances),
                    pairwise_distances(k_means.vectorized_documents, k_means.model.cluster_centers_,
                                       metric='cosine')))


def select_centroids_doc_id_center_distance(corpus, labels, distance_to_cluster):
    centroid_doc_id_center_distance = {}
    for doc_id in range(len(corpus)):
        assigned_centroid = labels[doc_id]
        distance_to_centroid = distance_to_cluster[doc_id]
        if assigned_centroid in centroid_doc_id_center_distance:
            centroid_doc_id_center_distance[assigned_centroid].append(
                (doc_id, distance_to_centroid))
            centroid_doc_id_center_distance[assigned_centroid] = sort_by_second_tuple_element(
                centroid_doc_id_center_distance[assigned_centroid])
        else:
            centroid_doc_id_center_distance[assigned_centroid] = [
                (doc_id, distance_to_centroid)]
    return centroid_doc_id_center_distance
