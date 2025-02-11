import os
import gradio as gr
from transformers import pipeline
import re

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

moderation_guidelines = """
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

"""

default_cuss_words = {"damn", "hell", "shit", "fuck", "ass", "bastard", "bitch", "bollocks", "bugger", 
"bullshit", "crap", "dammit", "douche", "dumbass", "faggot", "jackass", "jerk", 
"motherfucker", "piss", "prick", "slut", "son of a bitch", "twat", "wanker"}

community_terms = {"religion", "race", "ethnicity", "group", "community", "gender"}

def extract_blocked_words(guidelines):
    """Extracts blocked words from moderation guidelines."""
    match = re.search(r"block words:\s*(.*)", guidelines.lower())
    return {word.strip() for word in match.group(1).split(",") if word.strip()} if match else set()

def moderate_message(message, guidelines):
    """Moderates a message based on sentiment and dynamic moderation rules."""
    
    sentiment = sentiment_pipeline(message)[0]['label']  
    
    blocked_words = extract_blocked_words(guidelines)
    allow_positive = "allow positive" in guidelines.lower()
    block_cuss_words = "block cuss" in guidelines.lower()
    allow_negative_personal = "allow negative comments about individuals" in guidelines.lower()
    block_negative_community = "block negative comments against a community" in guidelines.lower()
    block_personal_names = "block personal names" in guidelines.lower() 

    words = set(re.findall(r'\w+', message.lower()))

    # 1. Block Cuss Words
    if block_cuss_words and words & default_cuss_words:
        return "❌ Message Blocked: Contains inappropriate language."

    # 2. Block Dynamically Defined Words
    if words & blocked_words:
        return "🚫 Message Blocked: Contains restricted words."

    # 3. Block Personal Names Dynamically
    if block_personal_names:
        entities = ner_pipeline(message)
        for entity in entities:
            if entity['entity_group'] == 'PER': 
                return "🚫 Message Blocked: Contains personal names."

    if sentiment == "POSITIVE" and allow_positive:
        return f"✅ Allowed (Positive): {message}"

    if sentiment == "NEGATIVE":
        if any(word in message.lower() for word in community_terms) and block_negative_community:
            return "🚫 Message Blocked: Negative content targeting a community."
        elif allow_negative_personal:
            return f"⚠️ Allowed (Negative - Personal Attack): {message}"
    
    return f"✅ Allowed (Neutral): {message}"

with gr.Blocks() as demo:
    gr.Markdown("### 🛡️ AI-Powered Moderation System")
    guidelines_input = gr.Textbox(value=moderation_guidelines, label="Moderation Guidelines (Admins Can Update)", lines=6)
    
    with gr.Row():
        msg_input = gr.Textbox(label="Enter Message")
        msg_output = gr.Textbox(label="Moderation Result", interactive=False)
    
    moderate_btn = gr.Button("Check Message")
    
    moderate_btn.click(moderate_message, inputs=[msg_input, guidelines_input], outputs=[msg_output])

# Run App with PORT Binding for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050)) 
    demo.launch(server_name="0.0.0.0", server_port=port)