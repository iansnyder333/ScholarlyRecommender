# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components


import ScholarlyRecommender as sr
import pandas as pd
from Utils.webutils import search_categories


@st.cache_data(show_spinner=False)
def load_sc_config():
    return sr.get_config()


def get_sc_config():
    return st.session_state.sys_config


def update_sc_config(new_config):
    st.session_state.sys_config = new_config


def build_query(selected_sub_categories: dict) -> list:
    query = []
    for key, value in selected_sub_categories.items():
        if len(value) > 0:
            query.extend(value)
        else:
            query.append(key)
    return query


def generate_feed_pipeline(query: list, n: int, days: int):
    with st.status("Working...", expanded=True) as status:
        status.update(label="Searching for papers...", state="running", expanded=True)

        if len(query) == 0:
            query = get_sc_config()["queries"]
        # Collect candidates
        candidates = sr.source_candidates(queries=query, as_df=True, prev_days=days)
        status.update(
            label="Generating recommendations...", state="running", expanded=True
        )

        # Generate recommendations
        recommendations = sr.get_recommendations(
            data=candidates,
            labels=get_sc_config()["labels"],
            size=n,
            as_df=True,
        )
        status.update(label="Generating feed...", state="running", expanded=True)

        # Generate feed
        source_code = sr.get_feed(
            data=recommendations,
            email=False,
            web=True,
        )
        status.update(label="Feed Generated", state="complete", expanded=False)

    components.html(source_code, height=1000, scrolling=True)


def fetch_papers(num_papers: int = 10) -> pd.DataFrame:
    # Import arxiv here to prevent unnecessary imports
    import arxiv

    # Source papers only once and store in session state
    c = sr.source_candidates(
        queries=get_sc_config()["queries"],
        max_results=100,
        as_df=True,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    sam = c.sample(frac=1)
    sam.reset_index(inplace=True)
    df = sam[["Title", "Abstract"]].copy()
    df["Abstract"] = df["Abstract"].str[:500] + "..."
    return df.head(num_papers)


def calibrate_rec_sys(num_papers: int = 10):
    # Initialize session state variables if they don't exist
    if "labels" not in st.session_state:
        st.session_state.labels = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "papers_df" not in st.session_state:
        st.session_state.papers_df = fetch_papers(num_papers=num_papers)

    if st.session_state.current_index < num_papers:
        # Display the paper at the current index
        row = st.session_state.papers_df.iloc[st.session_state.current_index]
        st.write(f"**{row['Title']}**")
        st.write(f"{row['Abstract']}")
        rating = st.number_input(
            f"Rate this paper on a scale of 1 to 10?",
            min_value=1,
            max_value=10,
        )

        if st.button(f"Submit Rating for {row['Title']}"):
            # Save the label and increment the index
            st.session_state.labels.append(rating)
            st.session_state.current_index += 1
            st.experimental_rerun()

    elif st.session_state.current_index == num_papers:
        # Save all labels once all papers are rated
        st.session_state.papers_df["label"] = st.session_state.labels
        # st.session_state.papers_df.to_csv(to_path)
        # Update the config file
        old_config = get_sc_config()
        old_config["labels"] = st.session_state.papers_df
        update_sc_config(old_config)
        st.success("Labels saved.")
        # Increment to prevent re-running this block
        st.session_state.current_index += 1

    else:
        st.write("Rating process is complete.")


if "sys_config" not in st.session_state:
    st.session_state.sys_config = load_sc_config()
# Theme Configuration
st.set_page_config(
    page_title="Scholarly Recommender",
    page_icon="images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for further customization
st.markdown(
    """
    <style>
        /* Add your custom CSS here */
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with logo and navigation
st.sidebar.image("images/logo.png", use_column_width=True)
st.sidebar.title("Navigation")
navigation = st.sidebar.radio(
    "Go to", ["Get Recommendations", "Configure", "About", "Contact"]
)

# Home Page
if navigation == "Get Recommendations":
    st.title("Scholarly Recommender")
    # User input section
    st.subheader("Customize your recommendations")

    # Collecting user details

    categories = st.multiselect(
        "What Interests You? (leave blank for default configuration)",
        search_categories.keys(),
    )
    selected_sub_categories = {}
    for selected in categories:
        selected_sub_categories[selected] = st.multiselect(
            f"Select sub-categories under {selected} (Optional)",
            search_categories[selected],
        )

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
    to_email = st.checkbox("Email Recommendations?")
    if to_email:
        st.write("This feature is currently in development, please check back later.")
    # Call to Action
    if st.button("Generate Recommendations", type="primary"):
        query = build_query(selected_sub_categories)
        generate_feed_pipeline(query, n, days)


elif navigation == "Configure":
    st.title("Scholarly Recommender Configuration")
    # User input section
    st.subheader("Welcome to the Scholarly Recommender System Calibration Tool \n")
    st.write(
        "This tool will help you calibrate the recommender system to your interests \n"
    )
    st.write(
        "Below are the various configuration steps, it is advised to do them in order \n"
    )
    with st.expander("Calibrate Interests"):
        st.write(
            "Please answer the following questions to help us get to know you better \n"
        )
        st.write("Select the categories that interest you the most: \n")
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
        if st.button("Done"):
            with st.spinner("Configuring..."):
                query = build_query(selected_sub_categories)
                # prevent empty queries
                assert len(query) > 0, "Please select at least one interest."
                configuration = get_sc_config()
                configuration["queries"] = query
                update_sc_config(configuration)

            st.success("Preferences updated successfully!")
    # Initialize a session state variable for calibration status if it doesn't exist
    if "calibration_started" not in st.session_state:
        st.session_state.calibration_started = False

    with st.expander("Calibrate Rec Sys"):
        st.write(
            "Please rate the following papers on a scale of 1 to 10, 1 being the least relevant and 10 being the most relevant \n"
        )
        # st.write("You can also skip a paper if you don't want to rate it \n") (TODO: Implement this feature)
        st.write("You will be shown 10 papers to rate \n")
        st.write("Click on the button below to get started \n")
        st.write(
            "Note: Currently, if you want to start over or repeat this process, you must refresh the page \n"
        )  # TODO: Fix this
        if st.button("Start Calibration"):
            st.session_state.calibration_started = True

        if st.session_state.calibration_started:
            with st.spinner("Preparing Calibration..."):
                calibrate_rec_sys(num_papers=10)

# About Page
elif navigation == "About":
    st.title("About")
    st.write(
        "As an upcoming data scientist with a strong passion for deep learning, I am always looking for new technologies and methodologies. Naturally, I spend a considerable amount of time researching and reading new publications to accomplish this. However, over 14,000 academic papers are published every day on average, making it extremely tedious to continuously source papers relevant to my interests. My primary motivation for creating ScholarlyRecommender is to address this, creating a fully automated and personalized system that prepares a feed of academic papers relevant to me. This feed is prepared on demand, through a completely abstracted streamlit web interface, or sent directly to my email on a timed basis. This project was designed to be scalable and adaptable, and can be very easily adapted not only to your own interests, but become a fully automated, self improving newsletter. Details on how to use this system, the methods used for retrieval and ranking, along with future plans and features planned or in development currently are listed below."
    )

# Contact Page
elif navigation == "Contact":
    st.title("Contact")
    st.write("Email: Project Email - scholarlyrecommender@gmail.com")
    st.write("My Website: https://iansnyder333.github.io/frontend/")
    st.write("My LinkedIn: www.linkedin.com/in/ian-snyder-aa1600182/")

# Footer
st.markdown(
    """
    <footer>
        
    </footer>
    """,
    unsafe_allow_html=True,
)
