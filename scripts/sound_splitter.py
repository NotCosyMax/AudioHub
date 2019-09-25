#!/usr/bin/env python3
"""Pass input directly to output.

See https://www.assembla.com/spaces/portaudio/subversion/source/HEAD/portaudio/trunk/test/patest_wire.c

"""
import argparse
import logging
import queue  # Python 3.x
import time

q1 = queue.Queue()
q2 = queue.Queue()

stream1_out = None
stream2_out = None

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-i', '--input-device', type=int_or_str,
                    help='input device ID or substring')
parser.add_argument('-o', '--output-device', type=int_or_str,
                    help='output device ID or substring')
parser.add_argument('-o2', '--output-device2', type=int_or_str,
                    help='output device two ID or substring')
parser.add_argument('-o3', '--output-device3', type=int_or_str,
                    help='output device three ID or substring')
parser.add_argument('-c', '--channels', type=int, default=2,
                    help='number of channels')
parser.add_argument('-t', '--dtype', help='audio data type')
parser.add_argument('-s', '--samplerate', type=float, help='sampling rate')
parser.add_argument('-b', '--blocksize', type=int, help='block size')
parser.add_argument('-l', '--latency', type=float, help='latency in seconds')
parser.add_argument('-l2', '--latency2', type=float, help='latency in seconds')
parser.add_argument('-l3', '--latency3', type=float, help='latency in seconds')

args = parser.parse_args()

try:
    import sounddevice as sd
    import numpy  # Make sure NumPy is loaded before it is used in the callback
    assert numpy  # avoid "imported but unused" message (W0611)

    def callback(indata, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = indata
        q1.put(indata)
        q2.put(indata)

    def callback2(outdata, frames, time, status):
        try:
            data = q1.get_nowait()
            outdata[:] = data
        except queue.Empty:
            print('Buffer is empty: increase buffersize?')
    def callback3(outdata, frames, time, status):
        try:
            data = q2.get_nowait()
            outdata[:] = data
        except queue.Empty:
            print('Buffer is empty: increase buffersize?')

    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,
                   channels=args.channels, callback=callback):

        stream1_out = sd.OutputStream(
            samplerate=args.samplerate, blocksize=args.blocksize,
            device=args.output_device2, channels=args.channels, dtype=args.dtype, latency=args.latency2, callback=callback2)
        stream2_out = sd.OutputStream(
            samplerate=args.samplerate, blocksize=args.blocksize,
            device=args.output_device3, channels=args.channels, dtype=args.dtype, latency=args.latency3, callback=callback3)
        
        with stream1_out:
            with stream2_out:
                input()

except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
