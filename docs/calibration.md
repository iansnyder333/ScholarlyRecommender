
# Scholarly Recommender System Calibration Tool

This document will help you calibrate the recommender system to your interests!
Below are the various configuration steps, it is advised to do them in order.
Once a step is completed, the changes will be applied automatically, regardless of whether you continue to the next step or not.

## Step 1: Access the Configuration API

First, use the following [link](https://scholarlyrecommender.streamlit.app) to access the cloud application. If you are running this project locally, you should refer to <a href="https://github.com/iansnyder333/ScholarlyRecommender/blob/main/docs/local-config.md">this document</a>. 

Once you are on the cloud app, use the navigation bar on the left side of the screen and click on the "Configure" tab, shown below.

<img width="1386" alt="Screen Shot 2023-09-22 at 8 20 59 AM" src="https://github.com/iansnyder333/ScholarlyRecommender/assets/58576523/276b828f-3777-41f6-bb54-3845eb8fa230">



## Step 2: Configure your interests

Follow the instructions displayed on the screen to start the configuration process. You will be asked to select categories and subcategories that are of interest to you. You may select as few or as many as you like, these categories will help the ScholarlyRecommender source candidate papers that align with your interests. Once you have selected all the categories, click the done button just below the categories box. You should see the following message indicating that your preferences were successfully changed.

<img width="964" alt="Screen Shot 2023-09-22 at 8 33 27 AM" src="https://github.com/iansnyder333/ScholarlyRecommender/assets/58576523/696e61e5-a912-4ae5-87a3-91bd796ef1b0">

Congratulations! ScholarlyRecommender will now automatically source candidates that are relevant to your interests, unless specified otherwise. You can go back and change this configuration at any time!

## Step 3: Calibrate the Recommender System

Scroll down to the next section on the page, labeled *Calibrate the Recommender System*. This step will calibrate the recommender system to rank candidate papers based on your interests, and will significantly improve recommendations. This process will show you snippets of 10 papers and ask you to rate them on a scale of 1 to 10 (1 being the least relevant and 10 being the most relevant). 

**Note**: Many improvements are planned for this process, including the ability to skip papers, change sample size, and dynamically update the system based on your feedback from the generated feed.

When you are ready, click the "Start Calibration" button, after rating the 10 papers, you should see the following message:

<img width="975" alt="Screen Shot 2023-09-22 at 8 40 27 AM" src="https://github.com/iansnyder333/ScholarlyRecommender/assets/58576523/f5f1b906-550b-4e36-845c-7fa574ce7a49">

Amazing! The ScholarlyRecommender is now configured and is ready to be your personal agent to find you new, personalized, academic publications. Now you can navigate to the Get Recommendations page and click the "generate recommendations" button to see your personalized feed!

<img width="1393" alt="Screen Shot 2023-09-22 at 8 48 25 AM" src="https://github.com/iansnyder333/ScholarlyRecommender/assets/58576523/a884a72e-b0fc-4db5-b9b0-c10c30924dda">

Thank you so much for using ScholarlyRecommender. I recently graduated college and am the sole developer of this project, so I would love any constructive feedback you have to offer to help me improve as a developer. 

Please report any issues by creating an issue on the GitHub repository, or by sending an email to the project email directly.

- **Github Issue**: https://github.com/iansnyder333/ScholarlyRecommender/issues
- **Project Email**: scholarlyrecommender@gmail.com


