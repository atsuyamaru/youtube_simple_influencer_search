import os

from googleapiclient.discovery import build
import streamlit as st

## Create a Service Object
api_key = os.environ['YOUTUBE_API_KEY']
service = build('youtube', 'v3', developerKey=api_key)


# Check if the filtered results are found or not
def check_results_exists(subscriber_num, min_subscriber_num, max_subscriber_num):
    """
    Check if the filtered results are found or not.
    """
    if min_subscriber_num <= subscriber_num <= max_subscriber_num:
        return True
    else:
        return False

# Output the results on each row
def output_results(item, response_channel_info, formatted_subscriber_num, subscriber_num):
    """
    Output the results on each row. Show the movie title, thumbnail, description, published date, channel title, and channel description.
    """
    st.write(f"""
        #### {item['snippet']['title']}
        Subscribers: **{formatted_subscriber_num}**  
        Content Type: {item['id']['kind'].split('#')[1]}
        """)
    st.image(item['snippet']['thumbnails']['default']['url'])
    with st.expander("Movie Info"):
        st.write(f"""
            ###### Movie Info
            - Description Excerpt:  
            {item['snippet']['description']}
            - Published: {item['snippet']['publishedAt']}
        """)

    # Results: The channel of the title
    with st.expander("Channel Description"):
        st.write(f"""
            ###### Channel Description
            Channel Title: 【{item['snippet']['channelTitle']}】  
            
            {response_channel_info['items'][0]['snippet']['description']} 
        """)

    custom_url = response_channel_info['items'][0]['snippet']['customUrl']
    st.write(f"""
        ###### More Contact Info, Go to the About Page 
        **[Go to "{item['snippet']['channelTitle']}" About Page](https://www.youtube.com/{custom_url}/about)**
    """)
    st.divider()


# Assign the columns
col1, col2 = st.columns(2, gap="medium")

### Streamlit Screen: Sidebar
st.sidebar.title('Youtube Influencer Search')
## Filters when search
st.sidebar.subheader('Search Filters')
# Search keywords: required
keywords = st.sidebar.text_input(label="Search Movie by Keywords", value="YouTube Influencer")
# maxResults
max_results = st.sidebar.slider(label="Max Search Results", min_value=1, max_value=50, value=5, step=1)
# search item type
search_type_list = st.sidebar.multiselect(label="Search Target Type", options=['video', 'channel', 'playlist'], default=['video'])
search_type_str = ','.join(search_type_list)
st.sidebar.divider()

## Filters when output
st.sidebar.subheader('Output Filters')
# Min Subscribers
min_subscriber_num = st.sidebar.number_input(label="Min Subscribers", min_value=0, max_value=None, value=1000, step=1)
# Max Subscribers
max_subscriber_num = st.sidebar.number_input(label="Max Subscribers", min_value=0, max_value=None, value=120000, step=1, format=None)

## Find movies by Search keywords: search().list()
if not keywords:
    st.sidebar.warning('Please enter keywords.')
if not min_subscriber_num <= max_subscriber_num:
    st.sidebar.warning('Please enter the correct range of subscribers.')
else:
    with st.spinner(text='Searching...'):
        if st.sidebar.button("Search"):
            # Execute the search
            request_search = service.search().list(
                q = keywords,
                part = 'snippet',
                type = search_type_str,
                maxResults = max_results 
            )
            response_movie_info = request_search.execute()

            # Execute the channel search for each movie
            results_counter = 0
            for item in response_movie_info['items']:
                ## Get Channel information: channels().list()
                channel_id = item['snippet']['channelId']
                request_channel = service.channels().list(
                    part = 'snippet,statistics',
                    id = channel_id
                )
                response_channel_info = request_channel.execute()
                
                # Format the subscriber number
                subscriber_num = int(response_channel_info['items'][0]['statistics']['subscriberCount'])
                formatted_subscriber_num = format(subscriber_num, ',d')

                # Check if the filtered results are found or not
                if check_results_exists(subscriber_num, min_subscriber_num, max_subscriber_num):
                    results_counter += 1
                    # Output the results
                    if results_counter % 2 != 0:
                        with col1:
                            output_results(item, response_channel_info, formatted_subscriber_num, subscriber_num)

                    elif results_counter % 2 == 0:
                        with col2:
                            output_results(item, response_channel_info, formatted_subscriber_num, subscriber_num)

            if results_counter == 0:
                st.warning('No results. Please change the search keywords or filters.')
