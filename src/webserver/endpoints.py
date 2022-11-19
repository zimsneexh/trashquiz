from webserver import webserver
from results import results
from results import score
from log import blog

import os

class endpoint():
    def __init__(self, path, handler):
        self.path = path
        self.handlerfunc = handler

def register_endpoints():
    webserver.register_endpoint(endpoint("img.png", img_endpoint))
    webserver.register_endpoint(endpoint("", root_endpoint))
    webserver.register_endpoint(endpoint("quiz", quiz_form_endpoint))
    webserver.register_endpoint(endpoint("submitquiz", submitquiz_endpoint))
    webserver.register_endpoint(endpoint("results", score_endpoint))
    
def img_endpoint(httphandler, form_data):
    img = open("web/logo.png", "rb")
    httphandler.send_file(img, os.path.getsize("web/logo.png"))

def submitquiz_endpoint(httphandler, form_data):
    q = results.quiz()

    if(not "fname" in form_data):
        httphandler.generic_malformed_request()
        return

    if(not "answer1" in form_data):
        httphandler.generic_malformed_request()
        return

    if(not "answer2" in form_data):
        httphandler.generic_malformed_request()
        return
    
    if(not "answer3" in form_data):
        httphandler.generic_malformed_request()
        return
    
    if(not "answer4" in form_data):
        httphandler.generic_malformed_request()
        return
   
    username = form_data["fname"]

    a1 = form_data["answer1"]
    a2 = form_data["answer2"]
    a3 = form_data["answer3"]
    a4 = form_data["answer4"]

    blog.info("Received result from {} : {} - {} - {} - {}".format(username, a1, a2, a3, a4))
    
    num_correct = 0

    if(q.validate_answer(0, a1)):
        num_correct = num_correct + 1

    if(q.validate_answer(1, a2)):
        num_correct = num_correct + 1

    if(q.validate_answer(2, a3)):
        num_correct = num_correct + 1

    if(q.validate_answer(3, a4)):
        num_correct = num_correct + 1

    
    blog.info("{} got {}/4".format(username, num_correct))
    score.score().add_score(username, num_correct)    

    httphandler.send_response(200)
    httphandler.send_header("Content-type", "text/html")
    httphandler.end_headers()

    httphandler.write_answer_encoded("<html><body>")
    httphandler.write_answer_encoded("<p>{} of 4 correct!</p>".format(num_correct))
    httphandler.write_answer_encoded("<a href=\"/\">Back to main page</a>")
    httphandler.write_answer_encoded("</body></html>")

def score_endpoint(httphandler, form_data):
    s = score.score()
    
    httphandler.send_response(200)
    httphandler.send_header("Content-type", "text/html")
    httphandler.end_headers()

    httphandler.write_answer_encoded("<html><body><table border=\"1px solid\">")

    httphandler.write_answer_encoded("<tr border=\"1px solid\">")
    httphandler.write_answer_encoded("<td>Username</td>")
    httphandler.write_answer_encoded("<td>Punkte</td>")
    httphandler.write_answer_encoded("<tr>")

    for x in s.get_scores():
        httphandler.write_answer_encoded("<tr border=\"1px solid\">")
        httphandler.write_answer_encoded("<td>{}</td>".format(x))
        httphandler.write_answer_encoded("<td>{} / 4</td>".format(s.get_scores()[x]))
        httphandler.write_answer_encoded("<tr>")

    httphandler.write_answer_encoded("</table>")
    httphandler.write_answer_encoded("<a href=\"/\">Back to main page</a>")
    httphandler.write_answer_encoded("</body></html>")
    
def quiz_form_endpoint(httphandler, form_data):
    html = open("web/quiz.html", "r").read()

    q = results.quiz()
    
    # TODO: ignore this..

    html = html.replace("{Q1}", q.questions[0].quest)
    html = html.replace("{Q1-A1}", q.questions[0].answers[1])
    html = html.replace("{Q1-A2}", q.questions[0].answers[0])
    html = html.replace("{Q1-A3}", q.questions[0].answers[2])

    html = html.replace("{Q2}", q.questions[1].quest)
    html = html.replace("{Q2-A1}", q.questions[1].answers[2])
    html = html.replace("{Q2-A2}", q.questions[1].answers[0])
    html = html.replace("{Q2-A3}", q.questions[1].answers[1])

    html = html.replace("{Q3}", q.questions[2].quest)
    html = html.replace("{Q3-A1}", q.questions[2].answers[0])
    html = html.replace("{Q3-A2}", q.questions[2].answers[1])
    html = html.replace("{Q3-A3}", q.questions[2].answers[2])

    html = html.replace("{Q4}", q.questions[3].quest)
    html = html.replace("{Q4-A1}", q.questions[3].answers[1])
    html = html.replace("{Q4-A2}", q.questions[3].answers[2])
    html = html.replace("{Q4-A3}", q.questions[3].answers[0])

    httphandler.send_response(200)
    httphandler.send_header("Content-type", "text/html")
    httphandler.end_headers()

    httphandler.wfile.write(bytes(html, "utf-8"))


def root_endpoint(httphandler, form_data):
    html = open("web/main.html", "rb")
    httphandler.send_html(html, os.path.getsize("web/main.html"))
