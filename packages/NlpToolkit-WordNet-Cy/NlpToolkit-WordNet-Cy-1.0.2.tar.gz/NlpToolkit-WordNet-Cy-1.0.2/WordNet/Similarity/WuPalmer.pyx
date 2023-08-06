from WordNet.Similarity.Similarity cimport Similarity
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet


cdef class WuPalmer(Similarity):

    def __init__(self, wordNet: WordNet):
        super().__init__(wordNet)

    cpdef double computeSimilarity(self, SynSet synSet1, SynSet synSet2):
        cdef list pathToRootOfSynSet1
        cdef list pathToRootOfSynSet2
        cdef int LCSDepth
        pathToRootOfSynSet1 = self.wordNet.findPathToRoot(synSet1)
        pathToRootOfSynSet2 = self.wordNet.findPathToRoot(synSet2)
        LCSDepth = self.wordNet.findLCSDepth(pathToRootOfSynSet1, pathToRootOfSynSet2)
        return 2 * LCSDepth / (len(pathToRootOfSynSet1) + len(pathToRootOfSynSet2))
