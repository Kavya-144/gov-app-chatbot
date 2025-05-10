from flask import Flask, request, render_template
import json
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

with open("schemes.json") as f:
    schemes = json.load(f)

def recommend(user):
    matched = []
    for s in schemes:
        c = s["criteria"]
        if (
            c.get("job") == user["job"].lower() and
            c.get("location") == user["location"].lower() and
            user.get("income", float('inf')) <= c.get("income_max", float('inf')) and
            user.get("age", 0) <= c.get("age_max", float('inf'))
        ):
            matched.append(s)
    return matched

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    if request.method == "POST":
        user = {
            "age": int(request.form["age"]),
            "job": request.form["job"],
            "location": request.form["location"],
            "income": int(request.form["income"])
        }
        lang = request.form["lang"]
        result = recommend(user)

        if lang != "en":
            for r in result:
                r["name"] = translator.translate(r["name"], dest=lang).text
                r["apply_steps"] = translator.translate(r["apply_steps"], dest=lang).text
    return render_template("index.html", schemes=result)

if __name__ == "__main__":
    app.run(debug=True)
