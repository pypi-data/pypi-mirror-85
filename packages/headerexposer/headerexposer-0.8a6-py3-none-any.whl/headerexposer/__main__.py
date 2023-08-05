#!/usr/bin/env python3

"""CLI to the HeaderExposer module."""

import argparse
import shutil
from importlib import resources

import requests
import urllib3  # type: ignore

import headerexposer as he  # type: ignore

BANNER = "".join(
    [
        "\n \033[1;94m┌───────────────────────────────\033[37m───────────────",
        "─\033[90m─────┐\n \033[94m│░█░█░█▀\033[34m▀░█▀█░█▀▄░█▀▀░█▀\033[37m▄░",
        "█▀▀░█░█░█▀█░█▀\033[90m█░█▀▀░█▀▀░█▀▄│\n \033[34m│░█▀█░█▀▀░█▀█░█░\033[",
        "37m█░█▀▀░█▀▄░█▀▀░▄▀\033[90m▄░█▀▀░█░█░▀▀█░█▀\033[94m▀░█▀▄│\n \033[34m",
        "│░▀░▀░▀▀\033[37m▀░▀░▀░▀▀░░▀▀▀░▀░\033[90m▀░▀▀▀░▀░▀░▀░░░▀▀\033[94m▀░▀▀",
        "▀░▀▀▀░▀░▀│\n \033[37m└───────────────\033[90m────────────────\033[94",
        "m────────────────\033[34m─────┘\033[0m\n",
    ]
)


def analyse(args, baseline):
    request_arguments = {
        "method": args.method,
        "url": args.url,
        "params": he.parse_request_parameters(args.params),
        "data": None,
        "headers": he.parse_request_headers(args.headers),
        "cookies": he.parse_request_cookies(args.cookies),
        "auth": None,
        "timeout": args.timeout,
        "allow_redirects": not args.disallow_redirects,
        "proxies": {"http": args.proxy, "https": args.proxy},
        "verify": args.verify,
        "cert": args.cert,
    }

    if args.data is not None:
        request_arguments["data"] = args.data.encode()

    elif args.file is not None:
        with open(args.file, "rb") as data_file:
            request_arguments["data"] = data_file.read()

    if args.user_agent is not None:
        request_arguments["headers"]["User-Agent"] = args.user_agent

    if args.username is not None and args.password is not None:
        request_arguments["auth"] = (args.username, args.password)

    if not args.short:
        he.print_special("[blue]Request parameters:[normal]")
        print(he.tabulate_dict(request_arguments, args.max_width))

    if not args.verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.request(**request_arguments)

    if not args.short:
        he.print_special("\n[blue]Response:[normal]")

        print(
            he.tabulate_dict(
                {
                    "Length": len(response.content),
                    "Status Code": response.status_code,
                    "Reason": response.reason,
                },
                args.max_width,
            )
        )

    if not args.short:
        he.print_special("\n[blue]Response headers:[normal]")
        print(he.tabulate_dict(response.headers, args.max_width))

    findings = he.analyse_headers(response.headers, baseline, args.short)

    he.print_special("\n[blue]Headers analysis:[normal]")
    print(he.tabulate_findings(findings, args.max_width))


def baseline_demo(args, baseline):
    del args

    he.baseline_demo(baseline)


def show_baseline(args, baseline):
    print("WIP! This function is not currently implemented. Stay tuned!")


