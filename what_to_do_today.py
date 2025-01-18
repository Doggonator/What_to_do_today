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
                    for result in DDGS().text(query, max_results = 15):
                        print(result)
                        if (result in results) == False:
                            results.append(result)
                    error.empty()
                    break
                except Exception as e:
                    print(e)
                    error.error("DuckDuckGo has rate limited the program for searching too much. The program will now wait out the ban period. Exit the program and come back later, or stay and wait for the period to lift")
                    time.sleep(30)
    st.write("Below are links for what to do today, in the region you inputted!")
    for item in results:
        st.link_button(item["title"], item["href"])
st.write("Created by Drew Warner")
st.caption("Created using python's duckduckgo-search and streamlit")