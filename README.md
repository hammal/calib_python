# Calib Python
A command-line tool for creating and visualizing data related to the [calest]().

## Useful Shorthand commands
A summary of some useful shorthand commands

### The calib_filter tool

- Create a new estimator filter
    ```bash
    calib_filter create -bw 0.1 -fn 1.0 -m 8 -k 512 -k0s 0.1 filter_path.npy
    ```
    where 
    - -bw (--bandwidth) is the bandwidth of the reference filter
    - - fn (--nyquist) is the Nyquist frequency of the resulting samples, defaults to 1.0
    - -m is the number of control signals
    - -k is the number of filter taps
    - -k0s is the scale of kappa_0 relative to kappa_1, defaults to 0.1

- Check the dimensions of estimator filter
    ```bash
    calib_filter check filter_path.npy
    ```

- Plot the Bode-plot and impulse response of the estimator filter
    ```bash
    calib_filter plot filter_path.npy
    ```

### The calib_visualize tool

```bash
calib_visualize -p output_path -bw 0.1 data.npy
```
where
- -p (--path) is the path for the output folder
- -bw (--bandwidth) is used by the SNR detection algorithm
