# MCQ Generator from Topic

A simple yet powerful web application built with Flask and powered by Google's Gemini AI. This tool allows users to generate multiple-choice questions (MCQs) on any topic they provide. Users can then take the generated quiz and receive instant feedback on their performance.

The application is fully containerized with Docker for easy setup and deployment.

## Features

-   **Dynamic MCQ Generation**: Input any topic and specify the number of questions to generate a custom quiz.
-   **Powered by Google Gemini**: Leverages the `gemini-1.5-flash` model for fast and accurate question generation.
-   **Interactive Quiz Interface**: A clean and user-friendly interface for answering the generated questions.
-   **Instant Scoring and Feedback**: After submitting, see your score, percentage, and a breakdown of correct vs. incorrect answers.
-   **Robust JSON Parsing**: Includes a helper to reliably extract JSON data from the AI's response, even with minor formatting inconsistencies.
-   **Containerized with Docker**: Easily build and run the application in an isolated environment using Docker and Docker Compose.

## Technology Stack

-   **Backend**: Python, Flask
-   **AI Model**: Google Gemini (`gemini-1.5-flash`) via `google-generativeai` SDK
-   **WSGI Server**: Waitress
-   **Frontend**: HTML5, Tailwind CSS (via CDN)
-   **Containerization**: Docker, Docker Compose
-   **Dependencies**: `python-dotenv` for environment management

---

### 1. Configuration

Before running the application, you need to set up your environment variables.

1.  Clone the repository:
    ```bash
    git clone https://github.com/AnantSom/ai-mcq-generator.git
    cd mcq-topic
    ```

2.  Create a file named `.env` in the root of the project directory. You can do this by copying the example file if one exists, or by creating a new file.

3.  Add the following content to your new `.env` file and edit the values:

    ```ini
    # .env

    # Your Google AI API Key
    MY_API_KEY="your_google_api_key_here"

    # The public-facing port for the Docker container
    # The application will be accessible at http://localhost:10000
    PUBLIC_PORT=10000
    ```

### 2. Running the Application

Choose one of the following methods.

#### Method A: Using Docker & Docker Compose (Recommended)

This is the simplest way to get the application running.

1.  Make sure Docker is running on your machine.
2.  Build and run the container in detached mode from your project's root directory:
    ```bash
    docker-compose up --build -d
    ```
3.  The application will be available at **http://localhost:10000** (or whatever port you set for `PUBLIC_PORT`).
4.  To stop the application, run:
    ```bash
    docker-compose down
    ```

#### Method B: Running in a Local Python Environment

1.  Create and activate a virtual environment:
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the Flask application:
    ```bash
    python app.py
    ```

4.  The application will be running in debug mode at **http://localhost:5000**.

