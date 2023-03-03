from log import blog
from endpoints import endpoints
from results import results

from branchweb import webserver

def main():
    blog.info("Trashquiz Initializing..") 
    blog.info("Serving on port 4000")

    results.read_quiz_file() 
    webserver.web_server.register_get_endpoints(endpoints.trashquiz_web_providers.get_endpoints())
    webserver.start_web_server("0.0.0.0", 4000)    


if(__name__ == "__main__"):
    main()
