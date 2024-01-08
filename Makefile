export PROJECT_NAME = frontend_developer_agent
VENV = .venv

.PHONY: clean
clean:
	rm -rf $(VENV)

Pipfile.lock: Pipfile
	pipenv lock

.PHONY: $(VENV)
$(VENV): $(VENV)/bin/activate
$(VENV)/bin/activate: Pipfile.lock setup.py
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

.PHONY: docker-image
docker-image:
	docker-compose build

models/deepseek-llm-7b-chat.Q4_K_M.gguf:
	mkdir -p models
	wget "https://huggingface.co/TheBloke/deepseek-llm-7b-chat-GGUF/resolve/main/deepseek-llm-7b-chat.Q4_K_M.gguf?download=true" \
		-O models/deepseek-llm-7b-chat.Q4_K_M.gguf