cdef class Similarity:

    cpdef double computeSimilarity(self, SynSet synSet1, SynSet synSet2):
        pass

    def __init__(self, wordNet: WordNet):
        self.wordNet = wordNet
