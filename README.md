# Document-Summarization-TextRank

In this project, a document summary is produced for every document by
selecting the most relevant sentences. The TextRank algorithm is used to select these sentences. This
algorithm creates a weighted non-directed graph from all the sentences in a document. The edge
weights indicate the similarity between the two connecting sentences. Then a formula similar to the
PageRank formula used to rank webpages is used to rank the sentences. To produce a summary of k sentences,
the top-k sentences are used.This algorithm is run on a dataset of scientific papers.

The document summaries produced is scored for similarity with the abstracts of the papers and these
similarity scores are reported. For scoring, an enhanced version of the
ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measure is used. Instead of considering only
the n-grams present in the reference summary and the machine-generated summary for Rouge (as is
usual), this project proposes an ‘Enhanced’ Rouge which also considers other relevant n-grams. This
relevance is indicated by parts of speech tags of the words present in the n-grams. These words are
present in both the summary and the abstract, though the n-grams themselves are only present in the
machine-generated summary.
 
For comparison, the output files conatining the 2 versions of the Rouge scores for k=3,4 & 5 are uploaded.
