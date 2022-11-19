from webserver import webserver
from log import blog
from webserver import endpoints
from results import results

def main():
    blog.info("Initializing..") 
    blog.info("Serving on port 4000")

    results.read_quiz_file() 
    
    for r in results.quiz.questions:
        print(r.quest)
        print(r.answers)

    endpoints.register_endpoints()

    webserver.start_web_server("0.0.0.0", 4000)
    


if(__name__ == "__main__"):
    main()
