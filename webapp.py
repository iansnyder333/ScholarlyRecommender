# Import necessary modules
# Third Party Imports
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Standard Library Imports
import smtplib
from email.message import EmailMessage
from re import match

# Local Imports
import ScholarlyRecommender as sr
from Utils.webutils import search_categories


@st.cache_data(show_spinner=False)
def load_sc_config():
    return sr.get_config()


def get_sc_config():
    return st.session_state.sys_config


def update_sc_config(new_config):
    st.session_state.sys_config = new_config


def build_query(cats: dict) -> list:
    if cats.__len__() == 0:
        return []

    usr_query = []
    for key, value in cats.items():
        if len(value) > 0:
            usr_query.extend(value)
        else:
            usr_query.append(key)
    return usr_query


def validate_email(email) -> bool:
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if match(regex, email):
        return True
    return False


def send_email(**kwargs):
    try:
        SUBSCRIBERS = kwargs["subscribers"]

        # Validate emails again before sending
        for email in SUBSCRIBERS:
            if not validate_email(email):
                raise ValueError(
                    f"{email} is not a valid email address. Please try again."
                )

        EMAIL_ADDRESS = st.secrets.email_credentials.EMAIL
        EMAIL_PASSWORD = st.secrets.email_credentials.EMAIL_PASSWORD
        PORT = st.secrets.email_credentials.PORT
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not PORT:
            raise ValueError(
                f"Email credentials not set in environment variables. Please report this issue to the developer."
            )
        if not kwargs["content"]:
            raise ValueError(
                f"Email content not set. Please report this issue to the developer."
            )

        msg = EmailMessage()
        msg["Subject"] = "Your Scholarly Recommender Newsletter"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = SUBSCRIBERS

        html_string = kwargs["content"]

        msg.set_content(html_string, subtype="html")
        with smtplib.SMTP_SSL("smtp.gmail.com", PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        st.success("Email sent successfully!")

    except Exception as e:
        st.error(f"Email failed to send. {e}", icon="🚨")
        # st.write(f"An error occurred: {e}")


def generate_feed_pipeline(query: list, n: int, days: int, to_email: bool):
    with st.status("Working...", expanded=True) as status:
        status.update(label="Searching for papers...",
                      state="running", expanded=True)

        if len(query) == 0:
            query = get_sc_config()["queries"]
        # Collect candidates
        candidates = sr.source_candidates(
            queries=query, as_df=True, prev_days=days)
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
        status.update(label="Generating feed...",
                      state="running", expanded=True)

        # Generate feed
        source_code = sr.get_feed(
            data=recommendations,
            email=to_email,
            web=True,
        )
        status.update(label="Feed Generated", state="complete", expanded=False)
        return source_code


# TODO make this more efficient
def fetch_papers(num_papers: int = 10) -> pd.DataFrame:
    # Import arxiv here to prevent unnecessary imports
    from arxiv.arxiv import SortCriterion

    c = sr.source_candidates(
        queries=get_sc_config()["queries"],
        max_results=100,
        as_df=True,
        sort_by=SortCriterion.Relevance,
    )
    sam = c[["Title", "Abstract"]].sample(
        frac=1, random_state=1).reset_index(drop=True)
    sam.sort_values(
        by="Abstract", key=lambda x: x.str.len(), inplace=True, ascending=False
    )
    res = sam.iloc[: min(num_papers, len(sam))].copy()
    return res


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
        with st.form("rating_form"):
            row = st.session_state.papers_df.iloc[st.session_state.current_index]
            st.markdown(f"""## {row['Title']} """)
            trimmed_abstract = row["Abstract"][:500] + "..."
            st.markdown(f"""{trimmed_abstract}""")

            rating = st.number_input(
                f"Rate this paper on a scale of 1 to 10?",
                min_value=1,
                max_value=10,
            )
            submit_rating = st.form_submit_button(
                f"Submit Rating for Paper: {st.session_state.current_index + 1}"
            )
            if submit_rating:
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
        st.success(
            "Labels saved. Get recommendations is now configured to your interests."
        )
        # Increment to prevent re-running this block
        st.session_state.current_index += 1

    else:
        st.write("Rating process is complete.")


if "sys_config" not in st.session_state:
    st.session_state.sys_config = load_sc_config()

# Theme Configuration
st.set_page_config(
    page_title="Scholarly Recommender API",
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
    st.title("Scholarly Recommender Cloud API")
    st.markdown(
        """
        ## Welcome to the Scholarly Recommender API

        This platform is designed to offer you highly tailored scholarly recommendations.
        Whether you're a researcher, academic, or just someone interested in scientific literature,
        this service is built to cater to your specific needs.

        ### To Get Started

        - **Configure**: The first step is to configure the system to your interests. This can be done by navigating to the configure page. If you skip this step, the system will use a default configuration tailored to the interests of the developer.
        - **Get Recommendations**: Once you've configured the system, you can get recommendations by pressing the 'generate recommendations' button at the bottom of the page.
        - **Categories & Subcategories**: You can customize your interests by selecting from a wide range of categories and subcategories, by default, the system will search based on your configured interests.
        - **Recommendation Count**: Choose how many recommendations you want to receive.
        - **Time Range**: Decide the time frame for the articles you're interested in.

        """,
        unsafe_allow_html=True,
    )
    # User input section
    st.subheader("Customize your recommendations")

    # Collecting user details

    categories = st.multiselect(
        "Would you like to search for any specific categories? (leave blank to use your configured interests)",
        search_categories.keys(),
    )
    selected_sub_categories = {}
    for selected in categories:
        selected_sub_categories[selected] = st.multiselect(
            f"Select subcategories under {selected} (leave blank for all)",
            search_categories[selected],
        )

    user_n = st.slider(
        "How many recommendations would you like?",
        min_value=1,
        max_value=10,
        value=5,
    )
    user_days = st.slider(
        "How many days back would you like to search?",
        min_value=1,
        max_value=30,
        value=7,
    )

    user_to_email = st.checkbox("Email Recommendations?")

    if user_to_email:
        with st.form("email_form"):
            st.write(
                "This feature is currently under development, please report any issues you encounter."
            )
            user_email = st.text_input(
                "your email address", placeholder="example@email.com", value=""
            )
            st.markdown(
                """Disclaimer: Scholarly Recommender will only send you an email with your recommendations
            and will not use your email address for any other purpose.""",
                unsafe_allow_html=True,
            )

            submit_button = st.form_submit_button(label="Confirm")
            if submit_button:
                if validate_email(user_email):
                    st.success(f"Email address confirmed")

                else:
                    st.error(f"Please enter a valid email address", icon="🚨")

    else:
        user_email = ""
    # Call to Action
    if st.button("Generate Recommendations", type="primary"):
        user_query = build_query(selected_sub_categories)

        user_feed = generate_feed_pipeline(
            query=user_query, n=user_n, days=user_days, to_email=user_to_email
        )

        if user_to_email:
            send_email(
                subscribers=[user_email],
                content=user_feed,
            )
            # st.success("Email sent successfully!")

        components.html(user_feed, height=1000, scrolling=True)


elif navigation == "Configure":
    st.title("Scholarly Recommender Configuration API")
    st.markdown(
        """
        ## Welcome to the Scholarly Recommender System Calibration Tool

        This tool will help you calibrate the recommender system to your interests!
        Below are the various configuration steps, it is advised to do them in order.
        Once a step is completed, the changes will be applied automatically, regardless of whether you continue to the next step or not.
                """
    )
    # User input section
    st.markdown(
        """
        ### Step 1: Configure your interests

        This section will help you configure the system to your interests.
        This ensures the system will use this to only scrape papers relevant to you.
        Follow the steps below to get started.
                """
    )

    categories = st.multiselect(
        "Select the categories that interest you the most, at least one is required:",
        search_categories.keys(),
    )
    selected_sub_categories = {}
    for selected in categories:
        selected_sub_categories[selected] = st.multiselect(
            f"Select subcategories under {selected} (Optional, leave blank for all)",
            search_categories[selected],
        )
    if st.button("Done", type="primary"):
        with st.spinner("Configuring..."):
            user_config_query = build_query(selected_sub_categories)
            # prevent empty queries
            assert len(
                user_config_query) > 0, "Please select at least one interest."
            configuration = get_sc_config()
            configuration["queries"] = user_config_query
            update_sc_config(configuration)

            st.success("Preferences updated successfully!")
    # Initialize a session state variable for calibration status if it doesn't exist
    if "calibration_started" not in st.session_state:
        st.session_state.calibration_started = False

    st.markdown(
        """
        ### Step 2: Calibrate the Recommender System

        This section will help you calibrate the recommender system based on your interests.
        This will help the system learn your preferences and will significantly improve recommendations.
        This process will show you snippets of 10 papers and ask you to rate them on a scale of 1 to 10 (1 being the least relevant and 10 being the most relevant).
        Many improvements are planned for this process, including the ability to skip papers, change sample size, and dynamically update the system based on your feedback from the generated feed.

        Click on the button below to get started.

        **Note** : Currently, if you want to start over or repeat this process, you must refresh the page
        """
    )

    if st.button("Start Calibration", type="primary"):
        st.session_state.calibration_started = True

    if st.session_state.calibration_started:
        with st.spinner("Preparing Calibration..."):
            calibrate_rec_sys(num_papers=10)
    st.markdown(
        """
    ### Step 3: All done! Navigate to the Get Recommendations page to generate your personalized feed!"""
    )
    # TODO add a button to navigate to the get recommendations page


# About Page
elif navigation == "About":
    st.markdown(
        """
        ## Welcome to the Scholarly Recommender Cloud API

        This platform is designed to offer you highly tailored scholarly recommendations.
        Whether you're a researcher, academic, or just someone interested in scientific literature,
        this service is built to cater to your specific needs.

        ### How It Works

        - **Configure**: The first step is to configure the system to your interests. This can be done by navigating to the configure page.
        - **Get Recommendations**: Once you've configured the system, you can generate recommendations by navigating to the get recommendations page.
        - **Categories & Subcategories**: You can customize your interests by selecting from a wide range of categories and subcategories, by default, the system will search based on your configured interests.
        - **Recommendation Count**: Choose how many recommendations you want to receive.
        - **Time Range**: Decide the time frame for the articles you're interested in.

        ### What Makes Us Different

        - **Personalized**: Recommendations are fine-tuned to match your unique academic interests.
        - **Up-to-Date**: The platform provides options to focus on the most recent articles.
        - **Quality Assured**: We prioritize recommendations from reputable sources and peer-reviewed journals.

        ### Mission Statement

        As an upcoming data scientist with a strong passion for deep learning, I am always looking for new technologies and methodologies. Naturally, I spend a considerable amount of time researching and reading new publications to accomplish this. However, over 14,000 academic papers are published every day on average, making it extremely tedious to continuously source papers relevant to my interests. My primary motivation for creating ScholarlyRecommender is to address this, creating a fully automated and personalized system that prepares a feed of academic papers relevant to me. This feed is prepared on demand, through a completely abstracted streamlit web interface, or sent directly to my email on a timed basis. This project was designed to be scalable and adaptable, and can be very easily adapted not only to your own interests, but become a fully automated, self improving newsletter. Details on how to use this system, the methods used for retrieval and ranking, along with future plans and features planned or in development currently are listed below.


        """
    )

# Contact Page
elif navigation == "Contact":
    st.markdown(
        """
        <h1 align="center">Contact Information</h1>

        ## Project Support

        Please report any issues by creating an issue on the GitHub repository, or by sending an email to the project email directly.

        - **Github Issue**: https://github.com/iansnyder333/ScholarlyRecommender/issues
        - **Project Email**: scholarlyrecommender@gmail.com

        ## Developer Contact Information

        If you have any questions or concerns, please feel free to reach out to me directly.
        I recently graduated college and am the sole developer of this project, so I would love any constructive feedback you have to offer to help me improve as a developer.

        - **Ian Snyder**: [@iansnydes](https://twitter.com/iansnydes) - idsnyder136@gmail.com
        - **Website and Portfolio**: [iansnyder333.github.io/frontend](https://iansnyder333.github.io/frontend)
        - **LinkedIn**: [www.linkedin.com/in/ian-snyder-aa1600182](https://www.linkedin.com/in/ian-snyder-aa1600182)


                """,
        unsafe_allow_html=True,
    )


# Footer
st.markdown(
    """
    <footer>

    </footer>
    """,
    unsafe_allow_html=True,
)
