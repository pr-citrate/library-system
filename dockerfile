FROM node:19
FROM python:3.11
RUN pip install pynecone
RUN pc init
CMD pc run