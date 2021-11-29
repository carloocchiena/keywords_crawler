from flask import Flask, request, render_template, Response
from concurrent.futures import ThreadPoolExecutor, as_completed
from processing import kw_ranking, crawler

app = Flask(__name__)
app.config["DEBUG"] = True

#orchestrator function
def generate_kw(links_input):
    MAX_THREADS = 50
    threads = min(MAX_THREADS, len(links_input))
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(kw_ranking, link): link for link in links_input}
        
        yield "Process started - results will follow below:<br><br>"  #this is to "immediately" return a value
        
        for result in as_completed(futures):
            link_list = futures.get(result)
            try:
                data=result.result()
            except Exception as e:
                return "NOK1"
            else:
                yield (f"Link: {link_list}\n<br> Data:{list(data.values())}\n<br><br>")

#render about page 
@app.route('/about', methods = ["GET"])
def about():
    return render_template("about.html")

#render content page
@app.route('/content')
def input_page():
    try:
        return Response(generate_kw(links), mimetype="text/html") 
    except Exception as e:
        return ""
    
#render main page
@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        url = f"https://www.{request.form['url']}"
        try:
            global links
            links = crawler(url)
        except Exception as e:
            errors = e
        
    elif request.method == "GET":
        url = None
    return render_template('index.html.jinja') 

if __name__ == '__main__':
    app.run(use_reloader=False)
