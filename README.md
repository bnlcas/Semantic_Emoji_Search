# Semantic_Emoji_Search
This is a prototype algorithm to find emojis that are semantically related to a key search phrase (Only works in English). This would allow someone to enter a search word and then receive a ranked list of emojis whose Unicode descriptions are the most semantically similar to the search phrase. This would be great for an emoji keyboard. Instead of finding a category like 'food', it would be possilbe to find things that are most similar to a specific concept like 'celebration'.

This algorithm relies on a semantic space representation of english tokens to calculate the semantic similarity between a search phrase an emoji descriptions.
In order to run this program, you will need to download or train a set of english word vectors. For my prototype I used [Facebook's FastText Word Vectors](https://fasttext.cc/docs/en/english-vectors.html).
I have also restricted the semantic space to only include the 10000 most common words in English.

The python prototype only runs on python 2.7 - will update if there is interest. Also, you will need to edit lines 101 and 102 of 'emoji_search.py' to match your local directory information, a

The javascript version should run in a browser out of the box.


