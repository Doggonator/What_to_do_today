from googlesearch import search
import time
import streamlit as st
keywords = ["Tickets", "Fun", "What to do", "Activity", "Event"]
if "index" not in st.session_state:#if opening websites, what index to open
    st.session_state.index = 0
if "prev_region" not in st.session_state:
    st.session_state.prev_region = "-1"
if "links" not in st.session_state:
    st.session_state.links = []
if "day" not in st.session_state:
    st.session_state.day = -1#will be changed to datetime once the 
st.title("What should you do today?")
st.write("This website can help find things to do!")
region = st.text_input("Input here where to search (i.e. city, county, district, not specific like a street or address)")
day = st.date_input("Select which day to search (Default is today)")
error = st.empty()
if region and (region != st.session_state.prev_region or str(day) != st.session_state.day):#check that region is not the same, and that region has been inputted
    st.session_state.prev_region = region
    st.session_state.day = str(day)
    with st.spinner("Retrieving results..."):
        results = []#just used to make sure we don't output the same thing
        #get all the results here
        for item in keywords:
            #parse the argument
            query = item+'+'+str(day)+'+'+region
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