# Coronavirus twitter analysis

You will scan all geotagged tweets sent in 2020 to monitor for the spread of the coronavirus on social media.

**Due date:** 
March 7th, 2023

This homework will require LOTs of computation time.
I recommend that you have your code working by **21 Mar** to ensure that you will have enough time to execute the code.
No extensions will be granted for any reason.

You will continue to have assignments during the next few weeks,
and so if you delay working on this homework,
you will have some very heavy work loads ahead of you.

**Learning Objectives:**

1. work with large scale datasets
1. work with multilingual text
1. use the MapReduce divide-and-conquer paradigm to create parallel code

## Background

Approximately 500 million tweets are sent everyday.
Of those tweets, about 1% are *geotagged*.
That is, the user's device includes location information about where the tweets were sent from.
The lambda server's `/data-fast/twitter\ 2020` folder contains all geotagged tweets that were sent in 2020.
In total, there are about 1.1 billion tweets in this dataset.
We can calculate the amount of disk space used by the dataset with the `du` command as follows:
```
$ du -h /data-fast/twitter\ 2020
```

The tweets are stored as follows.
The tweets for each day are stored in a zip file `geoTwitterYY-MM-DD.zip`,
and inside this zip file are 24 text files, one for each hour of the day.
Each text file contains a single tweet per line in JSON format.
JSON is a popular format for storing data that is closely related to python dictionaries.

Vim is able to open compressed zip files,
and I encourage you to use vim to explore the dataset.
For example, run the command
```
$ vim /data-fast/twitter\ 2020/geoTwitter20-01-01.zip
```
Or you can get a "pretty printed" interface with a command like
```
$ unzip -p /data-fast/twitter\ 2020/geoTwitter20-01-01.zip | head -n1 | python3 -m json.tool | vim -
```

