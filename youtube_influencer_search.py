import os

from googleapiclient.discovery import build
import streamlit as st

## Create a Service Object
api_key = os.environ['YOUTUBE_API_KEY']
service = build('youtube', 'v3', developerKey=api_key)


# Check if the filtered results are found or not
def check_filtered_results_exists(subscriber_num, min_subscriber_num, max_subscriber_num):
    """
    Check if the filtered results are found or not.
    """
    if min_subscriber_num <= subscriber_num <= max_subscriber_num:
        return True
    else:
        return False

# Output the results on each row
def output_results(title, formatted_subscriber_num, content_type, thumbnail_url, description, published, channel_title, channel_description, custom_url):
    """
    Output the results on each row. Show the movie title, thumbnail, description, published date, channel title, and channel description.
    """
    st.write(f"""
        #### {title}
        Subscribers: **{formatted_subscriber_num}**  
        Published: {published}
        """)
    st.image(thumbnail_url)
    with st.expander("Movie Info Excerpt"):
        st.write(f"""
            {description}
        """)

    # Results: The channel of the title
    with st.expander("Channel Description"):
        st.write(f"""
            ###### Channel Description
            Channel Title: 【{channel_title}】  
            
            {channel_description} 
        """)

    st.write(f"""
        Content Type: {content_type} 
        ###### More Contact Info, Go to the About Page 
        **[Go to "{channel_title}" About Page](https://www.youtube.com/{custom_url}/about)**
    """)
    st.divider()

# Store the results as a dictionary, and then append it to the list
# Each dictionary item has title, subscriber_num, formatted_subscriber_num, content_type, thumbnail_url, description, published, channel_title, channel_description, custom_url
all_results_list = []

# Assign the columns
col1, col2 = st.columns(2, gap="medium")

### Streamlit Screen: Sidebar
st.sidebar.title('Youtube Influencer Search')
## Filters when search
st.sidebar.subheader('Search Conditions')
# Search keywords: required
keywords = st.sidebar.text_input(label="Search Movie by Keywords", value="python tutorial free")
# maxResults
max_results = st.sidebar.slider(label="Max Search Results", min_value=1, max_value=50, value=20, step=1)
# search item type
search_type_list = st.sidebar.multiselect(label="Search Target Type", options=['video', 'channel', 'playlist'], default=['video'])
search_type_str = ','.join(search_type_list)
st.sidebar.divider()

## Sort the results
st.sidebar.subheader('Sort the Results')
with st.sidebar.expander("Sort Options", expanded=False):
    sort_option = st.radio(label="Sort the Results by", options=['Subscriber Number Descending', 'Subscriber Number Ascending', 'Newest to Oldest', 'Oldest to Newest'], index=0)

## Filters when output
st.sidebar.subheader('Output Filters')
output_filter = st.sidebar.checkbox(label="Output Filters", value=False)
if output_filter:
    st.sidebar.warning("'Output Filters' narrow down the search results. This means that the filtered results number may be smaller than the 'Max Search Results' number specified above.")
    # Min Subscribers
    min_subscriber_num = st.sidebar.number_input(label="Min Subscribers", min_value=0, max_value=None, value=10000, step=10000)
    # Max Subscribers
    max_subscriber_num = st.sidebar.number_input(label="Max Subscribers", min_value=0, max_value=None, value=1_200_000, step=10000)
if not output_filter:
    min_subscriber_num = 0
    max_subscriber_num = 1_200_000_000_000
st.sidebar.divider()

## Find movies by Search keywords: search().list()
search_executed = False
if not search_executed:
    st.info('Please enter keywords and click the "Search" button from the sidebar.')

if not keywords:
    st.warning('Please enter keywords.')
if min_subscriber_num >= max_subscriber_num: # type: ignore
    st.warning('Please enter the correct range of subscribers.')
else:
    with st.spinner(text='Searching...'):
        if st.sidebar.button("Search"):
            search_executed = True
            # Execute the search
            request_search = service.search().list(
                q = keywords,
                part = 'snippet',
                type = search_type_str,
                maxResults = max_results 
            )
            response_movie_info = request_search.execute()

            # Execute the channel search for each movie
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
                if check_filtered_results_exists(subscriber_num, min_subscriber_num, max_subscriber_num):
                    
                    # Store the results as a dictionary
                    # title, subscriber_num, formatted_subscriber_num, content_type, thumbnail_url, description, published, channel_title, channel_description, custom_url
                    results_dict = {}
                    results_dict['title'] = item['snippet']['title']
                    results_dict['subscriber_num'] = subscriber_num
                    results_dict['formatted_subscriber_num'] = formatted_subscriber_num
                    results_dict['content_type'] = item['id']['kind'].split('#')[1]
                    results_dict['thumbnail_url'] = item['snippet']['thumbnails']['default']['url']
                    results_dict['description'] = item['snippet']['description']
                    results_dict['published'] = item['snippet']['publishedAt'].split('T')[0]
                    results_dict['channel_title'] = item['snippet']['channelTitle']
                    results_dict['channel_description'] = response_channel_info['items'][0]['snippet']['description']
                    results_dict['custom_url'] = response_channel_info['items'][0]['snippet']['customUrl']
                    all_results_list.append(results_dict)

            # Output the results
            if len(all_results_list) != 0:
                # Sort the results
                if sort_option == 'Subscriber Number Descending':
                    all_results_list = sorted(all_results_list, key=lambda x: x['subscriber_num'], reverse=True)
                elif sort_option == 'Subscriber Number Ascending':
                    all_results_list = sorted(all_results_list, key=lambda x: x['subscriber_num'], reverse=False)
                elif sort_option == 'Newest to Oldest':
                    all_results_list = sorted(all_results_list, key=lambda x: x['published'], reverse=True)
                elif sort_option == 'Oldest to Newest':
                    all_results_list = sorted(all_results_list, key=lambda x: x['published'], reverse=False)

            # Display the results
                for results_counter, item in enumerate(all_results_list):
                    # Output the results on each row
                    if results_counter % 2 == 0:
                        with col1:
                            output_results(item['title'], item['formatted_subscriber_num'], item['content_type'], item['thumbnail_url'], item['description'], item['published'], item['channel_title'], item['channel_description'], item['custom_url'])

                    elif results_counter % 2 != 0:
                        with col2:
                            output_results(item['title'], item['formatted_subscriber_num'], item['content_type'], item['thumbnail_url'], item['description'], item['published'], item['channel_title'], item['channel_description'], item['custom_url'])

            # No results
            elif len(all_results_list) == 0:
                st.warning('No results. Please change the keywords, search conditions or output filters.')

        