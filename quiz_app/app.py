from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- CRITICAL FIX 1: Reliable File Paths ---
# Assumes app.py is in 'quiz_app/' and data files are in the parent directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

QUESTION_FILE = os.path.join(PARENT_DIR, "questions.json")
# CRITICAL FIX 2: Corrected file name typo from 'user_scores.json' to 'user_name_scores.json'
SCORE_FILE = os.path.join(PARENT_DIR, "user_name_scores.json") 
HISTORY_FILE = os.path.join(PARENT_DIR, "asked_questions.json")

def load_json_file(file_path, default_value):
    """Safely loads a JSON file with FileNotFoundError and JSONDecodeError handling."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {os.path.basename(file_path)}: {e}")
            return default_value
    return default_value

questions = load_json_file(QUESTION_FILE, [])
user_scores = load_json_file(SCORE_FILE, {})
history_data = load_json_file(HISTORY_FILE, {})

# 1️⃣ Enter player name (Root route)
@app.route("/", methods=["GET", "POST"])
def enter_name():
    error = ""
    if request.method == "POST":
        player_name = request.form["player_name"].strip()
        if player_name == "":
            error = "Please enter a valid name."
        elif not questions:
            error = "Quiz is currently unavailable: No questions were loaded."
        else:
            session["player_name"] = player_name
            # CRITICAL FIX 4: Redirect to the dedicated index/intro page before the quiz
            return redirect(url_for("index_page")) 
            
    return render_template("enter_name.html", error=error)

# 1.5️⃣ Index/Intro Page (Added route for the uploaded index.html)
@app.route("/index")
def index_page():
    if "player_name" not in session:
        return redirect(url_for("enter_name"))
    
    player_name = session["player_name"]
    # Pass 'username' to index.html as expected by the template
    return render_template("index.html", username=player_name) 

# 2️⃣ Quiz page (Handles GET to display quiz and POST to calculate score)
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "player_name" not in session:
        return redirect(url_for("enter_name"))
        
    if not questions:
        return "Error: No questions available to load.", 500

    player_name = session["player_name"]

    if request.method == "POST":
        selected_answers = request.form
        score = 0
        
        if "current_questions" not in session:
            # Handle case where user navigates back or session expires
            return redirect(url_for("enter_name")) 
            
        for idx, question in enumerate(session["current_questions"]):
            # Name 'q{idx}' matches the corrected 'name' attribute in quiz.html
            qid = f"q{idx}" 
            if selected_answers.get(qid) == question["answer"]:
                score += 1

        # Save score
        if player_name not in user_scores:
            user_scores[player_name] = []
        user_scores[player_name].append(score)
        
        with open(SCORE_FILE, "w") as f:
            json.dump(user_scores, f, indent=4)

        # Update history
        asked_indexes = history_data.get(player_name, [])
        asked_indexes.extend(session.get("question_indexes", [])) 
        history_data[player_name] = asked_indexes
        with open(HISTORY_FILE, "w") as f:
            json.dump(history_data, f, indent=4)

        return redirect(url_for("result", score=score))

    # --- GET request logic: Select random questions ---
    asked_indexes = history_data.get(player_name, [])
    remaining_indexes = [i for i in range(len(questions)) if i not in asked_indexes]
    
    # Reset history if we run out of unique questions (less than 10)
    if len(remaining_indexes) < 10:
        remaining_indexes = list(range(len(questions)))

    num_questions_to_sample = min(10, len(remaining_indexes))
    
    if num_questions_to_sample == 0:
         return "Error: No questions available to sample.", 500

    question_indexes = random.sample(remaining_indexes, num_questions_to_sample)
    session["question_indexes"] = question_indexes
    current_questions = [questions[i] for i in question_indexes]
    session["current_questions"] = current_questions

    return render_template("quiz.html", questions=current_questions, player=player_name)

# 3️⃣ Result page (Passing all variables needed by result.html)
@app.route("/result")
def result():
    score = int(request.args.get("score", 0))
    player_name = session.get("player_name", "Unknown")

    # Calculate Top 5 leaderboard (average scores)
    avg_scores = {user: sum(scores)/len(scores) for user, scores in user_scores.items()}
    ranking = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)[:5]

    return render_template("result.html", score=score, player=player_name, ranking=ranking, total=10)

# 4️⃣ Leaderboard Page
# CRITICAL FIX 3: Added missing leaderboard route
@app.route("/leaderboard")
def leaderboard():
    # Calculate leaderboard data required by the template
    # The template expects a list of dictionaries with 'rank', 'user', 'avg', 'games'
    
    # 1. Calculate Average Scores
    avg_scores = {}
    for user, scores in user_scores.items():
        if scores:
            avg_scores[user] = {
                'avg': sum(scores) / len(scores),
                'games': len(scores)
            }
        
    # 2. Sort and Rank
    sorted_scores = sorted(avg_scores.items(), key=lambda x: x[1]['avg'], reverse=True)
    
    leaderboard_list = []
    for rank, (user, data) in enumerate(sorted_scores, 1):
        leaderboard_list.append({
            'rank': rank,
            'user': user,
            'avg': data['avg'],
            'games': data['games']
        })
    
    return render_template("leaderboard.html", leaderboard=leaderboard_list[:10]) # Show top 10

# 5️⃣ Logout route
@app.route("/logout")
def logout():
    session.pop("player_name", None)
    session.pop("current_questions", None)
    session.pop("question_indexes", None)
    return redirect(url_for("enter_name"))

if __name__ == "__main__":
    app.run(debug=True)