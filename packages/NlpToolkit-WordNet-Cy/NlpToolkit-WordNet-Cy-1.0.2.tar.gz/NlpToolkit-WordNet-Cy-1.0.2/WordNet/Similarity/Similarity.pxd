from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet


cdef class Similarity:

    cdef WordNet wordNet

    cpdef double computeSimilarity(self, SynSet synSet1, SynSet synSet2)
