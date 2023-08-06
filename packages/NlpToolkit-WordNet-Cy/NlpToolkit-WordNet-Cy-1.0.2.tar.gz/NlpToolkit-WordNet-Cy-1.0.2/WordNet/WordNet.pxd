from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from MorphologicalAnalysis.MetamorphicParse cimport MetamorphicParse
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse

from WordNet.Literal cimport Literal
from WordNet.SemanticRelation cimport SemanticRelation
from WordNet.SynSet cimport SynSet


cdef class WordNet:

    cdef object __synSetList
    cdef object __literalList
    cdef dict __exceptionList
    cdef dict __interlingualList

    cpdef readExceptionFile(self, str exceptionFileName)
    cpdef addLiteralToLiteralList(self, Literal literal)
    cpdef list synSetList(self)
    cpdef list literalList(self)
    cpdef addSynSet(self, SynSet synSet)
    cpdef removeSynSet(self, SynSet synSet)
    cpdef changeSynSetId(self, SynSet synSet, str newId)
    cpdef SynSet getSynSetWithId(self, str synSetId)
    cpdef SynSet getSynSetWithLiteral(self, str literal, int sense)
    cpdef int numberOfSynSetsWithLiteral(self, str literal)
    cpdef list getSynSetsWithPartOfSpeech(self, object pos)
    cpdef list getLiteralsWithName(self, str literal)
    cpdef addSynSetsWithLiteralToList(self, list result, str literal, object pos)
    cpdef list getSynSetsWithLiteral(self, str literal)
    cpdef list getLiteralsWithPossibleModifiedLiteral(self, str literal)
    cpdef list getSynSetsWithPossiblyModifiedLiteral(self, str literal, object pos)
    cpdef addReverseRelation(self, SynSet synSet, SemanticRelation semanticRelation)
    cpdef removeReverseRelation(self, SynSet synSet, SemanticRelation semanticRelation)
    cpdef equalizeSemanticRelations(self)
    cpdef constructLiterals(self, str word, MorphologicalParse parse, MetamorphicParse metaParse,
                          FsmMorphologicalAnalyzer fsm)
    cpdef list constructSynSets(self, str word, MorphologicalParse parse, MetamorphicParse metaParse,
                         FsmMorphologicalAnalyzer fsm)
    cpdef list constructIdiomLiterals(self, FsmMorphologicalAnalyzer fsm, MorphologicalParse morphologicalParse1,
                               MetamorphicParse metaParse1, MorphologicalParse morphologicalParse2,
                               MetamorphicParse metaParse2, MorphologicalParse morphologicalParse3 = *,
                               MetamorphicParse metaParse3 = *)
    cpdef list constructIdiomSynSets(self, FsmMorphologicalAnalyzer fsm, MorphologicalParse morphologicalParse1,
                              MetamorphicParse metaParse1, MorphologicalParse morphologicalParse2,
                              MetamorphicParse metaParse2, MorphologicalParse morphologicalParse3 = *,
                              MetamorphicParse metaParse3 = *)
    cpdef sortDefinitions(self)
    cpdef list getInterlingual(self, str synSetId)
    cpdef bint __containsSameLiteral(self, SynSet synSet1, SynSet synSet2)
    cpdef saveAsXml(self, str fileName)
    cpdef int size(self)
    cpdef int findPathLength(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2)
    cpdef tuple __findLCS(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2)
    cpdef int findLCSDepth(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2)
    cpdef str findLCSid(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2)
    cpdef SynSet percolateUp(self, SynSet root)
    cpdef list findPathToRoot(self, SynSet synSet)
