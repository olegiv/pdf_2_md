install:
	python3 -m venv venv && \
	. venv/bin/activate || venv\Scripts\activate && \
	pip install -r requirements.txt && \
	python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

run:
	. venv/bin/activate || venv\Scripts\activate && \
	python main.py

test:
	. venv/bin/activate || venv\Scripts\activate && \
	pytest
