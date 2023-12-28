FROM node
RUN apt-get update && \
    apt-get install -y git tree
RUN git config --global user.email "frontend_developer_agent@github.com" && \
    git config --global user.name "Frontend Developer Agent"