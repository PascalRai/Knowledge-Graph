import networkx as nx
import matplotlib.pyplot as plt
import spacy

nlp = spacy.load("en_core_web_trf")
file_to_load = input("Enter the graph path: ")
G = nx.read_graphml(file_to_load)

pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=900, node_color='skyblue', font_size=8, edge_color='gray', alpha = 0.5)
edge_labels = {(n1, n2): G[n1][n2]['label'] for (n1, n2) in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', alpha=0.9)
plt.show()

try_again = 'Y'

while try_again.lower() == 'y':
    question = input("Enter the question: ")

    search_for_nodes = [token.lemma_.lower() for token in nlp(question)]
    # search_for_nodes = [token.lemma_ for token in nlp(question) if token.pos_ == 'NOUN']
    print('Searching these nodes in KG: ', search_for_nodes)

    match = 0
    for each_possible_node in search_for_nodes:
        if G.has_node(each_possible_node):
            match+=1
            neighbors_node = list(G.neighbors(each_possible_node))
            for each_neighbour_node in neighbors_node:
                relationship = G.get_edge_data(each_possible_node, each_neighbour_node)['label']
                print(f'{each_possible_node} -> {relationship} -> {each_neighbour_node}')

    if match == 0:
        print("No information found in Knowledge Graph")
    
    try_again = input('Wanna try again? (Y/N): ')
    if try_again == '':
        try_again = 'Y'