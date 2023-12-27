FROM node
RUN npm install -g @ionic/cli typescript
RUN git config --global user.email "frontend_developer_agent@github.com" && \
    git config --global user.name "Frontend Developer Agent"