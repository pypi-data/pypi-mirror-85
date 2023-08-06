from WordNet.Relation cimport Relation


cdef class Literal:

    cdef str name
    cdef int sense
    cdef str synSetId
    cdef str origin
    cdef list relations

    cpdef str getSynSetId(self)
    cpdef str getName(self)
    cpdef int getSense(self)
    cpdef str getOrigin(self)
    cpdef setOrigin(self, str origin)
    cpdef setSense(self, int sense)
    cpdef addRelation(self, Relation relation)
    cpdef removeRelation(self, Relation relation)
    cpdef bint containsRelation(self, Relation relation)
    cpdef bint containsRelationType(self, object semanticRelationType)
    cpdef Relation getRelation(self, int index)
    cpdef int relationSize(self)
    cpdef setName(self, str name)
    cpdef setSynSetId(self, str synSetId)
    cpdef saveAsXml(self, outfile)
