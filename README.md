# Document-Summarization-TextRank

In this project, a document summary is produced for every document by
selecting the most relevant sentences. The TextRank algorithm is used to select these sentences. This
algorithm creates a weighted non-directed graph from all the sentences in a document. The edge
weights indicate the similarity between the two connecting sentences. Then a formula similar to the
PageRank formula used to rank webpages is used to rank the sentences. To produce a summary of ksentences,
the top-k sentences are used.This algorithm is run on a dataset of scientific papers.

The document summaries produced will be scored for similarity with the abstracts of this paper and this
similarity score will be reported, along with the summaries. For scoring, an enhanced version of the
ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measure is used. Instead of considering only
the n-grams present in the reference summary and the machine-generated summary for Rouge (as is
usual), this project proposes an ‘Enhanced’ Rouge which also considers other relevant n-grams. This
relevance is indicated by parts of speech tags of the words present in the n-grams. These words are
present in both the summary and the abstract, though the n-grams themselves are only present in the
machine-generated summary.
 
