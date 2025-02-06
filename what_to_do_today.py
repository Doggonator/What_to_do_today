from googlesearch import search
from duckduckgo_search import DDGS
import time
import streamlit as st
#set the page title to something other than "Streamlit"
st.set_page_config(page_title = "What to do today")
keywords = ["Tickets", "Fun", "What to do", "Activity", "Event", "Concert", "Live Music"]
if "prev_region" not in st.session_state:
    st.session_state.prev_region = ""
if "day" not in st.session_state:
    st.session_state.day = -1#will be changed to datetime once the 
st.title("What should you do today?")
st.write("This website can help find things to do!")
region = st.text_input("Input here where to search (i.e. city, county, district, not specific like a street or address)")
day = st.date_input("Select which day to search")
error = st.empty()
try:#try using google
    if region and (region != st.session_state.prev_region or str(day) != st.session_state.day):#check that region is not the same, and that region has been inputted
        st.session_state.prev_region = region
        st.session_state.day = str(day)
        with st.spinner("Retrieving results..."):
            results = []#just used to make sure we don't output the same thing
            #get all the results here
            for item in keywords:
                #parse the argument
                query = item+'+'+str(day)+'+'+region
                for result in search(query, num_results=15, advanced = True):
                    if (result in results) == False:
                        results.append(result)
        st.write("Below are links for what to do today, in the region you inputted!")
        for item in results:
            st.link_button(item.title, item.url)
except:#use duckduckgo instead, as google failed
    if region and (region != st.session_state.prev_region or str(day) != st.session_state.day):#check that region is not the same, and that region has been inputted
        with error.container():
            st.info("Google api failed. Now using DuckDuckGo")
        st.session_state.prev_region = region
        st.session_state.day = str(day)
        with st.spinner("Retrieving results..."):
            results = []#just used to make sure we don't output the same thing
            #get all the results here
            for item in keywords:
                #parse the argument
                query = item+'+'+str(day)+'+'+region
                while True:
                    try:
                        for result in DDGS().text(query, max_results = 15):#duckduckgo version, if google ever fails
                            if (result in results) == False:
                                results.append(result)
                        error.empty()
                        break
                    except:
                        st.error("DuckDuckGo rate limit reached. Waiting for limit to lift...")
                        time.sleep(30)
        st.write("Below are links for what to do today, in the region you inputted!")
        for item in results:
            st.link_button(item["title"], item['href'])#duckduckgo version
st.write("Created by Drew Warner")
error.empty()#we had success, so remove any errors that showed up
