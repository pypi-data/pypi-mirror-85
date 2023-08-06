cdef class Relation:

    cdef str name

    cpdef str getName(self)
    cpdef setName(self, str name)
