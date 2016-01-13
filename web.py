from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory, send_file, url_for
import two_column_text
import vk_api

app = Flask(__name__)


@app.route("/")
def hello():
    # return send_file('results_share/wall-87512171_139.txt')
    return url_for("results_share", filename="wall-87512171_139.txt")
    # return "Hello World!"


@app.route("/enter_url_to_vk")
def welcome_process_post_text():
    return render_template("vk_url_field.html")


@app.route("/enter_url_to_vk", methods=["POST"])
def process_post_text():
    url = request.form["url_to_post"]
    url = vk_api.simplify_vk_url(url)
    text = vk_api.url_to_post_text_converter(url)
    t = two_column_text.TwoColumnText(text, url)
    result = t.handle_text()
    if not result:
        return "Bad text"
    else:
        path_to_file = t.save_handled_text()
        return path_to_file
        # return send_file(path_to_file)
        # path_to_dir = "/".join(path_to_file.split("/")[:-1])
        # filename = path_to_file.split("/")[-1]
        # return send_from_directory(path_to_dir, filename)
        # return render_template("download_file.html", filename=path_to_file)

if __name__ == "__main__":
    # url="https://vk.com/wall-12648877_1663646"
    # vk_api.url_to_post_text_converter(url)
    app.debug
    app.run()
