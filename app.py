from flask import Flask, request
import sqlite3, random

app = Flask(__name__)

career_options = {
    "python": ["Data Scientist", "Backend Developer", "AI Engineer"],
    "java": ["Software Developer", "Android Developer"],
    "ml": ["ML Engineer", "AI Researcher"],
    "web": ["Frontend Developer", "Full Stack Developer"],
    "cybersecurity": ["Cybersecurity Analyst", "Ethical Hacker"],
}

def get_career(skills):
    skills = skills.lower().split(",")
    careers = [random.choice(career_options[s.strip()]) for s in skills if s.strip() in career_options]
    return careers[0] if careers else "Software Engineer"

def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, skills TEXT, career TEXT)")
    conn.close()

init_db()
@app.route('/')
def home():
    return '''
    <h1>AI Career Guidance</h1>
    <form action="/predict" method="post">
        Name: <input type="text" name="name"><br>
        Skills (comma-separated): <input type="text" name="skills"><br>
        <button type="submit">Get Career</button>
    </form>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    name, skills = request.form['name'], request.form['skills']
    career = get_career(skills)
    
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO users (name, skills, career) VALUES (?, ?, ?)", (name, skills, career))
    conn.commit()
    conn.close()

    return f"<h1>Hello {name}, your suggested career is: {career}</h1><a href='/'>Try Again</a>"

if __name__ == '__main__':
    app.run(debug=True)
