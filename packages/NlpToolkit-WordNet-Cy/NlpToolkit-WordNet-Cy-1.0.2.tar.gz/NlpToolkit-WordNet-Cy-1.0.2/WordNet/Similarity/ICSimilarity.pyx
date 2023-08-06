cdef class ICSimilarity(Similarity):

    def __init__(self, wordNet: WordNet, informationContents: dict):
        super().__init__(wordNet)
        self.informationContents = informationContents

    cpdef double computeSimilarity(self, SynSet synSet1, SynSet synSet2):
        pass
