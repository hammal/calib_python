import argparse
import os


def _parse_arguments_filter() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='calib_filter', description="create, check, and visualize DE filters"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        default=False,
        action='store_true',
    )

    action = parser.add_subparsers(
        title='action', dest='action', help='action to perform', required=True
    )

    create = action.add_parser('create', help='create a filter')
    create.add_argument(
        "-bw",
        "--bandwidth",
        help="specify nominal bandwidth",
        required=True
    )
    create.add_argument(
        "-fn",
        "--nyquist",
        help="specify the Nyquist frequency",
        default=1.0,
        # required=True
    )
    create.add_argument(
        '-m',
        help="specify the number of controls",
        required=True
    )
    create.add_argument(
        '-k',
        help="specify the number of taps per control signal",
        required=True
    )
    create.add_argument(
        '-k0s',
        '--kappa-zero-scale',
        help="specify the scale of the kappa zero weight",
        default=0.1,
    )
    create.add_argument(
        "filter",
        help="save to filter filename",
        default=os.path.join(os.getcwd(), 'filter.npy'),
    )
    

    check = action.add_parser('check', help='check a filter')
    check.add_argument(
        "filter",
        help="path to filter file",
        # required=True
    )

    plot = action.add_parser('plot', help='plot a filter')
    plot.add_argument(
        "filter",
        help="path to filter file",
        # required=True
    )
    plot.add_argument(
        "-p",
        "--path",
        help="save to path",
        default=os.getcwd(),
    )

    return parser.parse_args()


def _parse_arguments_visualize() -> argparse.Namespace:
    """
    helper function for parsing input arguments
    """
    parser = argparse.ArgumentParser(
        prog='calib_visualize', description="visualize calib data"
    )
    parser.add_argument(
        "data_path",
        help="path to simulation data",
    )
    parser.add_argument(
        "-p",
        "--path",
        help="save to path",
        default=os.getcwd(),
    )

    parser.add_argument(
        "-bw",
        "--bandwidth",
        help="specify nominal bandwidth",
        default=1.0,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        default=False,
        action='store_true',
    )

    return parser.parse_args()
