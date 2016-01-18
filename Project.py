from __future__ import division #To avoid integer division
import os
#from nltk.tokenize.punkt import PunktSentenceTokenizer
import sys  
from Viterbi_POS_Universal import fn_assign_POS_tags
from nltk.corpus import brown
import math
import re
from time import time

#reload(sys)  
#sys.setdefaultencoding('utf8')

def clean_sents(sents_li):
    new_sents = []
    for se in sents_li:
        if se.find("@")!=-1:
            continue
        if se.find("*")!=-1:
            continue
        if se.find("!")!=-1:
            continue
        if se.find("_")!=-1:
            continue
        if se.find("+")!=-1:
            continue 
        if se.find("/")!=-1:
            continue 
        if se.find("\\")!=-1:
            continue
        if se.find("=")!=-1:
            continue                
        ws = sent_to_words(se)
        letters = sum([len(w) for w in ws])
        number = letters/len(ws)
        if number < 2.5:
            continue
        new_sents.append(se)    
    return new_sents
def text_to_sent(text):
    #sentence_tokenizer = PunktSentenceTokenizer()
    sents = re.split("[(.)]\W+",text)
    return clean_sents(sents)

def sent_to_words(sent):
    return sent.lower().split(" ")

def sents_to_graph(sents_li):
    graph = {}
    for outer in range(len(sents_li)-1):
        for inner in range(outer+1,len(sents_li)):
            ssc = sent_sim_score_num_words(sents_li[outer],sents_li[inner])
            if outer not in graph:
                graph[outer]=[]
            graph[outer].append((inner,ssc))
            if inner not in graph:
                graph[inner] = []
            graph[inner].append((outer,ssc))            
                
    return graph

def sent_sim_score_num_nn_words(sent1,sent2):
    words1 = sent_to_words(sent1.lower())
    words2 = sent_to_words(sent2.lower())
    
    denom = math.log(len(set(words1))) + math.log(len(set(words2)))
    if denom < 2:
        return 0
    
    pos_tags1 = fn_assign_POS_tags(words1)
    pos_tags2 = fn_assign_POS_tags(words2)    
    num_meaningful = 0    
    for counter1 in range(len(words1)):
        for counter2 in range(len(words2)):
            if words1[counter1]==words2[counter2]:
                if pos_tags1[counter1] in ['ADJ','N','NP'] or pos_tags2[counter2] in ['ADJ','N','NP']:
                    num_meaningful+=1
    
    return num_meaningful/denom


def sent_sim_score_num_words(sent1,sent2):
    words1 = sent_to_words(sent1.lower())
    words2 = sent_to_words(sent2.lower())
    
    denom = math.log(len(set(words1))) + math.log(len(set(words2)))
    if denom < 2:
        return 0
       
    num = 0    
    for counter1 in range(len(words1)):
        for counter2 in range(len(words2)):
            if words1[counter1]==words2[counter2]:
                num+=1
    
    return num/denom                    


    

def sent_sim_score_lcs(sent1,sent2):
    words1 = sent_to_words(sent1.lower())
    words2 = sent_to_words(sent2.lower())
    denom = math.log(len(set(words1))) + math.log(len(set(words2)))
    if denom < 2:
        return 0
    return lcs(words1,words2,len(words1),len(words2))/denom

def lcs(X, Y, m, n):
 
    if m == 0 or n == 0:
        return 0;
    elif X[m-1] == Y[n-1]:
        return 1 + lcs(X, Y, m-1, n-1);
    else:
        return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n));
 
 
 
            
        
    
    
    
def extract_abstract_text(file_n):
    abstr = ""
    main_b = ""
    file_obj = open(file_n)
    
    abstr_end = False
    
    
    for line in file_obj:
        valid_utf8 = True
        try:
            line.decode('utf-8')
        except UnicodeDecodeError:
            valid_utf8 = False
        if valid_utf8:
            if line.lower().find('acknowledgements')!=-1:
                return abstr.strip(),main_b.strip()      
            if line.lower().find('references')!=-1:
                return abstr.strip(),main_b.strip()      
    
            if line.lower().find('abstract')!=-1:
                line = line.lower()
                line = line.replace('abstract','')
                line = line.strip()
                if len(line)>0:
                    abstr+=line
                abstr_end = True

            elif abstr_end:
                main_b+=line.strip()+" "
            
            
           
    return abstr.strip(),main_b.strip()


def get_newscores(current_scores,graph):
    new_scores = {}
    N = len(graph)
    
    for key in current_scores:
        new_scores[key] = 0.15/N
    
    for p in graph:
        se = graph[p]
        sum_ssc = sum([tup[1] for tup in se])
        if sum_ssc != 0:
            for q,ssc in se:
                new_scores[q] += .85*((ssc*current_scores[p])/sum_ssc)
    
    return new_scores

def compute(graph,epsilon):
    num_iters = 1
    scores = {}
    N = len(graph)
    
    #print "%d people total" %N
    for key in sorted(graph):
        scores[key] = 1.0/N
     #   print key, graph[key]    
    
    
    while True:
        new_scores = get_newscores(scores,graph)
        diff = difference(new_scores,scores)
        """        
        print "Iteration: %d (Difference:%.6f)" %(num_iters,diff)
        for key in sorted(new_scores):
            print key,": %.4f" %new_scores[key],
        print  
        """
        if diff < epsilon:
            break
        scores= new_scores
        num_iters+=1
    
    return scores

