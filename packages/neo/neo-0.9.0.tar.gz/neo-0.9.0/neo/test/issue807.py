import neo
import numpy as np
time = np.array([0, 1, 2])
val = np.array([2, 3, 2])
id = np.array(['a', 'b', 'c'])
print(time.shape)
print(val.shape)
print(id.shape)
irsig0 = neo.IrregularlySampledSignal(time, val, units='mV', time_units='ms')
irsig0.array_annotate(id=id)
