"""calculate regrets and deviations gains"""
import argparse
import json
import sys

import numpy as np

from gameanalysis import gamereader
from gameanalysis import regret
from gameanalysis import scriptutils
from gameanalysis import utils


def is_pure_profile(game, prof):
    """Returns true of the profile is pure"""
    # For an asymmetric game, this will always return false, but then it
    # shouldn't be an issue, because pure strategy regret will be more
    # informative.
    pure = np.any(np.add.reduceat(prof, game.role_starts) > 1.5)
    utils.check(
        game.is_profile(np.asarray(prof, int)) if pure else game.is_mixture(prof),
        "profile must be valid",
    )
    return pure


def calc_reg(game, prof):
    """the regret of the profile"""
    if is_pure_profile(game, prof):  # pylint: disable=no-else-return
        return regret.pure_strategy_regret(game, np.asarray(prof, int)).item()
    else:
        return regret.mixture_regret(game, prof).item()


def calc_gains(game, prof):
    """the gains from deviating from profile"""
    if is_pure_profile(game, prof):  # pylint: disable=no-else-return
        gains = regret.pure_strategy_deviation_gains(game, prof)
        return game.devpay_to_json(gains)
    else:
        gains = regret.mixture_deviation_gains(game, prof)
        return game.payoff_to_json(gains)


TYPE = {
    "regret": calc_reg,
    "gains": calc_gains,
    "ne": calc_gains,
}
TYPE_HELP = " ".join("`{}` - {}.".format(s, f.__doc__) for s, f in TYPE.items())


def add_parser(subparsers):
    """Add parser for regret cli"""
    parser = subparsers.add_parser(
        "regret",
        aliases=["reg"],
        help="""Compute regret""",
        description="""Compute regret in input game of specified profiles.""",
    )
    parser.add_argument(
        "--input",
        "-i",
        metavar="<input-file>",
        default=sys.stdin,
        type=argparse.FileType("r"),
        help="""Input file for script.  (default:
        stdin)""",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="<output-file>",
        default=sys.stdout,
        type=argparse.FileType("w"),
        help="""Output file for script. (default:
        stdout)""",
    )
    parser.add_argument(
        "profiles",
        metavar="<profile>",
        nargs="+",
        help="""File with profiles
        or raw strings of profiles from the input. The input can be a json list
        of profiles or an individual profile.""",
    )
    parser.add_argument(
        "-t",
        "--type",
        default="regret",
        choices=TYPE,
        help="""What to return:
        {} (default: %(default)s)""".format(
            TYPE_HELP
        ),
    )
    return parser


def main(args):
    """Entry point for regret cli"""
    game = gamereader.load(args.input)
    prof_func = TYPE[args.type]
    regrets = [
        prof_func(game, game.mixture_from_json(prof, verify=False))
        for prof in scriptutils.load_profiles(args.profiles)
    ]
    json.dump(regrets, args.output)
    args.output.write("\n")
