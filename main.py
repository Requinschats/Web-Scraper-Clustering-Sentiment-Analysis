from cluster_Afinn.cluster_afinn import ClusterAfinn
from html_crawler.html_crawler import HtmlCrawler
from k_means.k_means import K_means
from link_crawler.link_crawler import link_crawler

URL_TO_FETCH_COUNT = 10
PAGES_TO_FETCH = 6
CLUSTER_COUNT_1 = 2
CLUSTER_COUNT_2 = 6
CONCORDIA_BASE_URL = "https://www.concordia.ca/robots.txt"

urls = link_crawler(CONCORDIA_BASE_URL, URL_TO_FETCH_COUNT)
html_documents = HtmlCrawler(CONCORDIA_BASE_URL).fetch_concordia_internal_links_html(PAGES_TO_FETCH)

k_means_2 = K_means(html_documents, n_clusters=CLUSTER_COUNT_1)
k_means_6 = K_means(html_documents, n_clusters=CLUSTER_COUNT_2)

cluster_2_titles = k_means_2.get_clusters_title()
cluster_6_titles = k_means_6.get_clusters_title()

#  6: very positive, 3: positive, 0: neutral, -3: negative, -6: very negative
afin_2_clusters = ClusterAfinn(k_means_2.get_centroids_doc_id_center_distance(), html_documents)
print(cluster_2_titles)
print(afin_2_clusters.get_clusters_sentiment_scores())
