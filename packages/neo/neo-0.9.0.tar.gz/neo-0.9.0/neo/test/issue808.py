import quantities as pq
import numpy as np
import neo
times = np.arange(0, 3) * pq.s
ev = neo.Event(
    times=times
)
new_time = ev.rescale('us')
