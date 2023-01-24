from calib_python.parser import _parse_arguments_filter, _parse_arguments_visualize
from calib_python.figures import plot_psd, plot_time_domain, plot_impulse_response, bode_plot
from cbadc.digital_estimator import initial_filter
from scipy.signal import firwin2
import jinja2
import logging
import numpy as np
import os

# Set logging level
logger = logging.getLogger(__name__)

_env = jinja2.Environment(
    loader=jinja2.PackageLoader("calib_python", package_path="templates"),
    autoescape=jinja2.select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def _data_folder_exist(data_folder: str):
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)


def main_filter():
    args = _parse_arguments_filter()

    logger.debug(f"command line args where: {args}")

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO, format="")

    if args.action == 'check':
        filter = np.load(args.filter)
        logger.info(
            _env.get_template('info_filter.j2').render(
                {
                    'filter': filter,
                }
            )
        )
    elif args.action == 'create':
        reference_filter = initial_filter(
            [
                -firwin2(
                    int(args.k),
                    np.array([0.0, 0.99 * float(args.bandwidth), 1.01 * float(args.bandwidth), float(args.nyquist)]),
                    np.array([1.0, 1.0, 0.0, 0.0]),
                )
                * float(args.kappa_zero_scale)
            ],
            [int(args.k) for _ in range(int(args.m))],
            [0],
        )

        np.save(args.filter, reference_filter)

    elif args.action == 'plot':
        _data_folder_exist(args.path)
        filter = np.load(args.filter)
        plot_impulse_response(filter, os.path.join(args.path, 'impulse_response.png'))
        bode_plot(filter, os.path.join(args.path, 'bode_plot.png'), bool(args.linear))

    exit(0)


def main_visualize():
    """
    The main command line function
    """
    args = _parse_arguments_visualize()
    logger.debug(f"command line args where: {args}")

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO, format="")

    data = np.load(args.data_path)

    logger.info(
        _env.get_template('info_visualize.j2').render(
            {
                'data': data,
            }
        )
    )

    _data_folder_exist(args.path)

    filters = [f"{os.path.join(args.path, f)}.png" for f in ['psd', 'time']]

    plot_psd(data, filters[0], float(args.bandwidth), bool(args.linear))
    plot_time_domain(data, filters[1])

    exit(0)
