import neo
import numpy as np
import quantities as pq
time = np.array([0, 1, 2])
val = np.array([2, 3, 2])
id = np.array(['a', 'b', 'c'])
print(time.shape)
print(val.shape)
print(id.shape)
sig0 = neo.AnalogSignal(val, units='mV', sampling_period=1.0*pq.ms, time_units='ms')
sig0.array_annotate(id=id)
