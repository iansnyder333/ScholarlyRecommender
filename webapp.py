# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components


import ScholarlyRecommender as sr
import pandas as pd

# Theme Configuration
st.set_page_config(
    page_title="Scholarly Recommender",
    page_icon="images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
search_categories = {
    "Computer Science": [
        "Artificial Intelligence",
        "Computer Vision and Pattern Recognition",
        "Computation and Language",
        "Databases",
        "Distributed, Parallel, and Cluster Computing",
        "Data Structures and Algorithms",
        "Computer Science and Game Theory",
        "Machine Learning",
        "Robotics",
        "Software Engineering",
    ],
    "Mathmatics": [
        "Combinatorics",
        "Dynamical Systems",
        "Numerical Analysis",
        "Number Theory",
        "Probability",
        "Quantum Algebra",
        "Logic",
    ],
    "Biology": [
        "Biomolecules",
        "Genomics",
        "Neurons and Cognition",
        "Subcellular Processes",
        "Quantitative Methods",
    ],
    "Physics": [
        "Astrophysics",
        "Condensed matter",
        "General relativity and quantum cosmology",
        "High energy physics",
        "Mathematical physics",
        "Nonlinear sciences",
        "Nuclear experiment",
        "Nuclear theory",
        "Quantum physics",
    ],
    "Statistics": ["Applications", "Computation", "Methodology", "Statistics Theory"],
}
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

    categories = st.multiselect(
        "What Interests You? (select at least one)",
        search_categories.keys(),
    )
    selected_sub_categories = {}
    for selected in categories:
        selected_sub_categories[selected] = st.multiselect(
            f"Select sub-categories under {selected} (Optional)",
            search_categories[selected],
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
        with st.status("Building Query...", expanded=True) as status:
            # st.write("Building Query...")
            query = []
            for key, value in selected_sub_categories.items():
                if len(value) > 0:
                    query.extend(value)
                else:
                    query.append(key)
            # Call your backend function here to generate recommendations
            assert len(query) > 0, "Please select at least one interest."
            # st.write("Searching for papers...")
            status.update(
                label="Searching for papers...", state="running", expanded=True
            )
            c = sr.source_candidates(queries=query, as_df=True, prev_days=days)
            # st.write("Generating recommendations...")
            status.update(
                label="Generating recommendations...", state="running", expanded=True
            )
            r = sr.get_recommendations(
                data=c,
                size=n,
                as_df=True,
            )
            # st.write("Generating feed...")
            status.update(label="Generating feed...", state="running", expanded=True)
            sr.get_feed(
                data=r,
                email=False,
                to_path="ScholarlyRecommender/Newsletter/html/WebFeed.html",
            )
            result = "ScholarlyRecommender/Newsletter/html/WebFeed.html"

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
