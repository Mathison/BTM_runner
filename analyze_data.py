#############2018/8/15
#############Jiawei Li
####This file is used to analyze the .json file and capture the words in it

import json
import math
import gzip
import os, sys
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import re
import collections
import social_read as sr

def clean(text):
    text = str.replace(text,',',' ')
    text = str.replace(text,'+',' ')
    text = str.replace(text,'=',' ')

    ######first we need to change the hyperlink, email and phone number
    ####change hyper link to ' '
    text = ' '.join(re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"," ", text).split())

    ####change phonenumber to ' '
    text = ' '.join(re.sub("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"," ", text).split())

    ####change email address to ' '
    text = ' '.join(re.sub("\S+@\S+"," ", text).split())

    text = str.replace(text,"'",' ')
    text = str.replace(text,'"',' ')
    text = str.replace(text,'!',' ')
    text = str.replace(text,'^',' ')
    text = str.replace(text,'(',' ')
    text = str.replace(text,')',' ')
    text = str.replace(text,'%',' ')
    text = str.replace(text,'-',' ')
    text = str.replace(text,'_',' ')
    text = str.replace(text,'|',' ')
    text = str.replace(text,'.',' ')
    text = str.replace(text,':',' ')

    word_list = text.split(' ')
    remove_words = []
    for word in word_list:
        if word == ' ' or word == '':
            continue
        if word[0] == '#' or word[0] == '@':
            remove_words.append(word)

    for word in remove_words:
        word_list.remove(word)
    text = ' '.join(word_list)

    text = text.split(' ')
    new_text = []
    for each in text:
        
        if(str.find(each,'http') != -1):
            continue
        
        if not each.isalnum():
            continue
        new_text.append(str.lower(each));
    text = ' '.join(new_text)

    return text

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def read_json(file,platform):
    text_data = []
    print("Reading " + file)
    try:
        with open(file,'r',encoding = 'utf-8') as f:
            text_data = get_data_text(f)
    except Exception as e:
        print(e)
        with open(file,'r',encoding = 'utf-16') as f:
            text_data = get_data_text(f)
    return text_data

###########used to go through the folder, and collect the data
###########it will return the list of json data in all files in the folder
def read_folder(path,platform):
    total_data = []
    read = 0
    for filename in sorted(os.listdir(path)):
        d = read_json(path+filename,platform)
        total_data.extend(d)
    return data


def get_data_text(f):
    data = []
    for index,line in enumerate(f):
        try:
            ori_data = json.loads(line)
            if line.strip():
                if platform == 'youtube_comment':
                #####clean the original json file
                    data += sr.get_youtube_comments_text(ori_data)
                                
                if platform == 'youtube_description':
                #####clean the original json file
                    data.append(ori_data['description'])

                if platform == 'youtube_title':
                #####clean the original json file
                    data.append(ori_data['title'])


                if platform == 'instagram_comment':
                #####clean the original json file
                    data += sr.get_instagram_comments_text(ori_data)
 
                if platform == 'instagram_post':
                #####clean the original json file
                    text = sr.get_instagram_text(ori_data)
                    data.append(text)
                       
                if platform == 'twitter':
                #####clean the original json file
                    text = sr.get_twitter_text(ori_data)
                    data.append(text) 
                           
                if platform == 'tumblr_comment':
                #####clean the original json file
                    data += sr.get_tumblr_comments_text(ori_data)

                if platform == 'tumblr_post':
                #####clean the original json file
                    data.append(ori_data['text'])

                if platform == 'tumblr_description':
                #####clean the original json file
                    data.append(ori_data['description']) 

                if platform == 'reddit_description':
                #####clean the original json file
                    text = sr.get_reddit_description_text(ori_data)
                    data.append(text)

                if platform == 'reddit_comment':
                #####clean the original json file
                    data += sr.get_reddit_comments_text(ori_data)

                if platform == 'reddit_title':                        
                    text = sr.get_reddit_title_text(ori_data)
                    data.append(text)

        except Exception as e:
            print(e)
            print("can't open line "+str(index))
    return data


###########get words from one single clean text, return a list of words
def get_word(text):
    special_word = ['rt','co','amp'] #here is the word we don't want it to show up in the sentence
    words = []
    for w in clean(text).split():
        if isEnglish(w):
            if w not in set(stopwords.words('english')) and w not in special_word:
                words.append(w)
    return words
    

############clean the text data and collect the words, the input should be a list of texts
############it will return a vocabulary of words and a dictionary of frequency
def collect_words(list_text,vocab):
    #words_vocab = []
    for t in list_text:
        vocab += get_word(t)
        vocab = list(set(vocab))
    return vocab

##########write vocab to a txt file
def write_vocab(vocab,vocab_path):
    try:
        file = open(vocab_path, 'w')
        for idx,item in enumerate(vocab):
            #file.write(str(idx)+'\t')
            file.write("%s\n" % item)
        file.close()
    except:
        print("can't open file" + vocab_path)
        
def read_vocab(vocab_path):
    try:
        with open(vocab_path) as f:
            vocab = f.readlines()
            vocab = [x.replace('\n','') for x in vocab] 
            return vocab
    except:
        print("can't open file" + vocab_path)

###########write the index code to the btm index file
def get_index(text_list,vocab):
    index_list = []
    for t in text_list:
        words = get_word(t)
        index = []
        for w in words:
            try:
                index.append(vocab.index(w))
            except Exception as e:
                print(e)
                continue
        index_list.append(index)
    return index_list

def write_index(index_list,output_path):
    #vocab = read_vocab(vocab_path)
    btm_input = open(output_path,'w')
    for i in index_list:
        #words = get_word(t)
        for w in i:
            btm_input.write(str(w)+' ')
        btm_input.write('\n')      
    btm_input.close()
      
    #except:
        #print("can't open file" + vocab_path + " or " +input_path)
    
def run_btm_learning(inputfile, no_topics, vocab_file, alpha, beta, total_number_of_iterations, save_step, output_path):
    # Example:
    # ../../BTM/src/btm est 150 3577 0.3 0.01 1000 10 data_processing_files/btm_input.txt output/BTM_OUTPUT/
    #btm_directory = '../BTM/batch/btm '
    execute_string = btm_directory + 'est ' + str(no_topics) + ' ' +             str(len(open(vocab_file,'r').readlines())) + ' ' +             str(alpha) + ' ' +             str(beta) + ' ' +             str(total_number_of_iterations) + ' ' +             str(save_step) + ' ' +             inputfile + ' ' +             output_path

    print(execute_string)
    os.system(execute_string)

def run_btm_inference(no_topics,inputfile,output_path):
    # Example
    # ../../BTM/src/btm inf sum_b 150 ../data_processing_files/btm_input.txt ../output/BTM_OUTPUT/models/first_run/
    #btm_directory = '../BTM/batch/btm '
    execute_string = btm_directory + 'inf sum_b ' + str(no_topics) + ' ' +             inputfile + ' ' +             output_path

    print(execute_string)
    os.system(execute_string)

#############this is the directory where we store the raw jason file
btm_directory = '/BTM-master/src/btm '

#########parameter
#num_topics = 20
beta = 0.01
total_number_of_iterations = 1000
save_step = 10
read = 0 

if __name__ == '__main__':
    ######analyze the data
    command = sys.argv[1:]
    option = command[0]  ##has option "--help", "vocab", "BTM"
                         ##"vocab" will write the vocabulary list of these data
                         ##"BTM" will run the btm algorithm to generate the result
    
    if len(command) == 1 and option == "--help":
        print("#########################################"+\
              "\nCommand 'analyze_data.py vocab vocab_path index_path j_path platform' \
              \nWill write the vocabulary of the json data based on 'j_path' to 'vocab_path' \
              \nThen write index of the text to 'output_path' \
              \nCommand 'analyze_data.py BTM vocab_path index_path btm_path num_topics' \
              \nWill apply BTM to index data in 'input_path' and write result to 'btm_path'"+\
              "\n#########################################")
        exit(1)
    
    if len(command) >= 3:
        vocab_path = command[1] 
        index_path = command[2]
        j_path = command[3]  ##path of the folder of json data when option = 'vocab'
                             ##when option == 'BTM' this is the path to the index file
        platform = command[4]

        if option == "vocab":
            word_vocab = []
            all_text = []
            index_list = []
            
            for index,filename in enumerate(sorted(os.listdir(j_path))):  
                if filename[-5:] == '.json':
                    text_list = read_json(j_path+filename,platform)
                elif os.path.exists(j_path + filename + '/'):
                    print(index)
                    j_file = j_path + filename + '/'
                    text_list = read_folder(j_file,platform)
                else:
                    continue
                print("Number of text is " + str(len(text_list)))

                if len(text_list) == 0:
                    continue
                word_vocab += collect_words(text_list,word_vocab)
            write_vocab(word_vocab,vocab_path)
            
            #word_vocab = read_vocab(vocab_path) #######no need to use it if we don't have the vocab.txt previously
            for index,filename in enumerate(sorted(os.listdir(j_path))):
                if filename[-5:] == '.json':
                    text_list = read_json(j_path+filename,platform)
                elif os.path.exists(j_path + filename + '/'):                        
                    j_file = j_path + filename + '/'
                    text_list = read_folder(j_file,platform)
                else:
                    continue

                index_list += get_index(text_list,word_vocab)
                print('Finish index generation on ' + str(filename))

            print('The total number of text is ' + str(len(index_list)))            
            write_index(index_list,index_path)
                
        ######excute the btm
        if option == "BTM":
            BTM_path = command[3]
            num_topics = command[4]
            alpha = 50/int(num_topics)
            if not os.path.exists(BTM_path):
                os.mkdir(BTM_path)
            run_btm_learning(index_path, num_topics, vocab_path, alpha, beta, total_number_of_iterations, save_step, BTM_path)
            run_btm_inference(num_topics,index_path,BTM_path)

