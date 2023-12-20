from flask import Flask, redirect, render_template, request
import redis
import hashlib

# r = redis.Redis()
r = redis.Redis(host='redis-11326.c302.asia-northeast1-1.gce.cloud.redislabs.com', password='tKxagI1L2BKTuL9t3lEE9AeVzjThkQyX', port=11326)

app = Flask(__name__)

# Function to shorten a URL
def shorten_url_fun(original_url):
  # Generate unique identifier and hash
  identifier = hashlib.sha256(original_url.encode()).hexdigest()[:6]
  r.set(identifier, original_url)
  return f"{request.url}{identifier}"

# Function to retrive the url from the database
def retrive_url(identifier):
  original_url = r.get(identifier).decode()
  return original_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = str(request.form.get("original_url"))
        shorten_url = shorten_url_fun(original_url)
        return render_template("index.html", shorten_url=shorten_url, original_url=original_url)
    return render_template("index.html", shorten_url="Shorten Url")

@app.route("/<short_code>")
def redirect_to_original_url(short_code):
    try:
        return redirect(retrive_url(short_code))
    except:
        return "ERROR in URL"


r.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)