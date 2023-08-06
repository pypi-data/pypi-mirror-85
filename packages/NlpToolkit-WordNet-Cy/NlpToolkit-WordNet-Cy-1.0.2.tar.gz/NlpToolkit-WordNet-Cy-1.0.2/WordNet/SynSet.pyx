from Dictionary.Pos import Pos
from WordNet.InterlingualDependencyType import InterlingualDependencyType
from WordNet.SemanticRelationType import SemanticRelationType


cdef class SynSet:

    def __init__(self, _id: str):
        """
        Constructor initialize SynSet ID, synonym and relations list.

        PARAMETERS
        ----------
        _id : str
            SynSet ID
        """
        self.__id = _id
        self.__synonym = Synonym()
        self.__relations = []
        self.__definition = []
        self.__pos = None
        self.__example = None

    def __eq__(self, other) -> bool:
        """
        An overridden equals method to compare two SynSets.

        PARAMETERS
        ----------
        other
            The reference object with which to compare

        RETURNS
        -------
        bool
            True if this object's ID is the same as the obj argument's ID; False otherwise.
        """
        return self.__id == other.__id

    def __hash__(self):
        """
        Returns a hash code for the ID.

        RETURNS
        -------
        int
            A hash code for the ID
        """
        return hash(self.__id)

    cpdef str getId(self):
        """
        Accessor for the SynSet ID.

        RETURNS
        -------
        str
            SynSet ID
        """
        return self.__id

    cpdef setId(self, str _id):
        """
        Mutator method for the SynSet ID.

        PARAMETERS
        ----------
        _id : str
            SynSet ID to be set
        """
        cdef int i
        self.__id = _id
        for i in range(self.__synonym.literalSize()):
            self.__synonym.getLiteral(i).setSynSetId(_id)

    cpdef setDefinition(self, str definition):
        """
        Mutator method for the definition.

        PARAMETERS
        ----------
        definition : str
            String definition
        """
        self.__definition = definition.split("|")

    cpdef removeDefinition(self, str definition):
        """
        Removes the specified definition from long definition.

        PARAMETERS
        ----------
        definition : str
            definition to be removed
        """
        cdef str longDefinition
        longDefinition = self.getLongDefinition()
        if longDefinition.startswith(definition + "|"):
            self.setDefinition(longDefinition.replace(definition + "|", ""))
        elif longDefinition.endswith("|" + definition):
            self.setDefinition(longDefinition.replace("|" + definition, ""))
        elif ("|" + definition + "|") in longDefinition:
            self.setDefinition(longDefinition.replace("|" + definition, ""))

    cpdef str getDefinition(self, index=None):
        """
        Accessor for the definition.

        RETURNS
        -------
        str
            Definition
        """
        if len(self.__definition) > 0:
            if index is None:
                index = 0
            if 0 <= index < len(self.__definition):
                return self.__definition[index]
            else:
                return None
        else:
            return None

    cpdef str representative(self):
        """
        Returns the first literal's name.

        RETURNS
        -------
        str
            The first literal's name.
        """
        return self.getSynonym().getLiteral(0).getName()

    cpdef str getLongDefinition(self):
        """
        Returns all the definitions in the list.

        RETURNS
        -------
        str
            All the definitions
        """
        cdef str longDefinition
        cdef int i
        if len(self.__definition) > 0:
            longDefinition = self.__definition[0]
            for i in range(1, len(self.__definition)):
                longDefinition = longDefinition + "|" + self.__definition[i]
            return longDefinition
        else:
            return None

    cpdef sortDefinitions(self):
        """
        Sorts definitions list according to their lengths.
        """
        cdef int i, j
        cdef str tmp
        if len(self.__definition) > 0:
            for i in range(len(self.__definition)):
                for j in range(i + 1, len(self.__definition)):
                    if len(self.__definition[i]) < len(self.__definition[j]):
                        tmp = self.__definition[i]
                        self.__definition[i] = self.__definition[j]
                        self.__definition[j] = tmp

    cpdef int numberOfDefinitions(self):
        """
        Returns number of definitions in the list.

        RETURNS
        -------
        int
            Number of definitions in the list.
        """
        return len(self.__definition)

    cpdef setExample(self, str example):
        """
        Mutator for the example.

        PARAMETERS
        ----------
        example : str
            String that will be used to set
        """
        self.__example = example

    cpdef str getExample(self):
        """
        Accessor for the example.

        RETURNS
        -------
        str
            String example
        """
        return self.__example

    cpdef setBcs(self, int bcs):
        """
        Mutator for the bcs value which enables the connection with the BalkaNet.

        PARAMETERS
        ----------
        bcs : int
            bcs value
        """
        if 1 <= bcs <= 3:
            self.__bcs = bcs

    cpdef int getBcs(self):
        """
        Accessor for the bcs value

        RETURNS
        -------
        int
            Bcs value
        """
        return self.__bcs

    cpdef setPos(self, object pos):
        """
        Mutator for the part of speech tags.

        PARAMETERS
        ----------
        pos : Pos
            part of speech tag
        """
        self.__pos = pos

    cpdef object getPos(self):
        """
        Accessor for the part of speech tag.

        RETURNS
        -------
        Pos
            Part of speech tag
        """
        return self.__pos

    cpdef setNote(self, str note):
        """
        Mutator for the available notes.

        PARAMETERS
        ----------
        note : str
            String note to be set
        """
        self.__note = note

    cpdef str getNote(self):
        """
        Accessor for the available notes.

        RETURNS
        -------
        str
            String note
        """
        return self.__note

    cpdef addRelation(self, Relation relation):
        """
        Appends the specified Relation to the end of relations list.

        PARAMETERS
        ----------
        relation : Relation
            Element to be appended to the list
        """
        self.__relations.append(relation)

    cpdef removeRelation(self, relationOrName):
        """
        Removes the first occurrence of the specified element from relations list according to relation name,
        if it is present. If the list does not contain the element, it stays unchanged.

        PARAMETERS
        ----------
        relationOrName
            Element to be removed from the list, if present
            element to be removed from the list, if present
        """
        cdef int i
        if isinstance(relationOrName, Relation):
            self.__relations.remove(relationOrName)
        elif isinstance(relationOrName, str):
            for i in range(len(self.__relations)):
                if self.__relations[i].getName() == relationOrName:
                    self.__relations.pop(i)
                    break

    cpdef Relation getRelation(self, int index):
        """
        Returns the element at the specified position in relations list.

        PARAMETERS
        ----------
        index : int
            index of the element to return

        RETURNS
        -------
        Relation
            The element at the specified position in the list
        """
        return self.__relations[index]

    cpdef list getInterlingual(self):
        """
        Returns interlingual relations with the synonym interlingual dependencies.

        RETURNS
        -------
        list
            A list of SynSets that has interlingual relations in it
        """
        cdef list result
        cdef int i
        cdef Relation relation
        result = []
        for i in range(len(self.__relations)):
            if isinstance(self.__relations[i], InterlingualRelation):
                relation = self.__relations[i]
                if relation.getType() == InterlingualDependencyType.SYNONYM:
                    result.append(relation.getName())
        return result

    cpdef int relationSize(self):
        """
        Returns the size of the relations list.

        RETURNS
        -------
        int
            The size of the relations list
        """
        return len(self.__relations)

    cpdef addLiteral(self, Literal literal):
        """
        Adds a specified literal to the synonym.

        PARAMETERS
        ----------
        literal : Literal
            literal to be added
        """
        self.__synonym.addLiteral(literal)

    cpdef Synonym getSynonym(self):
        """
        Accessor for the synonym.

        RETURNS
        -------
        Synonym
            synonym
        """
        return self.__synonym

    cpdef bint containsSameLiteral(self, SynSet synSet):
        """
        Compares literals of synonym and the specified SynSet, returns true if their have same literals.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet to compare

        RETURNS
        -------
        bool
            True if SynSets have same literals, False otherwise
        """
        cdef int i, j
        cdef str literal1, literal2
        for i in range(self.__synonym.literalSize()):
            literal1 = self.__synonym.getLiteral(i).getName()
            for j in range(synSet.getSynonym().literalSize()):
                literal2 = synSet.getSynonym().getLiteral(j).getName()
                if literal1 == literal2:
                    return True
        return False

    cpdef bint containsRelation(self, Relation relation):
        """
        Returns True if relations list contains the specified relation.

        PARAMETERS
        ----------
        relation : Relation
            Element whose presence in the list is to be tested

        RETURNS
        -------
        bool
            True if the list contains the specified element
        """
        return relation in self.__relations

    cpdef bint containsRelationType(self, object semanticRelationType):
        """
        Returns True if specified semantic relation type presents in the relations list.

        PARAMETERS
        ----------
        semanticRelationType : SemanticRelationType
            Element whose presence in the list is to be tested

        RETURNS
        -------
        bool
            True if specified semantic relation type presents in the relations list
        """
        cdef Relation relation
        for relation in self.__relations:
            if isinstance(relation, SemanticRelation) and relation.getRelationType() == semanticRelationType:
                return True
        return False

    cpdef mergeSynSet(self, SynSet synSet):
        """
        Merges synonym and a specified SynSet with their definitions, relations, part of speech tags and examples.

        PARAMETERS
        ----------
        synSet : SynSet
            SynSet to be merged
        """
        cdef int i
        for i in range(synSet.getSynonym().literalSize()):
            if not self.__synonym.contains(synSet.getSynonym().getLiteral(i)):
                self.__synonym.addLiteral(synSet.getSynonym().getLiteral(i))
        if len(self.__definition) == 0 and synSet.getDefinition() is not None:
            self.setDefinition(synSet.getDefinition())
        elif len(self.__definition) > 0 and synSet.getDefinition() is not None \
                and self.getLongDefinition() != synSet.getLongDefinition():
            self.setDefinition(self.getLongDefinition() + "|" + synSet.getLongDefinition())
        if synSet.relationSize() != 0:
            for i in range(0, synSet.relationSize()):
                if not self.containsRelation(synSet.getRelation(i)) and synSet.getRelation(i).getName() != id:
                    self.addRelation(synSet.getRelation(i))
        if self.__pos is None and synSet.getPos() is not None:
            self.setPos(synSet.getPos())
        if self.__example is None and synSet.getExample() is not None:
            self.__example = synSet.getExample()

    def __str__(self) -> str:
        """
        Overridden toString method to print the first definition or representative.

        RETURNS
        -------
        str
            Print the first definition or representative.
        """
        if len(self.__definition) > 0:
            return self.__definition[0]
        else:
            return self.representative()

    cpdef saveAsXml(self, outFile):
        """
        Method to write SynSets to the specified file in the XML format.

        PARAMETERS
        ----------
        outFile : file
            File to write XML files
        """
        cdef Relation relation
        outFile.write("<SYNSET>")
        outFile.write("<ID>" + self.__id + "</ID>")
        self.__synonym.saveAsXml(outFile)
        if self.__pos is not None:
            if self.__pos == Pos.NOUN:
                outFile.write("<POS>n</POS>")
            elif self.__pos == Pos.ADJECTIVE:
                outFile.write("<POS>a</POS>")
            elif self.__pos == Pos.VERB:
                outFile.write("<POS>v</POS>")
            elif self.__pos == Pos.ADVERB:
                outFile.write("<POS>b</POS>")
            elif self.__pos == Pos.CONJUNCTION:
                outFile.write("<POS>c</POS>")
            elif self.__pos == Pos.PRONOUN:
                outFile.write("<POS>r</POS>")
            elif self.__pos == Pos.INTERJECTION:
                outFile.write("<POS>i</POS>")
            elif self.__pos == Pos.PREPOSITION:
                outFile.write("<POS>p</POS>")
        for relation in self.__relations:
            if isinstance(relation, InterlingualRelation):
                outFile.write("<ILR>" + relation.getName() + "<TYPE>" + relation.getTypeAsString() + "</TYPE></ILR>")
            elif isinstance(relation, SemanticRelation):
                outFile.write("<SR>" + relation.getName() + "<TYPE>" + relation.getTypeAsString() + "</TYPE></SR>")
        if len(self.__definition) > 0:
            outFile.write("<DEF>" + self.getLongDefinition() + "</DEF>")
        if self.__example is not None:
            outFile.write("<EXAMPLE>" + self.__example + "</EXAMPLE>")
        outFile.write("</SYNSET>\n")
