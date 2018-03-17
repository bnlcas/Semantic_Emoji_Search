# Semantic_Emoji_Search
This is a prototype algorithm to find emojis that are semantically related to a key search phrase. The idea is that a user would enter a search phrase
and they would then receive a list of emojis whose English descriptions are semantically similar to the search phrase.

This algorithm relies on a semantic space representation of english tokens to calculate the semantic similarity between a search phrase an emoji descriptions.
In order to run this program, you will need to download or train a set of english word vectors. For my model, I used [Facebook's FastText Word Vectors](https://fasttext.cc/docs/en/english-vectors.html).
I have also restricted the semantic space to only include the 10000 most common words in English.

You will need to edit lines 101 and 102 of 'emoji_search.py' to match your local directory information.

