from flask import Flask, render_template, request,redirect
import requests

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("search.html")


@app.route("/search", methods=['POST'])
def getSearch():
    if request.method == "POST":
        search_v = request.form["name_search"]
        print("search_v = " ,search_v)
        if search_v is None or search_v == "" or search_v.isspace():
            return redirect("/")
        else:
            url = f'https://www.googleapis.com/books/v1/volumes?q="{search_v}"'
            response: list = requests.get(url=url).json()["items"]
            responseWithImages = getImages(response)
            return render_template("books.html", books=responseWithImages)


# @app.route("/search/<string:searchQuery>")
# def getSearchResults(searchQuery: str = "bhagvad gita"):
#     if searchQuery == "" or searchQuery.isspace():
#         return render_template("search.html")
#     else:
#         url = f'https://www.googleapis.com/books/v1/volumes?q="{searchQuery}"'
#         response: list = requests.get(url=url).json()["items"]
#         responseWithImages = getImages(response)
#         return render_template("books.html", books=responseWithImages)


def getImages(response: list):
    for i in response:
        if "imageLinks" in i["volumeInfo"]:
            i["image"] = i["volumeInfo"]["imageLinks"]["thumbnail"]
        else:
            i["image"] = "https://via.placeholder.com/200"
    return response


app.run(host="0.0.0.0", port="5001", debug=True)
