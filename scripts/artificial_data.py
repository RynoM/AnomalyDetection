import numpy as np
import pandas as pd
from random import sample

def create_sin(amplitude, level, frequency, length):
    '''
    Create sinusiod waves for the seasonality.
    :param amplitude: amplitude of the sinewave
    :param level: base level of the sinewave
    :param frequency: periodicity of the sinewave
    :param length: number of periods to generate
    :return: np.array of generated sinewave
    '''
    X = np.linspace(0, length*np.pi*2, length*frequency)
    return np.sin(X)*amplitude+level


def add_nonneg(A, B):
    Y = list(np.zeros(len(A)))
    for ix, num in enumerate(A):
        if (A[ix] > 0): #only multiply the amplitude if data is non-neg, to keep bottom the same
            Y[ix] = A[ix] * np.maximum(B[ix],0) #np.max should not be neccessairy, because B[ix] > 0
        else:
            Y[ix] = A[ix]
    return Y


def autocorr_noise(n_samples, corr, mu=0, sigma=1, n_vars=1):
    assert 0 < corr < 1, "Auto-correlation must be between 0 and 1"

    # Find out the offset `c` and the std of the white noise `sigma_e`
    # that produce a signal with the desired mean and variance.
    # See https://en.wikipedia.org/wiki/Autoregressive_model#Example:_An_AR.281.29_process
    c = mu * (1 - corr)
    sigma_e = np.sqrt((sigma ** 2) * (1 - corr ** 2))

    # Sample the auto-regressive process.
    signal = {}
    for i in range(n_vars):
        signal[i] = [c + np.random.normal(0, sigma_e)]

    for _ in range(1, n_samples):
        signal[0].append(c + corr * signal[0][-1] + np.random.normal(0, sigma_e))
        for i in range(1, n_vars):
            signal[i].append(c + np.sqrt(corr) * ((signal[0][-1]+signal[i][-1])/2) + (1/(1+(1-corr))*np.random.normal(0, sigma_e)))

    return signal



def add_noise_and_anomalies(input_data, percentage, std, mean, NC, AM, corr, n_vars):

    noisy = pd.DataFrame(columns=range(n_vars), index=range(len(input_data)))
    anoms_df = pd.DataFrame(columns=range(n_vars), index=range(int(len(input_data)*percentage)))
    gen = autocorr_noise(len(input_data)-int(len(input_data)*percentage), corr, mean, std, n_vars)
    # select a subset of points to become anomalies
    for var in range(n_vars):
        anomaly_ix = sample(range(0, len(input_data)), int(len(input_data) * percentage))
        # transform selected points to become anomalous
        anomalies = []
        for a in anomaly_ix:
            val = np.random.normal(mean, std * AM, 1)
            while abs(val) < std * AM or abs(val) > std * AM *1.2:
                val = np.random.normal(mean, std * AM, 1)
            anomalies.append(input_data[a] + val)

        # add noise to the rest of the data
        non_anom = [input_data[ix] for ix in range(0, len(input_data)) if ix not in anomaly_ix]
        noisy_s = non_anom + np.array(
            [x if abs(x) < std * NC else std * NC for x in gen[var]])

        # insert anomalies back into original
        for ix, x in enumerate(sorted(anomaly_ix)):
            noisy_s = np.insert(noisy_s, x, anomalies[ix])

        noisy[var] = noisy_s
        anoms_df[var] = sorted(anomaly_ix)
    return noisy, anoms_df

def create_data(amp1=1, amp2=0.5, lvl1=0, lvl2=1, freq1=24, freq2=168, len1=28, len2=4,
                std=0.15, mean=0.1, stdcut=1.68, AM=1.68, anom_pct=0.01, corr=0.85, n_vars=1):
    '''
    :param amp: amplitude of sine wave 1/2
    :param lvl: base level of sine wave 1/2
    :param freq: number of units for one full wave (e.g. 24 hours)
    :param len: length of the data created, freq1*len1 == freq2*len2
    :param std: standard deviation of the noise added to the data
    :param mean: mean of the noise added
    :param stdcut: number of standard deviations where normal noise should cut off
    :param AM: anomaly multiplier, how many standard deviations of noise anomalies need to at least be
    :param anom_pct: percentage of observations to become anomalous
    :return:
    '''
    Y = create_sin(amp1, lvl1, freq1, len1)
    A = create_sin(amp2, lvl2, freq2, len2)
    dataframe, anoms_df = add_noise_and_anomalies(add_nonneg(Y, A), anom_pct, std, mean, stdcut, AM, corr, n_vars)
    dataframe.set_index(pd.date_range('01-01-2018', periods=freq1*len1, freq='H'), inplace=True)
    return dataframe, anoms_df, Y, A