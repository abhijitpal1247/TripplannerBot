# Trip-Planner Bot: A Streamlit-Powered trip planning bot

## Project Introduction

This project uses the Langchain library to build a bot within a Streamlit framework, this project is a quick and dirty implementation, which serves as my first encounter with Langchain. 
The Trip-Planner Bot is an interactive tool for accessing geographic information, identifying points of interest, and getting travel routes with customizable waypoints and transportation modes.

## Functionality Overview

The Trip-Planner Bot uses some free APIs that provide geographical information to the LLM. Below are the key functionalities offered by this application:

- **Location Information Retrieval**: Provides details about a given location.
- **Exploration of Places of Interest**: Identifies and describes nearby attractions.
- **Route Planning**: Generates travel routes between designated points, and supports multiple waypoints between the travel and different transportation modes.

## Integration of APIs

This project harnesses the capabilities of several external APIs to furnish its core functionalities:

- **OpenStreetMap API (via Geopy)**: This API is pivotal in obtaining accurate geocodes for each location.
- **Bing Maps API**: Used for creating routes between specified locations. This API supports the addition of multiple waypoints between the travel and supports different transportation modes.
- **FourSquare API**: Provides up-to-date information about places of interest, including concise descriptions.
- **Wikipedia**: Provides information to answer general questions (tool provided by Langchain)

## LLM Used

The LLM used here is OpenAI's gpt-3.5-turbo, it can replaced with any other open-source LLM. 
To deploy the app on google-colab you can have a look at my other [repo](https://github.com/abhijitpal1247/image-mix-with-controlnet)

## Getting Started

To run the Trip-Planner Bot locally, you need to:

1. Clone the repository to your local machine.
2. Install necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```




3. Start the Streamlit application:
    ```bash
    streamlit run main.py
    ```
4. Navigate to the displayed URL in your web browser.

### Note:

Ensure you have valid API keys for OpenStreetMap, Bing Maps, and FourSquare configured in your environment.

## Contributions

Contributions are welcome! If you have ideas for improvements or encounter any issues, please feel free to fork the repository and submit a pull request or open an issue.

---

A video to show how the chatbot responds to different prompts of the user.

https://github.com/abhijitpal1247/TripplannerBot/assets/69110711/dcccf7b4-8369-41d6-a3b0-69fa7045e6b1


Please give a star to this repo, if it helps you in any way, thanks!!

---
