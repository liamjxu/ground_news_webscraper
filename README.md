# Description

The crawling happens on 3 different levels:
1. **To collect the topic list**
   1. BFS on the topics that are offered on `ground.news`
2. **To collect the story lists within each topic list**
   1. Each story has multiple articles 
3. **To collect the full texts for each topic**
   1. Currently we only attempted to keep higher quality stories



# TODOs:
**General**
* we need to reorganize the file structure

**Topic list collection** (output: `topic_list.json`)
* scalability (how to continue updating the topic list dynamically)
  * get topic, check if existing, integrate topic

**Story & Article info collection** (output: `interest/`)
* serious bug: sometimes no biases are given but additional information exists, resulting in misplacements, which affects the full texts too
* filter bad stories (due to previous crawling)
  * sometimes a story has an empty
* bug: mismatch between the topic list and the interest/ directory (not all topics in the list have been collected)
* check the current logs to see whether a story has been collected etc

**Full text collection** (output: `news/`)
* currently, the topic progress won't let us know how many are filtered because of higher quality story (HQS) requirements.
* currently we don't know the progress for each process rank, maybe we should maintain a log to show the progress for each rank.
* to avoid one article being included in mutliple stories and be crawled multiple times, maybe we should develop an indexing method and a dynamically checking process.
* we need a filtering process to show how much HQS are there. (So, might as well just collect for all stories)

# TODOs for deliverables
* we need to write a README for the data
* we need a counting program to show the stats.
* we need to clean up the logs