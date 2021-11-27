from cluster_Afinn.cluster_afinn import ClusterAfinn
from html_crawler.html_crawler import HtmlCrawler
from k_means.k_means import K_means
from link_crawler.link_crawler import link_crawler

urls = link_crawler("https://www.concordia.ca/", 10)

html_crawler = HtmlCrawler()

html_documents = html_crawler.fetch_concordia_internal_links_html(6)

k_means = K_means(html_documents, n_clusters=3)

model = k_means.model

cluster_titles = k_means.get_clusters_title()

clusters = k_means.get_centroids_doc_id_center_distance()

afin = ClusterAfinn(clusters, html_documents)

print(maafin.get_formatted_corpus())
