import os

path_to_demo_file = "./outputs/demo.txt"
if os.path.isfile(path_to_demo_file):
    os.remove(path_to_demo_file)


def output_cluster_evaluation(k_means, cluster_count):
    file = select_demo_file()
    file.write("\nNumber of clusters: " + str(cluster_count))
    file.write("\nSSE score for " + str(cluster_count) + " clusters: " + str(k_means.get_sse()))


def output_cluster_information(document_fetched_count, titles):
    file = select_demo_file()
    file.write("\n-----------------------------------------------------------")
    file.write("\nNumber of documents fetched: " + str(document_fetched_count))
    file.write("\nTitles: " + str(titles))


def select_demo_file():
    return open(path_to_demo_file, "a+")


def select_50_most_informative_terms_file(cluster_count):
    path_to_50_most_informative_terms_file = "outputs/" + str(
        cluster_count) + "_50_most_informative_terms.txt"
    return open(path_to_50_most_informative_terms_file, "w")


def output_most_informative_term_per_cluster(k_means, cluster_count):
    file = select_50_most_informative_terms_file(cluster_count)
    file.write(str(k_means.get_top_terms_per_cluster()))


def output_sentiment_results(afinn):
    file = select_demo_file()
    file.write(
        "\nSentiment scores: " + str(dict(sorted(afinn.get_clusters_sentiment_scores().items()))))


def output_clustering_information(PAGES_TO_FETCH, cluster_3_titles, cluster_6_titles, k_means_3,
                                  k_means_6, afinn3, afinn6):
    output_cluster_information(PAGES_TO_FETCH, cluster_3_titles)
    output_cluster_evaluation(k_means_3, 3)
    output_sentiment_results(afinn3)

    output_cluster_information(PAGES_TO_FETCH, cluster_6_titles)
    output_cluster_evaluation(k_means_6, 6)
    output_sentiment_results(afinn6)

    output_most_informative_term_per_cluster(k_means_3, 3)
    output_most_informative_term_per_cluster(k_means_6, 6)
