# Description

The crawling happens on 3 different levels:
1. **To collect the topic list**
   1. BFS on the topics that are offered on `ground.news`
2. **To collect the story lists within each topic list**
   1. Each story has multiple articles 
3. **To collect the full texts for each topic**
   1. Currently we only attempted to keep higher quality stories

The data:
1. **Topic**: the highest level, which is one of
   1. abstract topics such as `politics` or `trade`; 
   2. places such as `iran` or `pakistan`; 
   3. celebrities / famous people, such as `tim-cook` or `liz-truss`; 
   4. news sources, such as `npr` or `new-york-times`.
2. **Story**: the middel level, which is an event that got coverage from different sources
    * For example, `news/elon-musk/elon-musk-and-twitter-discussed-price-cut-to-44-billion-takeover-in-recent-weeks.json` contains news articles covering the recent event that concerns the recently proposed acquisition by Elon Musk.
    * Currently, we only attempted to keep stories with sufficient coverage from both sides (#articles > 2 for both left and right).
3. **Article**: the lowest level, which is the collection of information about an article:
   * `article_idx`: the index of the article within the story
   * `bias`: the bias labeled by `ground.news` (one of "Left", "Lean Left", "Center", "Lean Right", "Right", "Unknown")
   * `factuality`: the factuality labeled by `ground.news` (one of "High", "Low", "Mixed", "Unknown")
   * `name`: name of the news agency
   * `date_publish`: the date of the article got published
   * `image_url`: the URL to the news image (if any)
   * `language`: the language of the article
   * `url`: the URL to the original article
   * `source_domain`: the source domain of the original article
   * `title`: the article title
   * `authors`: the article author list
   * `maintext`: the main text of the article


# TODOs:
**General**
* None yet

**Topic list collection** (output: `topic_collection/topic_list.json`)
* None yet

**Story & Article info collection** (output: `story_collection/interest/`)
* create some slicing support

**Full text collection** (output: `news/`)
* currently, the topic progress won't let us know how many are filtered because of higher quality story (HQS) requirements.
* we should also collect not HQS stories because they might be beneficial in other ways.
* currently we don't know the progress for each process rank, maybe we should maintain a log to show the progress for each rank.
* to avoid one article being included in mutliple stories and be crawled multiple times, maybe we should develop an indexing method and a dynamically checking process.
* we need a filtering process to show how much HQS are there. (So, might as well just collect for all stories)
* `full_text_stat.py` seems to give a higher number for HQS than `stats.py` (I really need to work on the reformatting & renaming)
* beneficial to work on: balance load on each rank
* check the current logs to see whether an article has been collected etc
