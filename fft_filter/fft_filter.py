import sys
import argparse
import numpy as np
from scipy import fftpack as fftpack
from matplotlib import pyplot as plt

def demo():
    # Sine function with gaussian noise
    x0 = 0.
    xf = 6.
    points = 500

    x = np.linspace(x0, xf, points)
    y = np.sin(2 * np.pi * 2.5 * x) 
    noise = np.random.normal(scale=0.6, size=points)

    return np.c_[x, y + noise]

clicks = [-2, -1]
def onclick(event):
    global clicks
    clicks.append(event.xdata)
    if round(clicks[-2], 5) == round(clicks[-1], 5):
        plt.close()

def filter_signal(freq, fft_signal):
    """ Gets cutoff frequencies for FFT filter from mouse clicks 

    Args:
        freq: np.array -> frequency axis from rfftfreq
        fft_signal: np.array -> fft of transformed data
    Returns:
        fft_signal: np.array -> filtered fft data

    """
    for i in range(2):
        fig = plt.figure()
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.plot(freq, fft_signal)
        plt.xlabel('Frequency')
        plt.ylabel('FFT Signal')
        if i == 0:
            plt.title('Double click to set low pass frequency')
        else:
            plt.title('Double click to set high pass frequency')
        plt.show()
        cutoff = clicks[-1]
        fig.canvas.mpl_disconnect(cid)
        if i == 0:
            fft_signal = np.where(freq < cutoff, fft_signal, 0.)
        else:
            fft_signal = np.where(freq > cutoff, fft_signal, 0.)
    return fft_signal

def main(raw_data):
    """ Performs FFT band pass filter 
    plots and saves filtered data

    Args:
         raw_data -> np.array((points, 2))

    """


    # Perform FFT /
    fft_signal = fftpack.rfft(raw_data[:, 1])
    points = len(raw_data[:, 0])
    dx = raw_data[1, 0] - raw_data[0, 0]
    freq = fftpack.rfftfreq(points, d=dx)

    # apply band pass filter
    filtered_signal = filter_signal(freq, fft_signal)

    # transform back
    filtered_data = fftpack.irfft(filtered_signal)

    plt.subplot(211)
    plt.plot(raw_data[:, 0], raw_data[:, 1], 'k.')
    plt.ylabel('Signal a.u.')

    plt.subplot(212)
    plt.plot(raw_data[:, 0], filtered_data, 'b-')
    plt.ylabel('Signal')
    plt.xlabel('Time')
    plt.show()
    np.savetxt('filtered_data.out', np.c_[raw_data[:, 0], filtered_data], 
               header='{:22} {:22}'.format('Time','Filtered'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='FFT Filter')
    parser.add_argument('--filename', type=str, 
                         help='Name of file containing raw data',
                         default=None
                         )
    args = parser.parse_args()

    if args.filename:
        raw_data = np.loadtxt(args.filename)
    else:
        print 'Using Demo Data'
        raw_data = demo()

    main(raw_data)


