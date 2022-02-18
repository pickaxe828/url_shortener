import functions
import validators
import urllib

from flask import Flask, request, redirect, Response
from deta import Deta
from datetime import datetime
from jsoncomment import JsonComment

json = JsonComment()

with open("credentials.jsonc", "r") as conf_raw:
    conf_raw = conf_raw.read()
    conf = json.loads(conf_raw)

app = Flask(__name__)
deta = Deta(conf["deta_api_token"])
db = deta.Base(conf["deta_base_name"])


@app.route('/', methods=['GET'])
def empty():
    return redirect(f"{request.base_url}home")

@app.route('/home', methods=['GET'])
def home():
    return "Welcome to the URL shortener's backend! For more information/ usage, visit our github: "

@app.route('/create', methods=['GET', 'POST'])
def convert_to_id():
    url = request.args.get("url")
    if validators.url(url):
        url = urllib.parse.quote(url, safe='')
        _id = functions.randb58str(7)
        check = db.fetch({"url": url}).items
        # if cannot find any id with the same id, create a new one
        if check == []:
            db.put(data={
                "time": datetime.now().isoformat(),
                "url": url,
                "key": _id
            })
            return f"{'/'.join(request.url.split('/')[:-1])}/{_id}"

        else:
            return Response(f"Link already exists: {'/'.join(request.url.split('/')[:-1])}/{check[0]['key']}", status=409)
    else:
        return Response(status=400)


@app.route('/<string:arg>', methods=['GET', 'POST'])
def convert_to_url(arg):
    # Avoid favicon.ico requests
    if arg == "favicon.ico": return ""
    
    retrive = db.get(arg)
    if retrive != None:
        return redirect(urllib.parse.unquote(retrive['url']))
    else:
        return Response(status=404)

# No app.run() because we are using Deta Micros
