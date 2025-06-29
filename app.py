import os
import base64
import json
import re

from dotenv import load_dotenv
from flask import Flask, render_template, request
import google.generativeai as genai

# --- App Initialization ---
app = Flask(__name__)
load_dotenv()

# --- AI and API Setup ---
try:
    api_key = os.getenv("MY_API_KEY")
    if not api_key:
        raise ValueError("MY_API_KEY is not set in the .env file.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("[MCQ Topic] Google AI SDK configured successfully.")
except Exception as e:
    print(f"[MCQ Topic] ERROR: Failed to configure Google AI SDK: {e}")
    model = None

# --- Helper Functions ---
def clean_json_response(text):
    """Robustly finds and extracts a JSON array from a string."""
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return text.strip().strip('`').strip('json').strip()

# --- Global Template Variables ---
@app.context_processor
def inject_global_vars():
    """Injects variables into all templates for use in the navigation bar."""
    return {
        'WEBSITE_MANAGER_URL': os.getenv('WEBSITE_MANAGER_URL', 'http://localhost:10001'),
        'MCQ_VIDEO_URL': os.getenv('MCQ_VIDEO_URL', 'http://localhost:10002')
    }

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def generate_mcqs():
    if model is None:
        return render_template("index.html", error="Application is not configured correctly. Please check the API key.")

    if request.method == "GET":
        return render_template('index.html')
        
    topic = request.form.get("topic")
    mcq_count = request.form.get("mcq_count", "5")
    
    try:
        prompt = (
            f"Generate exactly {mcq_count} multiple-choice questions about '{topic}'. "
            f"The output must be a valid JSON array of objects, with no other text or markdown formatting. "
            f"Each object in the array must have three keys: 'question' (string), 'options' (an array of 4 strings), "
            f"and 'answer' (a string that exactly matches one of the options)."
        )
        
        response = model.generate_content(prompt)
        cleaned_text = clean_json_response(response.text)
        mcqs = json.loads(cleaned_text)
        
        encoded_json = base64.b64encode(json.dumps(mcqs).encode()).decode()
        
        return render_template("result.html", questions=mcqs, topic=topic, answers_json=encoded_json)
        
    except json.JSONDecodeError:
        raw_response = response.text if 'response' in locals() else "No response from AI."
        print(f"--- JSON PARSE ERROR ---\n{raw_response}\n----------------------")
        return render_template("index.html", error="The AI returned an invalid format. Please try again.")
    except Exception as e:
        print(f"--- UNKNOWN ERROR ---\n{e}\n---------------------")
        return render_template("index.html", error=f"An unexpected error occurred: {e}")

@app.route("/submit", methods=["POST"])
def submit_answers():
    try:
        encoded_json = request.form["answers_json"]
        questions = json.loads(base64.b64decode(encoded_json).decode())
        
        user_answers, correctness = [], []
        for i, q in enumerate(questions):
            selected_option = request.form.get(f"q{i}", "")
            user_answers.append(selected_option)
            correctness.append(selected_option == q["answer"])
            
        total = len(questions)
        score = sum(correctness)
        percentage = round((score / total) * 100, 2) if total > 0 else 0
        
        return render_template("submission_result.html",
                               topic=request.form.get("topic"),
                               questions=questions,
                               user_answers=user_answers,
                               correctness=correctness,
                               score=score,
                               total=total,
                               percentage=percentage)
    except Exception as e:
        print(f"Error processing submission: {e}")
        return render_template("index.html", error=f"Error processing your answers. Please try again.")

# --- For Local Execution ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
