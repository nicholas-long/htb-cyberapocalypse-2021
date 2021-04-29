import array
import struct
import sys
from collections import namedtuple
import wave

TYPE_DIGITAL = 0
TYPE_ANALOG = 1
expected_version = 0

DigitalData = namedtuple('DigitalData', ('initial_state', 'begin_time', 'end_time', 'num_transitions', 'transition_times'))

def parse_digital(f):
    # Parse header
    identifier = f.read(8)
    if identifier != b"<SALEAE>":
        raise Exception("Not a saleae file")

    version, datatype = struct.unpack('=ii', f.read(8))

    if version != expected_version or datatype != TYPE_DIGITAL:
        raise Exception("Unexpected data type: {}".format(datatype))

    # Parse digital-specific data
    initial_state, begin_time, end_time, num_transitions = struct.unpack('=iddq', f.read(28))

    # Parse transition times
    transition_times = array.array('d')
    transition_times.fromfile(f, num_transitions)

    return DigitalData(initial_state, begin_time, end_time, num_transitions, transition_times)


if __name__ == '__main__':
    filename = './export.bin/digital_3.bin'
    print("Opening " + filename)

    with open(filename, 'rb') as f:
        data = parse_digital(f)

    # Print out all digital data
    initial_state_str = 'low' if data.initial_state == 0 else 'high'
    print('Initial state: ' + initial_state_str)
    print('Begin time: {0:.6f}'.format(data.begin_time))
    print('End time: {0:.6f}'.format(data.end_time))
    print("Num transitions: {}".format(data.num_transitions))

    cur_state = data.initial_state

    print("  {0:>20} {1}".format("Time", "Bit State"))
    print("  {0:>20.6f} {1}".format(data.begin_time, 'low' if cur_state == 0 else 'high'))



    transition_iterator = iter(data.transition_times)
    next_time = next(transition_iterator, None)

    VOLUME = 5000

    wave_value = ((cur_state*2) - 1) * VOLUME
    wave_bytes = struct.pack('<h', wave_value)

    w = wave.open('alien_phoneme.wav','wb')

    sampleRate = 44100.0 # hertz
    duration = 1.0 # seconds
    w.setnchannels(1) # mono
    w.setsampwidth(2)
    w.setframerate(sampleRate)

    #data = struct.pack('<h', value)

    samples = 0
    while next_time != None:
        while next_time != None and samples / sampleRate >= next_time:
            cur_state = 0 if cur_state else 1
            wave_value = ((cur_state*2) - 1) * VOLUME
            wave_bytes = struct.pack('<h', wave_value)

            next_time = next(transition_iterator, None)
        
        samples += 1
        w.writeframes(wave_bytes)

    # for time in data.transition_times:
    #     # This is a transition, flip the bit state
    #     cur_state = 0 if cur_state else 1
    #     print("  {0:>20.6f} {1}".format(time, 'low' if  cur_state == 0 else 'high'))