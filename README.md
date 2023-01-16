
# Problem Statement

Given a collection of huge text files or word documents, give a scalable algorithm to search for a given word. If not an exact match, return the closest match.

For example, let's Assume the text document contains the word documents contain following sentences:

Word Document 1: """Following mice attacks, caring farmers were marching to Delhi for better living conditions. Delhi police on Tuesday fired water cannons and tear gas shells at protesting farmers as they tried to break barricades with their cars, automobiles, and tractors. """

Word Document 2: """Sometimes to understand a word's meaning you need more than a definition; you need to see the word used in a sentence. At YourDictionary, we give you the tools to learn what a word means and how to use it correctly. With this sentence maker, simply type a word in the search bar and see a variety of sentences with that word used in different ways. Our sentence generator can provide more context and relevance, ensuring you use a word the right way. """

Word Document 3: '""Whether it’s simple sentences for those just learning the English language or phrasing for an academic paper, this easy-to-use sentence generator will help you choose your words with confidence. """

If we wish to find the documents which contain the word “sentence”; clearly, the word is present in document 2 and document 3, then the algorithm should return both the documents along with the occurrences of the word in the document.

# Why is this a Problem?

Searching for the word linearly after getting a search request is not feasible because the best algorithm to do so is in the order O(N) where N is the number of words. For relatively big and denser documents, this approach is not feasible because the time it takes to retrieve the results is high. Through this project, we wish to retrieve the results in logarithmic time. And also, if a user is interested in the word “march”; the search should also be able to retrieve the words “marching”, “Marching”, “MARCH”, etc. which have the same meaning but have different letters or differ by case, tense, etc. This search is not possible through the Linear Search.

The other limitation of linear search is that it doesn’t order the search results by relevance. It simply orders the search results by the order of the occurrence in every document. However, a better approach would be to sort the results based on the relevance of the document. For example, if a user has searched for the same term and has clicked a document and found his “words of interest”, then, this document would be more relevant for the next user. Therefore, we devise a new parameter using which we calculate the relevance of the document.

# Approach

The idea behind the algorithm is to preprocess the documents, perform reverse indexing on the words and store them as the key-value pairs. However, before performing the indexing, the words should be preprocessed to store the words in a single tense and single case. Therefore, the steps performed are as follows:

1.  Perform Lemmatization on the words as we read them: Lemmatization usually refers to doing things properly with the use of a vocabulary and morphological analysis of words, normally aiming to remove inflectional endings only and to return the base or dictionary form of a word, which is known as the lemma.
    
2.  After Lemmatization, we perform indexing of the words. The idea of indexing is to:  Store the words in a key-value pair; where the key is the word and the value is the list of documents and lines in which the words occur. We store this information in a YAML file to avoid recomputation in sorted order.
    
3.  When we get a search query, we check the HashMap for an exact match and try to retrieve the occurrence of the word in Constant Time.
    
4.  If the word is present in the hashmap, we retrieve all the occurrences of the word in all the documents at a constant time. Once we retrieve the occurrences, we display the results in the order of relevance. The relevance of a document is computed by various parameters; mainly dealing with how many clicks a specific document received for a search and how frequent the word occurs in the document.
    
5.  If the exact word is not present in the HashMap, we perform Binary Search on the already stored sorted words to retrieve the closest word.
    
6.  Therefore, if we find an exact match, we can retrieve the result in a Constant time and if we don't find the exact match, we retrieve the closest word in the documents in a Log(N) time where N is the number of unique words present in all the documents.

# Data Structures & Algorithms Used

The following is the list of algorithms/steps we would be using in this project.

1.  Lemmatization
2.  Indexing - Forward Indexing
3.  Sorting - Insertion Sort
4. Custom Ranking Algorithm to rank the searched items.
5.  Heaps
6.  Heapify
7.  Tries

# Tech Stack Used


# How to Run this Project
https://text-based-search-engine.herokuapp.com/

# Demo

# Limitations
