import logging

logger = logging.getLogger('Formatter')


class RubyCodeParser:
    def __init__(self, target_filename):
        self.target_filename = target_filename
        self.words_list = []
        self.list_of_lines = []
        self.type_of_file = '.rb'
        self.list_name_defs_without_exclamation_mark = []

        self.list_signs = ('=', '==', '!=', '<', '<=', '>', '>=', '+')
        self.list_unnecessary_pref_in_question_def = ('is', 'does', 'can')
        self.list_other_parameter = ('+', '-', '*', '/', '**', '==', '>', '<', '|', '&', '^', 'eql?', 'equal?')
        self.list_item_parameter = ('<<', '[]', '===')

        self.list_of_classes_name = []

    ############

    def parser(self):
        self._get_list_of_lines()

        self.list_of_lines = self._check_variables_in_file()
        self.list_of_lines = self._check_def_in_file()
        self.list_of_lines = self._check_name_of_class()
        self.list_of_lines = self._check_variables_in_def_annotation()
        self.list_of_lines = self._check_other_parameter()
        self.list_of_lines = self._check_variables_in_file_cross_road()
        self.list_of_lines = self._check_foreign_class_method()
        self.list_of_lines = self._check_import_class()

        self.list_of_lines = self._check_comments()
        self.list_of_lines = self._check_comment_annotations()

        final_str = RubyCodeParser._convert_list_to_string(org_list=self.list_of_lines)
        return final_str

    ############

    ''' NAMING '''

    ############

    def check_name_of_file(self, full_name_of_folder):
        name_of_file = RubyCodeParser._get_only_name_of_file(full_name_of_folder)
        name_of_file = self._check_snake_case_format(name_of_file, isFile=True, isExclamationMark=False,
                                                     isQuestionMark=False, isScreaming_case=False)

    def _check_variables_in_file(self):
        new_list_of_lines = []

        for i in range(len(self.list_of_lines)):

            line = self._get_line_by_index(i)

            if line != '':

                words = self._get_words_in_line(line)

                if 'def' in words:
                    new_list_of_lines.append(line)
                    continue
                if '.' in words:
                    new_list_of_lines.append(line)
                    continue

                # print(f'line ---> {line}, words --> {words}')
                word = self._find_name_of_variable_in_words(words)

                new_word = ''

                if self._is_variable(words):
                    # print(f'variable --> {word}')
                    if RubyCodeParser._is_const(word):
                        logger.debug(f'find const')
                        new_word = self._check_snake_case_format(word, isFile=False, isExclamationMark=False,
                                                                 isQuestionMark=False, isScreaming_case=True)
                    else:
                        new_word = self._check_snake_case_format(word, isFile=False, isExclamationMark=False,
                                                                 isQuestionMark=False, isScreaming_case=False)

                if new_word != '':
                    line = RubyCodeParser._change_word_in_line(line, word, new_word)

                new_list_of_lines.append(line)
            else:
                new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_variables_in_file_cross_road(self):
        new_list_of_lines = []

        for i in range(len(self.list_of_lines)):

            line = self._get_line_by_index(i)

            if line != '':

                words = self._get_words_in_line(line)

                if 'def' in words or 'class' in words or '#' in words:
                    new_list_of_lines.append(line)
                    continue

                # print(f'line ---> {line}, words --> {words}')

                for j in range(1, len(words)):
                    if words[j] == '':
                        continue

                    # print(f'word --> |{words[j]}|', end=' ')

                    if words[j].isnumeric():
                        # print('\n')
                        continue
                    if words[j] in self.list_signs:
                        # print('\n')
                        continue
                    if words[j] in self.list_item_parameter:
                        # print('\n')
                        continue
                    if words[j] in self.list_other_parameter:
                        # print('\n')
                        continue
                    if '"' in words[j]:
                        # print('\n')
                        continue
                    if "'" in words[j]:
                        # print('\n')
                        continue
                    if "(" in words[j]:
                        # print('\n')
                        continue
                    if "#" in words[j]:
                        # print('\n')
                        continue
                    if "." in words[j]:
                        # print('\n')
                        continue
                    if "=" in words[j]:
                        # print('\n')
                        continue
                    if RubyCodeParser._is_const(words[j]):
                        continue

                    # print(f' can be var')

                    new_word = self._check_snake_case_format(words[j], isFile=False, isExclamationMark=False,
                                                             isQuestionMark=False, isScreaming_case=False)

                    if ',' in words[j]:
                        new_word += ','

                    line = RubyCodeParser._change_word_in_line(line, words[j], new_word)

                new_list_of_lines.append(line)
            else:
                new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_def_in_file(self):
        new_list_of_lines = []
        self._load_all_names_of_def_without_exclamation_mark()

        for i in range(len(self.list_of_lines)):

            line = self._get_line_by_index(i)

            if line != '':
                words = self._get_words_in_line(line)
                name_of_def = RubyCodeParser._find_name_of_def_in_words(words)
                new_name_of_def = ''
                if name_of_def != '':
                    other_of_def = RubyCodeParser._find_other_of_def_in_words(words)
                    # print(f'line ---> |{line}|, words --> |{words}|')
                    # print(f'def name --> |{name_of_def}|')
                    # print(f'def other --> |{other_of_def}|')

                    if RubyCodeParser._is_method_with_exclamation_mark(name_of_def):

                        # print(f'find method with ! --> |{name_of_def}|')
                        if self.there_is_this_def_without_exclamation_mark(name_of_def):
                            new_name_of_def = self._check_snake_case_format(name_of_def, isFile=False,
                                                                            isExclamationMark=True,
                                                                            isQuestionMark=False,
                                                                            isScreaming_case=False)
                        else:
                            new_name_of_def = self._check_snake_case_format(name_of_def, isFile=False,
                                                                            isExclamationMark=True,
                                                                            isQuestionMark=False,
                                                                            isScreaming_case=False)
                            new_name_of_def = new_name_of_def[:-1]
                            # print(f'def |{name_of_def}| can not be defined')

                    elif RubyCodeParser._is_method_with_question_mark(name_of_def):

                        # print(f'find method with ? --> |{name_of_def}|')

                        if RubyCodeParser._is_unnecessary_pref_and_his_len(name_of_def)[0]:
                            # print(f'find unnecessary pref --> |{name_of_def}|')
                            name_of_def = RubyCodeParser._remove_unnecessary_pref(name_of_def)
                            new_name_of_def = self._check_snake_case_format(name_of_def, isFile=False,
                                                                            isExclamationMark=False,
                                                                            isQuestionMark=True, isScreaming_case=False)

                    else:
                        new_name_of_def = self._check_snake_case_format(name_of_def, isFile=False,
                                                                        isExclamationMark=False,
                                                                        isQuestionMark=False,
                                                                        isScreaming_case=False)

                    if new_name_of_def != '':
                        # print(f'new name of def --> |{new_name_of_def}|')
                        # print(f'other of def --> |{other_of_def}|')
                        line = RubyCodeParser._change_def_name_in_line(line=line, new_name=new_name_of_def,
                                                                       old_name=name_of_def, other=other_of_def)

                        first_part = RubyCodeParser._find_word_def_spaces_before(words)
                        # print(f'first_part = |{first_part}|')
                        #
                        # print(f'new line --> |{line}|')

                    new_list_of_lines.append(line)
                else:
                    new_list_of_lines.append(line)
            else:
                new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_variables_in_def_annotation(self):
        new_list_of_lines = []

        list_variables_in_annotation = []

        for i in range(len(self.list_of_lines)):
            line = self._get_line_by_index(i)

            if line != '':
                words = RubyCodeParser._get_words_in_line(line)

                name_of_def = RubyCodeParser._find_name_of_def_in_words(words)

                if name_of_def != '':

                    tmp_list_variables_in_annotation = []
                    list_value_assignment = []

                    tmp_list_variables_in_annotation = RubyCodeParser._get_variables_in_def_annotation(words)

                    # print(f'find [line] with def --> {words}')
                    # print(f'find line with [def] --> {name_of_def}')
                    # print(f'find vars in def annotation --> {tmp_list_variables_in_annotation}')

                    if tmp_list_variables_in_annotation:

                        for element in tmp_list_variables_in_annotation:
                            # print(f'element --> {element}')

                            value_assignment = RubyCodeParser._get_value_assignment(element)
                            list_value_assignment.append(value_assignment)

                            element.replace(" ", "")
                            checked_element = self._check_snake_case_format(element, isFile=False,
                                                                            isExclamationMark=False,
                                                                            isQuestionMark=False,
                                                                            isScreaming_case=False)
                            list_variables_in_annotation.append(checked_element)

                        # print(f'new vars in annotation --> {list_variables_in_annotation}')
                        # print(f'value_assignment --> {value_assignment}')
                        first_part = RubyCodeParser._find_word_def_spaces_before(words)
                        # print(f'first_part = {first_part}')

                        was_scopes = RubyCodeParser._was_scope_in_name_of_def(words)

                        new_line = RubyCodeParser._create_new_line_with_def_annotation(first_part=first_part,
                                                                                       second_part=list_variables_in_annotation,
                                                                                       list_value_assignment=list_value_assignment,
                                                                                       name_of_def=name_of_def,
                                                                                       was_scopes=was_scopes)
                        list_variables_in_annotation = []
                        # print(f'new_line = |{new_line}|')
                        new_list_of_lines.append(new_line)

                    else:
                        new_list_of_lines.append(line)

                else:
                    new_list_of_lines.append(line)

            else:
                new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_other_parameter(self):

        new_list_of_lines = []

        need_word_other = False
        need_word_item = False

        list_variables_in_annotation = []

        for i in range(len(self.list_of_lines)):
            line = self._get_line_by_index(i)

            if line != '':
                words = RubyCodeParser._get_words_in_line(line)

                name_of_def = RubyCodeParser._find_name_of_def_in_words(words)

                if name_of_def != '':

                    tmp_list_variables_in_annotation = RubyCodeParser._get_variables_in_def_annotation(words)

                    # print(f'find [line] with def --> {words}')
                    # print(f'find line with [def] --> {name_of_def}')
                    # print(f'find vars in def annotation --> {tmp_list_variables_in_annotation}')

                    if name_of_def in self.list_other_parameter:
                        # print(f'find parameter --> {name_of_def} and we should use word other')

                        if tmp_list_variables_in_annotation[0] != 'other':
                            tmp_list_variables_in_annotation[0] = 'other'
                            need_word_other = True

                    elif name_of_def in self.list_item_parameter:
                        # print(f'find parameter --> {name_of_def} and we should use word item')

                        if tmp_list_variables_in_annotation[0] != 'item':
                            tmp_list_variables_in_annotation[0] = 'item'
                            need_word_item = True

                    else:
                        new_list_of_lines.append(line)
                        continue

                    first_part = RubyCodeParser._find_word_def_spaces_before(words)

                    new_line = first_part + ' ' + name_of_def + '(' + tmp_list_variables_in_annotation[0] + ')'
                    # print(f'old line |{line}|')
                    # print(f'new line |{new_line}|')
                    new_list_of_lines.append(new_line)

                else:

                    if need_word_other:
                        need_word_other = False
                        # print(f'need to change word item to other in line: {line}')
                        logger.debug(f'need to change word item to other')
                        line = RubyCodeParser._change_word_in_line(line=line, old_word='item', new_word='other')

                    if need_word_item:
                        need_word_item = False
                        # print(f'need to change word other to item in line: {line}')
                        logger.debug(f'need to change word other to item')
                        line = RubyCodeParser._change_word_in_line(line=line, old_word='other', new_word='item')

                    new_list_of_lines.append(line)

            else:
                new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_name_of_class(self):

        new_list_of_lines = []

        find_first_class = False
        find_one_more_class_in_file = False

        for i in range(len(self.list_of_lines)):

            line = self._get_line_by_index(i)

            if line != '':
                words = self._get_words_in_line(line)
                names_of_classes = RubyCodeParser._find_names_of_classes_in_words(words)

                if names_of_classes:

                    for j in range(len(names_of_classes)):
                        name_of_class = names_of_classes[j]

                        if name_of_class != '':

                            new_name_of_class = self._check_camel_case_format(name_of_folder=name_of_class)
                            new_name_of_class = RubyCodeParser._check_acronyms_format(name_of_folder=new_name_of_class)

                            line = RubyCodeParser._change_word_in_line(line, name_of_class, new_name_of_class)

                            if new_name_of_class != name_of_class:
                                logger.debug(f'You should name {name_of_class} to {new_name_of_class}')
                            else:
                                logger.debug(f'name {name_of_class} is ok')

                            self.list_of_classes_name.append(name_of_class)

                    tmp = RubyCodeParser._get_words_in_line(line)

                    if not find_first_class:
                        find_first_class = True
                    else:
                        if not find_one_more_class_in_file:
                            find_one_more_class_in_file = True

                    if find_one_more_class_in_file:
                        suitable_file_name = self._check_snake_case_format(name_of_folder=tmp[1],
                                                                           isQuestionMark=False, isFile=False,
                                                                           isExclamationMark=False,
                                                                           isScreaming_case=False)

                        logger.debug(
                            f'You should replace {tmp[1]} class to new file, suitable name will be {suitable_file_name}{self.type_of_file} ')

                    for j in range(len(tmp)):
                        if tmp[j] == '':
                            tmp[j] = '<'

                    line = RubyCodeParser._convert_list_to_string(tmp, seperator=' ')

            new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_foreign_class_method(self):

        def _get_words_by_point(word):
            words_chars = RubyCodeParser._get_chars_from_str(word)

            # print(f'chars: {words_chars}')

            find_point = False

            first_word = ''
            second_word = ''

            for i in range(len(words_chars)):

                if words_chars[i] == '.':
                    find_point = True
                    continue

                if not find_point:
                    first_word += words_chars[i]

                if find_point:
                    if words_chars[i] == '(':
                        break
                    second_word += words_chars[i]

            # print(f'first_word = |{first_word}|, second_word = |{second_word}|')

            return [first_word, second_word]

        def _get_part_in_scope(word):
            word_chars = RubyCodeParser._get_chars_from_str(word)

            i = 0
            scope = ''

            find_scope = False

            for i in range(len(word_chars)):
                if word_chars[i] == '(':
                    scope += word_chars[i]
                    find_scope = True
                    continue

                if find_scope:
                    if word_chars[i] == ')':
                        scope += word_chars[i]
                        return scope
                    scope += word_chars[i]

            return scope

        def _get_vars_with_value_in_scope(scope):
            list_of_variables = []

            part_with_annotation = RubyCodeParser._convert_list_to_string(scope, seperator=' ')

            chars = RubyCodeParser._get_chars_from_str(scope)

            # print(f'chars = {chars}')

            if '(' not in chars:
                return list_of_variables

            i = 0

            for i in range(len(chars)):
                if chars[i] == '(':
                    break

            i += 1

            if chars[i] == ')':
                return list_of_variables

            # print(f'chars[i] = {chars[i]}')

            tmp = ''

            while i <= (len(chars) - 1):
                if chars[i] == ',' or chars[i] == ')':
                    list_of_variables.append(tmp)
                    tmp = ''
                    i += 1
                    continue

                if chars[i] != ' ':
                    tmp += chars[i]
                i += 1

            return list_of_variables

        def _fixing_vars_in_scope(vars):

            list_vars_in_scope = []

            for i in range(len(vars)):

                vars_chars = RubyCodeParser._get_chars_from_str(vars[i])

                var = ''
                value_with_rovno = ''

                find_rovno = False

                # for j in range(len(vars_chars)):

                j = 0

                while j < len(vars_chars):
                    if vars_chars[j] == '=':
                        find_rovno = True
                        break
                    var += vars_chars[j]
                    j += 1

                if find_rovno:

                    while j < len(vars_chars):
                        value_with_rovno += vars_chars[j]
                        j += 1


                # print(f'var = {var}')
                var = self._check_snake_case_format(var, isScreaming_case=False, isExclamationMark=False, isQuestionMark=False, isFile=False)

                # print(f'value_with_rovno = {value_with_rovno}')

                list_vars_in_scope.append(var + value_with_rovno)

            return list_vars_in_scope


        new_list_of_lines = []

        find_foreign_class_method = False

        for i in range(len(self.list_of_lines)):

            line = self._get_line_by_index(i)
            # print(f'line = {line}')
            line_chars = RubyCodeParser._get_chars_from_str(line)
            # print(f'line_chars = {line_chars}')

            if line == '':
                new_list_of_lines.append(line)
                continue

            words = self._get_words_in_line(line)

            if 'def' in words:
                new_list_of_lines.append(line)
                continue

            if 'class' in words:
                new_list_of_lines.append(line)
                continue

            for j in range(len(words)):

                if '.' in words[j] and '=' in words:
                    find_foreign_class_method = True
                    logger.debug(f'{line_chars} can be name of class with method')

                    name_of_class = _get_words_by_point(word=words[j])[0]
                    name_of_method = _get_words_by_point(word=words[j])[1]
                    scope = _get_part_in_scope(line_chars)
                    scope = _get_vars_with_value_in_scope(scope)

                    # print(f'[before fixing] name_of_class = |{name_of_class}|, name_of_method = |{name_of_method}|')

                    fix_name_of_class = self._check_camel_case_format(name_of_class)
                    fix_name_of_method = self._check_snake_case_format(name_of_method, isScreaming_case=False,
                                                                       isExclamationMark=False, isQuestionMark=False,
                                                                       isFile=False)

                    # print(f'fix_name_of_class = |{fix_name_of_class}|, fix_name_of_method = |{fix_name_of_method}|')
                    # print(f'part in scope --> {scope}')

                    scope = _fixing_vars_in_scope(scope)
                    # print(f'[fixing]part in scope --> {scope}')

                    tmp_list = words[0:j]
                    start_line = RubyCodeParser._convert_list_to_string(tmp_list, seperator=' ')

                    new_line = start_line + ' ' + fix_name_of_class + '.' + fix_name_of_method + '(' + RubyCodeParser._convert_list_to_string(scope, seperator=', ') + ')'

                    # print(f'[fixing] line --> |{new_line}|')

                    new_list_of_lines.append(new_line)

                elif '.' in words[j] and not '=' in words:
                    find_foreign_class_method = True
                    logger.debug(f'{words[j]} can be object of class with method')

                    name_of_object = _get_words_by_point(word=words[j])[0]
                    name_of_method = _get_words_by_point(word=words[j])[1]
                    scope = _get_part_in_scope(words[j])
                    scope = _get_vars_with_value_in_scope(scope)
                    scope = _fixing_vars_in_scope(scope)

                    fix_name_of_object = self._check_snake_case_format(name_of_object, isScreaming_case=False,
                                                                       isExclamationMark=False, isQuestionMark=False,
                                                                       isFile=False)

                    fix_name_of_method = self._check_snake_case_format(name_of_method, isScreaming_case=False,
                                                                       isExclamationMark=False, isQuestionMark=False,
                                                                       isFile=False)

                    new_line = fix_name_of_object + '.' + fix_name_of_method + '(' + RubyCodeParser._convert_list_to_string(scope, seperator=', ') + ')'

                    new_list_of_lines.append(new_line)

            if not find_foreign_class_method:
                new_list_of_lines.append(line)
            else:
                find_foreign_class_method = False

        return new_list_of_lines

    def _check_import_class(self):

        def is_include(words):
            if 'include' in words:
                return True
            else:
                return False

        def get_names_of_include(words):

            def get_list_name(words):
                return words[1:len(words)]

            names = get_list_name(words)

            for i in range(len(names)):
                if ',' in names[i]:
                    names[i] = names[i].replace(',', '')

            return names

        def fix_names_of_import(list_names):

            for i in range(len(list_names)):
                list_names[i] = self._check_camel_case_format(list_names[i])

            return list_names

        new_list_of_lines = []

        for i in range(len(self.list_of_lines)):

            line = self._get_line_by_index(i)

            if line != '':
                words = self._get_words_in_line(line)

                if is_include(words):

                    logger.debug(f'find line with include --> {line}')

                    list_names_of_include = get_names_of_include(words)

                    # print(f'names of include --> {list_names_of_include}')

                    list_names_of_include = fix_names_of_import(list_names_of_include)

                    # print(f'[fixed] names of include --> {list_names_of_include}')

                    line = 'include ' + RubyCodeParser._convert_list_to_string(list_names_of_include, seperator=', ')

                    # print(f'new_line --> {line}')

            new_list_of_lines.append(line)

        return new_list_of_lines

    ############

    def _check_snake_case_format(self, name_of_folder, isFile, isExclamationMark, isQuestionMark, isScreaming_case):
        if isFile:
            logger.debug(f'verify {name_of_folder}{self.type_of_file}')
        else:
            logger.debug(f'verify {name_of_folder}')

        self.list_char_name = RubyCodeParser._get_chars_from_str(name_of_folder)

        recommend_new_name = ''

        for i in range(len(self.list_char_name)):

            if self.list_char_name[i].isnumeric():
                recommend_new_name += self.list_char_name[i]

            elif self.list_char_name[i].isalpha():

                if self.list_char_name[i].isupper():
                    recommend_new_name += self._verify_big_letter(i)
                else:
                    recommend_new_name += self.list_char_name[i]

            elif self.list_char_name[i] == '_':
                recommend_new_name += self._verify_under_line(i)

            elif self.list_char_name[i] == '@':
                recommend_new_name += self._verify_under_line(i)

            elif self.list_char_name[i] == '.':
                recommend_new_name += self._verify_under_line(i)

        if isFile:
            name_of_folder += self.type_of_file
            recommend_new_name += self.type_of_file

        if isExclamationMark:
            recommend_new_name += '!'

        if isQuestionMark:
            recommend_new_name += '?'

        if isScreaming_case:
            recommend_new_name = recommend_new_name.upper()

        if recommend_new_name != name_of_folder:
            logger.debug(f'You should name {name_of_folder} to {recommend_new_name}')
        else:
            logger.debug(f'name {name_of_folder} is ok')

        return recommend_new_name

    def _check_camel_case_format(self, name_of_folder):

        logger.debug(f'verify {name_of_folder}')

        self.list_char_name = RubyCodeParser._get_chars_from_str(name_of_folder)

        recommend_new_name = ''

        for i in range(len(self.list_char_name)):
            recommend_new_name += self._verify_big_letter_class(i)

        return recommend_new_name

    @staticmethod
    def _check_acronyms_format(name_of_folder):

        acronyms = RubyCodeParser._is_acronyms_and_name_index_first_letter(word=name_of_folder)

        if not acronyms[0]:
            return name_of_folder

        logger.debug(f'verify class name {name_of_folder} for acronyms')

        name_of_folder = name_of_folder[:acronyms[2]]
        name_of_folder += acronyms[1]

        return name_of_folder

    ############

    def _verify_big_letter(self, index):
        recommend_new_name_of_folder = ''
        logger.debug(f'find upper letter --> {self.list_char_name[index]}')
        if index > 0:
            if self.list_char_name[index - 1] != '_':
                recommend_new_name_of_folder += '_'
            recommend_new_name_of_folder += self.list_char_name[index].lower()
            return recommend_new_name_of_folder
        else:
            return self.list_char_name[index].lower()

    def _verify_under_line(self, index):
        recommend_new_name_of_folder = ''
        if index <= len(self.list_char_name):

            if self.list_char_name[index + 1].isnumeric():
                logger.debug(f'find number after {self.list_char_name[index]}')
            else:
                recommend_new_name_of_folder += self.list_char_name[index]
        return recommend_new_name_of_folder

    def _verify_big_letter_class(self, index):
        recommend_char = ''

        if index == 0:

            if self.list_char_name[index].isalpha():

                if not self.list_char_name[index].isupper():
                    logger.debug(f'Find small first letter --> letter will be big')
                    recommend_char += self.list_char_name[index].upper()
                else:
                    recommend_char += self.list_char_name[index]

        else:

            if self.list_char_name[index].isalpha():

                if self.list_char_name[index].isupper():
                    if self.list_char_name[index - 1] == '_':
                        logger.debug(f'Find big letter after _ --> remove _ and letter still big')
                        recommend_char += self.list_char_name[index]
                    else:
                        recommend_char += self.list_char_name[index].lower()
                else:
                    if self.list_char_name[index - 1] == '_':
                        logger.debug(f'Find small letter after _ --> remove _ and letter will be big')
                        recommend_char += self.list_char_name[index].upper()
                    else:
                        recommend_char += self.list_char_name[index]

            elif self.list_char_name[index].isnumeric():

                logger.debug(f'Find numeric --> should be removed')

            elif self.list_char_name[index] == '_':

                logger.debug(f'Find _ --> should be removed')

        return recommend_char

    ############

    def there_is_this_def_without_exclamation_mark(self, word):
        this_def_without_exclamation_mark = RubyCodeParser._get_name_of_def_without_exclamation_mark(word)
        this_def_without_exclamation_mark = RubyCodeParser._get_str_from_chars(this_def_without_exclamation_mark)
        # print(f'{this_def_without_exclamation_mark} <--> {word}')
        if this_def_without_exclamation_mark in self.list_name_defs_without_exclamation_mark:
            return True
        return False

    ############

    def _get_list_of_lines(self):
        with open(self.target_filename) as f:
            lines = f.readlines()

            for i in range(len(lines)):
                cur_line = RubyCodeParser._get_line_of_lines(lines, i)
                self.list_of_lines.append(cur_line[0])

    def _get_line_by_index(self, index):
        if index <= len(self.list_of_lines) - 1:
            return self.list_of_lines[index]
        return None

    ############

    def _load_all_names_of_def_without_exclamation_mark(self):
        for i in range(len(self.list_of_lines)):

            line = self._get_line_by_index(i)

            if line != '':
                words = self._get_words_in_line(line)
                word = RubyCodeParser._find_name_of_def_in_words(words)
                if word != '':
                    if RubyCodeParser._is_method_with_exclamation_mark(word):
                        pass
                    else:
                        self.list_name_defs_without_exclamation_mark.append(word)

    ############

    @staticmethod
    def _change_word_in_line(line, old_word, new_word):
        new_words = []
        words = RubyCodeParser._get_words_in_line(line)
        for word in words:
            if word == old_word:
                new_words.append(new_word)
            else:
                new_words.append(word)

        new_line = ' '.join(new_words)
        return new_line

    @staticmethod
    def _change_def_name_in_line(line, new_name, old_name, other):
        if other == '':
            return RubyCodeParser._change_word_in_line(line, old_name, new_name)

        words = RubyCodeParser._get_words_in_line(line)
        new_words = []
        res = ' '

        for i in range(len(words)):
            if i > 0:
                if words[i - 1] == 'def':
                    new_words.append(new_name)
                    new_words.append(other)
                    res = res.join(new_words)
                    index = res.find('(') - 1
                    res = res[0: index:] + res[index + 1::]
                    return res
                else:
                    new_words.append(words[i])
            else:
                new_words.append(words[i])

    ############

    @staticmethod
    def _get_words_in_line(line):
        return line.split(' ')

    @staticmethod
    def _get_name_of_def_without_exclamation_mark(word):
        res = []
        chars = RubyCodeParser._get_chars_from_str(word)
        for char in chars:
            if char != '!':
                res.append(char)
            else:
                return res

    ############

    def _find_name_of_variable_in_words(self, words):
        prev_word = ''

        for word in words:
            if word in self.list_signs:
                return prev_word
            prev_word = word

        return prev_word

    @staticmethod
    def _find_word_def_spaces_before(words):
        res = []

        for i in range(len(words)):
            if words[i] == 'def':
                res.append(words[i])
                tmp = RubyCodeParser._convert_list_to_string(res, seperator='')
                return tmp

            if words[i + 1] != 'def':
                res.append(' ')

    @staticmethod
    def _find_name_of_def_in_words(words):

        name_of_def = ''

        for i in range(len(words)):
            if i > 0:
                if words[i - 1] == 'def':
                    chars = RubyCodeParser._get_chars_from_str(words[i])

                    if '(' in chars:

                        for j in range(len(chars)):
                            if chars[j] == '(':
                                return name_of_def

                            name_of_def += chars[j]

                    else:
                        return words[i]

        return name_of_def

    @staticmethod
    def _was_scope_in_name_of_def(words):
        for i in range(len(words)):
            if i > 0:
                if words[i - 1] == 'def':
                    chars = RubyCodeParser._get_chars_from_str(words[i])

                    if '(' in chars:
                        return True
                    else:
                        return False

    @staticmethod
    def _find_other_of_def_in_words(words):

        other_of_def = ' '
        chars = []

        tmp_words = []

        for i in range(len(words)):
            if i > 0:
                if words[i - 1] == 'def':
                    tmp_words.append(words[i])

                    for j in range(i + 1, len(words)):
                        tmp_words.append(words[j])

        chars = RubyCodeParser._get_chars_from_str(tmp_words[0])

        if '(' in chars:
            i = 0
            while chars[i] != '(':
                i += 1

            tmp_list = chars[i:]
            tmpListToStr = ''.join([str(elem) for elem in tmp_list])

            tmp_list = tmp_words[1:]

            tmpListToStr2 = ' '.join([str(elem) for elem in tmp_list])

            listToStr = tmpListToStr + ' ' + tmpListToStr2

            return listToStr

        else:
            return other_of_def

    @staticmethod
    def _find_names_of_classes_in_words(words):
        names_of_classes = []

        for i in range(len(words)):
            if i > 0:
                if words[i - 1] == 'class':
                    names_of_classes.append(words[i])

            if words[i] == '<':
                for j in range(i + 1, len(words)):
                    if words[j] != ',':
                        names_of_classes.append(words[j])

        return names_of_classes

    @staticmethod
    def _get_variables_in_def_annotation(words):
        list_of_variables = []
        part_with_annotation = ''

        for i in range(len(words)):
            if i > 0:
                if words[i - 1] == 'def':
                    part_with_annotation = words[i:len(words)]

        part_with_annotation = RubyCodeParser._convert_list_to_string(part_with_annotation, seperator=' ')

        chars = RubyCodeParser._get_chars_from_str(part_with_annotation)

        # print(f'chars = {chars}')

        if '(' not in chars:
            return list_of_variables

        i = 0

        for i in range(len(chars)):
            if chars[i] == '(':
                break

        i += 1

        if chars[i] == ')':
            return list_of_variables

        # print(f'chars[i] = {chars[i]}')

        tmp = ''

        while i <= (len(chars) - 1):
            if chars[i] == ',' or chars[i] == ')':
                list_of_variables.append(tmp)
                tmp = ''
                i += 1
                continue

            if chars[i] != ' ':
                tmp += chars[i]
            i += 1

        # print(f'list_of_variables: {list_of_variables}')
        return list_of_variables

    @staticmethod
    def _get_value_assignment(words):
        chars = RubyCodeParser._get_chars_from_str(words)
        res = ''

        if '=' not in chars:
            return ''

        # print(f'chars = {chars}')

        i = chars.index('=')

        # print(f'i = {i}')

        for j in range(i, len(chars)):
            res += chars[j]

        return res

    ############

    def _is_variable(self, words):
        for word in words:
            if word in self.list_signs:
                return True
        return False

    @staticmethod
    def _is_const(word):
        chars = RubyCodeParser._get_chars_from_str(word)
        const_word = ''

        for i in range(len(chars)):

            if chars[i] == 'C' or chars[i] == 'c':
                const_word += chars[i]

                if i + 4 <= len(chars) - 1:

                    if chars[i + 1] == 'O' or chars[i + 1] == 'o':
                        const_word += chars[i + 1]
                    else:
                        return False

                    if chars[i + 2] == 'N' or chars[i + 2] == 'n':
                        const_word += chars[i + 2]
                    else:
                        return False

                    if chars[i + 3] == 'S' or chars[i + 3] == 's':
                        const_word += chars[i + 3]
                    else:
                        return False

                    if chars[i + 4] == 'T' or chars[i + 4] == 't':
                        const_word += chars[i + 4]
                        return True
                    else:
                        return False
                else:
                    return False

    @staticmethod
    def _is_method_with_exclamation_mark(word):
        list_chars = RubyCodeParser._get_chars_from_str(word)
        if list_chars[len(list_chars) - 1] == '!':
            return True
        return False

    @staticmethod
    def _is_method_with_question_mark(word):
        list_chars = RubyCodeParser._get_chars_from_str(word)
        if list_chars[len(list_chars) - 1] == '?':
            return True
        return False

    @staticmethod
    def _is_unnecessary_pref_and_his_len(word):
        chars = RubyCodeParser._get_chars_from_str(word)
        possible_unnecessary_pref = ''
        for i in range(len(chars)):
            if i == 0:

                if chars[i] == 'i' or chars[i] == 'd' or chars[i] == 'c':
                    possible_unnecessary_pref += chars[i]
                else:
                    return [False, len(possible_unnecessary_pref)]

            elif i == 1:

                if chars[i] == 's' or chars[i] == 'o' or chars[i] == 'a':
                    possible_unnecessary_pref += chars[i]
                else:
                    possible_unnecessary_pref = ''

                if possible_unnecessary_pref == 'is':
                    return [True, len(possible_unnecessary_pref)]

            elif i == 2:

                if chars[i] == 'e' or chars[i] == 'n':
                    possible_unnecessary_pref += chars[i]
                else:
                    possible_unnecessary_pref = ''

                if possible_unnecessary_pref == 'can':
                    return [True, len(possible_unnecessary_pref)]

            elif i == 3:

                if chars[i] == 's':
                    possible_unnecessary_pref += chars[i]
                else:
                    possible_unnecessary_pref = ''

                if possible_unnecessary_pref == 'does':
                    return [True, len(possible_unnecessary_pref)]

            else:
                return [False, len(possible_unnecessary_pref)]

    @staticmethod
    def _is_acronyms_and_name_index_first_letter(word):
        chars_list = RubyCodeParser._get_chars_from_str(word)

        for i in range(len(chars_list)):

            if chars_list[i] == 'x' or chars_list[i] == 'X':
                if i + 2 <= len(chars_list) - 1:
                    if chars_list[i + 1] == 'm' or chars_list[i + 1] == 'M':
                        if chars_list[i + 2] == 'l' or chars_list[i + 2] == 'L':
                            logger.debug(f'Find acronyms XML')
                            return [True, 'XML', i]

            elif chars_list[i] == 'r' or chars_list[i] == 'R':
                if i + 2 <= len(chars_list) - 1:
                    if chars_list[i + 1] == 'f' or chars_list[i + 1] == 'F':
                        if chars_list[i + 2] == 'c' or chars_list[i + 2] == 'C':
                            logger.debug(f'Find acronyms RFC')
                            return [True, 'RFC', i]

            elif chars_list[i] == 'h' or chars_list[i] == 'H':
                if i + 2 <= len(chars_list) - 1:
                    if chars_list[i + 1] == 't' or chars_list[i + 1] == 'T':
                        if chars_list[i + 2] == 't' or chars_list[i + 2] == 'T':
                            if chars_list[i + 3] == 'p' or chars_list[i + 3] == 'P':
                                logger.debug(f'Find acronyms HTTP')
                                return [True, 'HTTP', i]

        return [False, '', 0]

    @staticmethod
    def _remove_unnecessary_pref(word):
        chars = RubyCodeParser._get_chars_from_str(word)

        count = RubyCodeParser._is_unnecessary_pref_and_his_len(word)[1]
        # print(f'count = {count}')

        del chars[0:count]

        if chars[0] == '_':
            del chars[0]

        # print(f'chars = {chars}')

        new_word = RubyCodeParser._get_str_from_chars(chars)
        return new_word

    ############

    @staticmethod
    def _get_only_name_of_folder(full_name_of_folder):
        list_chars = RubyCodeParser._get_chars_from_str(full_name_of_folder)
        list_name_of_folder = []

        i = len(list_chars) - 1
        while list_chars[i] != '/':
            list_name_of_folder.append(list_chars[i])
            i -= 1

        list_name_of_folder.reverse()
        return RubyCodeParser._get_str_from_chars(list_name_of_folder)

    @staticmethod
    def _get_only_name_of_file(full_name_of_folder):
        list_chars = RubyCodeParser._get_chars_from_str(full_name_of_folder)
        list_name_of_folder = []

        j = 0
        i = len(list_chars) - 1
        while list_chars[i] != '.':
            i -= 1
            j += 1
        j += 1

        i = len(list_chars) - 1 - j
        while list_chars[i] != '/':
            # print(list_chars[i])
            list_name_of_folder.append(list_chars[i])
            i -= 1

        list_name_of_folder.reverse()
        return RubyCodeParser._get_str_from_chars(list_name_of_folder)

    @staticmethod
    def _get_chars_from_str(str):
        return [char for char in str]

    @staticmethod
    def _get_str_from_chars(chars_list):
        str = ""

        for char in chars_list:
            str += char

        return str

    @staticmethod
    def _convert_list_to_string(org_list, seperator='\n'):
        return seperator.join(org_list)

    @staticmethod
    def _get_line_of_lines(lines, index):
        return lines[index].split('\n')

    @staticmethod
    def _create_new_line_with_def_annotation(first_part, name_of_def, second_part, list_value_assignment, was_scopes):
        line = first_part + ' ' + name_of_def

        if was_scopes:
            line += '('

        if not second_part:
            line += ')'
            return line

        for i in range(len(second_part)):
            if i < len(second_part) - 1:
                line += second_part[i] + list_value_assignment[i] + ', '
            else:
                line += second_part[i] + list_value_assignment[i] + ')'

        return line

    ############

    ''' COMMENTS '''

    ############

    def _check_comments(self):
        new_list_of_lines = []
        was_line_with_comment = False

        for i in range(len(self.list_of_lines)):
            line = self._get_line_by_index(i)

            if RubyCodeParser._is_only_comment_in_line(line):
                was_line_with_comment = True
                comment = RubyCodeParser._get_comment_and_code_in_line(line)[0]
                code = RubyCodeParser._get_comment_and_code_in_line(line)[1]
                logger.debug(f'line: {i + 1} --> find comment --> {comment}')
                comment_new = RubyCodeParser._check_space_after_grid(comment=comment, index_line=i)

                if comment != comment_new:
                    line = code + comment_new
                    logger.debug(f'line: {i + 1} --> comment after fixing --> {comment_new}')
                else:
                    logger.debug(f'line: {i + 1} --> comment is good')

            elif line == '':
                if was_line_with_comment:
                    was_line_with_comment = False
                    logger.debug(f'line: {i + 1} --> need to delete ENTER')
                    continue

            new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_comment_annotations(self):
        self.list_of_lines = self._check_lines_with_code_and_comments_together(list_of_lines=self.list_of_lines)
        self.list_of_lines = self._check_double_points_after_keyword(list_of_lines=self.list_of_lines)
        self.list_of_lines = self._check_comments_between_lines(list_of_lines=self.list_of_lines)

        return self.list_of_lines

    def _check_lines_with_code_and_comments_together(self, list_of_lines):
        new_list_of_lines = []

        for i in range(len(list_of_lines)):
            line = self._get_line_by_index(i)

            if RubyCodeParser._is_comment_in_line(line):
                comment = RubyCodeParser._get_comment_and_code_in_line(line)[0]
                code = RubyCodeParser._get_comment_and_code_in_line(line)[1]

                if code != '':
                    logger.debug(f'line: {i + 1} --> find comment [{comment}] in one line with code')
                    logger.debug(f'line: {i + 1} --> delete this comment from current')
                    line = code
                    logger.debug(f'line: {i + 1} --> replace this comment to one line up')
                    new_list_of_lines.append('')
                    comment_new = RubyCodeParser._check_space_after_grid(comment=comment, index_line=i)
                    new_list_of_lines.append(comment_new)

            new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_comments_between_lines(self, list_of_lines):
        new_list_of_lines = []
        was_line_with_comment = False

        for i in range(len(list_of_lines)):

            line = self._get_line_by_index(i)

            if line is not None:

                if RubyCodeParser._is_comment_in_line(line):

                    if was_line_with_comment:

                        line = RubyCodeParser._add_2_extra_spaces_after_grid(line)
                        new_list_of_lines.append(line)
                        continue
                    else:
                        was_line_with_comment = True
                else:
                    was_line_with_comment = False

                new_list_of_lines.append(line)

        return new_list_of_lines

    def _check_double_points_after_keyword(self, list_of_lines):
        new_list_of_lines = []

        for i in range(len(list_of_lines)):

            line = self._get_line_by_index(i)

            if line is not None:
                if RubyCodeParser._is_comment_in_line(line):
                    line = RubyCodeParser._make_double_points_in_line(line)

            new_list_of_lines.append(line)

        return new_list_of_lines

    def _minimize_spaces(self):
        for i in range(len(self.list_of_lines)):
            self.list_of_lines[i] = ' '.join(self.list_of_lines[i].split())

    @staticmethod
    def _is_only_comment_in_line(line):
        chars = RubyCodeParser._get_chars_from_str(line)

        for i in range(len(chars)):

            if chars[i] == ' ':
                continue

            if chars[i] != ' ' and chars[i] != '#':
                return False

            if chars[i] == '#':
                return True

        return False

    @staticmethod
    def _is_comment_in_line(line):
        chars = RubyCodeParser._get_chars_from_str(line)

        for i in range(len(chars)):

            if chars[i] == '#':
                return True

        return False

    @staticmethod
    def _get_comment_and_code_in_line(line):
        chars = RubyCodeParser._get_chars_from_str(line)
        comment = ''
        not_comment = ''

        find_comment = False

        for i in range(len(chars)):

            if chars[i] == '#':
                find_comment = True

            if find_comment:
                comment += chars[i]
            else:
                not_comment += chars[i]

        return [comment, not_comment]

    @staticmethod
    def _check_space_before_grid(code, index_line):
        code = RubyCodeParser._get_chars_from_str(code)

        if code[len(code) - 1] != ' ':
            logger.debug(f'line: {index_line + 1} --> there isn\'t space before #')
            code.insert(index_line - 1, ' ')

        code = RubyCodeParser._get_str_from_chars(code)
        return code

    @staticmethod
    def _check_space_after_grid(comment, index_line):
        comment = RubyCodeParser._get_chars_from_str(comment)

        for i in range(len(comment)):

            if comment[i] == '#':
                if i + 1 < len(comment) - 1:
                    if comment[i + 1] != ' ':
                        logger.debug(f'line: {index_line + 1} --> there isn\'t space after #')
                        comment.insert(i + 1, ' ')
                    else:
                        i += 1
                        while comment[i] == ' ':
                            comment.pop(i)
                        comment.insert(i, ' ')
                        break

        comment = RubyCodeParser._get_str_from_chars(comment)
        return comment

    @staticmethod
    def _add_2_extra_spaces_after_grid(line):
        comment = RubyCodeParser._get_comment_and_code_in_line(line)[0]
        chars = RubyCodeParser._get_chars_from_str(comment)

        start = chars.index('#')
        end = 0

        for i in range(start + 1, len(chars)):
            if chars[i] == ' ':
                end += 1
                continue
            break

        del chars[start + 1:end]

        chars.insert(1, ' ')
        chars.insert(1, ' ')
        comment = RubyCodeParser._get_str_from_chars(chars)
        return comment

    @staticmethod
    def _make_double_points_in_line(line):
        comment = RubyCodeParser._get_comment_and_code_in_line(line)[0]
        chars = RubyCodeParser._get_chars_from_str(comment)

        for i in range(len(chars)):
            if chars[i] == 'T':
                i = i + 1
                if chars[i] == 'O':
                    i = i + 1
                    if chars[i] == 'D':
                        i = i + 1
                        if chars[i] == 'O':
                            i = i + 1
                            chars = RubyCodeParser._add_double_point_and_spaces_after_keyword(chars=chars, index=i)
                            break

            if chars[i] == 'H':
                i = i + 1
                if chars[i] == 'A':
                    i = i + 1
                    if chars[i] == 'C':
                        i = i + 1
                        if chars[i] == 'K':
                            i = i + 1
                            chars = RubyCodeParser._add_double_point_and_spaces_after_keyword(chars=chars, index=i)
                            break

            if chars[i] == 'F':
                i = i + 1
                if chars[i] == 'I':
                    i = i + 1
                    if chars[i] == 'X':
                        i = i + 1
                        if chars[i] == 'M':
                            i = i + 1
                            if chars[i] == 'E':
                                i = i + 1
                                chars = RubyCodeParser._add_double_point_and_spaces_after_keyword(chars=chars, index=i)
                                break

            if chars[i] == 'R':
                i = i + 1
                if chars[i] == 'E':
                    i = i + 1
                    if chars[i] == 'V':
                        i = i + 1
                        if chars[i] == 'I':
                            i = i + 1
                            if chars[i] == 'E':
                                i = i + 1
                                if chars[i] == 'W':
                                    i = i + 1
                                    chars = RubyCodeParser._add_double_point_and_spaces_after_keyword(chars=chars,
                                                                                                      index=i)
                                    break

            if chars[i] == 'O':
                i = i + 1
                if chars[i] == 'P':
                    i = i + 1
                    if chars[i] == 'T':
                        i = i + 1
                        if chars[i] == 'I':
                            i = i + 1
                            if chars[i] == 'M':
                                i = i + 1
                                if chars[i] == 'I':
                                    i = i + 1
                                    if chars[i] == 'Z':
                                        i = i + 1
                                        if chars[i] == 'E':
                                            i = i + 1
                                            chars = RubyCodeParser._add_double_point_and_spaces_after_keyword(
                                                chars=chars, index=i)
                                            break

        comment = RubyCodeParser._get_str_from_chars(chars)
        return comment

    @staticmethod
    def _add_double_point_and_spaces_after_keyword(chars, index):
        if chars[index] != ':':
            chars.insert(index, ':')
            i = index + 1
            if chars[i] != ' ':
                chars.insert(i, ' ')
        elif chars[index] == ':':
            chars.insert(index + 1, ' ')

        return chars
