FROM python:3.9.13

RUN apt-get update -yq && \
    apt-get install -yq tree vim

RUN pip install pipenv

# install nodejs
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    NODE_MAJOR=20 && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install nodejs -y
RUN npm install -g @angular/cli && \
    npx playwright install-deps && \
    npx playwright install chromium

WORKDIR /app
COPY . .
RUN make .venv
RUN cd app && npm install
WORKDIR /app/app