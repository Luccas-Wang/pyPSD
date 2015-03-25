__author__ = 'Administrator'
import yaml
import io
import h5py
import datetime as dt
import math
import numpy as np
import sys, getopt

from matplotlib.mlab import psd

class FrequencyUtility:
    def __init__(self):
        """
        Constructor
        """

    def load_data(self, inputFileName):
        with open(inputFileName, "r") as ins:
            array = []

            for line in ins:
                d = float(line)
                array.append(d)

            values = np.zeros(len(array), np.float32)

            i = 0
            for item in array:
                values[i] = item
                i += 1

            return array

    def write_data(self, outputFileName, pxx, frequencies):
        with open(outputFileName, "w") as outs:
            i = 0
            size = pxx.size

            for x in range(0, size):
                outputLine = str(frequencies[x]) + '|' + str(pxx[x]) + '\r\n'

                outs.write(outputLine)
        return

    def process_psd(self, data, nfft=1024, audio_sampling_rate=96000):
        return psd(data, nfft, audio_sampling_rate)

    def array_from_bytes(self, data_chunk, sample_width, data_type):
        data_length = len(data_chunk)
        remainder = data_length % sample_width

        if remainder == 0:
            reading_count = data_length // sample_width
            channel1 = np.zeros(reading_count, dtype=data_type)

            current_position = 0

            for x in range(0, reading_count):
                byte_array = bytearray(sample_width)
                bytearray.zfill(byte_array, sample_width)

                for y in range(0, sample_width):
                    byte_array[y] = data_chunk[current_position]
                    current_position += 1

                if data_type == np.int16 or data_type == np.int32:
                    channel1[x] = int.from_bytes(byte_array, byteorder='little', signed=True)
                else:
                    channel1[x] = float.from_bytes(byte_array, byteorder='little', signed=True)


            return {'Channel1': channel1 }
        else:
            return None

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('PowerSpectrumDensityProcessor.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    freqUtil = FrequencyUtility()
    inputData = freqUtil.load_data(inputfile)

    pxx, frequencies = freqUtil.process_psd(inputData, 1024, len(inputData))

    freqUtil.write_data(outputfile, pxx, frequencies)

if __name__ == "__main__":
   main(sys.argv[1:])