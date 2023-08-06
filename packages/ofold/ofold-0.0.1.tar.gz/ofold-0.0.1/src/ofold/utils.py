from midiutil import MIDIFile

def degree_to_note(root, mode, degree):   
    """Convert a list of relative degrees to midi note numbers.

    Parameters
    ----------
    key - MIDI note number for the root note
    mode - a number for the mode (0 - Ionian (major), 
           1 - Dorian, ..., 5 - Aeolian (minor), ...)
    degree - a scale degree number relative to root (root is 0), can be negative

    Returns
    -------
    an integer signifying MIDI note numbers
    """
    intervals = [2, 2, 1, 2, 2, 2, 1]
    intervals = intervals[mode:] + intervals[:mode]
    scale = [0]
    for interval in intervals:
        scale.append(scale[-1] + interval)
    root_mod = degree // 7
    return (root + 12 * root_mod) + scale[degree % 7]

    
def degrees_to_notes(root, mode, degrees):
    """Convert a list of relative degrees to midi note numbers.

    Parameters
    ----------
    key - MIDI note number for the root note
    mode - a number for the mode (0 - Ionian (major), 
           1 - Dorian, ..., 5 - Aeolian (minor), ...)
    degrees - a list of scale degrees relative to root (root is 0), can be negative

    Returns
    -------
    a list of integers signifying MIDI note numbers
    """
    assert((0 <= root) and (root <= 127))
    assert((0 <= mode) and (mode <= 7))
    return [degree_to_note(root, mode, degree) for degree in degrees]


def notes_to_midi(notes, durations, filename):
    """Write note values to a MIDI file.

    Parameters
    ----------
    notes - a list of MIDI note numbers
    durations - a list of durations
    filename - string
      filename to write to
    """
    assert(len(notes) == len(durations))
    track = 0
    channel = 0
    duration = 1
    tempo = 130
    volume = 100
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, 0, tempo)
    position = 0.0
    for note, duration in zip(notes, durations):
        MyMIDI.addNote(track, channel, note, position, duration, volume)
        position += duration
    with open(filename, "wb") as fd:
        MyMIDI.writeFile(fd)
