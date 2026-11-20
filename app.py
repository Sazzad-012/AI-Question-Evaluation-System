
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()

    print("Received Data:", data)

    return jsonify({
        "message": "Data received successfully!",
        "received_data": data
    })

if __name__ == "__main__":
    app.run(debug=True)
