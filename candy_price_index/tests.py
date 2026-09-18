from otree.api import Bot, SubmissionMustFail
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome, dict(comp_q1=30, comp_q2=1, comp_q3=False, needs_alternative=False)

        # Base: invalid first, then an unequal basket that generates deflation.
        yield SubmissionMustFail(PurchaseBase, dict(k0=1, r0=1, l0=1))
        yield PurchaseBase, dict(k0=2, r0=3, l0=1)

        yield Purchase1, dict(k1=6, r1=0, l1=0)
        yield Purchase2, dict(k2=0, r2=6, l2=0)
        yield Purchase3, dict(k3=0, r3=6, l3=0)
        yield Purchase4, dict(k4=3, r4=0, l4=0)
        yield Purchase5, dict(k5=6, r5=0, l5=0, s5=0)
        yield Purchase6, dict(k6=0, r6=0, l6=6, s6=0)

        yield RepresentativeBasket

        capi_answers = {
            f'capi_{idx}': compute_correct_capi(self.player.group, idx)
            for idx in range(C.NUM_PERIODS)
        }
        yield CalculateCaPI, capi_answers
        yield CaPIResults

        inflation_answers = {
            f'inf_{a}{b}': compute_correct_inflation(self.player.group, a, b)
            for a, b in zip(range(0, 6), range(1, 7))
        }
        yield CalculateInflation, inflation_answers
        yield InflationResults
        yield Payout
        yield Debrief
        yield Final
