"""Module for the OdkForm class."""
import os
import re
from sys import stderr

from ppp.config import get_template_env
from ppp.definitions.error import OdkFormError
from ppp.definitions.constants import ODK_SUPERGLOBALS, RELEVANCE_FIELD_TOKENS
from ppp.odkcalculate import OdkCalculate
from ppp.odkchoices import OdkChoices
from ppp.odkcustomtype import OdkCustomType
from ppp.odkgroup import OdkGroup, set_template_env as odkgroup_template
from ppp.odkprompt import OdkPrompt, set_template_env as odkpromt_template
from ppp.odkrepeat import OdkRepeat, set_template_env as odkrepeat_template
from ppp.odktable import OdkTable, set_template_env as odktable_template
from ppp.odkabstractprompt import set_template_env as odkabstractprompt_template
from ppp.definitions.utils import exclusion
from pmix import Xlsform

TEMPLATE_ENV = None


def set_template_env(template):
    """Set template env."""
    global TEMPLATE_ENV
    TEMPLATE_ENV = get_template_env(template)
    odkgroup_template(template)
    odkpromt_template(template)
    odkrepeat_template(template)
    odktable_template(template)
    odkabstractprompt_template(template)


class OdkForm:
    """Class to represent an entire XLSForm.

    Attributes:
        settings (dict): A dictionary representation of the original 'settings'
            worksheet of an ODK XLSForm.
        title (str): Title of the ODK form.
        choices (dict): A list of rows from the 'choices' worksheet.
        ext_choices (dict): A list of rows from the 'external_choices'
            worksheet.
        metadata (dict): A dictionary of metadata for the original and
            converted ODK forms.
        questionnaire (list): An ordered representation of the ODK form,
            comprised of OdkPrompt, OdkGroup, OdkRepeat, and OdkTable objects.

    custom_token_types: ['hidden', 'hidden string', 'hidden int',
        'hidden geopoint']
    """

    def __init__(self, wb):
        """Initialize the OdkForm.

        Create an instance of an ODK form, including survey representation,
        choice options, settings, and metadata.

        Args:
            wb (Xlsform): A Xlsform object meeting XLSForm specification.

        Raises:
            OdkformError: No ODK form is supplied.
        """
        self.settings = wb.settings
        self.language = wb.form_language

        self.title = self.get_title(settings=self.settings, wb=wb)
        self.metadata = {  # TODO Finish filling this out.
            "last_author": str(),
            "last_updated": str(),
            "changelog": None,
            "info": None,
            "raw_data": wb,
        }
        self.choices = self.get_choices(wb, "choices")
        self.ext_choices = self.get_choices(wb, "external_choices")
        self.metadata = {
            **self.metadata,
            **{
                "file_name": os.path.split(wb.filename)[1],
                "form_id": self.settings.get("form_id")
                if self.settings.get("form_id")
                else self.settings.get("id_string"),
                "country": lambda: self.metadata["form_id"][3:5],
                "round": lambda: self.metadata["form_id"][6:7],
                "type_of_form": lambda: self.metadata["form_id"][0:2],
            },
        }
        self.metadata = {
            **self.metadata,
            "country": self.metadata["country"](),
            "round": self.metadata["round"](),
            "type_of_form": self.metadata["type_of_form"](),
        }
        qre = self.convert_survey(wb, self.choices, self.ext_choices)
        qre = OdkForm._add_question_iter_nums(qre)
        self.questionnaire = qre

    @classmethod
    def from_file(cls, path):
        """Create Odkform object from file in path.

        Args:
            path (str): The path for the source file of the ODK form,
                typically an '.xlsx' file meeting the XLSForm specification.

        Returns:
            Odkform
        """
        xlsform = Xlsform(path)
        odkform = cls(xlsform)
        return odkform

    @staticmethod
    def get_settings(wb):
        """Get the XLSForm settings as a settings_dict.

        Args:
            wb (Xlsform): A workbook object representing ODK form.

        Returns:
            dict: Form settings.
        """
        settings_dict = {}
        try:
            settings = wb["settings"]
            header = settings[0]
            details = settings[1]
            settings_dict = {k: v for k, v in zip(header, details)}
        except (KeyError, IndexError):
            # KeyError: Worksheet does not exist.
            # IndexError: Does not have the correct rows.
            pass
        return settings_dict

    @staticmethod
    def get_choices(wb, ws):
        """Extract choices from an XLSForm.

        Args:
            wb (Xlsform): A Xlsform object representing ODK form.
            ws (Worksheet): One of 'choices' or 'external_choices'.

        Returns:
            dict: A dictionary of choice list names with list of choices
                options for each list.

        Raises:
            OdkformError: Catches instances where list specified in the
                'survey' worksheet, but the list does not appear in the
                designated 'choices' or 'external_choices' worksheet.
        """
        formatted_choices = {}
        try:
            choices = wb[ws]
            header = [str(x) for x in choices[0]]

            if "list_name" not in header:
                msg = 'Column "list_name" not found in {} tab'.format(ws)
                raise OdkFormError(msg)

            for i, row in enumerate(choices):
                if i == 0:
                    continue
                dict_row = {str(k): str(v) for k, v in zip(header, row)}
                list_name = dict_row["list_name"]
                if list_name in formatted_choices:
                    formatted_choices[list_name].add(dict_row)
                elif list_name:  # Not "else:" because possibly blank rows.
                    odkchoices = OdkChoices(list_name)
                    odkchoices.add(dict_row)
                    formatted_choices[list_name] = odkchoices
        except (KeyError, IndexError):  # Worksheet does not exist.
            pass
        return formatted_choices

    @staticmethod
    def get_title(settings, wb, lang=None):
        """Get questionnaire title.

        Args:
        settings (dict): A dictionary represetnation of the original 'settings'
            worksheet of an ODK XLSForm.
        wb (Workbook): A Workbook object representing an XLSForm.
        lang (str): The requested render language of the form.

        Returns:
            str: The title.
        """
        lookup_title = "form_title"
        if lang:
            try1 = settings.get("ppp_form_title" + "::" + lang)
            try2 = settings.get("ppp_form_title" + ":" + lang)
            lookup_title = try1 if try1 else try2
        backup_title = os.path.split(wb.filename)[1]
        return settings.get(lookup_title, backup_title)

    @staticmethod
    def _get_name_to_q_num_map(prompt_list):
        """Get map of variable name to question number in question list.

        Args:
        prompt_list (list): A list of objects representing form components.

        Returns:
            dict: Map of all variable names to question numbers for all
            questions in a given prompt_list.
        """
        qnum_map = {}

        for item in prompt_list:
            if isinstance(item, OdkPrompt):
                qnum_map[item.row["name"]] = item.row["question_number"]
            if isinstance(item, OdkTable):
                qnum_map = {**qnum_map, **OdkForm._get_name_to_q_num_map(item.data)}
            elif any([isinstance(item, x) for x in (OdkCalculate, OdkCustomType)]):
                qnum_map[item.row["name"]] = ""
            elif any(isinstance(item, x) for x in (OdkRepeat, OdkGroup)):
                qnum_map[item.row["name"]] = ""
                qnum_map = {**qnum_map, **OdkForm._get_name_to_q_num_map(item.data)}

        return qnum_map

    @staticmethod
    def _set_name_refs_to_q_nums(prompt_list, question_map):
        """Set question numbers for all variable name refs in relevants.

        Using 'map', mutate the 'relevant' attribute of all prompts [OdkPrompt]
        so that any references to a question variable name are converted to a
        question number.

        Args:
        prompt_list (list): A list of objects representing form components.
        question_map (dict): Map of all variable names to question numbers for
            all questions/prompts in a given questionnaire.

        Returns:
            list: A new prompt list.
        """
        logic_field_variations = (
            RELEVANCE_FIELD_TOKENS,
            ("calculation",),
            ("choice_filter",),
        )
        new_list = []

        for item in prompt_list:
            if any(isinstance(item, x) for x in (OdkPrompt, OdkCalculate)):
                for variations in logic_field_variations:
                    for fld_name in variations:
                        try:
                            fld = item.row[fld_name]
                        except KeyError:
                            continue
                        if fld:
                            matches = re.findall(r"\${[a-zA-Z0-9-_]*}", fld)
                            for m in matches:
                                if not m[2:-1] in ODK_SUPERGLOBALS:
                                    m2 = m.replace("${", "").replace("}", "")
                                    if m2 in question_map and question_map[m2]:
                                        fld = fld.replace(m, question_map[m2])
                                        item.row[fld_name] = fld
                new_list.append(item)
            elif any(isinstance(item, x) for x in (OdkRepeat, OdkGroup, OdkTable)):
                item.data = OdkForm._set_name_refs_to_q_nums(item.data, question_map)
                new_list.append(item)

        return new_list

    def to_text(self, lang=None):
        """Get the text representation of an entire XLSForm.

        Args:
            lang (str): The language.

        Returns:
            str: The detailed string of the XLSForm, ready to print or save.
        """
        title_lines = (
            "+{:-^50}+".format(""),
            "|{:^50}|".format(self.title),
            "+{:-^50}+".format(""),
        )
        title_box = "\n".join(title_lines)

        q_text = (q.to_text(lang) for q in self.questionnaire)
        sep = "\n\n" + "=" * 52 + "\n\n"
        result = sep.join(q_text)
        return title_box + sep + result + sep  # TODO: Finish below to_dict or

    # TODO: change debug feature. If fixed, change to_json to
    # TODO: call dump return of this method instead of raw data.

    # def to_dict(self, lang):
    #     """Get the dictionary representation of an entire XLSForm.
    #
    #     Args:
    #         lang (str): The language.
    #
    #     Returns:
    #         dict: A detailed dictionary representation of the XLSForm.
    #
    #     """
    #     lang = lang if lang \
    #         else self.languages['language_list']['default_language']
    #     html_questionnaire = {
    #         'title': self.title,
    #         'questions': []
    #     }
    #     for item in self.questionnaire:
    #         html_questionnaire['questions'].append(item.to_dict(lang))
    #     return html_questionnaire

    def to_json(self, pretty=False):
        """Get the JSON representation of raw ODK form.

        Args:
            pretty (bool): Activates prettification, involving insertion of
                several kinds of whitespace for readability.

        Returns:
            json: A detailed JSON representation of the XLSForm.
        """
        import json

        raw_survey = []
        header = self.metadata["raw_data"]["survey"][0]
        for i, row in enumerate(self.metadata["raw_data"]["survey"]):
            if i == 0:
                continue
            raw_survey.append({str(k): str(v) for k, v in zip(header, row)})

        if pretty:
            return json.dumps(raw_survey, indent=2)
        return json.dumps(raw_survey)

    @staticmethod
    def _add_question_iter_nums(obj, data={"qnum": "", "i": 0}, depth=0):
        """Add iteration numbers to unique question prompts.

        Possible improvements: Make it so that this doesn't depend on
        OdkPrompt._extract_question_numbers.

        Args:
            obj (list): From either: OdkForm.questionnaire (a list of objects
            representing form components.), OdkGroup.row, or OdkRepeat.row.
            data (dict): Running data. Tracks current question number 'qnum'
            and also current iteration 'i'. The 'i' should increment by 1 for
            each new question number. In this case, a question number is
            rigidly considered "new" if it is not exactly equal to whatever
            was considered to be the immediately preceding question number
            in the form.
            depth (int): Recursion depth. Starts at 0. Increments by 1 each
            time this function recurses, which happens every time an OdkRepeat
            or OdkGroup is encountered.

        Returns:
            list: OdkForm.questionnaire with new 'i' values included.
        """
        for i, element in enumerate(obj):
            if any(isinstance(element, x) for x in (OdkRepeat, OdkGroup, OdkTable)):
                element.data, data = OdkForm._add_question_iter_nums(
                    element.data, data, depth + 1
                )
            elif isinstance(element, OdkPrompt):
                element.row = OdkPrompt.extract_question_numbers(element.row)
                qnum = element.row["question_number"]
                if qnum not in (data["qnum"], ""):
                    data["i"] += 1
                    data["qnum"] = qnum
                element.row["i"] = data["i"]
            elif isinstance(element, OdkCalculate):
                element.row["i"] = data["i"]
        if depth == 0:
            return obj
        return obj, data

    def to_html(self, lang=None, **kwargs):
        """Get the JSON representation of an entire XLSForm.

        Args:
            lang (str): The language.
            **highlight (bool): For color highlighting of various components

            **debug (bool): For inclusion of debug information to be printed
                in the JavaScript console.

        Returns:
            str: A detailed HTML representation of the XLSForm.
        """
        render_calculates = True
        language = lang if lang else self.language
        debug = True if "debug" in kwargs and kwargs["debug"] else False
        html_questionnaire = ""
        qre = self.questionnaire
        if "template" not in kwargs:
            kwargs["template"] = "standard"
        if kwargs["template"] == "standard":
            name_to_q_nums = OdkForm._get_name_to_q_num_map(qre)
            qre = OdkForm._set_name_refs_to_q_nums(qre, name_to_q_nums)
            # render_calculates = False
        data = {
            "header": {
                "title": self.get_title(
                    settings=self.settings, wb=self.metadata["raw_data"], lang=lang
                )
            },
            "footer": {"data": self.to_json(pretty=True) if debug else "false"},
            "questionnaire": qre,
        }

        # - Render Header
        # pylint: disable=no-member
        header = TEMPLATE_ENV.get_template("header.html").render(
            data=data["header"],
            render_image=False if kwargs["format"] == "doc" else True,
            **kwargs,
            settings=kwargs
        )
        # pylint: disable=no-member
        grp_spc = TEMPLATE_ENV.get_template("content/group/group-spacing.html").render()
        html_questionnaire += header

        # - Render Body
        prev_item = None
        for index, item in enumerate(data["questionnaire"]):
            if exclusion(item=item, settings=kwargs):
                continue
            if isinstance(item, OdkCalculate):
                item.renderable = render_calculates
            if prev_item is not None and isinstance(item, OdkGroup):
                html_questionnaire += grp_spc
            elif isinstance(prev_item, OdkGroup) and not isinstance(item, OdkGroup):
                html_questionnaire += grp_spc
            if (
                isinstance(item, OdkPrompt)
                and item.is_section_header
                and isinstance(data["questionnaire"][index + 1], OdkGroup)
            ):
                html_questionnaire += item.to_html(
                    lang=language, **kwargs, bottom_border=True
                )
            else:
                html = item.to_html(lang=language, **kwargs)
                html_questionnaire += html
            prev_item = item

        # pylint: disable=no-member
        footer = TEMPLATE_ENV.get_template("footer.html").render(
            info=None,
            warnings="false",  # to-do: no warnings yet
            data=data["footer"]["data"],
            **kwargs,
            settings=kwargs
        )
        html_questionnaire += footer

        return html_questionnaire

    @staticmethod
    def parse_select_type(row, choices, ext_choices):
        """Extract relevant information from a select_* ODK prompt.

        Build a dictionary that distills the main details of the row. The
        select type questions can have a token type of 'prompt' or 'table'.
        The prompt type is default, and table type is if the appearance of the
        question has either 'label' or 'list-nolabel'.

        Args:
            row (dict): A row as a dictionary. Keys and values are strings.
            choices (dict): A diction   ary with list_names as keys. Represents
                the choices found in 'choices' tab.
            ext_choices (dict): A dictionary with list_names as keys.
                Represents choices found in 'external_choices' tab.

        Returns:
            A dictionary with the simple information about this prompt.

        Raises:
            OdkFormError: If the row is not select_[one|multiple](_external)?
            KeyError: If the select question's choice list is not found.
        """
        simple_row = {"token_type": "prompt"}
        simple_type = "select_one"
        row_type = row["type"]
        list_name = row_type.split(maxsplit=1)[1]

        try:
            if row_type.startswith("select_one_external "):
                choice_list = ext_choices[list_name]
            elif row_type.startswith("select_multiple_external "):
                simple_type = "select_multiple"
                choice_list = ext_choices[list_name]

            elif row_type.startswith("select_one "):
                choice_list = choices[list_name]
            elif row_type.startswith("select_multiple "):
                simple_type = "select_multiple"
                choice_list = choices[list_name]
            else:
                raise OdkFormError()
        except KeyError:
            raise OdkFormError("List '{}' not found.".format(list_name))

        simple_row["simple_type"] = simple_type
        simple_row["choice_list"] = choice_list

        appearance = row.get("appearance", "")
        if appearance in ("label", "list-nolabel"):
            simple_row["token_type"] = "table"

        return simple_row

    @staticmethod
    def parse_group_repeat(row):
        """Extract relevant information about a begin/end group/repeat.

        Args:
            row (dict): A row as a dictionary. Keys and values are strings.

        Returns:
            A dictionary with the simple information about this prompt.

        Raises:
            OdkFormError: If type is not begin/end group/repeat.
        """
        row_type = row["type"]
        token_type = row_type
        appearance = row.get("appearance", "")
        good = ("begin group", "end group", "begin repeat", "end repeat")
        if row_type == "begin group" and "field-list" not in appearance:
            token_type = "context group"
        elif row_type not in good:
            raise OdkFormError()
        simple_row = {"token_type": token_type}
        return simple_row

    @staticmethod
    def make_simple_prompt(row_type):
        """Extract relevant information from an ODK prompt.

        Make the simplest dictionary: token_type is set to 'prompt',
        simple_type is copied from the row type, and choices is set to None.

        Args:
            row_type (str): The type of the row.

        Returns:
            A dictionary with the simple information about this prompt.
        """
        simple_row = {
            "token_type": "prompt",
            "simple_type": row_type,
            "choice_list": None,
        }
        return simple_row

    @staticmethod
    def make_simple_calculate():
        """Make a simple calculate."""
        simple_row = {"token_type": "calculate", "simple_type": "calculate"}
        return simple_row

    @staticmethod
    def make_simple_custom_type():
        """Make a simple custom type."""
        simple_row = {"token_type": "custom"}
        return simple_row

    @staticmethod
    def parse_type(row, choices, ext_choices):
        """Describe the 'type' column of a row XLSForm.

        Args:
            row (dict): A row as a dictionary. Keys and values are strings.
            choices (dict): A dictionary with list_names as keys. Represents
                the choices found in 'choices' tab.
            ext_choices (dict): A dictionary with list_names as keys.
                Represents choices found in 'external_choices' tab.

        Returns:
            dict: simple_row information from parsing.
        """
        row_type = row["type"]
        simple_types = (
            OdkPrompt.visible_response_types + OdkPrompt.visible_non_response_types
        )
        if row_type in simple_types:
            simple_row = OdkForm.make_simple_prompt(row_type)
        elif row_type == "calculate":
            simple_row = OdkForm.make_simple_calculate()
        elif row_type.startswith("select_"):
            simple_row = OdkForm.parse_select_type(row, choices, ext_choices)
        elif row_type.startswith("begin ") or row_type.startswith("end "):
            simple_row = OdkForm.parse_group_repeat(row)
        elif row_type.startswith("hidden"):
            simple_row = OdkForm.make_simple_custom_type()
        else:  # Note - Some other custom token types remain.
            simple_row = {"token_type": "custom", "simple_type": row_type}
        return simple_row

    # pylint: disable=too-many-branches
    @staticmethod
    def convert_survey(wb, choices, ext_choices):
        """Convert rows and strings of a workbook into object components.

        Main types are:

        - prompt
        - calculate
        - begin group
        - end group
        - begin repeat
        - end repeat
        - table
        - context group (group without field-list appearance)

        Args:
            wb (Xlsform): A Xlsform object representing an XLSForm.

        Returns:
            list: A list of objects representing form components.

        Raises:
            OdkformError: Handle several errors, including: mismatched groups
                or repeat groups, errors when appending to groups or repeat
                groups, erroneously formed tables, duplicate context group
                names, and groups nested within a field-list group.
        """
        context = OdkForm.ConversionContext()
        survey, header = None, None
        try:
            survey = wb["survey"]
            header = survey[0]
        except KeyError:  # No survey found.
            pass

        if survey and header:
            for i, row in enumerate(survey):
                if i == 0:
                    continue
                dict_row = {str(k): str(v) for k, v in zip(header, row)}
                token = OdkForm.parse_type(dict_row, choices, ext_choices)

                if token["token_type"] == "prompt":
                    dict_row["simple_type"] = token["simple_type"]
                    choice_list = token["choice_list"]
                    this_prompt = OdkPrompt(dict_row, choice_list)
                    context.add_prompt(this_prompt)
                elif token["token_type"] == "calculate":
                    dict_row["simple_type"] = token["simple_type"]
                    this_calculate = OdkCalculate(dict_row)
                    context.add_calculate(this_calculate)
                elif token["token_type"] == "begin group":
                    this_group = OdkGroup(dict_row)
                    context.add_group(this_group)
                elif token["token_type"] == "context group":
                    # Possibly make an OdkGroup here...
                    context.add_context_group()
                elif token["token_type"] == "end group":
                    context.end_group()
                elif token["token_type"] == "begin repeat":
                    this_repeat = OdkRepeat(dict_row)
                    context.add_repeat(this_repeat)
                elif token["token_type"] == "end repeat":
                    context.end_repeat()
                elif token["token_type"] == "table":
                    dict_row["simple_type"] = token["simple_type"]
                    choice_list = token["choice_list"]
                    this_prompt = OdkPrompt(dict_row, choice_list)
                    context.add_table(this_prompt)
                elif token["token_type"] == "custom":
                    this_custom = OdkCustomType(dict_row)
                    context.add_custom_type(this_custom)
                else:
                    # TODO: Make an error?
                    pass

        return context.result

    class ConversionContext:
        """A class to help questionnaire conversion.

        This class is the context during questionnaire conversion. It
        remembers state, adds components in the correct order, and enforces
        rules during conversion.

        Instance attributes:
            result (list): The list of survey components that is built up
            pending_stack (list): A stack for tracking nested groups and
                repeats.
            group_stack (list): A stck for tracking nested groups and context
                groups.
        """

        def __init__(self):
            """Initialize a conversion context before parsing."""
            self.result = []
            self.pending_stack = []
            self.group_stack = []

        def add_prompt(self, prompt):
            """Add a prompt to the questionnaire.

            If there is an item on the pending stack, it is added there,
            otherwise it is added to the list of components.

            Args:
                prompt (OdkPrompt, OdkCalculate, OdkCustomType): Prompt to add.

            """
            if self.pending_stack:
                self.pending_stack[-1].add(prompt)
            else:
                self.result.append(prompt)

        def add_calculate(self, calculate):
            """Add a calculate to the questionnaire.

            If there is an item on the pending stack, it is added there,
            otherwise it is added to the list of components.

            Args:
                calculate (OdkCalculate): A calculate to add.

            """
            self.add_prompt(calculate)

        def add_custom_type(self, custom_type):
            """Add a calculate to the questionnaire.

            custom_token_types: ['hidden', 'hidden string', 'hidden int',
            'hidden geopoint']

            If there is an item on the pending stack, it is added there,
            otherwise it is added to the list of components.

            Args:
                custom_type (OdkCustomType): A custom type to add.

            """
            self.add_prompt(custom_type)

        def add_group(self, group):
            """Add a group to the pending stack.

            A group can be added to the pending stack as long as it is empty
            or the last pending stack item is a repeat. This is triggered by a
            'begin group' row with a 'field-list' in the appearance.

            Args:
                group (OdkGroup): The group to add to the pending stack.

            Raises:
                OdkFormError: If the parsing rules are broken based on the
                    current context.

            """
            if self.pending_stack:
                last = self.pending_stack[-1]
                if isinstance(last, OdkGroup):
                    msg = "Groups cannot be nested in each other."
                    raise OdkFormError(msg)
            self.pending_stack.append(group)
            self.group_stack.append(group)

        def add_context_group(self):
            """Add a context group to the group stack.

            Context groups are tracked only to help popping groups correctly
            from the pending stack.

            """
            self.group_stack.append(None)

        def end_pending_group(self):
            """End a pending group.

            A pending group is a group on the pending stack. This is not a
            context group. This function is only called internally in response
            to receiving and dealing with an 'end group' type.

            If the pending group is nested in a repeat, then it is added to
            that repeat.

            Raises:
                OdkFormError: If the parsing rules are broken based on the
                    current context.

            """
            if self.pending_stack:
                last_pending = self.pending_stack.pop()
                if not isinstance(last_pending, OdkGroup):
                    msg = "Found end group but no group in pending stack"
                    raise OdkFormError(msg)
                last_pending.add_pending()
                if self.pending_stack:
                    self.pending_stack[-1].add(last_pending)
                else:
                    self.result.append(last_pending)
            else:
                msg = "Found end group but nothing pending stack."
                raise OdkFormError(msg)

        def end_group(self):
            """Finish a group after seeing 'end group' type.

            The 'end group' type can finish a field-list group or a context
            group. This function handles the logic for finishing both types.

            Raises:
                OdkFormError: If the parsing rules are broken based on the
                    current context.

            """
            if self.group_stack:
                last_group = self.group_stack.pop()
                if isinstance(last_group, OdkGroup):
                    self.end_pending_group()
            else:
                msg = "Begin/end group mismatch"
                raise OdkFormError(msg)

        def add_repeat(self, repeat):
            """Add a repeat to the pending stack.

            The pending stack must first be empty because a repeat cannot be
            nested in a group or other repeat.

            Args:
                repeat (OdkRepeat): The repeat to deal with.

            Raises:
                OdkFormError: If the parsing rules are broken based on the
                    current context.

            """
            if not self.pending_stack:
                self.pending_stack.append(repeat)
            else:
                msg = "Unable to nest repeat inside a group or repeat."
                raise OdkFormError(msg)

        def end_repeat(self):
            """Finish a repeat in this questionniare.

            A repeat can be ended only if it is first on the pending stack.

            Raises:
                OdkFormError: If the parsing rules are broken based on the
                    current context.

            """
            if self.pending_stack:
                last_pending = self.pending_stack.pop()
                if isinstance(last_pending, OdkRepeat):
                    self.result.append(last_pending)
                else:
                    msg = "Found end repeat but no repeat in pending stack."
                    raise OdkFormError(msg)
            else:
                msg = "Found end repeat but nothing in pending stack."
                raise OdkFormError(msg)

        def add_table(self, prompt):
            """Add a table row to the questionnaire.

            The table can only be added if there is a group on the pending
            stack.

            Args:
                prompt (OdkPrompt): The prompt representing the table row.

            Raises:
                OdkFormError: If the parsing rules are broken based on the
                    current context.
            """
            if self.pending_stack:
                last_pending = self.pending_stack[-1]
                if not isinstance(last_pending, OdkGroup):
                    msg = "A table can only be in a group. Errored on: {}".format(
                        prompt.row
                    )
                    raise OdkFormError(msg)
                last_pending.add_table(prompt)
            else:
                msg = (
                    "A table can only be in a group, no group found. "
                    "Errored on {}".format(prompt.row)
                )
                raise OdkFormError(msg)
