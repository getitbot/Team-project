import os
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = "learnflow_123"
EXCEL_FILE = "submissions.xlsx"

def save_to_excel(student_id, name, link):
    """Saves data efficiently to Excel."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = {
        "Date": [timestamp],
        "ID": [student_id],
        "Student Name": [name],
        "GitHub Link": [link]
    }
    df_new = pd.DataFrame(new_data)

    if not os.path.exists(EXCEL_FILE):
        df_new.to_excel(EXCEL_FILE, index=False)
    else:
        # Read existing, append, and save
        df_old = pd.read_excel(EXCEL_FILE)
        # Check for duplicate ID
        if student_id in df_old["ID"].astype(str).values:
            return False
        df_final = pd.concat([df_old, df_new], ignore_index=True)
        df_final.to_excel(EXCEL_FILE, index=False)
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    sid = request.form.get('sid')
    sname = request.form.get('sname')
    gh_link = request.form.get('gh_link')

    if not sid or not sname or not gh_link:
        flash("All fields are required!", "error")
        return redirect(url_for('home'))

    success = save_to_excel(sid, sname, gh_link)
    
    if success:
        flash("Project submitted successfully!", "success")
    else:
        flash("Error: This Student ID has already submitted.", "error")
        
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
