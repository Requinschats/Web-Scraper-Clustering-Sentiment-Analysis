from cluster_Afinn.cluster_afinn import ClusterAfinn
from html_crawler.html_crawler import HtmlCrawler
from k_means.k_means import K_means
from link_crawler.link_crawler import link_crawler
from outputs import output_clustering_information

URL_TO_FETCH_COUNT = 10
PAGES_TO_FETCH = 10
CLUSTER_COUNT_1 = 3
CLUSTER_COUNT_2 = 6
CONCORDIA_BASE_URL = "https://www.concordia.ca/robots.txt"

urls = link_crawler(CONCORDIA_BASE_URL, URL_TO_FETCH_COUNT)
html_documents = HtmlCrawler(CONCORDIA_BASE_URL).fetch_concordia_internal_links_html(PAGES_TO_FETCH)

k_means_3 = K_means(html_documents, n_clusters=CLUSTER_COUNT_1)
k_means_6 = K_means(html_documents, n_clusters=CLUSTER_COUNT_2)

cluster_3_titles, cluster_6_titles = k_means_3.get_clusters_title(), k_means_6.get_clusters_title()

afinn_3_clusters = ClusterAfinn(k_means_3.get_centroids_doc_id_center_distance(), html_documents)
afinn_6_clusters = ClusterAfinn(k_means_6.get_centroids_doc_id_center_distance(), html_documents)

output_clustering_information(PAGES_TO_FETCH, cluster_3_titles, cluster_6_titles, k_means_3,
                              k_means_6, afinn_3_clusters, afinn_6_clusters)
