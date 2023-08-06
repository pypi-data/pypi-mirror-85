import xml.etree.ElementTree
from collections import OrderedDict

from Dictionary.ExceptionalWord cimport ExceptionalWord
from Dictionary.Pos import Pos
from WordNet.InterlingualRelation cimport InterlingualRelation
from WordNet.Relation cimport Relation
from WordNet.SemanticRelationType import SemanticRelationType


cdef class WordNet:

    def __init__(self, fileName: str = None, exceptionFileName: str = None):
        """
        Constructor that initializes the SynSet list, literal list, reads exception.

        PARAMETERS
        ----------
        fileName : str
            Resource to be read for the WordNet.
        """
        cdef SynSet currentSynSet
        cdef str interlingualId
        cdef list synSetList
        cdef Literal currentLiteral
        self.__exceptionList = {}
        if fileName is None:
            fileName = "turkish_wordnet.xml"
        elif exceptionFileName is not None:
            self.readExceptionFile(exceptionFileName)
        self.__interlingualList = {}
        self.__synSetList = OrderedDict()
        self.__literalList = OrderedDict()
        root = xml.etree.ElementTree.parse(fileName).getroot()
        currentSynSet = None
        for synSetNode in root:
            for partNode in synSetNode:
                if partNode.tag == "ID":
                    currentSynSet = SynSet(partNode.text)
                    self.addSynSet(currentSynSet)
                elif partNode.tag == "DEF":
                    currentSynSet.setDefinition(partNode.text)
                elif partNode.tag == "EXAMPLE":
                    currentSynSet.setExample(partNode.text)
                elif partNode.tag == "BCS":
                    currentSynSet.setBcs(int(partNode.text))
                elif partNode.tag == "POS":
                    if partNode.text == "a":
                        currentSynSet.setPos(Pos.ADJECTIVE)
                    elif partNode.text == "v":
                        currentSynSet.setPos(Pos.VERB)
                    elif partNode.text == "b":
                        currentSynSet.setPos(Pos.ADVERB)
                    elif partNode.text == "n":
                        currentSynSet.setPos(Pos.NOUN)
                    elif partNode.text == "i":
                        currentSynSet.setPos(Pos.INTERJECTION)
                    elif partNode.text == "c":
                        currentSynSet.setPos(Pos.CONJUNCTION)
                    elif partNode.text == "p":
                        currentSynSet.setPos(Pos.PREPOSITION)
                    elif partNode.text == "r":
                        currentSynSet.setPos(Pos.PRONOUN)
                elif partNode.tag == "SR":
                    if len(partNode) > 0 and partNode[0].tag == "TYPE":
                        typeNode = partNode[0]
                        if len(partNode) > 1 and partNode[1].tag == "TO":
                            toNode = partNode[1]
                            currentSynSet.addRelation(SemanticRelation(partNode.text, typeNode.text, int(toNode.text)))
                        else:
                            currentSynSet.addRelation(SemanticRelation(partNode.text, typeNode.text))
                elif partNode.tag == "ILR":
                    if len(partNode) > 0 and partNode[0].tag == "TYPE":
                        typeNode = partNode[0]
                        interlingualId = partNode.text
                        if interlingualId in self.__interlingualList:
                            synSetList = self.__interlingualList[interlingualId]
                        else:
                            synSetList = []
                        synSetList.append(currentSynSet)
                        self.__interlingualList[interlingualId] = synSetList
                        currentSynSet.addRelation(InterlingualRelation(interlingualId, typeNode.text))
                elif partNode.tag == "SYNONYM":
                    for literalNode in partNode:
                        currentLiteral = None
                        for childNode in literalNode:
                            if childNode.tag == "SENSE":
                                currentLiteral = Literal(literalNode.text, int(childNode.text), currentSynSet.getId())
                                currentSynSet.addLiteral(currentLiteral)
                                self.addLiteralToLiteralList(currentLiteral)
                            elif childNode.tag == "SR":
                                typeNode = childNode[0]
                                if len(childNode) > 1 and childNode[1].tag == "TO":
                                    toNode = childNode[1]
                                    currentLiteral.addRelation(
                                        SemanticRelation(childNode.text, typeNode.text, int(toNode.text)))
                                else:
                                    currentLiteral.addRelation(SemanticRelation(childNode.text, typeNode.text))

    cpdef readExceptionFile(self, str exceptionFileName):
        """
        Method constructs a DOM parser using the dtd/xml schema parser configuration and using this parser it
        reads exceptions from file and puts to exceptionList HashMap.

        PARAMETERS
        ----------
        exceptionFileName : str
            Exception file to be read
        """
        cdef str wordName, rootForm
        cdef list wordList
        root = xml.etree.ElementTree.parse(exceptionFileName).getroot()
        for wordNode in root:
            wordName = wordNode.attrib["name"]
            rootForm = wordNode.attrib["root"]
            if wordNode.attrib["pos"] == "Adj":
                pos = Pos.ADJECTIVE
            elif wordNode.attrib["pos"] == "Adv":
                pos = Pos.ADVERB
            elif wordNode.attrib["pos"] == "Noun":
                pos = Pos.NOUN
            elif wordNode.attrib["pos"] == "Verb":
                pos = Pos.VERB
            else:
                pos = Pos.NOUN
            if wordName in self.__exceptionList:
                wordList = self.__exceptionList[wordName]
            else:
                wordList = []
            wordList.append(ExceptionalWord(wordName, rootForm, pos))
            self.__exceptionList[wordName] = wordList

    cpdef addLiteralToLiteralList(self, Literal literal):
        """
        Adds a specified literal to the literal list.

        PARAMETERS
        ----------
        literal : Literal
            literal to be added
        """
        cdef list literals
        if literal.getName() in self.__literalList:
            literals = self.__literalList[literal.getName()]
        else:
            literals = []
        literals.append(literal)
        self.__literalList[literal.getName()] = literals

    cpdef list synSetList(self):
        """
        Returns the values of the SynSet list.

        RETURNS
        -------
        list
            Values of the SynSet list
        """
        return list(self.__synSetList.values())

    cpdef list literalList(self):
        """
        Returns the keys of the literal list.

        RETURNS
        -------
        list
            Keys of the literal list
        """
        return list(self.__literalList.keys())

    cpdef addSynSet(self, SynSet synSet):
        """
        Adds specified SynSet to the SynSet list.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet to be added
        """
        self.__synSetList[synSet.getId()] = synSet

    cpdef removeSynSet(self, SynSet synSet):
        """
        Removes specified SynSet from the SynSet list.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet to be removed
        """
        self.__synSetList.pop(synSet.getId())

    cpdef changeSynSetId(self, SynSet synSet, str newId):
        """
        Changes ID of a specified SynSet with the specified new ID.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet whose ID will be updated
        newId : str
            new ID
        """
        self.__synSetList.pop(synSet.getId())
        synSet.setId(newId)
        self.__synSetList[newId] = synSet

    cpdef SynSet getSynSetWithId(self, str synSetId):
        """
        Returns SynSet with the specified SynSet ID.

        PARAMETERS
        ----------
        synSetId : str
            ID of the SynSet to be returned

        RETURNS
        -------
        SynSet
            SynSet with the specified SynSet ID
        """
        if synSetId in self.__synSetList:
            return self.__synSetList[synSetId]
        else:
            return None

    cpdef SynSet getSynSetWithLiteral(self, str literal, int sense):
        """
        Returns SynSet with the specified literal and sense index.

        PARAMETERS
        ----------
        literal : Literal
            SynSet literal
        sense : int
            SynSet's corresponding sense index

        RETURNS
        -------
        SynSet
            SynSet with the specified literal and sense index
        """
        cdef list literals
        cdef Literal current
        if literal in self.__literalList:
            literals = self.__literalList[literal]
            for current in literals:
                if current.getSense() == sense:
                    return self.getSynSetWithId(current.getSynSetId())
        return None

    cpdef int numberOfSynSetsWithLiteral(self, str literal):
        """
        Returns the number of SynSets with a specified literal.

        PARAMETERS
        ----------
        literal : Literal
            literal to be searched in SynSets

        RETURNS
        -------
        int
            The number of SynSets with a specified literal
        """
        if literal in self.__literalList:
            return len(self.__literalList[literal])
        else:
            return 0

    cpdef list getSynSetsWithPartOfSpeech(self, object pos):
        """
        Returns a list of SynSets with a specified part of speech tag.

        PARAMETERS
        ----------
        pos : Pos
            Part of speech tag to be searched in SynSets

        RETURNS
        -------
        list
            A list of SynSets with a specified part of speech tag
        """
        cdef list result
        cdef SynSet synSet
        result = []
        for synSet in self.__synSetList.values():
            if synSet.getPos() is not None and synSet.getPos() == pos:
                result.append(synSet)
        return result

    cpdef list getLiteralsWithName(self, str literal):
        """
        Returns a list of literals with a specified literal String.

        PARAMETERS
        ----------
        literal : Literal
            literal String to be searched in literal list

        RETURNS
        -------
        list
            A list of literals with a specified literal String
        """
        if literal in self.__literalList:
            return self.__literalList[literal]
        else:
            return []

    cpdef addSynSetsWithLiteralToList(self, list result, str literal, object pos):
        """
        Finds the SynSet with specified literal String and part of speech tag and adds to the given SynSet list.

        PARAMETERS
        ----------
        result : list
            SynSet list to add the specified SynSet
        literal : str
            literal String to be searched in literal list
        pos : Pos
            part of speech tag to be searched in SynSets
        """
        cdef Literal current
        cdef SynSet synSet
        for current in self.__literalList[literal]:
            synSet = self.getSynSetWithId(current.getSynSetId)
            if synSet is not None and synSet.getPos() == pos:
                result.append(synSet)

    cpdef list getSynSetsWithLiteral(self, str literal):
        """
        Finds SynSets with specified literal String and adds to the newly created SynSet list.

        PARAMETERS
        ----------
        literal : Literal
            literal String to be searched in literal list

        RETURNS
        -------
        list
            Returns a list of SynSets with specified literal String
        """
        cdef list result
        cdef Literal current
        cdef SynSet synSet
        result = []
        if literal in self.__literalList:
            for current in self.__literalList[literal]:
                synSet = self.getSynSetWithId(current.getSynSetId())
                if synSet is not None:
                    result.append(synSet)
        return result

    cpdef list getLiteralsWithPossibleModifiedLiteral(self, str literal):
        """
        Finds literals with specified literal String and adds to the newly created literal String list.
        Ex: cleanest - clean

        PARAMETERS
        ----------
        literal : Literal
            literal String to be searched in literal list

        RETURNS
        -------
        list
            Returns a list of literals with specified literal String
        """
        cdef list result
        cdef str wordWithoutLastOne, wordWithoutLastTwo, wordWithoutLastThree
        result = [literal]
        wordWithoutLastOne = literal[:len(literal) - 1]
        wordWithoutLastTwo = literal[:len(literal) - 2]
        wordWithoutLastThree = literal[:len(literal) - 3]
        if literal in self.__exceptionList:
            for exceptionalWord in self.__exceptionList[literal]:
                result.append(exceptionalWord.getRoot())
        if literal.endswith("s") and wordWithoutLastOne in self.__literalList:
            result.append(wordWithoutLastOne)
        if (literal.endswith("es") or literal.endswith("ed") or literal.endswith("er")) \
                and wordWithoutLastTwo in self.__literalList:
            result.append(wordWithoutLastTwo)
        if literal.endswith("ed") and (wordWithoutLastTwo + literal[len(literal) - 3]) in self.__literalList:
            result.append(wordWithoutLastTwo + literal[len(literal) - 3])
        if (literal.endswith("ed") or literal.endswith("er")) and (wordWithoutLastTwo + "e") in self.__literalList:
            result.append(wordWithoutLastTwo + "e")
        if (literal.endswith("ing") or literal.endswith("est")) and wordWithoutLastThree in self.__literalList:
            result.append(wordWithoutLastThree)
        if literal.endswith("ing") and (wordWithoutLastThree + literal[len(literal) - 4]) in self.__literalList:
            result.append(wordWithoutLastThree + literal[len(literal) - 4])
        if (literal.endswith("ing") or literal.endswith("est")) and (wordWithoutLastThree + "e") in self.__literalList:
            result.append(wordWithoutLastThree + "e")
        if literal.endswith("ies") and (wordWithoutLastThree + "y") in self.__literalList:
            result.append(wordWithoutLastThree + "y")
        return result

    cpdef list getSynSetsWithPossiblyModifiedLiteral(self, str literal, object pos):
        """
        Finds SynSets with specified literal String and part of speech tag, then adds to the newly created SynSet list.
        Ex: cleanest - clean

        PARAMETERS
        ----------
        literal : str
            Literal String to be searched in literal list
        pos : Pos
            part of speech tag to be searched in SynSets

        RETURNS
        -------
        list
            Returns a list of SynSets with specified literal String and part of speech tag
        """
        cdef list result
        cdef list modifiedLiterals
        cdef str modifiedLiteral
        result = []
        modifiedLiterals = self.getLiteralsWithPossibleModifiedLiteral(literal)
        for modifiedLiteral in modifiedLiterals:
            if modifiedLiteral in self.__literalList:
                self.addSynSetsWithLiteralToList(result, modifiedLiteral, pos)
        return result

    cpdef addReverseRelation(self, SynSet synSet, SemanticRelation semanticRelation):
        """
        Adds the reverse relations to the SynSet.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet to add the reverse relations
        semanticRelation : SemanticRelation
            relation whose reverse will be added
        """
        cdef SynSet otherSynSet
        cdef SemanticRelation otherRelation
        otherSynSet = self.getSynSetWithId(semanticRelation.getName())
        if otherSynSet is not None and SemanticRelation.reverse(semanticRelation.getRelationType()) is not None:
            otherRelation = SemanticRelation(synSet.getId(),
                                             SemanticRelation.reverse(semanticRelation.getRelationType()))
            if not otherSynSet.containsRelation(otherRelation):
                otherSynSet.addRelation(otherRelation)

    cpdef removeReverseRelation(self, SynSet synSet, SemanticRelation semanticRelation):
        """
        Removes the reverse relations from the SynSet.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet to remove the reverse relation
        semanticRelation : SemanticRelation
            relation whose reverse will be removed
        """
        cdef SynSet otherSynSet
        cdef SemanticRelation otherRelation
        otherSynSet = self.getSynSetWithId(semanticRelation.getName())
        if otherSynSet is not None and SemanticRelation.reverse(semanticRelation.getRelationType()) is not None:
            otherRelation = SemanticRelation(synSet.getId(),
                                             SemanticRelation.reverse(semanticRelation.getRelationType()))
            if otherSynSet.containsRelation(otherRelation):
                otherSynSet.removeRelation(otherRelation)

    cpdef equalizeSemanticRelations(self):
        """
        Loops through the SynSet list and adds the possible reverse relations.
        """
        cdef SynSet synSet
        cdef int i
        for synSet in self.__synSetList.values():
            for i in range(synSet.relationSize()):
                if isinstance(synSet.getRelation(i), SemanticRelation):
                    self.addReverseRelation(synSet, synSet.getRelation(i))

    cpdef constructLiterals(self, str word, MorphologicalParse parse, MetamorphicParse metaParse,
                          FsmMorphologicalAnalyzer fsm):
        """
        Creates a list of literals with a specified word, or possible words corresponding to morphological parse.

        PARAMETERS
        ----------
        word : str
            literal String
        parse : MorphologicalParse
            morphological parse to get possible words
        metaParse : MetamorphicParse
            metamorphic parse to get possible words
        fsm : FsmMorphologicalAnalyzer
            finite state machine morphological analyzer to be used at getting possible words

        RETURNS
        -------
        list
            A list of literal
        """
        cdef list result
        cdef list possibleWords
        cdef str possibleWord
        result = []
        if parse.size() > 0:
            if not parse.isPunctuation() and not parse.isCardinal() and not parse.isReal():
                possibleWords = fsm.getPossibleWords(parse, metaParse)
                for possibleWord in possibleWords:
                    result.extend(self.getLiteralsWithName(possibleWord))
            else:
                result.extend(self.getLiteralsWithName(word))
        else:
            result.extend(self.getLiteralsWithName(word))
        return result

    cpdef list constructSynSets(self, str word, MorphologicalParse parse, MetamorphicParse metaParse,
                         FsmMorphologicalAnalyzer fsm):
        """
        Creates a list of SynSets with a specified word, or possible words corresponding to morphological parse.

        PARAMETERS
        ----------
        word : str
            literal String  to get SynSets with
        parse : MorphologicalParse
            morphological parse to get SynSets with proper literals
        metaParse : MetamorphicParse
            metamorphic parse to get possible words
        fsm : FsmMorphologicalAnalyzer
            finite state machine morphological analyzer to be used at getting possible words

        RETURNS
        -------
        list
            A list of SynSets
        """
        cdef list result
        cdef list possibleWords
        cdef str possibleWord
        cdef list synSets
        result = []
        if parse.size() > 0:
            if parse.isProperNoun():
                result.append(self.getSynSetWithLiteral("(özel isim)", 1))
            if parse.isTime():
                result.append(self.getSynSetWithLiteral("(zaman)", 1))
            if parse.isDate():
                result.append(self.getSynSetWithLiteral("(tarih)", 1))
            if parse.isHashTag():
                result.append(self.getSynSetWithLiteral("(hashtag)", 1))
            if parse.isEmail():
                result.append(self.getSynSetWithLiteral("(email)", 1))
            if parse.isOrdinal():
                result.append(self.getSynSetWithLiteral("(sayı sıra sıfatı)", 1))
            if parse.isPercent():
                result.append(self.getSynSetWithLiteral("(yüzde)", 1))
            if parse.isFraction():
                result.append(self.getSynSetWithLiteral("(kesir sayı)", 1))
            if parse.isRange():
                result.append(self.getSynSetWithLiteral("(sayı aralığı)", 1))
            if parse.isReal():
                result.append(self.getSynSetWithLiteral("(reel sayı)", 1))
            if not parse.isPunctuation() and not parse.isCardinal() and not parse.isReal():
                possibleWords = fsm.getPossibleWords(parse, metaParse)
                for possibleWord in possibleWords:
                    synSets = self.getSynSetsWithLiteral(possibleWord)
                    if len(synSets) > 0:
                        for synSet in synSets:
                            if synSet.getPos() is not None and (parse.getPos() == "NOUN" or parse.getPos() == "ADVERB"
                                                                or parse.getPos() == "VERB" or parse.getPos() == "ADJ"
                                                                or parse.getPos() == "CONJ"):
                                if synSet.getPos() == Pos.NOUN:
                                    if parse.getPos() == "NOUN" or parse.getRootPos() == "NOUN":
                                        result.append(synSet)
                                elif synSet.getPos() == Pos.ADVERB:
                                    if parse.getPos() == "ADVERB" or parse.getRootPos() == "ADVERB":
                                        result.append(synSet)
                                elif synSet.getPos() == Pos.VERB:
                                    if parse.getPos() == "VERB" or parse.getRootPos() == "VERB":
                                        result.append(synSet)
                                elif synSet.getPos() == Pos.ADJECTIVE:
                                    if parse.getPos() == "ADJ" or parse.getRootPos() == "ADJ":
                                        result.append(synSet)
                                elif synSet.getPos() == Pos.CONJUNCTION:
                                    if parse.getPos() == "CONJ" or parse.getRootPos() == "CONJ":
                                        result.append(synSet)
                                else:
                                    result.append(synSet)
                            else:
                                result.append(synSet)
                if len(result) == 0:
                    for possibleWord in possibleWords:
                        synSets = self.getSynSetsWithLiteral(possibleWord)
                        result.extend(synSets)
            else:
                result.extend(self.getSynSetsWithLiteral(word))
            if parse.isCardinal() and len(result) == 0:
                result.append(self.getSynSetWithLiteral("(tam sayı)", 1))
        else:
            result.extend(self.getSynSetsWithLiteral(word))
        return result

    cpdef list constructIdiomLiterals(self, FsmMorphologicalAnalyzer fsm, MorphologicalParse morphologicalParse1,
                               MetamorphicParse metaParse1, MorphologicalParse morphologicalParse2,
                               MetamorphicParse metaParse2, MorphologicalParse morphologicalParse3 = None,
                               MetamorphicParse metaParse3 = None):
        """
        Returns a list of literals using 3 possible words gathered with the specified morphological parses and
        metamorphic parses.

        PARAMETERS
        ----------
        morphologicalParse1 : MorphologicalParse
            morphological parse to get possible words
        morphologicalParse2 : MorphologicalParse
            morphological parse to get possible words
        morphologicalParse3 : MorphologicalParse
            morphological parse to get possible words
        metaParse1 : MetamorphicParse
            metamorphic parse to get possible words
        metaParse2 : MetamorphicParse
            metamorphic parse to get possible words
        metaParse3 : MetamorphicParse
            metamorphic parse to get possible words
        fsm : FsmMorphologicalAnalyzer
            finite state machine morphological analyzer to be used at getting possible words

        RETURNS
        -------
        list
            A list of literals
        """
        cdef list result
        cdef list possibleWords1
        cdef list possibleWords2
        cdef list possibleWords3
        cdef str possibleWord1, possibleWord2, possibleWord3
        result = []
        possibleWords1 = fsm.getPossibleWords(morphologicalParse1, metaParse1)
        possibleWords2 = fsm.getPossibleWords(morphologicalParse2, metaParse2)
        if morphologicalParse3 is not None and metaParse3 is not None:
            possibleWords3 = fsm.getPossibleWords(morphologicalParse3, metaParse3)
            for possibleWord1 in possibleWords1:
                for possibleWord2 in possibleWords2:
                    for possibleWord3 in possibleWords3:
                        result.extend(self.getLiteralsWithName(possibleWord1 + " " + possibleWord2 +
                                                               " " + possibleWord3))
        else:
            for possibleWord1 in possibleWords1:
                for possibleWord2 in possibleWords2:
                    result.extend(self.getLiteralsWithName(possibleWord1 + " " + possibleWord2))
        return result

    cpdef list constructIdiomSynSets(self, FsmMorphologicalAnalyzer fsm, MorphologicalParse morphologicalParse1,
                              MetamorphicParse metaParse1, MorphologicalParse morphologicalParse2,
                              MetamorphicParse metaParse2, MorphologicalParse morphologicalParse3 = None,
                              MetamorphicParse metaParse3 = None):
        """
        Returns a list of SynSets using 3 possible words gathered with the specified morphological parses and
        metamorphic parses.

        PARAMETERS
        ----------
        morphologicalParse1 : MorphologicalParse
            morphological parse to get possible words
        morphologicalParse2 : MorphologicalParse
            morphological parse to get possible words
        morphologicalParse3 : MorphologicalParse
            morphological parse to get possible words
        metaParse1 : MetamorphicParse
            metamorphic parse to get possible words
        metaParse2 : MetamorphicParse
            metamorphic parse to get possible words
        metaParse3 : MetamorphicParse
            metamorphic parse to get possible words
        fsm : FsmMorphologicalAnalyzer
            finite state machine morphological analyzer to be used at getting possible words

        RETURNS
        -------
        list
            A list of SynSets
        """
        cdef list result
        cdef list possibleWords1
        cdef list possibleWords2
        cdef list possibleWords3
        cdef str possibleWord1, possibleWord2, possibleWord3
        result = []
        possibleWords1 = fsm.getPossibleWords(morphologicalParse1, metaParse1)
        possibleWords2 = fsm.getPossibleWords(morphologicalParse2, metaParse2)
        if morphologicalParse3 is not None and metaParse3 is not None:
            possibleWords3 = fsm.getPossibleWords(morphologicalParse3, metaParse3)
            for possibleWord1 in possibleWords1:
                for possibleWord2 in possibleWords2:
                    for possibleWord3 in possibleWords3:
                        if self.numberOfSynSetsWithLiteral(possibleWord1 + " " + possibleWord2 + " "
                                                           + possibleWord3) > 0:
                            result.extend(self.getSynSetsWithLiteral(possibleWord1 + " " + possibleWord2 +
                                                                     " " + possibleWord3))
        else:
            for possibleWord1 in possibleWords1:
                for possibleWord2 in possibleWords2:
                    if self.numberOfSynSetsWithLiteral(possibleWord1 + " " + possibleWord2) > 0:
                        result.extend(self.getSynSetsWithLiteral(possibleWord1 + " " + possibleWord2))
        return result

    cpdef sortDefinitions(self):
        """
        Sorts definitions of SynSets in SynSet list according to their lengths.
        """
        cdef SynSet synSet
        for synSet in self.__synSetList:
            synSet.sortDefinitions()

    cpdef list getInterlingual(self, str synSetId):
        """
        Returns a list of SynSets with the interlingual relations of a specified SynSet ID.

        PARAMETERS
        ----------
        synSetId : str
            SynSet ID to be searched

        RETURNS
        -------
        list
            A list of SynSets with the interlingual relations of a specified SynSet ID
        """
        if synSetId in self.__interlingualList:
            return self.__interlingualList[synSetId]
        else:
            return []

    cpdef bint __containsSameLiteral(self, SynSet synSet1, SynSet synSet2):
        cdef int i, j
        cdef Literal literal1, literal2
        for i in range(synSet1.getSynonym().literalSize()):
            literal1 = synSet1.getSynonym().getLiteral(i)
            for j in range(i + 1, synSet2.getSynonym().literalSize()):
                literal2 = synSet2.getSynonym().getLiteral(j)
                if literal1.getName() == literal2.getName() and synSet1.getPos() is not None:
                    return True
        return False

    cpdef saveAsXml(self, str fileName):
        """
        Method to write SynSets to the specified file in the XML format.

        PARAMETERS
        ----------
        fileName : str
            file name to write XML files
        """
        cdef SynSet synSet
        outFile = open(fileName, "w", encoding="utf8")
        outFile.write("<SYNSETS>\n")
        for synSet in self.__synSetList.values():
            synSet.saveAsXml(outFile)
        outFile.write("</SYNSETS>\n")
        outFile.close()

    cpdef int size(self):
        """
        Returns the size of the SynSet list.

        RETURNS
        -------
        int
            The size of the SynSet list
        """
        return len(self.__synSetList)

    cpdef int findPathLength(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2):
        """
        Conduct common operations between similarity metrics.

        PARAMETERS
        ----------
        pathToRootOfSynSet1 : list
            First list of Strings
        pathToRootOfSynSet2 : list
            Second list of Strings

        RETURNS
        -------
        int
            Path length
        """
        cdef int i, foundIndex
        for i in range(len(pathToRootOfSynSet1)):
            if pathToRootOfSynSet1[i] in pathToRootOfSynSet2:
                foundIndex = pathToRootOfSynSet2.index(pathToRootOfSynSet1[i])
                return i + foundIndex - 1
        return -1

    cpdef tuple __findLCS(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2):
        """
        Returns depth and ID of the LCS.

        PARAMETERS
        ----------
        pathToRootOfSynSet1 : list
            First list of Strings
        pathToRootOfSynSet2 : list
            Second list of Strings

        RETURNS
        -------
        tuple
            Depth and ID of the LCS
        """
        cdef int i
        cdef str LCSid
        for i in range(len(pathToRootOfSynSet1)):
            LCSid = pathToRootOfSynSet1[i]
            if LCSid in pathToRootOfSynSet2:
                return LCSid, len(pathToRootOfSynSet1) - i + 1
        return None

    cpdef int findLCSDepth(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2):
        """
        Returns the depth of path.

        PARAMETERS
        ----------
        pathToRootOfSynSet1 : list
            First list of Strings
        pathToRootOfSynSet2 : list
            Second list of Strings

        RETURNS
        -------
        int
            LCS depth
        """
        cdef tuple temp
        temp = self.__findLCS(pathToRootOfSynSet1, pathToRootOfSynSet2)
        if temp is not None:
            return temp[1]
        else:
            return -1

    cpdef str findLCSid(self, list pathToRootOfSynSet1, list pathToRootOfSynSet2):
        """
        Returns the ID of LCS of path.

        PARAMETERS
        ----------
        pathToRootOfSynSet1 : list
            First list of Strings
        pathToRootOfSynSet2 : list
            Second list of Strings

        RETURNS
        -------
        str
            LCS ID
        """
        cdef tuple temp
        temp = self.__findLCS(pathToRootOfSynSet1, pathToRootOfSynSet2)
        if temp is not None:
            return temp[0]
        else:
            return None

    cpdef SynSet percolateUp(self, SynSet root):
        """
        Finds the parent of a node. It does not move until the root, instead it goes one level up.

        PARAMETERS
        ----------
        root : SynSet
            SynSet whose parent will be find

        RETURNS
        -------
        SynSet
            Parent SynSet
        """
        cdef int i
        cdef Relation r
        for i in range(root.relationSize()):
            r = root.getRelation(i)
            if isinstance(r, SemanticRelation):
                if r.getRelationType() == SemanticRelationType.HYPERNYM \
                        or r.getRelationType() == SemanticRelationType.INSTANCE_HYPERNYM:
                    root = self.getSynSetWithId(r.getName())
                    return root
        return None

    cpdef list findPathToRoot(self, SynSet synSet):
        """
        Finds the path to the root node of a SynSets.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet whose root path will be found

        RETURNS
        -------
        list
            List of String corresponding to nodes in the path
        """
        cdef list pathToRoot
        pathToRoot = []
        while synSet is not None:
            if synSet.getId() in pathToRoot:
                break
            pathToRoot.append(synSet.getId())
            synSet = self.percolateUp(synSet)
        return pathToRoot
