from WordNet.Literal cimport Literal


cdef class Synonym:

    cdef list __literals

    cpdef addLiteral(self, Literal literal)
    cpdef moveFirst(self, Literal literal)
    cpdef Literal getLiteral(self, object indexOrName)
    cpdef int literalSize(self)
    cpdef bint contains(self, Literal literal)
    cpdef bint containsLiteral(self, str literalName)
    cpdef removeLiteral(self, Literal toBeRemoved)
    cpdef saveAsXml(self, outFile)
