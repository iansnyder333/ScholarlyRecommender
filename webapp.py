# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components

from testing import main_Pipeline

# Theme Configuration
st.set_page_config(
    page_title="Scholarly Recommender",
    page_icon="images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown(
    """
    <style>
        /* Add your custom CSS here */
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with logo and navigation
st.sidebar.image("images/logo.png", width=200)
st.sidebar.title("Navigation")
navigation = st.sidebar.radio("Go to", ["Get Recommendations", "About", "Contact"])

# Home Page
if navigation == "Get Recommendations":
    st.title("Scholarly Recommender")
    # User input section
    st.subheader("User Inputs")

    # Collecting user details

    query = st.multiselect(
        "What Interests You? (select at least one)",
        ["Computer Science", "Machine Learning", "Mathmatics", "Physics", "Statistics"],
    )

    # Advanced filters
    with st.expander("Advanced Filters"):
        keyword = st.text_input("Keyword")
        n = st.slider(
            "How many recommendations would you like?",
            min_value=1,
            max_value=10,
            value=5,
        )
        days = st.slider(
            "How many days back would you like to search?",
            min_value=1,
            max_value=30,
            value=7,
        )

    # Call to Action
    if st.button("Generate Recommendations"):
        # Call your backend function here to generate recommendations
        assert len(query) > 0, "Please select at least one interest."
        with st.status("Working..", expanded=True) as status:
            result = main_Pipeline(q=query, n=n, days=days)
            st.write("Almost Done...")
            HtmlFile = open(
                result,
                "r",
                encoding="utf-8",
            )
            source_code = HtmlFile.read()
            status.update(label="Feed Generated", state="complete", expanded=False)
        components.html(source_code, height=1000, scrolling=True)

# About Page
elif navigation == "About":
    st.title("About")
    st.write("Detailed information about this application.")

# Contact Page
elif navigation == "Contact":
    st.title("Contact")
    st.write("Contact details here.")

# Footer
st.markdown(
    """
    <footer>
        <p>Created by Ian Snyder</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
