from WordNet.Relation cimport Relation


cdef class InterlingualRelation(Relation):

    cdef object __dependencyType

    cpdef object getType(self)
    cpdef str getTypeAsString(self)
