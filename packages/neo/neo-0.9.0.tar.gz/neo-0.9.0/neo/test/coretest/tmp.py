from neo.core import AnalogSignal, SpikeTrain, Block
from neo.test.generate_datasets import fake_neo, clone_object
from neo.test.tools import (assert_neo_object_is_compliant,
                            assert_same_sub_schema)


self_nchildren = 2
blk = fake_neo(Block, seed=0, n=self_nchildren)
self_unit1, self_unit2, self_unit3, self_unit4 = blk.list_units
self_seg1, self_seg2 = blk.segments
self_targobj = self_seg1
self_seed1 = self_seg1.annotations['seed']
self_seed2 = self_seg2.annotations['seed']

del self_seg1.annotations['i']
del self_seg2.annotations['i']
del self_seg1.annotations['j']
del self_seg2.annotations['j']

self_sigarrs1 = self_seg1.analogsignals
self_sigarrs2 = self_seg2.analogsignals
self_irsigs1 = self_seg1.irregularlysampledsignals
self_irsigs2 = self_seg2.irregularlysampledsignals

self_trains1 = self_seg1.spiketrains
self_trains2 = self_seg2.spiketrains

self_epcs1 = self_seg1.epochs
self_epcs2 = self_seg2.epochs
self_evts1 = self_seg1.events
self_evts2 = self_seg2.events

self_sigarrs1a = clone_object(self_sigarrs1, n=2)
self_irsigs1a = clone_object(self_irsigs1)

self_trains1a = clone_object(self_trains1)

self_epcs1a = clone_object(self_epcs1)
self_evts1a = clone_object(self_evts1)
seg1a = fake_neo(Block, seed=self_seed1, n=self_nchildren).segments[0]
assert_same_sub_schema(self_seg1, seg1a)
seg1a.annotations.pop("i")  # check_creation doesn't expect these
seg1a.annotations.pop("j")  # so we delete them
self_check_creation(seg1a)
seg1a.epochs.append(self_epcs2[0])
seg1a.annotate(seed=self_seed2)
seg1a.merge(self_seg2)
self_check_creation(seg1a)

assert_same_sub_schema(self_sigarrs1a + self_sigarrs2,
                        seg1a.analogsignals)
assert_same_sub_schema(self_irsigs1a + self_irsigs2,
                        seg1a.irregularlysampledsignals)

assert_same_sub_schema(self_epcs1 + self_epcs2, seg1a.epochs)
assert_same_sub_schema(self_evts1 + self_evts2, seg1a.events)

assert_same_sub_schema(self_trains1 + self_trains2, seg1a.spiketrains)
