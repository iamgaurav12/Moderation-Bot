# Moderation Bot

This project is an AI-powered moderation system that uses NLP models to analyze and moderate messages based on predefined guidelines.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Moderation_bot.git
    cd Moderation_bot
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open the provided Gradio interface in your browser.

3. Enter the message you want to moderate and click "Check Message".

## Moderation Guidelines

The moderation guidelines can be updated by admins through the Gradio interface. The default guidelines include:
- Allow positive messages.
- Block cuss words.
- Allow negative comments about individuals but block negative comments against a community.
- Block personal names.
- Block hate speech or offensive language.
- Block messages containing threats, violence, or self-harm.
- Block excessive use of capital letters (potential shouting).
- Block messages with spam, links, or promotional content.
- Block messages with excessive special characters (potential spam).
- Allow constructive criticism but block harassment and bullying.
- Allow neutral discussions about sensitive topics but block inciting hate.
- Block messages with misleading or false information.
- Block messages containing phone numbers or personal addresses.
- Block messages with excessive repetition of words (spam behavior).

## License

This project is licensed under the MIT License.
