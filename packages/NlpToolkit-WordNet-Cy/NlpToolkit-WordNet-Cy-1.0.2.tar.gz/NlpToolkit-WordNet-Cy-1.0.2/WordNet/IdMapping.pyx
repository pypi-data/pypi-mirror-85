cdef class IdMapping:

    cdef dict __map

    def __init__(self, fileName=None):
        """
        Constructor to load ID mappings from given file to a map.

        PARAMETERS
        ----------
        fileName : str
            String file name input that will be read
        """
        cdef str line
        cdef list items
        self.__map = {}
        if fileName is not None:
            infile = open(fileName, "r", encoding="utf8")
            lines = infile.readlines()
            for line in lines:
                items = line.split("->")
                self.__map[items[0]] = items[1]

    cpdef set keySet(self):
        """
        Returns a Set view of the keys contained in this map.

        RETURNS
        -------
        set
            A set view of the keys contained in this map
        """
        return set(self.__map.keys())

    cpdef str map(self, str _id):
        """
        Returns the value to which the specified key is mapped, or None if this map contains no mapping for the key.

        PARAMETERS
        ----------
        _id : str
            String id of a key

        RETURNS
        -------
        str
            Value of the specified key
        """
        cdef str mappedId
        if _id not in self.__map:
            return None
        mappedId = self.__map[_id]
        while mappedId in self.__map:
            mappedId = self.__map[mappedId]
        return mappedId

    cpdef str singleMap(self, str _id):
        """
        Returns the value to which the specified key is mapped.

        PARAMETERS
        ----------
        _id : str
            String id of a key

        RETURNS
        -------
        str
            Value of the specified key
        """
        return self.__map[_id]

    cpdef add(self, str key, str value):
        """
        Associates the specified value with the specified key in this map.

        PARAMETERS
        ----------
        key : str
            key with which the specified value is to be associated
        value : str
            value to be associated with the specified key
        """
        self.__map[key] = value

    cpdef remove(self, str key):
        """
        Removes the mapping for the specified key from this map if present.

        PARAMETERS
        ----------
        key : str
            key whose mapping is to be removed from the map
        """
        self.__map.pop(key)

    cpdef save(self, str fileName):
        """
        Saves map to the specified file.

        PARAMETERS
        ----------
        fileName : str
            String file to write map
        """
        cdef str key
        outfile = open(fileName, "w", encoding="utf8")
        for key in self.__map:
            outfile.write(key + "->" + self.__map[key] + "\n")
        outfile.close()
