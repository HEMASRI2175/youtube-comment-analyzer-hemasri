
# My Project

## Overview

This project leverages various Python packages and APIs to create a powerful application. It includes functionality to interact with the YouTube API and OpenAI API, and is built using Streamlit for an interactive web interface.

## Installation and Setup

### Step 1: Clone the Repository

```sh
git clone https://github.com/HEMASRI2175/Youtube_comment_analyzer.git
cd yourproject
```

### Step 2: Create a Virtual Environment

Create a virtual environment to manage your project dependencies.

```sh
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Download all the dependencies by running the following command in your terminal:

```sh
make requirements
```

### Step 4: Setup Google Cloud Project

1. Create a project on the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the YouTube Data API v3 for your project.
3. Follow the instructions [here](https://developers.google.com/youtube/registering_an_application) to get your API key.

### Step 5: Configure Streamlit Secrets

1. Create a `.streamlit` folder at the source level of your project.
2. Add a `secrets.toml` file to this folder.
3. Set your YouTube and OpenAI API keys in the `secrets.toml` file. Refer to the `secrets.toml.example` file for structure.

Your `secrets.toml` should look like this:

```toml
[general]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
```

### Step 6: Run the Application

Run the Streamlit app using the following command:

```sh
make run
```

Open the app in your browser at [http://localhost:8501](http://localhost:8501).

## Best Practices

- **API Key Safety**: Ensure that your API keys are not hard-coded in your scripts. Use environment variables or secure vaults to manage your keys safely. See best practices around API key safety [here](https://cloud.google.com/docs/authentication/api-keys).

## Dependencies

- `nltk`
- `streamlit`
- `tenacity`
- `openai`
- `google-api-python-client`
- `pytube`
- `transformers`
- `python-dotenv`
- `google-auth-httplib2`
- `google-auth-oauthlib`

