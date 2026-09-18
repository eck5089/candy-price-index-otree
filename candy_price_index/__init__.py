from otree.api import *

import math
import random
from collections import Counter
from statistics import mean


class C(BaseConstants):
    NAME_IN_URL = 'candy_price_index'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    BUDGET_CENTS = 30

    # Internal field names retain the original k/r/l/s codes so existing
    # sessions and database fields remain compatible. These display names are
    # the candies currently used in class.
    CANDY_KISS = 'Smarties roll'
    CANDY_REESES = 'Classic Tootsie Roll'
    CANDY_LIFESAVER = 'Fruit Life Saver'
    CANDY_SNICKERS = 'Starburst'

    # Base, then Periods 1–6.
    KISS_PRICES = (5, 5, 5, 10, 10, 5, 10)
    REESES_PRICES = (5, 10, 5, 5, 5, 10, 10)
    LIFESAVER_PRICES = (5, 5, 10, 5, 10, 10, 5)
    SNICKERS_PRICES = (0, 0, 0, 0, 0, 15, 10)

    PERIOD_NAMES = ('Base period', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6')
    PERIOD_SHORT_NAMES = ('Base', '1', '2', '3', '4', '5', '6')
    NUM_PERIODS = 7
    PERIODS_WITH_SNICKERS = (5, 6)

    CAPI_SCALE = 100
    CAPI_TOLERANCE = 0.5
    INFLATION_TOLERANCE = 0.2

    PAYOFF_PERIOD_MIN = 1
    PAYOFF_PERIOD_MAX = 6

    # True means students cannot progress beyond classmates between periods/stages.
    PACE_PURCHASE_PERIODS = True
    PACE_MAJOR_STAGES = True

    WAIT_TITLE = 'Waiting for the class'
    WAIT_BODY = 'Please keep this tab open. The next screen will appear after everyone finishes this stage.'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    representative_kiss = models.IntegerField()
    representative_reeses = models.IntegerField()
    representative_lifesaver = models.IntegerField()

    avg_kiss = models.FloatField()
    avg_reeses = models.FloatField()
    avg_lifesaver = models.FloatField()

    payoff_period = models.IntegerField()


class Player(BasePlayer):
    # Welcome/comprehension fields.
    comp_q1 = models.IntegerField(
        label='How much purchasing credit do you have in each purchase period?',
        choices=[[10, '10 cents'], [30, '30 cents'], [50, '50 cents']],
        widget=widgets.RadioSelect,
    )
    comp_q2 = models.IntegerField(
        label='How many periods will actually determine the candy or alternative reward you receive?',
        choices=[[1, 'One period'], [7, 'All seven periods']],
        widget=widgets.RadioSelect,
    )
    comp_q3 = models.BooleanField(
        label='Does spending in one period reduce the 30-cent budget available in another period?',
        choices=[[True, 'Yes'], [False, 'No']],
        widget=widgets.RadioSelect,
    )
    needs_alternative = models.BooleanField(
        label='Do you need or prefer a non-food alternative rather than candy?',
        choices=[[False, 'No'], [True, 'Yes']],
        widget=widgets.RadioSelect,
    )

    # Purchase quantities. k=Kiss, r=Reese's, l=Lifesaver, s=Snickers.
    k0 = models.IntegerField(initial=0, min=0, max=6, label='')
    r0 = models.IntegerField(initial=0, min=0, max=6, label='')
    l0 = models.IntegerField(initial=0, min=0, max=6, label='')

    k1 = models.IntegerField(initial=0, min=0, max=6, label='')
    r1 = models.IntegerField(initial=0, min=0, max=6, label='')
    l1 = models.IntegerField(initial=0, min=0, max=6, label='')

    k2 = models.IntegerField(initial=0, min=0, max=6, label='')
    r2 = models.IntegerField(initial=0, min=0, max=6, label='')
    l2 = models.IntegerField(initial=0, min=0, max=6, label='')

    k3 = models.IntegerField(initial=0, min=0, max=6, label='')
    r3 = models.IntegerField(initial=0, min=0, max=6, label='')
    l3 = models.IntegerField(initial=0, min=0, max=6, label='')

    k4 = models.IntegerField(initial=0, min=0, max=6, label='')
    r4 = models.IntegerField(initial=0, min=0, max=6, label='')
    l4 = models.IntegerField(initial=0, min=0, max=6, label='')

    k5 = models.IntegerField(initial=0, min=0, max=6, label='')
    r5 = models.IntegerField(initial=0, min=0, max=6, label='')
    l5 = models.IntegerField(initial=0, min=0, max=6, label='')
    s5 = models.IntegerField(initial=0, min=0, max=6, label='')

    k6 = models.IntegerField(initial=0, min=0, max=6, label='')
    r6 = models.IntegerField(initial=0, min=0, max=6, label='')
    l6 = models.IntegerField(initial=0, min=0, max=6, label='')
    s6 = models.IntegerField(initial=0, min=0, max=6, label='')

    # Student calculations.
    capi_0 = models.FloatField(label='')
    capi_1 = models.FloatField(label='')
    capi_2 = models.FloatField(label='')
    capi_3 = models.FloatField(label='')
    capi_4 = models.FloatField(label='')
    capi_5 = models.FloatField(label='')
    capi_6 = models.FloatField(label='')

    inf_01 = models.FloatField(min=-100, max=1000, label='')
    inf_12 = models.FloatField(min=-100, max=1000, label='')
    inf_23 = models.FloatField(min=-100, max=1000, label='')
    inf_34 = models.FloatField(min=-100, max=1000, label='')
    inf_45 = models.FloatField(min=-100, max=1000, label='')
    inf_56 = models.FloatField(min=-100, max=1000, label='')

    # Stored evaluation fields, useful in exports.
    capi_correct_0 = models.BooleanField(initial=False)
    capi_correct_1 = models.BooleanField(initial=False)
    capi_correct_2 = models.BooleanField(initial=False)
    capi_correct_3 = models.BooleanField(initial=False)
    capi_correct_4 = models.BooleanField(initial=False)
    capi_correct_5 = models.BooleanField(initial=False)
    capi_correct_6 = models.BooleanField(initial=False)

    inf_correct_01 = models.BooleanField(initial=False)
    inf_correct_12 = models.BooleanField(initial=False)
    inf_correct_23 = models.BooleanField(initial=False)
    inf_correct_34 = models.BooleanField(initial=False)
    inf_correct_45 = models.BooleanField(initial=False)
    inf_correct_56 = models.BooleanField(initial=False)

    selected_payoff_period = models.IntegerField()
    payout_kiss = models.IntegerField(initial=0)
    payout_reeses = models.IntegerField(initial=0)
    payout_lifesaver = models.IntegerField(initial=0)
    payout_snickers = models.IntegerField(initial=0)

    finished = models.BooleanField(initial=False)


# -----------------------------------------------------------------------------
# Core helpers
# -----------------------------------------------------------------------------


def get_display_name(candy_code):
    return {
        'k': C.CANDY_KISS,
        'r': C.CANDY_REESES,
        'l': C.CANDY_LIFESAVER,
        's': C.CANDY_SNICKERS,
    }[candy_code]


def get_price(period_idx, candy_code):
    return {
        'k': C.KISS_PRICES,
        'r': C.REESES_PRICES,
        'l': C.LIFESAVER_PRICES,
        's': C.SNICKERS_PRICES,
    }[candy_code][period_idx]


def get_candies_for_period(period_idx):
    candies = ['k', 'r', 'l']
    if period_idx in C.PERIODS_WITH_SNICKERS:
        candies.append('s')
    return candies


def get_period_fields(period_idx):
    return [f'{code}{period_idx}' for code in get_candies_for_period(period_idx)]


def get_bundle(player, period_idx):
    return {code: getattr(player, f'{code}{period_idx}') for code in get_candies_for_period(period_idx)}


def get_total_cost(player, period_idx):
    return sum(getattr(player, f'{code}{period_idx}') * get_price(period_idx, code)
               for code in get_candies_for_period(period_idx))


def validate_purchase(values, period_idx):
    total = 0
    for code in get_candies_for_period(period_idx):
        quantity = values.get(f'{code}{period_idx}')
        if quantity is None:
            return 'Please enter a whole-number quantity for every available candy.'
        total += quantity * get_price(period_idx, code)

    if total != C.BUDGET_CENTS:
        difference = C.BUDGET_CENTS - total
        if difference > 0:
            return f'You have {difference}¢ left. Please spend exactly {C.BUDGET_CENTS}¢ before continuing.'
        return f'You are {abs(difference)}¢ over budget. Please spend exactly {C.BUDGET_CENTS}¢ before continuing.'


def representative_basket_tuple(group):
    return (group.representative_kiss, group.representative_reeses, group.representative_lifesaver)


def basket_cost(group, period_idx):
    k, r, l = representative_basket_tuple(group)
    return (
        k * C.KISS_PRICES[period_idx]
        + r * C.REESES_PRICES[period_idx]
        + l * C.LIFESAVER_PRICES[period_idx]
    )


def compute_correct_capi(group, period_idx):
    base_cost = basket_cost(group, 0)
    return C.CAPI_SCALE * basket_cost(group, period_idx) / base_cost


def compute_correct_inflation(group, from_period, to_period):
    old_index = compute_correct_capi(group, from_period)
    new_index = compute_correct_capi(group, to_period)
    return C.CAPI_SCALE * (new_index - old_index) / old_index


def average_quantity(group, period_idx, candy_code):
    players = group.get_players()
    if candy_code not in get_candies_for_period(period_idx):
        return None
    return mean(getattr(p, f'{candy_code}{period_idx}') for p in players)


def set_representative_basket_and_payout(group):
    """Select a feasible representative basket and one common payoff period."""
    players = group.get_players()
    if not players:
        raise RuntimeError('Cannot construct a representative basket without participants.')

    avg_k = mean(p.k0 for p in players)
    avg_r = mean(p.r0 for p in players)
    avg_l = mean(p.l0 for p in players)

    group.avg_kiss = avg_k
    group.avg_reeses = avg_r
    group.avg_lifesaver = avg_l

    all_bundles = [(p.k0, p.r0, p.l0) for p in players]
    bundle_counts = Counter(all_bundles)

    def squared_distance(bundle):
        k, r, l = bundle
        return (k - avg_k) ** 2 + (r - avg_r) ** 2 + (l - avg_l) ** 2

    minimum_distance = min(squared_distance(bundle) for bundle in all_bundles)
    closest_bundles = sorted({
        bundle for bundle in all_bundles
        if math.isclose(squared_distance(bundle), minimum_distance, abs_tol=1e-9)
    })

    # Prefer the most common among tied closest bundles; final tie is lexicographic.
    selected = sorted(closest_bundles, key=lambda bundle: (-bundle_counts[bundle], bundle))[0]
    group.representative_kiss, group.representative_reeses, group.representative_lifesaver = selected

    group.payoff_period = random.randint(C.PAYOFF_PERIOD_MIN, C.PAYOFF_PERIOD_MAX)

    for player in players:
        period = group.payoff_period
        player.selected_payoff_period = period
        player.payout_kiss = getattr(player, f'k{period}')
        player.payout_reeses = getattr(player, f'r{period}')
        player.payout_lifesaver = getattr(player, f'l{period}')
        player.payout_snickers = getattr(player, f's{period}', 0)


def set_capi_correctness(player):
    for period_idx in range(C.NUM_PERIODS):
        submitted = getattr(player, f'capi_{period_idx}')
        correct = compute_correct_capi(player.group, period_idx)
        setattr(player, f'capi_correct_{period_idx}', abs(submitted - correct) <= C.CAPI_TOLERANCE)


def set_inflation_correctness(player):
    for from_period, to_period in zip(range(0, 6), range(1, 7)):
        submitted = getattr(player, f'inf_{from_period}{to_period}')
        correct = compute_correct_inflation(player.group, from_period, to_period)
        setattr(player, f'inf_correct_{from_period}{to_period}', abs(submitted - correct) <= C.INFLATION_TOLERANCE)


def purchase_page_vars(player, period_idx):
    return dict(
        period_idx=period_idx,
        period_name=C.PERIOD_NAMES[period_idx],
        progress=f'{period_idx + 1} of {C.NUM_PERIODS}',
        new_product=(period_idx == 5),
        candy_rows=[
            dict(
                code=code,
                name=get_display_name(code),
                price=get_price(period_idx, code),
                field_name=f'{code}{period_idx}',
            )
            for code in get_candies_for_period(period_idx)
        ],
    )


def purchase_results_rows(group):
    rows = []
    for period_idx in range(C.NUM_PERIODS):
        rows.append(dict(
            period=C.PERIOD_SHORT_NAMES[period_idx],
            kiss=average_quantity(group, period_idx, 'k'),
            reeses=average_quantity(group, period_idx, 'r'),
            lifesaver=average_quantity(group, period_idx, 'l'),
            snickers=average_quantity(group, period_idx, 's'),
        ))
    return rows


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------


class Welcome(Page):
    form_model = 'player'
    form_fields = ['comp_q1', 'comp_q2', 'comp_q3', 'needs_alternative']

    @staticmethod
    def error_message(player, values):
        errors = []
        if values['comp_q1'] != C.BUDGET_CENTS:
            errors.append(f'You have {C.BUDGET_CENTS} cents of purchasing credit in every period.')
        if values['comp_q2'] != 1:
            errors.append('Only one randomly selected period determines what you receive.')
        if values['comp_q3'] is not False:
            errors.append('Every period has a fresh 30-cent budget; one period does not reduce another.')
        if errors:
            return 'Please review the instructions: ' + ' '.join(errors)


class PurchaseBase(Page):
    form_model = 'player'
    form_fields = get_period_fields(0)
    template_name = 'candy_price_index/Purchase.html'
    vars_for_template = staticmethod(lambda player: purchase_page_vars(player, 0))
    error_message = staticmethod(lambda player, values: validate_purchase(values, 0))


class WaitAfterBase(WaitPage):
    title_text = C.WAIT_TITLE
    body_text = C.WAIT_BODY
    is_displayed = staticmethod(lambda player: C.PACE_PURCHASE_PERIODS)


class Purchase1(Page):
    form_model = 'player'
    form_fields = get_period_fields(1)
    template_name = 'candy_price_index/Purchase.html'
    vars_for_template = staticmethod(lambda player: purchase_page_vars(player, 1))
    error_message = staticmethod(lambda player, values: validate_purchase(values, 1))


class WaitAfter1(WaitPage):
    title_text = C.WAIT_TITLE
    body_text = C.WAIT_BODY
    is_displayed = staticmethod(lambda player: C.PACE_PURCHASE_PERIODS)


class Purchase2(Page):
    form_model = 'player'
    form_fields = get_period_fields(2)
    template_name = 'candy_price_index/Purchase.html'
    vars_for_template = staticmethod(lambda player: purchase_page_vars(player, 2))
    error_message = staticmethod(lambda player, values: validate_purchase(values, 2))


class WaitAfter2(WaitPage):
    title_text = C.WAIT_TITLE
    body_text = C.WAIT_BODY
    is_displayed = staticmethod(lambda player: C.PACE_PURCHASE_PERIODS)


class Purchase3(Page):
    form_model = 'player'
    form_fields = get_period_fields(3)
    template_name = 'candy_price_index/Purchase.html'
    vars_for_template = staticmethod(lambda player: purchase_page_vars(player, 3))
    error_message = staticmethod(lambda player, values: validate_purchase(values, 3))


class WaitAfter3(WaitPage):
    title_text = C.WAIT_TITLE
    body_text = C.WAIT_BODY
    is_displayed = staticmethod(lambda player: C.PACE_PURCHASE_PERIODS)


class Purchase4(Page):
    form_model = 'player'
    form_fields = get_period_fields(4)
    template_name = 'candy_price_index/Purchase.html'
    vars_for_template = staticmethod(lambda player: purchase_page_vars(player, 4))
    error_message = staticmethod(lambda player, values: validate_purchase(values, 4))


class WaitAfter4(WaitPage):
    title_text = C.WAIT_TITLE
    body_text = C.WAIT_BODY
    is_displayed = staticmethod(lambda player: C.PACE_PURCHASE_PERIODS)


class Purchase5(Page):
    form_model = 'player'
    form_fields = get_period_fields(5)
    template_name = 'candy_price_index/Purchase.html'
    vars_for_template = staticmethod(lambda player: purchase_page_vars(player, 5))
    error_message = staticmethod(lambda player, values: validate_purchase(values, 5))


class WaitAfter5(WaitPage):
    title_text = C.WAIT_TITLE
    body_text = C.WAIT_BODY
    is_displayed = staticmethod(lambda player: C.PACE_PURCHASE_PERIODS)


class Purchase6(Page):
    form_model = 'player'
    form_fields = get_period_fields(6)
    template_name = 'candy_price_index/Purchase.html'
    vars_for_template = staticmethod(lambda player: purchase_page_vars(player, 6))
    error_message = staticmethod(lambda player, values: validate_purchase(values, 6))


class BasketWaitPage(WaitPage):
    title_text = 'Building the class basket'
    body_text = 'Please wait while the class finishes purchasing. The app will then construct one representative base-period basket.'
    after_all_players_arrive = set_representative_basket_and_payout


class RepresentativeBasket(Page):
    @staticmethod
    def vars_for_template(player):
        group = player.group
        return dict(
            base_cost=basket_cost(group, 0),
            representative_rows=[
                dict(name=C.CANDY_KISS, average=group.avg_kiss, quantity=group.representative_kiss),
                dict(name=C.CANDY_REESES, average=group.avg_reeses, quantity=group.representative_reeses),
                dict(name=C.CANDY_LIFESAVER, average=group.avg_lifesaver, quantity=group.representative_lifesaver),
            ],
        )


class ReadyForCaPIWait(WaitPage):
    title_text = 'Ready to calculate the index'
    body_text = 'Please wait until everyone has reviewed the representative basket.'
    is_displayed = staticmethod(lambda player: C.PACE_MAJOR_STAGES)


class CalculateCaPI(Page):
    form_model = 'player'
    form_fields = [f'capi_{idx}' for idx in range(C.NUM_PERIODS)]

    @staticmethod
    def vars_for_template(player):
        group = player.group
        return dict(
            basket_rows=[
                dict(name=C.CANDY_KISS, quantity=group.representative_kiss),
                dict(name=C.CANDY_REESES, quantity=group.representative_reeses),
                dict(name=C.CANDY_LIFESAVER, quantity=group.representative_lifesaver),
            ],
            base_cost=basket_cost(group, 0),
            price_rows=[
                dict(
                    period=C.PERIOD_SHORT_NAMES[idx],
                    kiss=C.KISS_PRICES[idx],
                    reeses=C.REESES_PRICES[idx],
                    lifesaver=C.LIFESAVER_PRICES[idx],
                    field_name=f'capi_{idx}',
                )
                for idx in range(C.NUM_PERIODS)
            ],
        )

    before_next_page = staticmethod(lambda player, timeout_happened: set_capi_correctness(player))


class CaPIResults(Page):
    @staticmethod
    def vars_for_template(player):
        rows = []
        for idx in range(C.NUM_PERIODS):
            rows.append(dict(
                period=C.PERIOD_SHORT_NAMES[idx],
                basket_cost=basket_cost(player.group, idx),
                submitted=getattr(player, f'capi_{idx}'),
                correct=compute_correct_capi(player.group, idx),
                is_correct=getattr(player, f'capi_correct_{idx}'),
            ))
        return dict(rows=rows, all_correct=all(row['is_correct'] for row in rows))


class ReadyForInflationWait(WaitPage):
    title_text = 'Ready to calculate inflation'
    body_text = 'Please wait until everyone has reviewed the Candy Price Index results.'
    is_displayed = staticmethod(lambda player: C.PACE_MAJOR_STAGES)


class CalculateInflation(Page):
    form_model = 'player'
    form_fields = [f'inf_{a}{b}' for a, b in zip(range(0, 6), range(1, 7))]

    @staticmethod
    def vars_for_template(player):
        return dict(rows=[
            dict(
                transition=f'{C.PERIOD_SHORT_NAMES[a]} → {C.PERIOD_SHORT_NAMES[b]}',
                old_capi=compute_correct_capi(player.group, a),
                new_capi=compute_correct_capi(player.group, b),
                field_name=f'inf_{a}{b}',
            )
            for a, b in zip(range(0, 6), range(1, 7))
        ])

    before_next_page = staticmethod(lambda player, timeout_happened: set_inflation_correctness(player))


class InflationResults(Page):
    @staticmethod
    def vars_for_template(player):
        rows = []
        for a, b in zip(range(0, 6), range(1, 7)):
            rows.append(dict(
                transition=f'{C.PERIOD_SHORT_NAMES[a]} → {C.PERIOD_SHORT_NAMES[b]}',
                submitted=getattr(player, f'inf_{a}{b}'),
                correct=compute_correct_inflation(player.group, a, b),
                is_correct=getattr(player, f'inf_correct_{a}{b}'),
            ))
        return dict(rows=rows, all_correct=all(row['is_correct'] for row in rows))


class ReadyForPayoutWait(WaitPage):
    title_text = 'Preparing the class results'
    body_text = 'Please wait until everyone has completed the inflation calculations.'
    is_displayed = staticmethod(lambda player: C.PACE_MAJOR_STAGES)


def payout_vars(player):
    period = player.selected_payoff_period
    return dict(
        participant_number=player.id_in_group,
        period_name=C.PERIOD_NAMES[period],
        price_rows=[
            dict(name=get_display_name(code), price=get_price(period, code))
            for code in get_candies_for_period(period)
        ],
        payout_rows=[
            dict(name=C.CANDY_KISS, quantity=player.payout_kiss),
            dict(name=C.CANDY_REESES, quantity=player.payout_reeses),
            dict(name=C.CANDY_LIFESAVER, quantity=player.payout_lifesaver),
            dict(name=C.CANDY_SNICKERS, quantity=player.payout_snickers),
        ],
    )


class Payout(Page):
    vars_for_template = staticmethod(payout_vars)


class Debrief(Page):
    @staticmethod
    def vars_for_template(player):
        group = player.group
        capi_rows = [
            dict(period=C.PERIOD_SHORT_NAMES[idx], capi=compute_correct_capi(group, idx))
            for idx in range(C.NUM_PERIODS)
        ]
        inflation_rows = [
            dict(
                transition=f'{C.PERIOD_SHORT_NAMES[a]} → {C.PERIOD_SHORT_NAMES[b]}',
                inflation=compute_correct_inflation(group, a, b),
            )
            for a, b in zip(range(0, 6), range(1, 7))
        ]
        purchase_rows = purchase_results_rows(group)
        return dict(
            capi_rows=capi_rows,
            inflation_rows=inflation_rows,
            purchase_rows=purchase_rows,
            payoff_period=C.PERIOD_NAMES[group.payoff_period],
            reeses_base=average_quantity(group, 0, 'r'),
            reeses_p1=average_quantity(group, 1, 'r'),
            lifesaver_p1=average_quantity(group, 1, 'l'),
            lifesaver_p2=average_quantity(group, 2, 'l'),
            snickers_p5=average_quantity(group, 5, 's'),
            snickers_p6=average_quantity(group, 6, 's'),
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.finished = True
        player.participant.finished = True


class Final(Page):
    vars_for_template = staticmethod(payout_vars)


page_sequence = [
    Welcome,
    PurchaseBase, WaitAfterBase,
    Purchase1, WaitAfter1,
    Purchase2, WaitAfter2,
    Purchase3, WaitAfter3,
    Purchase4, WaitAfter4,
    Purchase5, WaitAfter5,
    Purchase6,
    BasketWaitPage,
    RepresentativeBasket,
    ReadyForCaPIWait,
    CalculateCaPI,
    CaPIResults,
    ReadyForInflationWait,
    CalculateInflation,
    InflationResults,
    ReadyForPayoutWait,
    Payout,
    Debrief,
    Final,
]


# -----------------------------------------------------------------------------
# Instructor report and custom export
# -----------------------------------------------------------------------------


def vars_for_admin_report(subsession):
    groups = subsession.get_groups()
    if not groups:
        return dict(num_participants=0, basket_ready=False)

    group = groups[0]
    players = group.get_players()
    basket_ready = group.representative_kiss is not None

    bundle_distribution = Counter((p.k0, p.r0, p.l0) for p in players)
    bundle_rows = [
        dict(kiss=bundle[0], reeses=bundle[1], lifesaver=bundle[2], count=count)
        for bundle, count in sorted(bundle_distribution.items(), key=lambda item: (-item[1], item[0]))
    ]

    purchase_rows = purchase_results_rows(group)

    capi_rows = []
    inflation_rows = []
    if basket_ready:
        for idx in range(C.NUM_PERIODS):
            submitted = [getattr(p, f'capi_{idx}') for p in players if getattr(p, f'capi_{idx}') is not None]
            correct_count = sum(
                getattr(p, f'capi_correct_{idx}') for p in players if getattr(p, f'capi_{idx}') is not None
            )
            capi_rows.append(dict(
                period=C.PERIOD_SHORT_NAMES[idx],
                correct=compute_correct_capi(group, idx),
                average_answer=mean(submitted) if submitted else None,
                percent_correct=100 * correct_count / len(submitted) if submitted else None,
            ))

        for a, b in zip(range(0, 6), range(1, 7)):
            submitted = [getattr(p, f'inf_{a}{b}') for p in players if getattr(p, f'inf_{a}{b}') is not None]
            correct_count = sum(
                getattr(p, f'inf_correct_{a}{b}') for p in players if getattr(p, f'inf_{a}{b}') is not None
            )
            inflation_rows.append(dict(
                transition=f'{C.PERIOD_SHORT_NAMES[a]} → {C.PERIOD_SHORT_NAMES[b]}',
                correct=compute_correct_inflation(group, a, b),
                average_answer=mean(submitted) if submitted else None,
                percent_correct=100 * correct_count / len(submitted) if submitted else None,
            ))

    payout_rows = []
    payout_totals = dict(kiss=0, reeses=0, lifesaver=0, snickers=0)
    alternative_count = 0
    if group.payoff_period is not None:
        for p in players:
            if p.needs_alternative:
                alternative_count += 1
            else:
                payout_totals['kiss'] += p.payout_kiss
                payout_totals['reeses'] += p.payout_reeses
                payout_totals['lifesaver'] += p.payout_lifesaver
                payout_totals['snickers'] += p.payout_snickers
            payout_rows.append(dict(
                participant_number=p.id_in_group,
                participant=p.participant.label or p.participant.code,
                alternative=p.needs_alternative,
                kiss=p.payout_kiss,
                reeses=p.payout_reeses,
                lifesaver=p.payout_lifesaver,
                snickers=p.payout_snickers,
            ))

    return dict(
        num_participants=len(players),
        basket_ready=basket_ready,
        bundle_rows=bundle_rows,
        purchase_rows=purchase_rows,
        representative_basket=(
            f'{group.representative_kiss} Smarties rolls, {group.representative_reeses} Tootsie Rolls, '
            f'{group.representative_lifesaver} Fruit Life Savers'
            if basket_ready else 'Not yet calculated'
        ),
        capi_rows=capi_rows,
        inflation_rows=inflation_rows,
        payoff_period=(C.PERIOD_NAMES[group.payoff_period] if group.payoff_period is not None else 'Not yet selected'),
        payout_totals=payout_totals,
        alternative_count=alternative_count,
        payout_rows=payout_rows,
    )


def custom_export(players):
    header = [
        'session_code', 'participant_code', 'participant_label', 'needs_alternative',
    ]
    for idx in range(C.NUM_PERIODS):
        header += [f'smarties_p{idx}', f'tootsie_rolls_p{idx}', f'life_savers_p{idx}', f'starbursts_p{idx}', f'total_cost_p{idx}']
    header += [
        'representative_kiss', 'representative_reeses', 'representative_lifesaver',
        'selected_payoff_period', 'payout_smarties', 'payout_tootsie_rolls', 'payout_life_savers', 'payout_starbursts',
    ]
    for idx in range(C.NUM_PERIODS):
        header += [f'capi_submitted_{idx}', f'capi_correct_value_{idx}', f'capi_answer_correct_{idx}']
    for a, b in zip(range(0, 6), range(1, 7)):
        header += [f'inflation_submitted_{a}{b}', f'inflation_correct_value_{a}{b}', f'inflation_answer_correct_{a}{b}']
    yield header

    for p in players:
        group = p.group
        row = [p.session.code, p.participant.code, p.participant.label, p.needs_alternative]
        for idx in range(C.NUM_PERIODS):
            row += [
                getattr(p, f'k{idx}'),
                getattr(p, f'r{idx}'),
                getattr(p, f'l{idx}'),
                getattr(p, f's{idx}', 0),
                get_total_cost(p, idx),
            ]
        row += [
            group.representative_kiss,
            group.representative_reeses,
            group.representative_lifesaver,
            p.selected_payoff_period,
            p.payout_kiss,
            p.payout_reeses,
            p.payout_lifesaver,
            p.payout_snickers,
        ]
        for idx in range(C.NUM_PERIODS):
            row += [
                getattr(p, f'capi_{idx}'),
                compute_correct_capi(group, idx),
                getattr(p, f'capi_correct_{idx}'),
            ]
        for a, b in zip(range(0, 6), range(1, 7)):
            row += [
                getattr(p, f'inf_{a}{b}'),
                compute_correct_inflation(group, a, b),
                getattr(p, f'inf_correct_{a}{b}'),
            ]
        yield row