def difference(new_scores,current_scores):
    s = 0
    for key in new_scores:
        s+= abs(new_scores[key]-current_scores[key])
    return s

def valid_ref_n_grams(reference_sents):
    flag = True
    for n in range(1,6):
        
        ref_n_grams = set()
        for se in reference_sents:
            words = sent_to_words(se)
            for index in range(len(words)+1-n):
                ref_n_grams.add(' '.join(words[index:index+n]))
        if len(ref_n_grams)==0:
            return False
    
    return True


def rouge(n,reference_sents,machine_sents,counter):
    
    ref_n_grams = set()
    for se in reference_sents:
        words = sent_to_words(se)
        for index in range(len(words)+1-n):
            ref_n_grams.add(' '.join(words[index:index+n]))
    if len(ref_n_grams)==0:
        return -1
    mac_n_grams = set()
    for se in machine_sents:
        #print "se=",se
        words = sent_to_words(se)
        for index in range(len(words)+1-n):
            mac_n_grams.add(' '.join(words[index:index+n]))
    


    intersect = ref_n_grams&mac_n_grams
    return len(intersect)/len(ref_n_grams)
    
def enhanced_rouge(n,reference_sents,machine_sents,counter):
    
    ref_n_grams = set()
    for se in reference_sents:
        words = sent_to_words(se)
        for index in range(len(words)+1-n):
            ref_n_grams.add(' '.join(words[index:index+n]))
    
    if len(ref_n_grams)==0:
        return -1    
    
            
    mac_n_grams = set()
    for se in machine_sents:
        #print "se=",se
        words = sent_to_words(se)
        for index in range(len(words)+1-n):
            mac_n_grams.add(' '.join(words[index:index+n]))
            

    special = set()
    intersect = ref_n_grams&mac_n_grams
    if n > 1:
        uniq_mac = mac_n_grams - ref_n_grams
        for uniq in uniq_mac:
            ws = uniq.split()
            pos_tags = fn_assign_POS_tags(ws)
            for index in range(len(ws)):
                if pos_tags[index] in ['ADJ','N','NP'] :
                    
                    for ref in ref_n_grams:
                        if ref.find(ws[index])!=-1:
                            special.add(uniq)
                   
                            
                   
                
    num = len(special)/n
    return (len(intersect)+num)/len(ref_n_grams)        
        
    

if __name__ == "__main__":
    rouge_li_sum = [0]
    rouge_li_sum*=5
    t1 = time()
    tot_files = 0
    file_write_obj = open("Enahnced_rouge_output.txt","w")
    write_string = "File  \tRouge-1\tRouge-2\tRouge-3\tRouge-4\tRouge-5\n"
    #print write_string
    file_write_obj.write(write_string)
    directory = "D:\\OneDrive\\RPI\\Acads\\1_1\\NLP_Heng_Ji_6962\\Term_Project\\plain"
    file_names = os.listdir(directory)
    os.chdir(directory)
    counter = 0
    for file_n in file_names:
        #Do the operations on the files one by one
        #Read abstract
        #Read main body
        counter+=1
        time1 = time()
        abstract,main_body = extract_abstract_text(file_n)
        if abstract=='' or main_body=='':
            continue
        main_b_sents = text_to_sent(main_body)
        abstract_sents = text_to_sent(abstract)
        if not main_b_sents or not abstract_sents:
            continue
        
        if not valid_ref_n_grams(abstract_sents):
            continue
        
        graph = sents_to_graph(main_b_sents)    

        textrank_scores = compute(graph,0.00001)
        li_tuples = []
        for key in textrank_scores:
            li_tuples.append((textrank_scores[key],key))
        
        li_tuples.sort(reverse=True)
        k=3
        top_sents = [main_b_sents[tup[1]] for tup in li_tuples][:k]
        
        rouge_li = [0]
        rouge_li*=5
        write_string = file_n+"\t"
        for loop_counter in range(5):
            x = enhanced_rouge(loop_counter+1,abstract_sents,top_sents,counter)
            rouge_li[loop_counter] = x
            write_string+=("%.5f" %rouge_li[loop_counter])
            write_string+="\t"
            if x==-1:
                continue
            rouge_li_sum[loop_counter] += rouge_li[loop_counter]
        
        write_string+="\n"
        if x!=-1:
            tot_files +=1
        file_write_obj.write(write_string)
        #print write_string
        
        
    
    
    
    write_string = "Average\t"
    for loop_counter in range(5):
        rouge_li_sum[loop_counter] /= tot_files
        write_string+=("%.5f" %rouge_li_sum[loop_counter])
        write_string+="\t"
    write_string+="\n"
    file_write_obj.write(write_string)
    #print write_string
    write_string = "Total time taken= %.2f seconds" %(time()-t1)
    #print write_string
    file_write_obj.write(write_string+"\n")
    file_write_obj.close()
            
            
            
            
            
        
        
