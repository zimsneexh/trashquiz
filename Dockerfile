FROM alpine
RUN mkdir /gahut
RUN mkdir /gahut/src/
RUN mkdir /gahut/web/
RUN mkdir /gahut/res/
COPY src/ gahut/src
COPY web/ gahut/web
COPY res/ gahut/res
COPY branchweb /branchweb/
RUN apk update && apk add python3 py3-pip make
RUN pip install setuptools && pip install bcrypt
RUN cd /branchweb/ && python3 setup.py sdist && pip install dist/branchweb-1.0.tar.gz
CMD /gahut/src/entry.sh
EXPOSE 4000/tcp
