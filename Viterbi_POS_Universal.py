from __future__ import division #To avoid integer division
from operator import itemgetter
from nltk.corpus import brown

import time
start_time = time.time()

def fn_train(category):

###Training Phase###
    """As an experiment, I will train on the data of the news category
    & test on the data of the government category
    The tagset is the minimal universal
    """
    brown_news_tagged = brown.tagged_words(categories=category,simplify_tags=True)
    num_words_train = len(brown_news_tagged)
    train_li_words = ['']
    train_li_words*= num_words_train

    train_li_tags = ['']
    train_li_tags*= num_words_train

    for i in range(num_words_train):
        train_li_words[i] = brown_news_tagged[i][0]
        train_li_tags[i] = brown_news_tagged[i][1]


    dict2_tag_follow_tag_ = {}
    """Nested dictionary to store the transition probabilities
    each tag A is a key of the outer dictionary
    the inner dictionary is the corresponding value
    The inner dictionary's key is the tag B following A
    and the corresponding value is the number of times B follows A
    """

    dict2_word_tag = {}
    """Nested dictionary to store the emission probabilities.
    Each word W is a key of the outer dictionary
    The inner dictionary is the corresponding value
    The inner dictionary's key is the tag A of the word W
    and the corresponding value is the number of times A is a tag of W
    """

    dict_word_tag_baseline = {}
    #Dictionary with word as key and its most frequent tag as value

    for i in range(num_words_train-1):
        outer_key = train_li_tags[i]
        inner_key = train_li_tags[i+1]
        dict2_tag_follow_tag_[outer_key]=dict2_tag_follow_tag_.get(outer_key,{})
        dict2_tag_follow_tag_[outer_key][inner_key] = dict2_tag_follow_tag_[outer_key].get(inner_key,0)
        dict2_tag_follow_tag_[outer_key][inner_key]+=1

        outer_key = train_li_words[i]
        inner_key = train_li_tags[i]
        dict2_word_tag[outer_key]=dict2_word_tag.get(outer_key,{})
        dict2_word_tag[outer_key][inner_key] = dict2_word_tag[outer_key].get(inner_key,0)
        dict2_word_tag[outer_key][inner_key]+=1


    """The 1st token is indicated by being the 1st word of a senetence, that is the word after period(.)
    Adjusting for the fact that the first word of the document is not accounted for that way
    """

    dict2_tag_follow_tag_['.'] = dict2_tag_follow_tag_.get('.',{})
    dict2_tag_follow_tag_['.'][train_li_tags[0]] = dict2_tag_follow_tag_['.'].get(train_li_tags[0],0)
    dict2_tag_follow_tag_['.'][train_li_tags[0]]+=1


    last_index = num_words_train-1

    #Accounting for the last word-tag pair
    outer_key = train_li_words[last_index]
    inner_key = train_li_tags[last_index]
    dict2_word_tag[outer_key]=dict2_word_tag.get(outer_key,{})
    dict2_word_tag[outer_key][inner_key] = dict2_word_tag[outer_key].get(inner_key,0)
    dict2_word_tag[outer_key][inner_key]+=1


    """Converting counts to probabilities in the two nested dictionaries
    & also converting the nested dictionaries to outer dictionary with inner sorted lists
    """
    for key in dict2_tag_follow_tag_:
        di = dict2_tag_follow_tag_[key]
        s = sum(di.values())
        for innkey in di:
            di[innkey] /= s
        di = di.items()
        di = sorted(di,key=lambda x: x[0])
        dict2_tag_follow_tag_[key] = di

    for key in dict2_word_tag:
        di = dict2_word_tag[key]
        dict_word_tag_baseline[key] = max(di, key=di.get)
        s = sum(di.values())
        for innkey in di:
            di[innkey] /= s
        di = di.items()
        di = sorted(di,key=lambda x: x[0])
        dict2_word_tag[key] = di

    return dict2_tag_follow_tag_, dict2_word_tag, dict_word_tag_baseline


###Testing Phase###

def fn_assign_POS_tags(words_list):

    num_words_test = len(words_list)

    output_li = ['']
    output_li*= num_words_test
    for i in range(num_words_test):
        if i==0:    #Accounting for the 1st word in the test document for the Viterbi
            di_transition_probs = dict2_tag_follow_tag_['.']
        else:
            di_transition_probs = dict2_tag_follow_tag_[output_li[i-1]]
            
        di_emission_probs = dict2_word_tag.get(words_list[i],'')

        #If unknown word  - tag = 'NP'
        if di_emission_probs=='':
            output_li[i]='NP'
            
        else:
            max_prod_prob = 0
            counter_trans = 0
            counter_emis =0
            prod_prob = 0
            while counter_trans < len(di_transition_probs) and counter_emis < len(di_emission_probs):
                tag_tr = di_transition_probs[counter_trans][0]
                tag_em = di_emission_probs[counter_emis][0]
                if tag_tr < tag_em:
                    counter_trans+=1
                elif tag_tr > tag_em:
                    counter_emis+=1
                else:
                    prod_prob = di_transition_probs[counter_trans][1] * di_emission_probs[counter_emis][1]
                    if prod_prob > max_prod_prob:
                        max_prod_prob = prod_prob
                        output_li[i] = tag_tr
                        #print "i=",i," and output=",output_li[i]
                    counter_trans+=1
                    counter_emis+=1    
        

        if output_li[i]=='': #In case there are no matching entries between the transition tags and emission tags, we choose the most frequent emission tag
            output_li[i] = max(di_emission_probs,key=itemgetter(1))[0]  
            
    return output_li

tup = fn_train("news")
dict2_tag_follow_tag_ = tup[0]
dict2_word_tag = tup[1]
dict_word_tag_baseline = tup[2]

if __name__ == "__main__":

    category = "news"

    brown_gov_tagged =  brown.tagged_words(categories='government',simplify_tags=True)

    num_words_test = len(brown_gov_tagged)

    test_li_words = ['']
    test_li_words*= num_words_test

    test_li_tags = ['']
    test_li_tags*= num_words_test

    num_errors = 0
    num_errors_baseline = 0

    for i in range(num_words_test):
        temp_li = brown_gov_tagged[i]
        test_li_words[i] = temp_li[0]
        test_li_tags[i] = temp_li[1]


    output_li = fn_assign_POS_tags(test_li_words)
    
    for i in range(num_words_test):
        if output_li[i]!=test_li_tags[i]:
            num_errors+=1

    print "Fraction of errors (Viterbi) :",(num_errors/num_words_test)



    print time.time() - start_time, "seconds"
    
    print set(test_li_tags)
    print set(output_li)



