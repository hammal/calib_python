import numpy as np
import cbadc
import matplotlib.pyplot as plt

plt.rcParams['agg.path.chunksize'] = 10000

psd_size = 1 << 12
dpi = 1200


def psd_evaluate(u_hat: np.ndarray, fs: float, BW: float, psd_size: int = 1 << 14):
    f, psd = cbadc.utilities.compute_power_spectral_density(
        u_hat,
        fs=fs,
        nperseg=psd_size,
    )
    signal_index = cbadc.utilities.find_sinusoidal(psd, 25)
    # print(signal_index)
    # psd_harm = psd
    # psd_harm[signal_index] = psd[:int(np.mean(signal_index)) - 15].mean()
    # harmonics_mask = cbadc.utilities.find_n_sinusoidals(psd_harm, 1, 25)
    noise_index = np.ones(psd.size, dtype=bool)
    noise_index[signal_index] = False
    noise_index[f < (BW * 1e-2)] = False
    noise_index[f > BW] = False
    # print(harmonics_mask)
    fom = cbadc.utilities.snr_spectrum_computation_extended(
        psd,
        signal_index,
        noise_index,
        # harmonics_mask,
        fs=fs,
    )
    est_SNR = cbadc.fom.snr_to_dB(fom["snr"])
    est_ENOB = cbadc.fom.snr_to_enob(est_SNR)
    return {
        "u_hat": u_hat,
        "psd": psd,
        "f": f,
        "est_SNR": est_SNR,
        "est_ENOB": est_ENOB,
        "t": np.arange(u_hat.size) / fs,
    }


def plot_psd(u_hat: np.ndarray, figure_path: str, BW: float, linear: bool=False):
    # u_hat = np.load(data_path)
    res = psd_evaluate(u_hat, 1.0, BW, psd_size)
    f_psd, ax_psd = plt.subplots(1, 1, sharex=True)
    if linear:
        ax_psd.plot(
            res["f"],
            10 * np.log10(res["psd"]),
            label=f"SNR: {res['est_SNR']:.2f} dB",
        )
    else:
        ax_psd.semilogx(
            res["f"],
            10 * np.log10(res["psd"]),
            label=f"SNR: {res['est_SNR']:.2f} dB",
        )
    ax_psd.legend()
    ax_psd.set_title("power spectral density (PSD)")
    ax_psd.set_xlabel("frequency")
    ax_psd.set_ylabel("dB")
    ax_psd.grid(True)
    f_psd.savefig(
        figure_path,
        dpi=dpi,
    )
    plt.close(f_psd)


def plot_impulse_response(h: np.ndarray, figure_path: str):
    # h = np.load(filter_path)
    f_h, ax_h = plt.subplots(2, 1, sharex=True)
    # L = h.shape[0]
    # K = h.shape[2]
    M = h.shape[1]
    for m in range(M):
        h_version = h[0, m, :]
        ax_h[0].plot(
            np.arange(h_version.size) - h_version.size // 2,
            h_version,
            label="$h_{" + f"{m}" + "}$",
        )
        ax_h[1].semilogy(
            np.arange(h_version.size) - h_version.size // 2,
            np.abs(h_version),
            label="$h_{" + f"{m}" + "}$",
        )

    ax_h[0].legend()
    ax_h[0].set_title("impulse responses")
    ax_h[1].set_xlabel("filter taps")
    ax_h[0].set_ylabel("$h[.]$")
    ax_h[1].set_ylabel("$|h[.]|$")
    ax_h[0].grid(True)
    ax_h[1].grid(True)
    f_h.savefig(
        figure_path,
        dpi=dpi,
    )
    plt.close(f_h)


def bode_plot(h: np.ndarray, figure_path: str, linear: bool=False):
    f_h, ax_h = plt.subplots(2, 1, sharex=True)
    M = h.shape[1]
    for m in range(M):
        h_version = h[0, m, :]

        h_freq = np.fft.rfft(h_version)
        freq = np.fft.rfftfreq(h_version.size)

        if linear:
            ax_h[1].plot(
                freq,
                np.angle(h_freq),
                label="$h_{" + f"{m}" + "}$",
            )
            ax_h[0].plot(
                freq,
                np.abs(h_freq),
                label="$h_{" + f"{m}" + "}$",
            )
        else:
            ax_h[1].semilogx(
                freq,
                np.angle(h_freq),
                label="$h_{" + f"{m}" + "}$",
            )
            ax_h[0].semilogx(
                freq,
                20 * np.log10(np.abs(h_freq)),
                label="$h_{" + f"{m}" + "}$",
            )

    ax_h[0].legend()
    ax_h[0].set_title("Bode diagram")
    ax_h[1].set_xlabel("frequency [Hz]")
    ax_h[1].set_ylabel("$ \\angle h[.]$ rad")
    ax_h[0].set_ylabel("$|h[.]|$ dB")
    ax_h[0].grid(True)
    ax_h[1].grid(True)
    f_h.savefig(
        figure_path,
        dpi=dpi,
    )
    plt.close(f_h)

def plot_time_domain(y: np.ndarray, figure_path: str):
    # y = np.load(data_path)
    x = np.arange(y.size)
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(x, y)
    ax[0].set_title("time evolution")
    ax[1].semilogy(x, np.abs(y))
    ax[1].set_xlabel("time index")
    ax[0].set_ylabel("$\hat{u}[.]$")
    ax[1].set_ylabel("$|\hat{u}[.]|$")
    fig.savefig(figure_path, dpi=dpi)
    plt.close(fig)
