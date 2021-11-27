from cluster_Afinn.cluster_afinn import ClusterAfinn
from html_crawler.html_crawler import HtmlCrawler
from k_means.k_means import K_means
from link_crawler.link_crawler import link_crawler

PAGES_TO_FETCH = 6
CLUSTER_COUNT = 2

urls = link_crawler("https://www.concordia.ca/", 10)
html_documents = HtmlCrawler().fetch_concordia_internal_links_html(PAGES_TO_FETCH)

k_means = K_means(html_documents, n_clusters=CLUSTER_COUNT)
cluster_titles = k_means.get_clusters_title()

#  6: very positive
#  3: positive
#  0: neutral
# -3: negative
# -6: very negative

afin = ClusterAfinn(k_means.get_centroids_doc_id_center_distance(), html_documents)

print(cluster_titles)
print(afin.get_clusters_sentiment_scores())
