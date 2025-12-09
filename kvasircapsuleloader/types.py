from enum import Enum


class FindingCategory(Enum):
    LUMINAL = 0
    ANATOMY = 1


class FindingClass(Enum):
    AMPULLA_OF_VATER = 0
    ANGIECTASIA = 1
    BLOOD_FRESH = 2
    BLOOD_HEMATIN = 3
    EROSION = 4
    ERYTHEMA = 5
    FOREIGN_BODY = 6
    ILEOCECAL_VALVE = 7
    LYMPHANGIECTASIA = 8
    NORMAL_CLEAN_MUCOSA = 9
    POLYP = 10
    PYLORUS = 11
    REDUCED_MUCOSAL_VIEW = 12
    ULCER = 13


ClassByCategory = {
    FindingCategory.LUMINAL: [
        FindingClass.ANGIECTASIA,
        FindingClass.BLOOD_FRESH,
        FindingClass.BLOOD_HEMATIN,
        FindingClass.EROSION,
        FindingClass.ERYTHEMA,
        FindingClass.FOREIGN_BODY,
        FindingClass.LYMPHANGIECTASIA,
        FindingClass.NORMAL_CLEAN_MUCOSA,
        FindingClass.POLYP,
        FindingClass.REDUCED_MUCOSAL_VIEW,
        FindingClass.ULCER,
    ],
    FindingCategory.ANATOMY: [
        FindingClass.AMPULLA_OF_VATER,
        FindingClass.ILEOCECAL_VALVE,
        FindingClass.PYLORUS,
    ],
}


CategoryByClass = {
    FindingClass.AMPULLA_OF_VATER: FindingCategory.ANATOMY,
    FindingClass.ANGIECTASIA: FindingCategory.LUMINAL,
    FindingClass.BLOOD_FRESH: FindingCategory.LUMINAL,
    FindingClass.BLOOD_HEMATIN: FindingCategory.LUMINAL,
    FindingClass.EROSION: FindingCategory.LUMINAL,
    FindingClass.ERYTHEMA: FindingCategory.LUMINAL,
    FindingClass.FOREIGN_BODY: FindingCategory.LUMINAL,
    FindingClass.ILEOCECAL_VALVE: FindingCategory.ANATOMY,
    FindingClass.LYMPHANGIECTASIA: FindingCategory.LUMINAL,
    FindingClass.NORMAL_CLEAN_MUCOSA: FindingCategory.LUMINAL,
    FindingClass.POLYP: FindingCategory.LUMINAL,
    FindingClass.PYLORUS: FindingCategory.ANATOMY,
    FindingClass.REDUCED_MUCOSAL_VIEW: FindingCategory.LUMINAL,
    FindingClass.ULCER: FindingCategory.LUMINAL,
}


def str_to_findingcategory(s: str) -> FindingCategory:
    """
    Translate string to correspoding FindingCategory object.

    :param s: String that should be "luminal" or "anatomy".
    :type s: str
    :raises ValueError: If string cannot be interpreted
    :return: FindingCategory object
    :rtype: FindingCategory
    """
    if s.lower().strip() not in ("luminal", "anatomy"):
        raise ValueError(
            f"Finding category string must be 'luminal' or 'anatomy', is: '{s}'"
        )
    return {"luminal": FindingCategory.LUMINAL, "anatomy": FindingCategory.ANATOMY}[
        s.lower()
    ]


def str_to_findingclass(s: str) -> FindingClass:
    """
    Try to translate any string to the corresponding FindingClass.

    Can be used for strings in metadata.csv or directory names.

    :param s: String to be translated
    :type s: str
    :return: Corresponding FindingClass or None if translation fails
    :rtype: FindingClass | None
    """
    translation = {
        "ampullaofvater": FindingClass.AMPULLA_OF_VATER,
        "angiectasia": FindingClass.ANGIECTASIA,
        "bloodfresh": FindingClass.BLOOD_FRESH,
        "bloodhematin": FindingClass.BLOOD_HEMATIN,
        "erosion": FindingClass.EROSION,
        "erythema": FindingClass.ERYTHEMA,
        "foreignbody": FindingClass.FOREIGN_BODY,
        "ileocecalvalve": FindingClass.ILEOCECAL_VALVE,
        "lymphangiectasia": FindingClass.LYMPHANGIECTASIA,
        "normalcleanmucosa": FindingClass.NORMAL_CLEAN_MUCOSA,
        "polyp": FindingClass.POLYP,
        "pylorus": FindingClass.PYLORUS,
        "reducedmucosalview": FindingClass.REDUCED_MUCOSAL_VIEW,
        "ulcer": FindingClass.ULCER,
    }
    slug = s.lower().replace(" ", "").replace("-", "")
    if slug not in translation:
        raise ValueError(
            f"Finding class string must be one of {translation.keys()}, but is '{s}' (slug: '{slug}')"
        )
    return translation[slug]


def findingclass_to_dirname(c: FindingClass) -> str:
    """
    Translate any FindingClass to corresponding folder name in original KvasirCapsule
    structure. Folders should not be renamed.

    :param c: FindingClass object
    :type c: FindingClass
    :return: Folder name
    :rtype: str
    """
    return {
        FindingClass.AMPULLA_OF_VATER: "Ampulla of vater",
        FindingClass.ANGIECTASIA: "Angiectasia",
        FindingClass.BLOOD_FRESH: "Blood - fresh",
        FindingClass.BLOOD_HEMATIN: "Blood - hematin",
        FindingClass.EROSION: "Erosion",
        FindingClass.ERYTHEMA: "Erythema",
        FindingClass.FOREIGN_BODY: "Foreign body",
        FindingClass.ILEOCECAL_VALVE: "Ileocecal valve",
        FindingClass.LYMPHANGIECTASIA: "Lymphangiectasia",
        FindingClass.NORMAL_CLEAN_MUCOSA: "Normal clean mucosa",
        FindingClass.POLYP: "Polyp",
        FindingClass.PYLORUS: "Pylorus",
        FindingClass.REDUCED_MUCOSAL_VIEW: "Reduced mucosal view",
        FindingClass.ULCER: "Ulcer",
    }[c]
