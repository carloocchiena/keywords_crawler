from flask import Flask, request, render_template
from processing import kw_ranking, crawler, cleaner

app = Flask(__name__)
app.config["DEBUG"] = True

#render about page 
@app.route('/about', methods = ["GET"])
def about():
    return render_template("about.html")

#render main page
@app.route('/', methods = ["GET", "POST"])
def input_page():
    errors = ""
    if request.method == "POST":
        url = None
        url = f"https://www.{request.form['url']}"
      
        if url is not None:
            try:
                links = crawler(url)
                result = kw_ranking(links)
                return render_template("results.html", result=result)
            except Exception as e:
                #errors = "🐸 The anti-bug frog has caught something! Can you try again with another site? Sorry, it's still a beta version!"
                errors = e
    return render_template("main.html", errors=errors)

if __name__ == '__main__':
    app.run(use_reloader=False)
  
