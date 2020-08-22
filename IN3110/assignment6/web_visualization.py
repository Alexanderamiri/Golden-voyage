from visualize import *
from flask import (
    Flask,
    render_template,
    request,
    Response,
    send_file,
    make_response,
    redirect,
    url_for,
)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

app = Flask(__name__, static_url_path="/static")
import io
import base64


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/makeplot", methods=["GET", "POST"])
def makeplot():
    if request.method == "POST":
        img = io.BytesIO()
        feat = [
            request.form.get("features2", None),
            request.form.get("features1", None),
        ]
        cl = request.form.get("classifier", None)
        clf = ft.fit(feat, eval(cl), "diabetes.csv")
        fig = visualize(feat, clf, "diabetes.csv")
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        canvas.print_png(output)
        response = make_response(output.getvalue())
        response.mimetype = "image/png"
        return response


@app.route("/docs", methods=["GET", "POST"])
def docs():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5002, debug=True)
