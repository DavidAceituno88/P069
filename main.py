# main.py
import streamlit as st
import phase3.py
import phase4.py  # Import your separate app files

# Dictionary to hold pages
PAGES = {
    "Phase 3": phase3,
    "Phase 4": phase4,
}

container = st.container()
with container:
        nav_selection = st.selectbox("Please Select a Phase", options=list(PAGES.keys()))

# Add a divider for better separation
st.markdown("---")

# Run the selected app
page = PAGES[nav_selection]
page.app()
