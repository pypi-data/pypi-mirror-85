cdef class Relation:

    def __init__(self, name: str):
        """
        A constructor that sets the name of the relation.

        PARAMETERS
        ----------
        name : str
            String relation name
        """
        self.name = name

    def __eq__(self, other) -> bool:
        """
        An overridden equals method to compare two relations.

        PARAMETERS
        ----------
        other : Relation
            The reference object with which to compare

        RETURNS
        -------
        bool
            True if this object is the same as the obj argument; False otherwise.
        """
        return self.name == other.name

    cpdef str getName(self):
        """
        Accessor method for the relation name.

        RETURNS
        ------
        str
            String relation name
        """
        return self.name

    cpdef setName(self, str name):
        """
        Mutator for the relation name.

        PARAMETERS
        ----------
        name : str
            String relation name
        """
        self.name = name
