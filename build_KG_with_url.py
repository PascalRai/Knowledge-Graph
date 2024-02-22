# https://thehimalayantimes.com/world/indian-farmers-reject-government-offer-and-say-they-will-carry-on-marching-to-new-delhi-28849
# https://thehimalayantimes.com/business/nepse-drops-near-2000-points-amidst-market-fluctuations
# https://thehimalayantimes.com/nepal/over-150000-cases-yet-to-be-settled

import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import spacy
import networkx as nx

def find_noun_for_pronoun(token):
    for ancestor in token.ancestors:
        if ancestor.pos_ == 'NOUN':
            return ancestor
    return None

def get_entities(sentences):
    if isinstance(sentences, str):
        sentences = [sentences]
    entities = {}
    for i in range(len(sentences)):
        doc = nlp(sentences[i])

        for token in doc:
            temp = find_noun_for_pronoun(token)

            token_head_l = token.head.lemma_
            token_l = token.lemma_
            
            if token.dep_ in ['nsubj', 'nsubjpass'] and token.head.pos_ in ['VERB']:
                if temp:
                    token_l = temp.lemma_

                if token_head_l in entities.keys():
                    entities[token_head_l] = {**entities[token_head_l],**{token_l : token.dep_}}
                else:    
                    entities[token_head_l] = {token_l : token.dep_}

            elif token.dep_ in ['dobj','pobj'] and token.head.pos_ in ['VERB']:
                if token_head_l in entities.keys():
                    entities[token_head_l] = {**entities[token_head_l],**{token_l : token.dep_}}
                else:    
                    entities[token_head_l] = {token_l : token.dep_}

        entities = {k:v for k, v in entities.items() if len(entities[k].keys())>1}
        {entities[k].popitem() for k in entities.keys() if len(entities[k])%2!=0}
    
    return entities

nlp = spacy.load("en_core_web_trf")
G = nx.DiGraph()

url = input("Enter the url of the article: ")

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article = soup.find('div', class_='dropcap column-1 animate-box').find_all('p')
article = (' ').join([article[i].get_text() for i in range(1, len(article))])

doc = nlp(article)

sentences = [sent.text for sent in doc.sents]

entities = get_entities(sentences)

for edge, nodes in entities.items():
    for idx in range(0, len(nodes.keys()), 2):
        G.add_edge(list(nodes.keys())[idx], list(nodes.keys())[idx+1], label=edge)

file_name = input("Enter the Graph filename to be saved (with .gz extension): ")

nx.write_graphml(G, file_name)

pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=900, node_color='skyblue', font_size=8, edge_color='gray', alpha = 0.5)
edge_labels = {(n1, n2): G[n1][n2]['label'] for (n1, n2) in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', alpha=0.9)
plt.show()