from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#3b82f6"
    elif 18.5 <= bmi < 25:
        return "Normal Weight", "#22c55e"
    elif 25 <= bmi < 30:
        return "Overweight", "#f59e0b"
    else:
        return "Obese", "#ef4444"

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route("/doom", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            age    = int(request.form["age"])
            gender = request.form["gender"]

            if weight <= 0 or height <= 0:
                result = {"error": "Weight and height must be positive numbers."}
            else:
                bmi = calculate_bmi(weight, height)
                category, color = get_category(bmi)

                height_m = height / 100
                ideal_min = round(18.5 * (height_m ** 2), 1)
                ideal_max = round(24.9 * (height_m ** 2), 1)

                result = {
                    "bmi"      : bmi,
                    "category" : category,
                    "color"    : color,
                    "weight"   : weight,
                    "height"   : height,
                    "age"      : age,
                    "gender"   : gender,
                    "ideal_min": ideal_min,
                    "ideal_max": ideal_max,
                }
        except ValueError:
            result = {"error": "Please enter valid numeric values."}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
