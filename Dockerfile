FROM python:3

WORKDIR /usr/src/app

COPY *.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV GITHUB_TOKEN= CHANNEL_ID= MATTERMOST_TOKEN= MATTERMOST_URL=

CMD ["sh", "publish.sh"]
