def select_concordia_internal_links():
    internal_links_list = []
    with open("paths/www.concordia.ca_internal_links.txt") as internal_links:
        for internal_link in internal_links:
            internal_links_list.append(internal_link.strip())
    return internal_links_list
