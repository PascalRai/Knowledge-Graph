# Knowledge-Graph

1. data:
   - contains Articles CSV; with link and article column
   - KG - made using articles from CSV (file.gz)

2. KG_bagmati_articles.ipynb
   - code for making KG out of the csv

3. build_KG_with_url.py
   - code for making a single KG with a single URL
  
4. extract_articles.ipynb
   - used for extracting articles from web URL

5. question.py
   - Uses KG saved on disk to respond to the question

___
The KG is made using spacy, extracting single tokens subject, object, and relationship (verb)

REBEL model is also tested.
<br>The model has good extraction of relations and can be a benchmark for making nodes and edges.
<br>Though a self-made model is necessary for it to work.