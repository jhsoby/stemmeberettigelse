Voting eligibility tool living at http://tools.wmflabs.org/stemmeberettigelse

Setup:

    python3 -m venv www/python/venv
    source www/python/venv/bin/activate
    pip install -r requirements.txt
    webservice --backend=kubernetes python start

