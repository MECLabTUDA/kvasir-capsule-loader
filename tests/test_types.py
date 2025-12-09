from kvasircapsuleloader import (
    FindingClass,
    FindingCategory,
    str_to_findingcategory,
    str_to_findingclass,
    findingclass_to_dirname,
)


def test_finding_classes():
    assert len(FindingClass) == 14
    assert str_to_findingclass("bLood --- fresh") == FindingClass.BLOOD_FRESH
    assert str_to_findingclass("fore ig N bo d y") == FindingClass.FOREIGN_BODY
    assert findingclass_to_dirname(FindingClass.FOREIGN_BODY) == "Foreign body"


def test_finding_categories():
    assert len(FindingCategory) == 2
    assert str_to_findingcategory("ANATOMY") == FindingCategory.ANATOMY