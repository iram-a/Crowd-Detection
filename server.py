from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)   # move this *after* app is created

@app.route("/crowd_status")
def crowd_status():
    coaches = []
    for i in range(12):
        occ = random.randint(0, 100)  # random occupancy %
        if occ < 40:
            status = "safe"
        elif occ < 70:
            status = "moderate"
        else:
            status = "overcrowded"
        coaches.append({
            "coach": i + 1,
            "occupancy": occ,
            "level": status  # 👈 IMPORTANT: match key name with frontend script.js
        })
    return jsonify(coaches)  # 👈 return list, not {"coaches": [...]}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
