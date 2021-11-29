def select_formatted_document(doc):
    return doc.replace('\r', '').replace('\n', '')


def select_doc_array_distance_sum(doc_array):
    distance_sum = 0
    for distance_sentences in doc_array:
        distance = distance_sentences[0]
        distance_sum += distance
    return distance_sum


def select_doc_distance_inverse_score(doc_distance, distance_sum):
    if distance_sum == 0: return 1
    return distance_sum / doc_distance


def select_doc_distance_inverse_score_sum(doc_array):
    distance_sum = select_doc_array_distance_sum(doc_array)
    doc_distance_inverse_score_sum = 0
    for distance_sentences in doc_array:
        distance = distance_sentences[0]
        doc_inverse_score = select_doc_distance_inverse_score(distance, distance_sum)
        doc_distance_inverse_score_sum += doc_inverse_score
    return doc_distance_inverse_score_sum


def select_doc_weight(distance, doc_array):
    inverse_score_sum = select_doc_distance_inverse_score_sum(doc_array)
    distance_sum = select_doc_array_distance_sum(doc_array)
    doc_distance_inverse_score = select_doc_distance_inverse_score(distance, distance_sum)
    return doc_distance_inverse_score / inverse_score_sum
