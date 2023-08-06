"""Script utility for running equilibrium trace"""
import asyncio
import json
import logging
from concurrent import futures

from gameanalysis import regret
from gameanalysis import rsgame

from egta import canonsched
from egta import schedgame
from egta import trace
from egta.script import schedspec
from egta.script import utils


def add_parser(subparsers):
    """Create parser for tracing"""
    parser = subparsers.add_parser(
        "trace",
        help="""Compute trace of equilibria between two games""",
        description="""Computes traces of equilibria as the probability of
        mixing between two games changes. This uses quiesce as a subroutine and
        sparsely schedules profiles so that this can be done without having to
        fully sample either game. The results is a list of traces, where each
        trace is a list of the mixture probability, the equilibriium, and the
        regret. In order to allow this to work on games with singleton players,
        games are "normalized" by removing them prior to scheduling. Thus, any
        roles with only one strategy should be omitted from reductions, and
        will also be omitted from equilibria as their answer is trivial.""",
    )
    parser.add_argument(
        "sched0",
        metavar="<sched-spec-0>",
        help="""The scheduler specification
        for the game when t is 0. See `egta spec` for more info.""",
    )
    parser.add_argument(
        "sched1",
        metavar="<sched-spec-1>",
        help="""The scheduler specification
        for the game when t is 1. See `egta spec` for more info.""",
    )
    parser.add_argument(
        "--regret-thresh",
        metavar="<reg>",
        type=float,
        default=1e-3,
        help="""Regret threshold for a mixture to be considered an equilibrium.
        This can't be strictly enforced as the ODE that this solves has some
        numerical instability, and there is no way to guarantee the equilibria
        stays small.  (default: %(default)g)""",
    )
    parser.add_argument(
        "--dist-thresh",
        metavar="<norm>",
        type=float,
        default=0.1,
        help="""Norm threshold for two mixtures to be considered distinct.
        (default: %(default)g)""",
    )
    parser.add_argument(
        "--max-restrict-size",
        metavar="<support>",
        type=int,
        default=3,
        help="""Support size threshold, beyond which restricted games are not
        required to be explored.  (default: %(default)d)""",
    )
    parser.add_argument(
        "--num-equilibria",
        metavar="<num>",
        type=int,
        default=1,
        help="""Number of equilibria requested to be found. This is mainly
        useful when game contains known degenerate equilibria, but those
        strategies are still useful as deviating strategies. (default:
        %(default)d)""",
    )
    parser.add_argument(
        "--num-backups",
        metavar="<num>",
        type=int,
        default=1,
        help="""Number
        of backup restricted strategy set to pop at a time, when no equilibria
        are confirmed in initial required set.  When games get to this point
        they can quiesce slowly because this by default pops one at a time.
        Increasing this number can get games like tis to quiesce more quickly,
        but naturally, also schedules more, potentially unnecessary,
        simulations. (default: %(default)d)""",
    )
    parser.add_argument(
        "--dev-by-role",
        action="store_true",
        help="""Explore deviations in
        role order instead of all at once. By default, when checking for
        beneficial deviations, all role deviations are scheduled at the same
        time. Setting this will check one role at a time. If a beneficial
        deviation is found, then that restricted strategy set is scheduled
        without exploring deviations from the other roles.""",
    )
    parser.add_argument(
        "--style",
        default="best",
        choices=["fast", "more", "best", "one"],
        help="""Style of equilibrium finding to use. `fast` is the fastests but
        least thorough, `one` will guarantee an equilibrium is found in
        potentially exponential time.""",
    )
    parser.add_argument(
        "--procs",
        type=int,
        default=2,
        metavar="<num-procs>",
        help="""Number
        of process to use. This will speed up computation if doing
        computationally intensive things simultaneously, i.e. nash finding or
        ode solving. (default: %(default)d)""",
    )
    utils.add_reductions(parser)
    parser.run = run


async def run(args):  # pylint: disable=too-many-locals
    """Command line entry point for tracing"""
    sched0 = CanonWrapper(await schedspec.parse_scheduler(args.sched0))
    sched1 = CanonWrapper(await schedspec.parse_scheduler(args.sched1))
    red, red_players = utils.parse_reduction(sched0, args)
    agame0 = schedgame.schedgame(sched0, red, red_players)
    agame1 = schedgame.schedgame(sched1, red, red_players)

    async def get_point(prob, eqm):
        """Get the point in a trace for an equilibrium"""
        supp = eqm > 0
        game0 = await agame0.get_deviation_game(supp)
        game1 = await agame1.get_deviation_game(supp)
        reg = regret.mixture_regret(rsgame.mix(game0, game1, prob), eqm)
        return {
            "t": float(prob),
            "equilibrium": sched0.mixture_to_json(eqm),
            "regret": float(reg),
        }

    async def get_trace(probs, peqa):
        """Get the trace for probabilities and equilibria"""
        return await asyncio.gather(*[get_point(p, eqm) for p, eqm in zip(probs, peqa)])

    async with sched0, sched1:
        with futures.ProcessPoolExecutor(args.procs) as executor:
            traces = await trace.trace_all_equilibria(
                agame0,
                agame1,
                regret_thresh=args.regret_thresh,
                dist_thresh=args.dist_thresh,
                restricted_game_size=args.max_restrict_size,
                num_equilibria=args.num_equilibria,
                num_backups=args.num_backups,
                devs_by_role=args.dev_by_role,
                style=args.style,
                executor=executor,
            )
        jtraces = await asyncio.gather(*[get_trace(ts, teqa) for ts, teqa in traces])

    max_reg = 0.0
    spans = [[-1, -1]]
    for jtrace in jtraces:
        max_reg = max(max_reg, max(p["regret"] for p in jtrace))
        span = spans[-1]
        start, *_, end = jtrace
        if start["t"] <= span[1]:
            span[1] = max(span[1], end["t"])
        else:
            spans.append([start["t"], end["t"]])

    logging.error(
        "tracing finished finding %d traces covering %s, with maximum regret " "%g",
        len(jtraces),
        " U ".join("[{:g}, {:g}]".format(s, e) for s, e in spans[1:]),
        max_reg,
    )

    json.dump(jtraces, args.output)
    args.output.write("\n")


class CanonWrapper(canonsched._CanonScheduler):  # pylint: disable=protected-access
    """Async context manager for canon scheduler"""

    async def __aenter__(self):
        await self._sched.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._sched.__aexit__(*args)
