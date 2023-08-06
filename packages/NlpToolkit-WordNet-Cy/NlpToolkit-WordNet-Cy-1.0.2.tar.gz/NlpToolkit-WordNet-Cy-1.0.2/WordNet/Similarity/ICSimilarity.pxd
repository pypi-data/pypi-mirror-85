from WordNet.Similarity.Similarity cimport Similarity
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet


cdef class ICSimilarity(Similarity):

    cdef dict informationContents

    cpdef double computeSimilarity(self, SynSet synSet1, SynSet synSet2)
