# Deploying the Candy Price Index experiment to Heroku

This project is ready to deploy as a standalone oTree 6 app.

## Recommended setup

- Create a **separate Heroku app** for this experiment.
- Add **Heroku Postgres**.
- Set these config vars:

```text
OTREE_PRODUCTION=1
OTREE_AUTH_LEVEL=STUDY
OTREE_ADMIN_PASSWORD=<your admin password>
OTREE_SECRET_KEY=<long random secret>
```

## Important classroom note

This app uses wait pages to synchronize the class. Because wait pages release only when **all participants in the session** arrive, create the session with the **exact number of participating students**.

Do **not** create extra unused participant slots.

## Rooms

A room named `candy_class` is defined in `settings.py`.

Suggested workflow:

1. Deploy the app.
2. Log in as admin.
3. Go to **Rooms**.
4. Open `Candy Price Index Classroom Room`.
5. Create a session for `candy_price_index` with the exact number of students.
6. Share the room URL:

```text
https://YOUR-APP.herokuapp.com/room/candy_class/?welcome_page_ok=1
```

That URL lets students enter directly without seeing the oTree demo/session pages.

## Database setup

After the first Heroku deploy, run once:

```text
otree resetdb
```

This should only be done before collecting live class data.

## Local testing

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
otree devserver
```

## Updating the deployment

If you connect Heroku to GitHub, future changes can be redeployed from the `main` branch.
