# youtube_simple_influencer_search with Streamlit, through YouTube API

this app allows you to find YouTube Influencer candidates easily.  
Filtering the number of subscribers helps you find candidates efficiently.  
You can easily access the contact information of every candidate with the direct contact page links.

Made with Streamlit,and python > 3.7.  
Check requirements.txt for more packages information.

## ScreenShot

<img width="1269" alt="CleanShot 2023-06-14 at 16 57 43@2x" src="https://github.com/atsuyamaru/youtube_simple_influencer_search/assets/5616593/8158d6df-3d7c-4ddf-9d3c-934c6f3c03d5">

## Functions

- Search YouTube Videos, Playlists, Channels by keywords
- Filter by the number of subscribers
- Sort by the number of subscribers (Ascending, Descending)
- Sort by the published date (Newest, Oldest)
- Get direct contact page links of the channels (About page of the channels)

## How to Use

Get your YouTube Data API key.  
And set your API key to your environment variable as $YOUTUBE_API_KEY

If you deploy at the Streamlit Community Cloud, you should set $YOUTUBE_API_KEY in the "secret" config of Streamlit Community Cloud.

## Reference written by me (Japanese)

- [Python で YouTube Data API を利用！GCP での API キー作成から解説](https://scr.marketing-wizard.biz/dev/python-youtube-api-gcp)
- [Python で YouTube Data API v3 の Search:List を操作: YouTube データ分析](https://scr.marketing-wizard.biz/dev/youtube-dataapi-v3-search-list)
- [Streamlit Community Cloud で Web アプリを公開する際の準備事項](https://scr.marketing-wizard.biz/dev/streamlit-community-cloud-publish)
