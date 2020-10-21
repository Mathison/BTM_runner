# BTM_runner

This is a Python package to run the BTM (Biterm Topic Model) on json data of Twitter, Instagram, Tumblr, Youtube and Reddit

The original C++ code for BTM is here https://github.com/xiaohuiyan/BTM

Please see this reference if you want to know the details of BTM:
Yan, X., Guo, J., Lan, Y., & Cheng, X. (2013, May). A biterm topic model for short texts. In Proceedings of the 22nd international conference on World Wide Web (pp. 1445-1456).

### Please construct your system before run this package
- Install python3 in your system
- Install C++ BTM code list above, put them in folder BTM_master (you can name the fodler whatever you want, but please change the BTM path name in the analyze_data.py file)
- Configure the C++ file in ./BTM_master/src/ using make, get the btm excute file
- Install nltk package

### Then download the BTM_runner package and run the following command

$ python3 analyze_data.py vocab /local/path/to/vocab.txt /local/path/to/index.txt /your/path/to/json_data/ platform

-This command will help us build a vocabulary dictionary for each word based on the text we have in the json file, the vocabulary wil be written to /local/path/to/vocab.txt, and then it will do teh word embedding for each text and put the vector in /local/path/to/index.txt

/your/path/to/json_data/ is a folder used to store the json data for different platforms

platform: This is used specify which platform we are running BTM for, currently it has option:

- youtube_comment, instagram_comment,tumblr_comment,reddit_comment
- youtube_title,youtube_description,instagram_post,twitter,tumblr_post,tumblr_description,reddit_description,reddit_title

Each option specify the text part we want to analyze, comment option will run all the comment under each post

$ python3 analyze_data.py BTM /local/path/to/vocab.txt /local/path/to/index.txt /local/path/to/BTM_result/ k

-This command will help us generate the BTM_result from BTM and write that to /local/path/to/BTM_result/, k is the number of topics we selected

$ python3 write_topicDisplay.py /local/path/to/ BTM_result k /local/path/to/vocab.txt

-This function will write the result of top 30 keywords for each topic under the /local/path/to/BTM_result_topic.txt

#### The BTM_result_topic basically looks like below
![BTM_Topic_result_sample](https://github.com/Mathison/BTM_runner/topic_result.PNG)
