import os
from ofold.utils import degree_to_note, degrees_to_notes, notes_to_midi

def test_degree_to_note():
    assert(degree_to_note(60, 0, 0) == 60)
    a_minor = [57, 59, 60, 62, 64, 65, 67]
    for degree in range(7):
        assert(degree_to_note(57, 5, degree) == a_minor[degree])
    a_minor_ = [note - 12 for note in a_minor]
    a_minor_.reverse()
    for degree in range(1, 8):
        assert(degree_to_note(57, 5, -degree) == a_minor_[degree - 1])

def test_degrees_to_notes():
    degrees = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    notes = [43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71]
    assert(degrees_to_notes(57, 5, degrees) == notes)


def test_degrees_to_midi(tmpdir):
    filename = os.path.join(tmpdir, 'test.mid')
    notes_to_midi([60, 62, 43, 18], [1, 0.5, 0.3, 9], filename)
    assert(os.path.isfile(filename))
    os.remove(filename)
