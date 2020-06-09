from fontTools.ttLib.tables import otTables as ot
from itertools import groupby

class ClassDefBuilder(object):
    """Helper for building ClassDef tables."""
    def __init__(self, useClass0, glyphset = None):
        self.classes_ = set()
        self.glyphs_ = {}
        self.useClass0_ = useClass0
        self.glyphset = glyphset

    def canAdd(self, glyphs):
        if isinstance(glyphs, (set, frozenset)):
            glyphs = sorted(glyphs)
        glyphs = tuple(glyphs)
        if glyphs in self.classes_:
            return True
        for glyph in glyphs:
            if glyph in self.glyphs_:
                return False
        return True

    def add(self, glyphs):
        if isinstance(glyphs, (set, frozenset)):
            glyphs = sorted(glyphs)
        glyphs = tuple(glyphs)
        if glyphs in self.classes_:
            return
        self.classes_.add(glyphs)
        for glyph in glyphs:
            assert glyph not in self.glyphs_
            self.glyphs_[glyph] = glyphs

    def indexOf(self, glyphs, failok = False):
        classes = self.classes()
        # Glyphs may arrive as lists, sets, ordered dictionary keys...
        for i in range(0, len(classes)):
            if set(classes[i]) == set(glyphs):
                return i
        if failok:
            return None
        raise KeyError

    def sizeOfClass(self, glyphs):
        glyphs = sorted([ self.glyphset.index(g) for g in glyphs ])
        size = 0
        for i, els in groupby(enumerate(glyphs), lambda i: i[0]-i[1]):
            size += 1
            if len(list(els)) > 1: size += 1
        return size

    def classes(self):
        # In ClassDef1 tables, class id #0 does not need to be encoded
        # because zero is the default. Therefore, we use id #0 for the
        # glyph class that has the largest number of members. However,
        # in other tables than ClassDef1, 0 means "every other glyph"
        # so we should not use that ID for any real glyph classes;
        # we implement this by inserting an empty set at position 0.
        if self.glyphset:
            result = sorted(self.classes_, key=lambda s: self.sizeOfClass(s), reverse=True)
        else:
            result = sorted(self.classes_, key=lambda s: (len(s), s), reverse=True)
        if not self.useClass0_:
            result.insert(0, frozenset())
        return result

    def build(self):
        glyphClasses = {}
        for classID, glyphs in enumerate(self.classes()):
            if classID == 0:
                continue
            for glyph in glyphs:
                glyphClasses[glyph] = classID
        classDef = ot.ClassDef()
        classDef.classDefs = glyphClasses
        return classDef
