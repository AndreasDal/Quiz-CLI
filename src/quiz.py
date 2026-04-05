# -*- coding: utf-8 -*-
import random
import pathlib
import os
import platform
from string import ascii_lowercase
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_DIR = pathlib.Path(__file__).parent / "questions"

# Global state for simplicity (in production, use a database)
user_sessions = {}  # e.g., {"session_id": {"questions": [...], "current": 0, "score": 0}}

def prepare_questions(questions_dir, num_questions):
    topics = {}
    for toml_file in questions_dir.glob("*.toml"):
        topic_info = tomllib.loads(toml_file.read_text(encoding="utf-8"))
        for topic_data in topic_info.values():
            topics[topic_data["label"]] = topic_data["questions"]
    return topics

class QuizHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_start_page()
        elif self.path.startswith("/quiz"):
            self.send_quiz_page()
        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path).path
        if parsed_path == "/select_topic":
            self.handle_topic_selection()
        elif parsed_path == "/answer":
            self.handle_answer()
        else:
            self.send_error(404)

    def send_start_page(self):
        topics = prepare_questions(QUESTIONS_DIR, NUM_QUESTIONS_PER_QUIZ)
        html = f"""
        <html><body>
        <h1>Quiz App</h1>
        <form method="post" action="/select_topic">
        <label>Choose topic:</label><br>
        {"".join(f'<input type="radio" name="topic" value="{t}"> {t}<br>' for t in sorted(topics))}
        <input type="submit" value="Start Quiz">
        </form>
        </body></html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_topic_selection(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        data = urllib.parse.parse_qs(post_data)
        topic = data['topic'][0]
        
        topics = prepare_questions(QUESTIONS_DIR, NUM_QUESTIONS_PER_QUIZ)
        questions = random.sample(topics[topic], k=min(NUM_QUESTIONS_PER_QUIZ, len(topics[topic])))
        session_id = "user1"  # Simple: use a fixed ID; in real app, generate unique
        user_sessions[session_id] = {"questions": questions, "current": 0, "score": 0}
        
        self.send_response(302)
        self.send_header("Location", f"/quiz?session={session_id}")
        self.end_headers()

    def send_quiz_page(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        session_id = params.get('session', [''])[0]
        if session_id not in user_sessions:
            self.send_error(400, "Invalid session")
            return
        
        session = user_sessions[session_id]
        if session["current"] >= len(session["questions"]):
            self.send_results_page(session)
            return
        
        question = session["questions"][session["current"]]
        correct_answers = question["answers"]
        alternatives = question["answers"] + question["alternatives"]
        ordered_alternatives = random.sample(alternatives, k=len(alternatives))
        
        options = "".join(f'<input type="checkbox" name="answer" value="{alt}"> {alt}<br>' for alt in ordered_alternatives)
        html = f"""
        <html><body>
        <h1>Question {session["current"] + 1}</h1>
        <p>{question["question"]}</p>
        <form method="post" action="/answer">
            <input type="hidden" name="session" value="{session_id}">
        {options}
        <input type="submit" value="Submit">
        </form>
        </body></html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_answer(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        data = urllib.parse.parse_qs(post_data)

        session_id = data.get('session', [''])[0]
        if session_id not in user_sessions:
            self.send_error(400, "Invalid session")
            return
        
        answers = data.get('answer', [])
        
        session = user_sessions[session_id]
        question = session["questions"][session["current"]]
        correct = set(answers) == set(question["answers"])
        if correct:
            session["score"] += 1
        
        session["current"] += 1
        self.send_response(302)
        self.send_header("Location", f"/quiz?session={session_id}")
        self.end_headers()

    def send_results_page(self, session):
        html = f"""
        <html><body>
        <h1>Quiz Complete!</h1>
        <p>You scored {session["score"]} out of {len(session["questions"])}.</p>
        <a href="/">Try Again</a>
        </body></html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, QuizHandler)
    print("Server running at http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()