"""Python script for performing egta"""
import argparse
import asyncio
import contextlib
import logging
from logging import handlers
import smtplib
import sys
import traceback

import egta
from egta.script import bootstrap
from egta.script import brute
from egta.script import innerloop
from egta.script import schedspec
from egta.script import trace


# TODO Create outerloop, a version that takes a whole game will require that
# asyncgames implement restrict.
# TODO Create a scheduler that runs jobs on flux, but without going through
# egta online, potentially using spark


def create_parser():
    """Create parser"""
    parser = argparse.ArgumentParser(
        description="""Command line egta. To run, both an equilibrium finding
        method and a profile scheduler must be specified. Each element
        processes the arguments after it, e.g. `egta -a brute -b game -c` will
        pass -a to the base parser, -b to the brute equilibrium solver, and -c
        to the game profile scheduler."""
    )

    # Standard arguments
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version="%(prog)s {}".format(egta.__version__),
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="<output-file>",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="""The file to write the output to. (default:
        stdout)""",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="""Increases the
        verbosity level for standard error.""",
    )
    parser.add_argument(
        "-e",
        "--email_verbosity",
        action="count",
        default=0,
        help="""Increases
        the verbosity level for emails.""",
    )
    parser.add_argument(
        "-r",
        "--recipient",
        metavar="<email-address>",
        action="append",
        default=[],
        help="""Specify an email address to receive email logs at.
        Can specify multiple email addresses.""",
    )
    parser.add_argument(
        "--tag",
        metavar="<tag>",
        help="""Specify an optional tag that will get
        appended to logs and appear in the email subject.""",
    )

    # All of the actual methods to run
    eq_methods = parser.add_subparsers(
        title="operations",
        dest="method",
        metavar="<operation>",
        help="""The
        operation to run on the game. Available commands are:""",
    )

    class _Wrap(str):
        """A class that allows getting the run command from sub command"""

        async def run(self, args):
            """Run the sub command"""
            return await eq_methods.choices[self].run(args)

    eq_methods.required = True
    eq_methods.type = _Wrap
    for module in [brute, bootstrap, innerloop, trace, schedspec]:
        module.add_parser(eq_methods)

    return parser


async def amain(*argv):  # pylint: disable=too-many-locals
    """Async entry point for arbitrary command line arguments"""
    # Parse args and process
    parser = create_parser()
    args = parser.parse_args(argv)

    tag = "" if args.tag is None else " " + args.tag

    stderr_handle = logging.StreamHandler(sys.stderr)
    stderr_handle.setLevel(50 - 10 * min(args.verbose, 4))
    stderr_handle.setFormatter(
        logging.Formatter("%(asctime)s {}{} %(message)s".format(args.method, tag))
    )
    log_handlers = [stderr_handle]

    # Email Logging
    if args.recipient:  # pragma: no cover
        smtp_host = "localhost"

        # We need to do this to match the from address to the local host name
        # otherwise, email logging will not work. This seems to vary somewhat
        # by machine
        with smtplib.SMTP(smtp_host) as server:
            smtp_fromaddr = "EGTA Online <egta_online@{host}>".format(
                host=server.local_hostname
            )

        email_handler = handlers.SMTPHandler(
            smtp_host,
            smtp_fromaddr,
            args.recipient,
            "EGTA Status for {}{}".format(args.method, tag),
        )
        email_handler.setLevel(50 - args.email_verbosity * 10)
        email_handler.setFormatter(logging.Formatter("%(message)s"))
        log_handlers.append(email_handler)

    logging.basicConfig(level=0, handlers=log_handlers)

    try:
        await args.method.run(args)

    except KeyboardInterrupt as ex:  # pragma: no cover
        logging.critical("execution interrupted by user")
        raise ex

    except Exception as ex:  # pragma: no cover
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.critical(
            "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        )
        raise ex


def main():  # pragma: no cover
    """Entry point for egta cli"""
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(amain(*sys.argv[1:]))
    try:
        loop.run_until_complete(task)
        loop.close()
    except KeyboardInterrupt:
        task.cancel()
        loop.run_forever()
        raise
    finally:
        with contextlib.suppress(asyncio.CancelledError, SystemExit):
            task.exception()
