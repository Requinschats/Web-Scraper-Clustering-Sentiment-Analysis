import numpy as np

from html_crawler.html_crawler import HtmlCrawler
from k_means.k_means import K_means
from link_crawler.link_crawler import link_crawler

urls = link_crawler("https://www.concordia.ca/", 10)

html_crawler = HtmlCrawler()

html_documents = html_crawler.fetch_concordia_internal_links_html(6)

k_means = K_means(html_documents, n_clusters=2)

model = k_means.model

cluster_titles = k_means.get_clusters_title()




# doc_id_dic = {i: np.where(model.labels_ == i)[0] for i in range(model.n_clusters)}
# clusters = []
# for key, value in doc_id_dic.items():
#     temp = value.tolist()
#     clusters.append(temp)
#
# print(model.cluster_centers_)
# print(clusters)


