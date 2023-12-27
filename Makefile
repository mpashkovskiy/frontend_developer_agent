PROJECT_NAME = frontend_developer_agent
VENV = .venv
# MODEL_NAME = deepseek-coder-6.7b-instruct
MODEL_NAME = deepseek-llm-7b-chat
MODEL_CTX_SIZE = 16000
MODEL_QUANTIZATION = Q4_K_M
MODEL_FILE = $(MODEL_NAME).$(MODEL_QUANTIZATION).gguf
PORT = 8080

.PHONY: clean
clean:
	rm -rf $(VENV)

Pipfile.lock: Pipfile
	pipenv lock

$(VENV)/bin/activate: Pipfile.lock setup.py
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

.PHONY: $(VENV)
$(VENV): $(VENV)/bin/activate

.PHONY: docker-image
docker-image:
	docker build -t $(PROJECT_NAME):latest .

.PHONY: tests
tests: TEST ?= ""
tests:
	pipenv run pytest $(TEST)

models/$(MODEL_FILE):
	mkdir -p models
	wget \
		"https://huggingface.co/TheBloke/$(MODEL_NAME)-GGUF/resolve/main/$(MODEL_FILE)?download=true" \
		-O models/$(MODEL_FILE)

.PHONY: model
model: models/$(MODEL_FILE)

.PHONY: server
server: models/$(MODEL_FILE)
	docker run \
		--entrypoint /app/server \
		-p $(PORT):$(PORT) \
		--rm \
		-v `pwd`/models:/models \
		ghcr.io/ggerganov/llama.cpp:full \
			--ctx-size $(MODEL_CTX_SIZE) \
			--host 0.0.0.0 \
			--mlock \
			--model /models/$(MODEL_FILE) \
			--port $(PORT)