# 

# from flask import Flask, request, redirect, send_file, render_template
# import datetime
# import logging
# import csv
# import os

# app = Flask(__name__)

# # Log file for tracking
# LOG_FILE = 'tracking.csv'
# logging.basicConfig(filename='server.log', level=logging.INFO)

# # Ensure CSV file exists with headers
# if not os.path.exists(LOG_FILE):
#     with open(LOG_FILE, mode='w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['email', 'tracking_id', 'event', 'time'])

# # Utility to log tracking events
# def log_event(email, tracking_id, event):
#     with open(LOG_FILE, mode='a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([email, tracking_id, event, datetime.datetime.now()])
#     logging.info(f"[{event}] {email} - {tracking_id} at {datetime.datetime.now()}")

# @app.route("/")
# def home():
#     return "<h2>✅ Email Tracking Server is Running</h2><p>Visit <a href='/dashboard'>/dashboard</a> to view logs.</p>"

# @app.route("/pixel")
# def pixel():
#     tracking_id = request.args.get("id")
#     email = request.args.get("email", "unknown@example.com")
#     log_event(email, tracking_id, "OPEN")
#     return send_file("transparent.png", mimetype='image/png')

# @app.route("/redirect")
# def redirect_link():
#     tracking_id = request.args.get("id")
#     email = request.args.get("email", "unknown@example.com")
#     log_event(email, tracking_id, "CLICK")
#     return redirect("https://drive.google.com/file/d/1bemImkvQ62BP3glYnm8b88p9jcQsTDG0/view?usp=sharing")

# @app.route("/dashboard")
# def dashboard():
#     events = []
#     with open(LOG_FILE, newline='') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             events.append({
#                 "email": row["email"],
#                 "tracking_id": row["tracking_id"],
#                 "event": row["event"],
#                 "time": row["time"]
#             })
#     return render_template("dashboard.html", events=events)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, send_file, request, redirect, render_template
import csv
from datetime import datetime
import os

app = Flask(__name__)

TRACKING_FILE = 'tracking.csv'
TRANSPARENT_IMAGE = 'transparent.png'

@app.route('/')
def home():
    return "<h2>Welcome to the Email Tracking Server</h2><p>Visit <a href='/dashboard'>/dashboard</a> to see tracking logs.</p>"

@app.route('/pixel')
def pixel():
    tracking_id = request.args.get('id')
    email = request.args.get('email')
    log_event(email, tracking_id, 'OPEN')
    return send_file(TRANSPARENT_IMAGE, mimetype='image/png')

@app.route('/redirect')
def redirect_link():
    tracking_id = request.args.get('id')
    email = request.args.get('email')
    target_url = request.args.get('url', 'https://www.google.com')
    log_event(email, tracking_id, 'CLICK')
    return redirect(target_url)

@app.route('/dashboard')
def dashboard():
    rows = []
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if all(k in row and row[k] for k in ['email', 'tracking_id', 'event', 'time']):
                    rows.append(row)
    return render_template('dashboard.html', logs=rows)

def log_event(email, tracking_id, event_type):
    now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    file_exists = os.path.isfile(TRACKING_FILE)
    with open(TRACKING_FILE, 'a', newline='') as csvfile:
        fieldnames = ['email', 'tracking_id', 'event', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'email': email, 'tracking_id': tracking_id, 'event': event_type, 'time': now})

if __name__ == '__main__':
    app.run(debug=True)