def main():
    """Only called when the module is called directly as a script."""
    parser = argparse.ArgumentParser(
        prog="headerexposer",
        description=f"{BANNER}\nAnalyse the security of your website's"
        " headers!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=""
        "Authors:\n"
        "  * Frédéric Proux, senior pentester at Beijaflore\n"
        "  * Alexandre Janvrin, pentester at Beijaflore\n"
        "    (https://www.beijaflore.com/en/)\n\n"
        "License: AGPLv3+\n\n"
        'This software is provided "as is", without '
        "any warranty of any kind, express or implied.\n"
        "For more information, please consult "
        "https://github.com/LivinParadoX/headerexposer.",
    )

    subparsers = parser.add_subparsers(
        title="commands",
        description="Use [command] -h for additional help.",
        dest="command",
    )

    analysis_parser = subparsers.add_parser(
        "analyse", help="Analyse a given url's headers."
    )
    analysis_parser.set_defaults(func=analyse)

    demo = subparsers.add_parser(
        "demo",
        help="Show a demonstration of what would be printed for sample"
        " headers with the selected baseline.json.",
    )
    demo.set_defaults(func=baseline_demo)

    show = subparsers.add_parser(
        "show", help="Show the selected baseline without doing any analysis."
    )
    show.set_defaults(func=show_baseline)

    with resources.path("headerexposer", "baseline.json") as baseline_path:
        parser.add_argument(
            "-b",
            "--baseline-path",
            help="Path to the baseline.json file for the header analysis"
            f" (default: {baseline_path}).",
            default=baseline_path,
        )

    output_options = parser.add_argument_group("output options")

    output_options.add_argument(
        "-s",
        "--short",
        action="store_true",
        help="Shorten the output. Do not print the request parameters,"
        " do not print the response details,"
        " do not print headers' descriptions, do not print references.",
    )

    output_options.add_argument(
        "--no-explanation-colors",
        action="store_true",
        help="Suppress colors in explanations, except in reference links.",
    )

    output_options.add_argument(
        "-w",
        "--max-width",
        type=int,
        help="The maximum width of the output. Defaults to the screen"
        f" width ({shutil.get_terminal_size().columns} columns)",
        default=shutil.get_terminal_size().columns,
    )

    request_options = analysis_parser.add_argument_group("request options")

    request_options.add_argument(
        "-m",
        "--method",
        help='HTTP method to use for the request. Default: "GET"',
        choices=["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"],
        default="GET",
    )

    request_options.add_argument(
        "--params",
        help="Add multiple, ampersand-separated parameters to the request",
    )

    group = request_options.add_mutually_exclusive_group()

    group.add_argument(
        "-d",
        "--data",
        help="Data to append to the request." " Mutually exclusive with --file"
    )

    group.add_argument(
        "-f",
        "--file",
        help="Path to a file to append to the request."
        " Mutually exclusive with --data",
    )

    request_options.add_argument(
        "-H",
        "--headers",
        help="Add multiple, newline-separated HTTP headers to the request",
    )

    request_options.add_argument(
        "-C",
        "--cookies",
        help="Add multiple, semicolon-separated cookies to the request",
    )

    request_options.add_argument(
        "-U",
        "--username",
        help="username to use in Basic/Digest/Custom HTTP Authentication",
    )

    request_options.add_argument(
        "-P",
        "--password",
        help="password to use in Basic/Digest/Custom HTTP Authentication",
    )

    request_options.add_argument(
        "-t",
        "--timeout",
        type=float,
        help="How many seconds to wait for the server to send data"
        " before giving up, as float",
    )

    request_options.add_argument(
        "-r",
        "--disallow-redirects",
        action="store_true",
        help="Disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection."
        " Defaults to enabled redirection",
    )

    request_options.add_argument(
        "-p",
        "--proxy",
        help="Proxy to use for the request")

    request_options.add_argument(
        "-k",
        "--verify",
        action="store_true",
        help="Verify SSL certificates. Defaults to an insecure behavior",
    )

    request_options.add_argument(
        "-c",
        "--cert",
        help="Optional path to the SSL client .pem certificate"
        " for client authentication",
    )

    request_options.add_argument(
        "-a",
        "--user-agent",
        help="User Agent to use."
        " Defaults to a recent Google Chrome user agent",
        default="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1"
        " (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
    )

    analysis_output_options = analysis_parser.add_argument_group(
        "output options"
    )

    analysis_output_options.add_argument(
        "-s",
        "--short",
        action="store_true",
        help="Shorten the output. Do not print the request parameters,"
        " do not print the response details,"
        " do not print headers' descriptions, do not print references.",
    )

    analysis_parser.add_argument("url", help="The url to test")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        exit()

    baseline = he.load_baseline(args.baseline_path, args.no_explanation_colors)

    if not args.short:
        print(BANNER)

    args.func(args, baseline)


if __name__ == "__main__":
    main()
