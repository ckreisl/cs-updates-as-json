# Counter-Strike: Global Offensive Updates as JSON
## About
All Counter-Strike: Global Offensive **announced** updates (2012 - 202x) collected together in one `.json` file. The file can be used for data operations and visualizations.

## Setup
Create a Python (vers. 3.10) virtual environment and install dependencies in order to run the update crawler if required. Only the web crawler uses non default Python modules like `Beautifulsoup` and `requests`. Operations on the data can be done without any 3rd party package.

`pip install -r requirements.txt`

## Data
The collected **raw** data can be found in `data/updates_combined_raw.json`. The file is put together based on `data/updates_old.json` and `data/updates_new.json`. The content looks like the following for every update post entry:
```
{
    "id": "<post_id>",
    "timestamp": "16 Aug 2012",
    "link": "<link_to_post>",
    "entry" "<update_content_string>"
}
```
For the old updates which are stored here: [Steam CS:GO Updates](https://store.steampowered.com/oldnews/?appids=730&appgroupname=Counter-Strike%3A+Global+Offensive&feed=steam_updates) the `id` field is based on the post ID crawled from the HTML div content. For all newer updates from [Counter-Strike.net](https://blog.counter-strike.net/index.php/category/updates/) we just hashed the date string and used that one as `id` since no HTML div id could be found.

In order to do some additional data analysis we introduced **custom tags**. See `csgo_update_data.json` (The list might grow in future).

```
{
    (...) // same content as above
    "tags": "<tags_identifing_the_update>",
    "chars": "<integer_character_length_of_update_content>"
}
```
`tags` have been added manually based on the update content.

## Examples
Announced updates so far: **502** (2023-02-27)

![CS:GO updates over the past years](images/csgo_updates_per_year.png)