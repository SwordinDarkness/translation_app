#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
import re

import requests
from translation_app.crew  import TranslationApp

from crewai_tools import ScrapeWebsiteTool



warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

text = "Sample"


    # Initialize the tool with the website URL,
    # so the agent can only scrap the content of the specified website



# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    url = input("Enter a URL: ").strip()

    # Add 'http://' if no scheme is provided
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    if is_valid_url(url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ The URL '{url}' is reachable!")
            else:
                print(f"⚠️ The URL returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: Could not reach '{url}'.\nDetails: {e}")
    else:
        print("❌ Invalid URL format. Please enter a valid URL.")

    # Extract the text from the site
    tool = ScrapeWebsiteTool(
        website_url=url)
    text = tool.run()
    print(text)
    inputs = {
        'article' : text
    }
    
    try:
        TranslationApp().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {

    }
    try:
        TranslationApp().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TranslationApp().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'article' : text
    }
    try:
        TranslationApp().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def is_valid_url(url):
    """Check if the entered URL is in a valid format."""
    pattern = re.compile(r'^(https?://)?(www\.)?([a-zA-Z0-9-]+)\.([a-z]{2,6})(/[^\s]*)?$')
    return re.match(pattern, url)
