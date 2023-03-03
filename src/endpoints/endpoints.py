from results import results
from results import score
from log import blog

import os

class trashquiz_web_providers():
    
    @staticmethod
    def get_endpoints():
        providers = {
                "img.png": trashquiz_web_providers.img_endpoint,
                "": trashquiz_web_providers.root_endpoint,
                "quiz": trashquiz_web_providers.quiz_form_endpoint,
                "submitquiz": trashquiz_web_providers.submitquiz_endpoint,
                "results": trashquiz_web_providers.score_endpoint,
                "music": trashquiz_web_providers.music_endpoint
        }
        return providers
    
    @staticmethod
    def img_endpoint(httphandler, form_data):
        with open("web/logo_new.png", "rb") as img:
            httphandler.send_file(img, os.path.getsize("web/logo_new.png"), "logo.png")

    @staticmethod
    def music_endpoint(httphandler, form_data):
        with open("web/background-music.mp3", "rb") as mp3:
            httphandler.send_file(mp3, os.path.getsize("web/background-music.mp3"), "music.mp3")


    @staticmethod
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
        score.score.add_score(username, num_correct)    

        httphandler.send_response(200)
        httphandler.send_header("Content-type", "text/html")
        httphandler.end_headers()

        httphandler.write_answer_encoded("<html><body>")
        httphandler.write_answer_encoded("<script>".format(num_correct))
        httphandler.write_answer_encoded("window.onload = function() { window.location.href = \"/results\";}")
        httphandler.write_answer_encoded("</script>")
    
    @staticmethod
    def score_endpoint(httphandler, form_data):
        
        httphandler.send_response(200)
        httphandler.send_header("Content-type", "text/html")
        httphandler.end_headers()

        with open("web/results.html", "r") as f:
            file_contents = f.read()

            table_contents = ""

            for x in score.score.get_scores():
                table_contents = table_contents + "<tr>"
                table_contents = table_contents + "<td>{}</td>".format(x)
                table_contents = table_contents + "<td>{} / 4</td>".format(score.score.get_scores()[x])
                table_contents = table_contents + "</tr>"

            file_contents = file_contents.replace("DATA_INSERT_POINT", table_contents)
            httphandler.write_answer_encoded(file_contents)

    
    @staticmethod
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

    @staticmethod
    def root_endpoint(httphandler, form_data):
        with open("web/main.html", "r") as file:
            httphandler.send_str_raw(200, file.read())

