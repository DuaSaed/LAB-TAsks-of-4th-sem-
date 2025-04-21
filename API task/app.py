from flask import Flask, render_template, request

app = Flask(__name__)

vehicle_data = {
    "toyota": {"origin": "Japan", "founded": 1937, "popular_model": "Corolla"},
    "honda": {"origin": "Japan", "founded": 1948, "popular_model": "Civic"},
    "bmw": {"origin": "Germany", "founded": 1916, "popular_model": "BMW 3 Series"},
    "ford": {"origin": "USA", "founded": 1903, "popular_model": "F-150"},
    "audi": {"origin": "Germany", "founded": 1909, "popular_model": "A4"},
    # add more if needed
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        brand = request.form["brand"].strip().lower()  # normalize input
        info = vehicle_data.get(brand)
        if info:
            return render_template("result.html", brand=brand.title(), info=info)
        else:
            return render_template("result.html", error=f"No information found for '{brand.title()}'. Try again with a valid brand.")
    return render_template("interface.html")

if __name__ == "__main__":
    app.run(debug=True)
