# Ground News Webscraper

This is the repostory hosting the code for 
1. Webscraping structured article informations from [`ground.news`](https://ground.news/)
2. Collecting the full article texts from their own websites. 

## Background

Since there are ad hoc efforts targeting the ground.news website, some background info about it is beneficial for understanding the code. Below is a quick key-point recap about ground.news:
1. ground.news is a News Aggregation platform. It has a clear topic-story-article structure.
   1. Topic is the highest level, it can be an social aspect (*e.g.*, `politics`), a person (*e.g.*, `tim-cook`), a place (*e.g.*, `iran`), or a news source (*e.g.*, `npr`).
   2. Story is the middel level, which is an event that got coverage from different sources.
   3. Article is the lowest level, which is the collection of information about an article.
2. ground.news provides, for each article, some critical information that we are querying:
   1. News agency labels such as their `bias` and `factuality`.
   2. The `URL` to the original news website (Note that it does not offer full texts directly, thus we need the second step in the [overview](#ground-news-webscraper))

## Usage

### 1. Set up the Environment
```bash
# You may want to use a virtual environment or conda environment
pip install -r requirements.txt
```

### 2. Set up the Credentials
```bash
# Replace <your-username> and <your-password> with your ground.news credentials
export YOUR_USERNAME=<your-username>
export YOUR_PASSWORD=<your-password>

# create the credentials.json file
echo "{\"username\": \"${YOUR_USERNAME}\", \"password\": \"${YOUR_PASSWORD}\"}" > credentials.json
```

### 3. Utilize the Functionalities

The webscraper has the following functionalities:
1. **To collect the topic list (from ground.news)**
    * The topic list is a collection of ground.news topics. Currenlty we implemented BFS in attempt to collect ALL topics that are offered on the ground.news website. **If you already have a specific topic that you are interested in, skip this step and start with step 2, script Option 2.**
    
    * To collect the topic list automatically, refer to [`topic_collection/get_more_topic.sh`](topic_collection/get_more_topic.sh)
  
        ```bash
        # Data Collection version is controlled by tagging
        export TAG=<your-tag> 
        sh topic_collection/get_more_topic.sh
        ```
    
    * If the program executes correctly, you should see 5 json files under `topic_collection/`, 1 for each of the types as described [here](#background), and one compiled `${TAG}_topic_list.json` that should contain >300 topics. Note that one run of the above code is not exhaustive (as BFS does not necessarily cover all nodes in a graph). You can run the above code multiple times and the topics collected will be unionized.
  
2. **To collect story lists for topics**
    * Under each topic there are multiple stories that ground.news compiles and releases everyday. To collect the story list we query all stories under the topic page on the ground.news website.

    * To collect the story lists automatically, refer to [`story_collection/get_story.sh`](story_collection/get_story.sh)
  
        ```bash
        # Data Collection version is controlled by tagging
        export TAG=<your-tag> 

        # Option 1: collect from a topic list from step 1
        # This option assumes ${TAG}_topic_list.json exists under topic_collection/
        python -m story_collection.main --source topic_list --tag ${TAG} --headless

        # Option 2: collect from a specific topic with that topic's href
        # See below on what to fill in for <topic-href>
        python -m story_collection.main --source href --href <topic-href> --tag ${TAG} --headless
        ```

    * In Option 2, the `<topic-href>` can be found in the URL of the topic page. E.g., https://ground.news/interest/gun-control talks about gun control, and the `<topic-href>` for the topic gun control is `/interest/gun-control`
    
    * The collecting process can be monitored in a terminal with 

        ```bash
        TAG=<your-tag> sh story_collection/monitor.sh
        ```
    
    * If the program is executed correctly, under `story_collection/` you should see 2 non-empty directories, 1 with name `${TAG}_interest/` and the other  `${TAG}_logs/`, the former containing story informations and the lateer logs. 


3. **To collect the full texts**
    * Each story has multiple articles. In this step, you will need the story list(s) generated from step 2.
    * To collect the story lists automatically, refer to [`full_text_collection/get_full_texts.sh`](full_text_collection/get_full_texts.sh)
  
        ```bash
        # Data Collection version is controlled by tagging
        export TAG=<your-tag> 

        # Option 1: collect from all story lists from step 2
        python -m full_text_collection.get_full_texts --source all --tag ${TAG}

        # Option 2: collect from a specific topic with that topic's story list
        # See below on what to fill in for <topic-name>
        python -m full_text_collection.get_full_texts --source <topic-name> --tag ${TAG}
        ```

    * In Option 2, the `<topic-name>` can be found in the URL of the topic page. E.g., https://ground.news/interest/gun-control talks about gun control, and the `<topic-name>` for the topic gun control is `gun-control`

    * The collecting process can be monitored in a terminal with 

        ```bash
        TAG=<your-tag> sh full_text_collection/monitor.sh
        ```

    * If the program is executed correctly, under the root directory you should see a `{TAG}_news/` directory containing all the articles, organized into topics and stories.

## Data Structures
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
   * `factuality`: the factuality labeled by `ground.news` (one of "High Factuality", "Low Factuality", "Mixed Factuality", "Unknown")
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
* note that some topics are getting much lower stories than it should be (e.g., `tim-cook` has only 20-ish stories?? Ok I see, this might be due to the fact that we cancelled the waiting between clicking "more stories"), some sort of auto-merging is needed for sure now.

**Full text collection** (output: `news/`)
* to avoid one article being included in mutliple stories and be crawled multiple times, maybe we should develop an indexing method and a dynamically checking process (check the current logs to see whether an article has been collected etc).
* check the stats, e.g., there seem to be a discrepancy between the number of stories in `full_text_collection\full_text_stats.py` and `story_collection\stats.py`
