from os import environ

SESSION_CONFIGS = [
    dict(
        name='candy_price_index',
        display_name='Candy Price Index Experiment',
        app_sequence=['candy_price_index'],
        num_demo_participants=8,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.00,
    participation_fee=0.00,
    doc='Classroom adaptation of Hazlett and Hill (2003), Calculating the Candy Price Index.',
)

PARTICIPANT_FIELDS = ['finished']
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'admin')

DEMO_PAGE_INTRO_HTML = """
<p>A classroom experiment in which students purchase candy under changing prices,
build a fixed basket, and calculate a Candy Price Index and inflation rates.</p>
"""

SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'replace-this-with-a-random-secret-key-before-deploying')
INSTALLED_APPS = ['otree']

ROOMS = [
    dict(
        name='candy_class',
        display_name='Candy Price Index Classroom Room',
    ),
]
