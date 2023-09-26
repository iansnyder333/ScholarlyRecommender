"""
This script allows you to reconfigure the recommender system to your interests without having to use the web interface. 
It is not nearly as robust as the web interface, but offers a quick and lightweight alternative for users who do not want to use the web interface.
"""
import ScholarlyRecommender as sr
import pandas as pd
import arxiv

to_path = "ScholarlyRecommender/Repository/labeled/Candidates_Labeled.csv"
old_config = sr.get_config()


def calibrate_rec_sys(query: list, num_papers: int = 10, to_path: str = to_path):
    # get sample of papers to label
    c = sr.source_candidates(
        queries=query,
        max_results=100,
        as_df=True,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    sam = c.sample(frac=1)
    sam.reset_index(inplace=True)
    df = sam[["Title", "Abstract"]].copy()
    df["Abstract"] = df["Abstract"].str[:500] + "..."

    df = df.head(num_papers)

    labels = []
    for _, row in df.iterrows():
        print(f"{row['Title']} \n")
        print(f"{row['Abstract']} \n")
        print("Rate this paper on a scale of 1 to 10? \n")
        labels.append(int(input("enter a number: ")))
        print("\n \n")
    df["label"] = labels
    df.to_csv(to_path)
    old_config["labels"] = to_path
    sr.update_config(old_config)
    return True


def main():
    print(
        "\n WARNING: This script is deprecated and will be removed in a future release."
    )
    print("Please use the web interface instead. \n")
    print("Welcome to the Scholarly Recommender System Calibration Tool \n")
    print(
        "This tool will help you calibrate the recommender system to your interests \n"
    )
    print("Please answer the following questions to help us get to know you better \n")
    print("Select the categories that interest you the most: \n")
    print("1. Computer Science")
    print("2. Mathematics")
    print("3. Physics")
    print("4. Quantitative Biology")
    print("5. Quantitative Finance")
    print("6. Statistics")
    print("Please enter the numbers of the categories that interest you the most.")
    print("Separate each number with a comma. EX 1,2,3 \n")
    categories = input("Enter a list of numbers: ")
    categories = categories.split(",")
    categories = [int(i) for i in categories]
    search_categories = {
        1: "Computer Science",
        2: "Mathematics",
        3: "Physics",
        4: "Quantitative Biology",
        5: "Quantitative Finance",
        6: "Statistics",
    }
    categories = list(map(search_categories.get, categories))
    print(f"Thank you for your input. You selected {categories} \n")
    print("Now we will ask you to rate a few papers to help us know you better.")
    print("This will take a few minutes.")
    res = input("Press enter if you want to proceed, or skip if you want to skip: \n")
    if res == "skip":
        print("You have chosen to skip this step. \n")
        print("The recommender system will not be calibrated to your interests. \n")
        return
    print("Please rate the following papers on a scale of 1 to 10 \n")
    state = calibrate_rec_sys(categories)
    if state:
        print("Thank you for your input. Your results have been saved. \n")
        print("The recommender system will now be calibrated to your interests \n")
        print("No further action is required! \n")

        return
    else:
        print("Something went wrong. Please try again. \n")
        return


if __name__ == "__main__":
    main()
