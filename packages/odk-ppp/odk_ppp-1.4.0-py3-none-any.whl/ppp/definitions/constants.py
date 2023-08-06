"""A list of reusable constants for the package.

MEDIA_FIELDS (tuple): Fields that can be set to file names of allowable
    media types for the given field.
LANGUAGE_DEPENDENT_FIELDS (tuple): Fields for which values can vary by
    language. A single ODK XLSForm can have many such fields, suffixed
    by '::language'.
TRUNCATABLE_FIELDS (tuple): Fields that should be limited to a specific
    length. Current limit is 100 chars, which is somewhat arbitrary but
    turns out good in converted forms.
"""
ODK_SUPERGLOBALS = (
    "start",
    "end",
    "deviceid",
    "phonenumber",
    "simserial",
    "meta",
    "instanceID",
    "instanceName",
)
EXCLUSION_TOKEN = "X"
SYNTAX = {"xlsforms": {"language_field_delimiters": [":", "::"]}}
IGNORE_RELEVANT_TOKEN = "#####"
SUPPORTED_FORMATS = ("html", "doc")
LANGUAGE_PERTINENT_WORKSHEETS = ("survey", "choices", "external_choices")
XLSFORM_SUPPORTED_MULTIMEDIA_TYPES = ["image", "audio", "video"]
# MEDIA_FIELDS = (image, media:image, media::image, ...)
MEDIA_FIELDS = tuple(x for x in XLSFORM_SUPPORTED_MULTIMEDIA_TYPES) + tuple(
    "media" + y + x
    for x in XLSFORM_SUPPORTED_MULTIMEDIA_TYPES
    for y in SYNTAX["xlsforms"]["language_field_delimiters"]
)
# for x in XLSFORM_SUPPORTED_MULTIMEDIA_TYPES:
#     MEDIA_FIELDS.append(x)
#     for y in SYNTAX['xlsforms']['language_field_delimiters']:
#         MEDIA_FIELDS.append('media' + y + x)
CONSTRAINT_MESSAGE_VARIATIONS = tuple(
    "constraint{}message".format(x) for x in [" ", "_"]
)
LANGUAGE_DEPENDENT_FIELDS_NONMEDIA_FIELDS = (
    "label",
    "hint",
    "ppp_input",
) + CONSTRAINT_MESSAGE_VARIATIONS
LANGUAGE_DEPENDENT_FIELDS = LANGUAGE_DEPENDENT_FIELDS_NONMEDIA_FIELDS + MEDIA_FIELDS
RELEVANCE_FIELD_TOKENS = ("relevant", "relevance")
TRUNCATABLE_FIELDS = ("constraint",) + RELEVANCE_FIELD_TOKENS
MULTI_ARGUMENT_CONVERSION_OPTIONS = ("template", "format", "language")
PPP_REPLACEMENTS_FIELDS = ("label",) + RELEVANCE_FIELD_TOKENS
CHOICE_NAME_VARIATIONS = ("name", "value")
TEMPLATES = {
    "detailed": {
        "field_replacements": (),
        "field_exclusions": (),
        "other_specific_exclusions": (),
        "general_exclusions": False,
        "render_settings": {"html": {"side_letters": True}},
    },
    "internal": {
        "field_replacements": (),
        "field_exclusions": (),
        "other_specific_exclusions": (),
        "general_exclusions": False,
        "render_settings": {"html": {"side_letters": True}},
    },
    "standard": {
        "field_replacements": PPP_REPLACEMENTS_FIELDS,
        "field_exclusions": ("constraint", "constraint_message", "type"),
        # 'type') + CHOICE_NAME_VARIATIONS,
        "other_specific_exclusions": ("choice names",),
        "general_exclusions": True,
        "render_settings": {"html": {"side_letters": False}},
    },
    "public": {
        "field_replacements": (),
        "field_exclusions": (),
        "other_specific_exclusions": (),
        "general_exclusions": False,
        "render_settings": {"html": {"side_letters": True}},
    },
}
TEMPLATES["full"] = TEMPLATES["detailed"]
TEMPLATES["developer"] = TEMPLATES["detailed"]  # alias
TEMPLATES["minimal"] = TEMPLATES["standard"]  # alias
TEMPLATES["basic"] = TEMPLATES["standard"]  # alias
