<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/iansnyder333/ScholarlyRecommender">
    <img src="images/logo.png" alt="Logo" width="400" height="400">
  </a>

<h3 align="center">Scholarly Recommender</h3>

  <p align="center">
    End-to-end product that sources recent academic publications and prepares a feed of recommended readings in seconds. 
    <br />
    <a href="https://github.com/iansnyder333/ScholarlyRecommender"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/iansnyder333/ScholarlyRecommender">View Demo</a>
    ·
    <a href="https://github.com/iansnyder333/ScholarlyRecommender/issues">Report Bug</a>
    ·
    <a href="https://github.com/iansnyder333/ScholarlyRecommender/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

  As an upcoming data scientist with a strong passion for deep learning, I am always looking for new technologies and methodologies. Naturally, I spend a considerable amount of time researching and reading new publications to accomplish this. However, **over 14,000 academic papers are published every day** on average, making it extremely tedious to continuously source papers relevant to my interests. My primary motivation for creating ScholarlyRecommender is to address this, creating a fully automated and personalized system that prepares a feed of academic papers relevant to me. This feed is prepared on demand, through a completely abstracted streamlit web interface, or sent directly to my email on a timed basis. This project was designed to be scalable and adaptable, and can be very easily adapted not only to your own interests, but become a fully automated, self improving newsletter. Details on how to use this system, the methods used for retrieval and ranking, along with future plans and features planned or in development currently are listed below.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python.com]][Python-url]
* [![Streamlit][Streamlit.com]][Python-url]
* [![Pandas][Pandas.com]][Pandas-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To try ScholarlyRecommender, you can use the streamlit web application found HERE. This will allow you to use the system in its entirety without needing to install anything, however your recommendations will not be personalized and will use the default labeled dataset which is based on my own interests. In order to tailor the application to give relevant recommendations tailored to you, you must install the app and make some modifications detailed below.

### Prerequisites

In order to install this app locally you need to have git along with a suitable Python version. This app was developed using Python 3.11 and has not been tested on any earlier versions.


### Installation

MacOS
1. Clone the repo
   ```sh
   git clone https://github.com/iansnyder333/ScholarlyRecommender.git
   ```
2. cd into the repo and setup a enviroment
   ```sh
   cd ScholarlyRecommender
   python3.11 -m venv env
   source env/bin/activate
   ```
3. install dependencies 
   ```sh
   pip3.11 install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Webapp, email, parameters, labeling etc


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/iansnyder333/ScholarlyRecommender/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Not Distributed under the MIT License. Don't See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ian Snyder - [@iansnydes](https://twitter.com/iansnydes) - idsnyder136@gmail.com 

Project Email - scholarlyrecommender@gmail.com

My Website: [iansnyder333.github.io/frontend/](https://iansnyder333.github.io/frontend/)

Linkedin: [www.linkedin.com/in/ian-snyder-aa1600182/](https://www.linkedin.com/in/ian-snyder-aa1600182/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python.com]:https://img.shields.io/badge/Python-blue
[Python-url]:https://www.python.org/
[Streamlit.com]:https://img.shields.io/badge/Streamlit-red
[Streamlit-url]:https://streamlit.io/
[Pandas.com]:https://img.shields.io/badge/pandas-purple
[Pandas-url]:https://pandas.pydata.org/

