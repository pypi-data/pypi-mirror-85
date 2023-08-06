"""This module allows you to call directly from command prompt using -m flag.

"""
import logging
import threading
import requests
import argparse
from knilb import agent
from knilb import parser


log = logging.getLogger(__name__)

# FOR REFERENCE
# def _agent_thread(user, passkey, cloud, step=False, fname=None):
#     a = agent.Agent(user, passkey, cloud, step, fname)
#     log.info(a)
#     try:
#         status = a.register()
#     except requests.exceptions.RequestException as e:
#         log.critical('Registration failed {}'.format(e))
#     else:
#         a.run() if status == 200 else None


def main():
    """Entry point to module.  -h for help."""

    # Process and validate user input.
    args = parser.parse_args()

    # Logging configuration.
    # fmt = '[%(levelname)s][%(threadName)s][%(funcName)s] %(message)s'
    fmt_long = '[%(levelname)s][%(funcName)s] %(message)s'
    fmt_short = '[%(levelname)s] %(message)s'
    fmt = fmt_long if args.verbose else fmt_short
    lvl = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=lvl, format=fmt)

    # Create and run the Agent
    worker = agent.Agent(args.uuid, args.passkey, args.cloud, args.step,
                    args.mock.name)
    log.info(worker)

    try:
        status = worker.register()
    except requests.exceptions.RequestException as e:
        log.critical('Registration failed {}'.format(e))
    else:
        if not args.register and status < 400:
            worker.run()

    # FOR REFERENCE
    # Run the agent in a daemon thread.
    # You can extend this to run multiple agents in parallel.
    # worker = threading.Thread(name='Agent-{}'.format(args.uuid),
    #                           target=_agent_thread,
    #                           args=(args.uuid, args.passkey, args.cloud,
    #                                 args.step, args.mock.name))
    # worker.start()


if __name__ == '__main__':
    main()
