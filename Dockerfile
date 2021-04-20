# Dockerfile for AWS deployment with Elastic Beanstalk:
# - https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/docker.html
#
# Link to the github code can be done with CodePipeline:
# - https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html#welcome-get-started
# - Deployment with Elastic Beanstalk

FROM python:3.8-slim-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["bash", "-c", "streamlit run --browser.serverAddress 0.0.0.0 --server.port 80 streamlit_app.py"]
