from WordNet.Similarity.Similarity cimport Similarity
from WordNet.SynSet cimport SynSet
from WordNet.WordNet cimport WordNet


cdef class SimilarityPath(Similarity):

    def __init__(self, wordNet: WordNet):
        super().__init__(wordNet)

    cpdef double computeSimilarity(self, SynSet synSet1, SynSet synSet2):
        cdef list pathToRootOfSynSet1
        cdef list pathToRootOfSynSet2
        cdef int pathLength, maxDepth
        pathToRootOfSynSet1 = self.wordNet.findPathToRoot(synSet1)
        pathToRootOfSynSet2 = self.wordNet.findPathToRoot(synSet2)
        pathLength = self.wordNet.findPathLength(pathToRootOfSynSet1, pathToRootOfSynSet2)
        maxDepth = max(len(pathToRootOfSynSet1), len(pathToRootOfSynSet2))
        return 2 * maxDepth - pathLength
