from datetime import date
from googlesearch import search
import time
import streamlit as st
from mechanize import Browser
today = str(date.today())
keywords = ["Tickets", "Fun", "What to do", "Activity", "Event"]
if "index" not in st.session_state:#if opening websites, what index to open
    st.session_state.index = 0
if "prev_region" not in st.session_state:
    st.session_state.prev_region = "-1"
if "links" not in st.session_state:
    st.session_state.links = []
#region = input("Please input the area to find activities for today here: ")
#open_results = 'y' in input("Open results in search engine? (y/n) (Warning: opens many tabs): ").lower()
st.title("What should you do today?")
region = st.text_input("Input here where to search (i.e. city)")
error = st.empty()
if region and region != st.session_state.prev_region:#check that region is not the same, and that region has been inputted
    st.session_state.prev_region = region
    with st.spinner("Retrieving results..."):
        results = []#just used to make sure we don't output the same thing
        #get all the results here
        for item in keywords:
            #parse the argument
            query = item+'+'+today+'+'+region
            while True:
                try:#search, but make sure we are not annoying google api.
                    for result in search(query, num_results = 20):
                        if (result in results) == False:
                            results.append(result)
                    error.empty()
                    break
                except Exception as e:
                    error.error("Google has rate limited the program for searching too much. The program will now wait out the ban period. Exit the program and come back later, or wait for the period to lift")
                    time.sleep(30)
    st.write("Below are links for what to do today, in the region you inputted!")
    for item in results:
        #find the title of the webpage
        browser = Browser()
        browser.open(item)

        st.link_button(browser.title(), item)
st.write("Created by Drew Warner")
st.caption("Created using python's googlesearch-python, streamlit and mechanize")