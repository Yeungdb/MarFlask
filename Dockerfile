FROM yeungdb/marsyas_flask

ENV KEY="alsdjflasjdflkjaslgknlak"

EXPOSE 5000

WORKDIR /home/MarFlask
#RUN git pull origin master 
COPY ./MarsyasServer.py ./MarsyasServer.py
ENTRYPOINT ["python"]
CMD ["MarsyasServer.py"]
