# Description

The crawling happens on 3 different levels:
1. To collect the topic list
2. To collect the story and article information within each topic list
3. To collect the full texts



# TODOs:

**Topic list collection** (output: `topic_list.json`)
* scalability (how to continue updating the topic list dynamically)

**Story & Article info collection** (output: `interest/`)
* serious bug: sometimes no biases are given but additional information exists, resulting in misplacements, which affects the full texts too
* filter bad stories (due to previous crawling)
* bug: mismatch between the topic list and the interest/ directory
* check the current logs to see whether a story has been collected etc

**Full text collection** (output: `news/`)
* currently, the topic progress won't let us know how many are filtered because of higher quality story requirements, I want to know how much are filtered because of HQS
* currently we don't know the progress for each process rank, maybe we should maintain a log to show the progress for each rank
* to avoid one article being included in mutliple stories and be crawled multiple times, maybe we should develop an indexing method
* we need a counting program to show the stats
  
**Done**:
* filter high quality stories
* record which websites we have etc, expanding 