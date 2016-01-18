# Document-Summarization-TextRank

Short Version: A summary of a scientific paper is generated using TextRank algorithm. This summary is evaluated with Rouge and a proposed evaluation measure - "Enhanced Rouge". 

Long Version:
In this project, a document summary is produced for every document by
selecting the most relevant sentences. The TextRank algorithm is used to select these sentences. This
algorithm creates a weighted non-directed graph from all the sentences in a document. The edge
weights indicate the similarity between the two connecting sentences. Then a formula similar to the
PageRank formula used to rank webpages is used to rank the sentences. To produce a summary of k sentences,
the top-k sentences are used.This algorithm is run on a dataset of scientific papers.

The document summaries produced is scored for similarity with the abstracts of the papers and these
similarity scores are reported. For scoring, an enhanced version of the
ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measure is used. Instead of considering only
the exact n-grams present in both the reference summary and the machine-generated summary for Rouge (as is
usual), this project proposes an ‘Enhanced’ Rouge which considers other relevant n-grams. 
These other n-grams in the machine-generated summary contain nouns and adjectives present in both the summaries,
though the exact n-gram is absent in the reference summary.
 
For comparison, the output files containing the 2 versions of the Rouge scores for k=3,4 & 5 are uploaded.
