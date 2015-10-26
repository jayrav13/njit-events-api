### Events at NJIT's RESTful API

This repository contains the RESTful API that serves all NJIT's upcoming events, along with available details. The repository also contains `scrape.py`, the file that parses the .ics file with all of the upcoming events. The events are updated every Monday, so scrape.py should be scheduled to run accordingly (approx. 8:00AM EST).

##### Install SQLite Database
Execute:

```bash
sqlite3 events.db
sqlite> .databases
sqlite> .quit
```

##### Install Dependencies 
Execute:

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

##### Migrate Databases
Execute:

```bash
python model.py events init
python model.py events migrate
python model.py events upgrade 
```

##### Scrape Data
Execute:

```bash
python scrape.py
```

##### RESTful API
Execute

```bash
python app.py
```

Visit `localhost:5000/api/v0.2/events` to view the JSON output.

##### License
MIT License



By Jay Ravaliya
