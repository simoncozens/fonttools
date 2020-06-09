import pytest
from fontTools.otlLib.classdefbuilder import ClassDefBuilder
from fontTools.ttLib.tables import otTables


class ClassDefBuilderTest(object):
    def test_build_usingClass0(self):
        b = ClassDefBuilder(useClass0=True)
        b.add({"aa", "bb"})
        b.add({"a", "b"})
        b.add({"c"})
        b.add({"e", "f", "g", "h"})
        cdef = b.build()
        assert isinstance(cdef, otTables.ClassDef)
        assert cdef.classDefs == {"a": 2, "b": 2, "c": 3, "aa": 1, "bb": 1}

    def test_build_notUsingClass0(self):
        b = ClassDefBuilder(useClass0=False)
        b.add({"a", "b"})
        b.add({"c"})
        b.add({"e", "f", "g", "h"})
        cdef = b.build()
        assert isinstance(cdef, otTables.ClassDef)
        assert cdef.classDefs == {
            "a": 2,
            "b": 2,
            "c": 3,
            "e": 1,
            "f": 1,
            "g": 1,
            "h": 1,
        }

    def test_canAdd(self):
        b = ClassDefBuilder(useClass0=True)
        b.add({"a", "b", "c", "d"})
        b.add({"e", "f"})
        assert b.canAdd({"a", "b", "c", "d"})
        assert b.canAdd({"e", "f"})
        assert b.canAdd({"g", "h", "i"})
        assert not b.canAdd({"b", "c", "d"})
        assert not b.canAdd({"a", "b", "c", "d", "e", "f"})
        assert not b.canAdd({"d", "e", "f"})
        assert not b.canAdd({"f"})

    def test_sizeOfClass(self):
        glyphset = "abcdefghijkl"
        b = ClassDefBuilder(useClass0=True, glyphset=glyphset)
        assert b.sizeOfClass(["a","b","c","d"]) == 2
        assert b.sizeOfClass(["a","c","e"]) == 3
        assert b.sizeOfClass(["a","c","e", "f", "g"]) == 4
        assert b.sizeOfClass(["a","c","e", "f", "g", "h"]) == 4
