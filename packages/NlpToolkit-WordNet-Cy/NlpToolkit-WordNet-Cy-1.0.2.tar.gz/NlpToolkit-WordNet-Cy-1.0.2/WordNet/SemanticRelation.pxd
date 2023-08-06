from WordNet.Relation cimport Relation


cdef class SemanticRelation(Relation):

    cdef object __relationType
    cdef int __toIndex

    cpdef int toIndex(self)
    cpdef object getRelationType(self)
    cpdef setRelationType(self, object relationType)
    cpdef str getTypeAsString(self)
