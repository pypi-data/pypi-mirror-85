from WordNet.InterlingualRelation cimport InterlingualRelation
from WordNet.Literal cimport Literal
from WordNet.Relation cimport Relation
from WordNet.SemanticRelation cimport SemanticRelation
from WordNet.Synonym cimport Synonym


cdef class SynSet:

    cdef str __id
    cdef object __pos
    cdef list __definition
    cdef str __example
    cdef Synonym __synonym
    cdef list __relations
    cdef str __note
    cdef int __bcs

    cpdef str getId(self)
    cpdef setId(self, str _id)
    cpdef setDefinition(self, str definition)
    cpdef removeDefinition(self, str definition)
    cpdef str getDefinition(self, index=*)
    cpdef str representative(self)
    cpdef str getLongDefinition(self)
    cpdef sortDefinitions(self)
    cpdef int numberOfDefinitions(self)
    cpdef setExample(self, str example)
    cpdef str getExample(self)
    cpdef setBcs(self, int bcs)
    cpdef int getBcs(self)
    cpdef setPos(self, object pos)
    cpdef object getPos(self)
    cpdef setNote(self, str note)
    cpdef str getNote(self)
    cpdef addRelation(self, Relation relation)
    cpdef removeRelation(self, relationOrName)
    cpdef Relation getRelation(self, int index)
    cpdef list getInterlingual(self)
    cpdef int relationSize(self)
    cpdef addLiteral(self, Literal literal)
    cpdef Synonym getSynonym(self)
    cpdef bint containsSameLiteral(self, SynSet synSet)
    cpdef bint containsRelation(self, Relation relation)
    cpdef bint containsRelationType(self, object semanticRelationType)
    cpdef mergeSynSet(self, SynSet synSet)
    cpdef saveAsXml(self, outFile)
