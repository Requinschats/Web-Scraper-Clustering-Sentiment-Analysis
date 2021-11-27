from afinn import Afinn

from cluster_Afinn.selectors import select_formatted_document
from common.common import select_list_average
from html_crawler.html_crawler import HtmlCrawler


class ClusterAfinn:
    def __init__(self, clusters, corpus):
        print("Computing sentiment analysis...")
        self.clusters = clusters
        self.cluster_count = len(self.clusters)
        self.corpus = corpus
        self.afinn = Afinn()

    def select_distance_formatted_doc_tuple(self, doc_id_distance):
        distance = doc_id_distance[1]
        doc_content = self.get_formatted_corpus()[doc_id_distance[0]]
        doc_content = self.get_formatted_doc_array(doc_content)
        return distance, doc_content

    def get_sorted_corpus_by_cluster(self):
        for cluster_id in self.clusters:
            self.clusters[cluster_id] = list(
                map(self.select_distance_formatted_doc_tuple, self.clusters[cluster_id]))
        return self.clusters

    def get_formatted_corpus(self):
        return list(map(select_formatted_document, self.corpus))

    @staticmethod
    def get_formatted_doc_array(doc):
        doc_array = doc.split(HtmlCrawler.HTML_SEPARATOR)
        return list(filter(len, doc_array))

    def get_sentence_sentiment_score(self, sentence):
        return self.afinn.score(sentence)

    def get_doc_array_sentiment_score(self, doc_array):
        centroid_sentiments = []
        for distance_sentences in doc_array:
            sentences = distance_sentences[1]
            sentiment_scores = list(map(self.get_sentence_sentiment_score, sentences))
            doc_sentiment = select_list_average(sentiment_scores)
            centroid_sentiments.append(doc_sentiment)
        return select_list_average(centroid_sentiments)

    def get_clusters_sentiment_scores(self):
        clusters = self.get_sorted_corpus_by_cluster()
        for cluster in clusters:
            clusters[cluster] = self.get_doc_array_sentiment_score(clusters[cluster])
        return clusters
