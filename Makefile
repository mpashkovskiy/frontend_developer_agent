VENV = .venv
MODEL = deepseek-coder-6.7b-instruct
QUANTIZATION = Q4_K_M
MODEL_FILE = $(MODEL).$(QUANTIZATION).gguf
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

models/$(MODEL_FILE):
	wget \
		"https://huggingface.co/TheBloke/$(MODEL)-GGUF/resolve/main/$(MODEL_FILE)?download=true" \
		-O models/$(MODEL_FILE)

.PHONY: model
model: models/$(MODEL_FILE)

.PHONY: server
server: models/$(MODEL_FILE)
	docker run \
		--rm \
		--entrypoint /app/server \
		-p $(PORT):$(PORT) \
		-v `pwd`/models:/models \
		ghcr.io/ggerganov/llama.cpp:full \
			--ctx-size 16000 \
			--host 0.0.0.0 \
			--mlock \
			--model /models/$(MODEL_FILE) \
			--port $(PORT)