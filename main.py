import argparse

import util


def network(start_url, depth):
    # print(start_url, depth)
    util.create_network(start_url, depth)

def path(start_url, end_url):
    # print(start_url, end_url)
    util.shortest_path(start_url, end_url)

if __name__ == '__main__':
    command_parser = argparse.ArgumentParser()

    subparsers = command_parser.add_subparsers(help="Choose a command (network or path)", dest='command')

    start_parser = subparsers.add_parser('network', help='network help')
    start_parser.add_argument('START_URL', metavar="START_URL", type=str, help="URL of starting website")
    start_parser.add_argument('-d', '--depth', dest="DEPTH", type=int, default=2, help="maximum depth (default: 2)")

    stop_parser = subparsers.add_parser('path', help='path help')
    stop_parser.add_argument('START_URL', metavar="START_URL", type=str, help="URL of starting website")
    stop_parser.add_argument('END_URL', metavar="END_URL", type=str, help="URL of ending website")

    args = command_parser.parse_args()

    if args.command == "network":
        network(args.START_URL, args.DEPTH)

    elif args.command == "path":
        path(args.START_URL, args.END_URL)
