from cluster_Afinn.selectors import select_formatted_document
from html_crawler.html_crawler import HtmlCrawler


class ClusterAfinn:
    def __init__(self, clusters, corpus):
        self.clusters = clusters
        self.cluster_count = len(self.clusters)
        self.corpus = corpus

    def get_sorted_corpus_by_cluster(self):
        for cluster_id in self.clusters:
            ranked_doc_id_distance = self.clusters[cluster_id]
            self.clusters[cluster_id] = list(
                map(lambda doc_id_distance: (doc_id_distance[1], self.corpus[doc_id_distance[0]]),
                    ranked_doc_id_distance))
        return self.clusters

    def get_formatted_corpus(self):
        corpus = list(map(select_formatted_document, self.corpus))
        print(corpus)

    @staticmethod
    def get_formatted_doc_array(doc):
        doc_array = doc.split(HtmlCrawler.HTML_SEPARATOR)
        return list(filter(len, doc_array))
