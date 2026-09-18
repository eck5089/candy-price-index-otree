# Candy Price Index Experiment

A standalone **oTree 6** classroom experiment adapted from Denise Hazlett and Cynthia Hill (2003), “Calculating the Candy Price Index: A Classroom Inflation Experiment.”

Students purchase candy under changing prices, the class generates a representative fixed basket, and students then calculate a Candy Price Index and inflation rates using their own class data.

## Features

- 7 purchasing periods (base period plus periods 1–6)
- exact 30-cent budget validation in every period
- optional non-food alternative indicator for students with allergies or dietary restrictions
- class pacing via wait pages after each purchase period and before major stages
- representative basket constructed from the base-period class average using the nearest feasible student bundle
- common randomly selected payout period from periods 1–6
- answer checking for both CaPI and inflation calculations
- instructor report with class purchases, representative basket, correct answers, and total candy owed
- custom export for downstream analysis

## Important classroom note

This app uses synchronous wait pages. Therefore, when creating a session you should use the **exact number of participating students**. If you create extra participant slots, the class can get stuck waiting for nonexistent students.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
otree devserver
```

Then open `http://localhost:8000`.

## Deploy to Heroku

This repository includes the files needed for Heroku deployment:

- `Procfile`
- `.python-version`
- PostgreSQL driver in `requirements.txt`
- room definition in `settings.py`
- deployment instructions in `DEPLOYMENT.md`

Recommended production config vars:

```text
OTREE_PRODUCTION=1
OTREE_AUTH_LEVEL=STUDY
OTREE_ADMIN_PASSWORD=<your admin password>
OTREE_SECRET_KEY=<long random secret>
```

A reusable room named `candy_class` is defined. After deployment, create a session in that room with the exact class size and share:

```text
https://YOUR-APP.herokuapp.com/room/candy_class/?welcome_page_ok=1
```

## Automated test

```powershell
otree test candy_price_index 8
```

## Citation reminder

If you publish research using oTree, cite Chen, Schonger, and Wickens (2016), “oTree—An open-source platform for laboratory, online, and field experiments.”
