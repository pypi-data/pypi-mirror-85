"""Script utility for running inner loop"""
import asyncio
import json
import logging
from concurrent import futures

from gameanalysis import regret

from egta import innerloop
from egta import schedgame
from egta.script import schedspec
from egta.script import utils


def add_parser(subparsers):
    """Create innerloop parser"""
    parser = subparsers.add_parser(
        "quiesce",
        help="""Compute equilibria using the quiesce procedure""",
        description="""Samples profiles from small restricted strategy sets,
        expanding set support by best responses to candidate restricted game
        equilibria. For games with a large number of players, a reduction
        should be specified. The result is a list where each element specifies
        an "equilibrium".""",
    )
    parser.add_argument(
        "scheduler",
        metavar="<sched-spec>",
        help="""A scheduler specification,
        see `egta spec` for more info.""",
    )
    parser.add_argument(
        "--regret-thresh",
        metavar="<reg>",
        type=float,
        default=1e-3,
        help="""Regret threshold for a mixture to be considered an equilibrium.
        (default: %(default)g)""",
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
        computationally intensive things simultaneously, i.e. nash finding.
        (default: %(default)d)""",
    )
    utils.add_reductions(parser)
    parser.run = run


async def run(args):
    """Entry point for cli"""
    sched = await schedspec.parse_scheduler(args.scheduler)
    red, red_players = utils.parse_reduction(sched, args)
    agame = schedgame.schedgame(sched, red, red_players)

    async def get_regret(eqm):
        """Gets the regret of an equilibrium"""
        game = await agame.get_deviation_game(eqm > 0)
        return float(regret.mixture_regret(game, eqm))

    async with sched:
        with futures.ProcessPoolExecutor(args.procs) as executor:
            eqa = await innerloop.inner_loop(
                agame,
                regret_thresh=args.regret_thresh,
                dist_thresh=args.dist_thresh,
                restricted_game_size=args.max_restrict_size,
                num_equilibria=args.num_equilibria,
                num_backups=args.num_backups,
                devs_by_role=args.dev_by_role,
                style=args.style,
                executor=executor,
            )
        regrets = await asyncio.gather(*[get_regret(eqm) for eqm in eqa])

    logging.error(
        "quiesce finished finding %d equilibria:\n%s",
        eqa.shape[0],
        "\n".join(
            "{:d}) {} with regret {:g}".format(i, sched.mixture_to_repr(eqm), reg)
            for i, (eqm, reg) in enumerate(zip(eqa, regrets), 1)
        ),
    )

    json.dump(
        [
            {"equilibrium": sched.mixture_to_json(eqm), "regret": reg}
            for eqm, reg in zip(eqa, regrets)
        ],
        args.output,
    )
    args.output.write("\n")