You will follow the [MapReduce](https://en.wikipedia.org/wiki/MapReduce) procedure to analyze these tweets.
MapReduce is a famous procedure for large scale parallel processing that is widely used in industry.
It is a 3 step procedure summarized in the following image:

<img src=mapreduce.png width=100% />

I have already done the partition step for you (by splitting up the tweets into one file per day).
You will have to do the map and reduce steps.

**Runtime:**

The simplest and most common scenario is that the map procedure takes time O(n) and the reduce procedure takes time O(1).
If you have p<<n processors, then the overall runtime will be O(n/p).
This means that:
1. doubling the amount of data will cause the analysis to take twice as long;
1. doubling the number of processors will cause the analysis to take half as long;
1. if you want to add more data and keep the processing time the same, then you need to add a proportional number of processors.

More complex runtimes are possible.
Merge sort over MapReduce is the classic example. 
Here, mapping is equivalent to sorting and so takes time O(n log n),
and reducing is a call to the `_reduce` function that takes time O(n).
But they are both rare in practice and require careful math to describe,
so we will ignore them. '#코로나바이러스',  # korean
    '#コロナウイルス',  # japanese
    '#冠状病毒',        # chinese
    '#covid2019',
    '#covid-2019',
    '#covid19',
    '#covid-19',
    '#coronavirus',
    '#corona',
    '#virus',
    '#flu',
    '#sick',
    '#cough',
    '#sneeze',
    '#hospital',
    '#nurse',
    '#doctor',

In the merge sort example, it requires p=n processors just to reduce the runtime down to O(n)...
that's a lot of additional computing power for very little gain,
and so is impractical.

## Background Tasks

Complete the following tasks to familiarize yourself with the sample code:

1. Fork the [twitter\_coronavirus](https://github.com/mikeizbicki/twitter_coronavirus) repo and clone your fork onto the lambda server.

1. **Mapping:**
   The `map.py` file processes a single zip file of tweets.
   From the root directory of your clone, run the command
   ```
   $ ./src/map.py --input_path=/data-fast/twitter\ 2020/geoTwitter20-02-16.zip
   ```
   This command will take a few minutes to run as it is processing all of the tweets within the zip file.
   After the command finishes, you will now have a folder `outputs` that contains a file `geoTwitter20-02-16.zip.lang`.
   This is a file that contains JSON formatted information summarizing the tweets from 16 February.

1. **Visualizing:**
   The `visualize.py` file displays the output from running the `map.py` file.
   Run the command
   ```
   $ ./src/visualize.py --input_path=outputs/geoTwitter20-02-16.zip.lang --key='#coronavirus'
   ```
   This displays the total number of times the hashtag `#coronavirus` was used on 16 February in each of the languages supported by twitter.
   Now manually inspect the output of the `.lang` file using vim:
   ```
   $ vim outputs/geoTwitter20-02-16.zip.lang
   ```
   You should see that the file contains a dictionary of dictionaries.
   The outermost dictionary has languages as the keys, 
   and the innermost dictionary has hashtags as the keys.
   The `visualize.py` file simply provides a nicer visualization of these dictionaries.

1. **Reducing:**
   The `reduce.py` file merges the outputs generated by the `map.py` file so that the combined files can be visualized.
   Generate a new output file by running the command
   ```
   $ ./src/map.py --input_path=/data-fast/twitter\ 2020/geoTwitter20-02-17.zip
   ```
   Then merge these output files together by running the command
   ```
   $ ./src/reduce.py --input_paths outputs/geoTwitter20-02-16.zip.lang outputs/geoTwitter20-02-17.zip.lang --output_path=reduced.lang
   ```
   Alternatively, you can use the glob to merge all output files with the command
   ```
   $ ./src/reduce.py --input_paths outputs/geoTwitter*.lang --output_path=reduced.lang
   ```
   Now you can visualize the `reduced.lang` file with the command
   ```
   $ ./src/visualize.py --input_path=reduced.lang --key='#coronavirus'
   ```
   and this displays the combined result.

## Tasks

Complete the following tasks:


**Task 1: Map**

Modify the map.py file so that it tracks the usage of the hashtags on both a language and country level. This will require creating a variable counter_country similar to the variable counter_lang, and modifying this variable in the #search hashtags section of the code appropriately. The output of running map.py should be two files now, one that ends in .lang for the language dictionary (same as before), and one that ends in .country for the country dictionary.
```
HINT: Most tweets contain a place key, which contains a dictionary with the country_code key. This is how you should lookup the country that a tweet was sent from. Some tweets, however, do not have a country_code key. This can happen, for example, if the tweet was sent from international waters or the international space station. Your code will have to be generic enough to handle edge cases similar to this without failing.
```
**Task 2: Reduce**

Once your map.py file has been modified to track results for each country, you should run the map file on all the tweets in the /data/Twitter\ dataset folder from 2020.

HINT: Use the glob * to select only the tweets from 2020 and not all tweets.

You should create a shell script run_maps.sh that loops over each file in the dataset and runs map.py on that file. Each call to map.py can take up to a day to finish, so you should use the nohup command to ensure the program continues to run after you disconnect and the & operator to ensure that all map.py commands run in parallel.

After your modified map.py has run on all the files, you should have a large number of files in your outputs folder. Use the reduce.py file to combine all of the .lang files into a single file, and all of the .country files into a different file.

**Task 3: reduce**

Recall that you can visualize your output files with the command

```
$ ./src/visualize.py --input_path=PATH --key=HASHTAG
```
Currently, this prints the top keys to stdout.

Modify the visualize.py file so that it generates a bar graph of the results and stores the bar graph as a png file. The horizontal axis of the graph should be the keys of the input file, and the vertical axis of the graph should be the values of the input file. The final results should be sorted from low to high, and you only need to include the top 10 keys.

HINT: We are not covering how to create images from python code in this class. I recommend you use the matplotlib library, and you can find some samples to base your code off of in the documentation here.

Then, run the visualize.py file with the --input_path equal to both the country and lang files created in the reduce phase, and the --key set to #coronavirus and #코로나바이러스. This should generate four plots in total.

**Task 4: uploading**

Commit all of your code and images output files to your github repo and push the results to github. You must edit the README.md file to provide a brief explanation of your results and include the 4 generate png files. This explanation should be suitable for a future employer to look at while they are interviewing you to get a rough idea of what you accomplished. (And you should tell them about this in your interviews!)


##Results:
 
In this project, I used a dataset that had geotagged tweets in 2020 in order to understand how users used coronavirus related hashtags on twitter across different countries and languages. The plots folder shows the usage of different coronavirus related hashtags in various countries and languages. The plots folder shows the visualizations for all of the following hashtags: 
 '#코로나바이러스',  '#コロナウイルス', '#冠状病毒', '#covid2019', '#covid-2019', '#covid19', '#covid-19', '#coronavirus', '#corona', '#virus', '#flu', '#sick', '#cough', '#sneeze', '#hospital', 
 '#nurse', '#doctor'

 I automated these graphs using a `run_visualize.sh` shell script that creates two bar graphs for each hashtag. One bar graph shows the usage of the hashtag in the top 10 countries it was used in while the other shows the usage of the hashtag in the top 10 languages it was used in. In the plots folder, the `reduced.country."$hashtag".png` shows the usage of the hashtag in different countries while `reduced.lang."$hashtag".png` shows the usage of the hashtag in different languages. 
 
 The following two graphs show the usage of `#coronavirus` in the top 10 countries and languages it was used in. 

![Country #coronavirus](https://github.com/snarayan23/twitter_coronavirus/blob/master/plots/reduced.country.%23coronavirus.png)

 The bar graph shows that `#coronavirus` was used most in the US followed by India and Great Britain. We can also see that comparatively, Turkey and France had a much lower usage of `#coronavirus`.


![Language #coronavirus](https://github.com/snarayan23/twitter_coronavirus/blob/master/plots/reduced.lang.%23coronavirus.png)

 The bar graph shows that `#coronavirus` was tweeted most in English and Spanish. 


 The following two graphs show the usage of the hashtag `#코로나바이러스` in the top 10 countries and languages it was used in. 

![Country #코로나바이러스](https://github.com/snarayan23/twitter_coronavirus/blob/master/plots/reduced.country.%23%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4.png)

 The bar graph shows that `#코로나바이러스` was used most in Korea which makes sense since the hashtag is in Korean. 


![Language #코로나바이러스](https://github.com/snarayan23/twitter_coronavirus/blob/master/plots/reduced.lang.%23%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4.png)

 The bar graph shows that the hashtag `#코로나바이러스` was mostly used in Korean. 


Similar analysis can be performed using the plots to determine the usage of other coronavirus related hashtags across countries and language.

## Submission

Upload a link to you github repository on sakai.
I will look at your code and visualization to determine your grade.

Notice that we are not using CI to grade this assignment.
That's because you can get slightly different numbers depending on some of the design choices you make in your code.
For example, should the term `corona` count tweets that contain `coronavirus` as well as tweets that contain just `corona`?
These are relatively insignificant decisions.
I'm more concerned with your ability to write a shell script and use `nohup`, `&`, and other process control tools effectively.
