from datetime import date, timedelta
from googlesearch import search
import time
import streamlit as st
today = str(date.today())
keywords = ["Tickets", "Fun", "What to do", "Activity", "Event"]
if "index" not in st.session_state:#if opening websites, what index to open
    st.session_state.index = 0
if "prev_region" not in st.session_state:
    st.session_state.prev_region = "-1"
if "links" not in st.session_state:
    st.session_state.links = []
if "tomorrow" not in st.session_state:
    st.session_state.tomorrow = -1#will be changed to bool when tomorrow toggle is updated
st.title("What should you do today?")
st.write("This website can help find things to do!")
region = st.text_input("Input here where to search (i.e. city, county, district, not specific like a street or address)")
tomorrow = st.toggle("Search for tomorrow instead of today")
error = st.empty()
if region and (region != st.session_state.prev_region or tomorrow != st.session_state.tomorrow):#check that region is not the same, and that region has been inputted
    st.session_state.prev_region = region
    st.session_state.tomorrow = tomorrow
    with st.spinner("Retrieving results..."):
        results = []#just used to make sure we don't output the same thing
        #get all the results here
        for item in keywords:
            #parse the argument
            query = item+'+'+today+'+'+region
            if tomorrow:
                query = item+'+'+str(date.today()+timedelta(1))+'+'+region
            while True:
                try:#search, but make sure we are not annoying google api.
                    for result in search(query, num_results = 20, advanced = True):
                        if (result in results) == False:
                            results.append(result)
                    error.empty()
                    break
                except Exception as e:
                    error.error("Google has rate limited the program for searching too much. The program will now wait out the ban period. Exit the program and come back later, or stay and wait for the period to lift")
                    time.sleep(30)
    st.write("Below are links for what to do today, in the region you inputted!")
    for item in results:
        st.link_button(item.title, item.url)
st.write("Created by Drew Warner")
st.caption("Created using python's googlesearch-python and streamlit")