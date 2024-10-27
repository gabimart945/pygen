init:
    pip install -r requirements.txt

run:
    python pygen.py

test:
    py.test tests

.PHONY: init test
