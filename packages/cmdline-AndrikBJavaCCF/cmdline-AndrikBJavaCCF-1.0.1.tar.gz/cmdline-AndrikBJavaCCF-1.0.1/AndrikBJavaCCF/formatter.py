import logging
import re
from os import chdir, listdir, rename
from os.path import dirname, abspath
from pathlib import Path

from .lexer import TokenType, Token, Position


def get_files_rec(path):
    return list(Path(path).rglob("*.[jJ][aA][vV][aA]"))


def get_files(path):
    return list(Path(path).glob("*.[jJ][aA][vV][aA]"))


def print_files(files):
    for file in files:
        file.print_file()


def format_files(files):
    formatter = Formatter(files)
    formatter.format_files()


def validate(files):
    format_files(files)
    logging.basicConfig(filename='verification.log', level=logging.WARN)
    for file in files:
        for token in file.tokens:
            if token.value != token.second_value and token.token_type in (TokenType.comment, TokenType.identifier):
                logging.warn(f'{file.filename}\t {token.position.row}:{token.position.column}\t -> '
                             f'expected {token.second_value}, actual {token.value}')


def rename_dirs(files):
    for file in files:
        chdir(dirname(abspath(file.filename)))
        for package in file.packages:
            chdir('..')
            if package[0] in listdir():
                if package[0] != package[1]:
                    rename(package[0], package[1])
            else:
                break


def fix(files):
    format_files(files)
    logging.basicConfig(filename='fixing.log', level=logging.WARN)
    for file in files:
        for token in file.tokens:
            if token.value != token.second_value and token.token_type in (TokenType.comment, TokenType.identifier):
                logging.warn(f'{file.filename}\t {token.position.row}:{token.position.column}\t replace '
                             f'{token.value} -> {token.second_value}')
    print_files(files)
    rename_dirs(files)


def start_tests():
    files = ('no_changes', 'add_comments', 'change_comment', 'rename_fields', 'rename_class')
    chdir('tests')
    for file in files:
        try:
            file_before = open(file+'_before.java')
            print('opened')
        except Exception as e:
            print(f'something was wrong with files {file}_before.java and {file}_after.java')
            print(e)
    pass


class_interface_enum = ('class', 'interface', 'enum', '@interface')


class Formatter:

    def __init__(self, files):
        self.files = files

    @staticmethod
    def get_next_no_whitespace_token_id(file, _id):
        while _id + 1 < len(file.tokens):
            _id += 1
            if file.tokens[_id].token_type != TokenType.whitespace:
                return _id
        return -1

    @staticmethod
    def get_prev_no_whitespace_token_id(file, _id):
        while _id < len(file.tokens):
            _id -= 1
            if file.tokens[_id].token_type != TokenType.whitespace:
                return _id
        return -1

    @staticmethod
    def get_previous_token_id_with_such_value(tokens, i, values):
        while i > 0:
            i -= 1
            if tokens[i].value in values:
                return i
        return -1

    def replace_all_tokens_like_this(self, token):
        for file in self.files:
            for file_token in file.tokens:
                if file_token.value == token.value:
                    file_token.second_value = token.second_value

    @staticmethod
    def to_upper(string, i):
        if len(string) == i:
            return string
        return string[:i] + string[i].upper() + string[i + 1:]

    @staticmethod
    def to_lower(string, i):
        if len(string) == i:
            return string
        return string[:i] + string[i].lower() + string[i + 1:]

    @staticmethod
    def insert_into_string(string, i, value):
        if len(string) == i:
            return string + value
        return string[:i] + value + string[i:]

    # replace
    @staticmethod
    def replace_underscore_to_uppercase(token):
        i = 0
        while i < len(token.second_value):
            if token.second_value[i] == '_':
                token.second_value = token.second_value.replace('_', '', 1)
                token.second_value = Formatter.to_upper(token.second_value, i)
            i += 1

    @staticmethod
    def is_camel_case_first_up(token):
        return re.search('^[A-Z][a-zA-Z0-9]*$', token.second_value)

    def replace_to_camel_case_first_up(self, token):
        if Formatter.is_camel_case_first_up(token) or token.token_type != TokenType.identifier:
            return

        if Formatter.is_upper_case(token):
            token.second_value = token.second_value.lower()

        Formatter.replace_underscore_to_uppercase(token)
        token.second_value = Formatter.to_upper(token.second_value, 0)

        if not Formatter.is_camel_case_first_up(token):
            print(f'wtf in token camel_case_first_up: {token}')

        self.replace_all_tokens_like_this(token)

    @staticmethod
    def fix_filename(file):
        filename = Token(TokenType.identifier, file.new_filename)

        if Formatter.is_upper_case(filename):
            file.new_filename = file.new_filename.lower()

        Formatter.replace_underscore_to_uppercase(filename)
        file.new_filename = Formatter.to_upper(filename.second_value, 0)

    @staticmethod
    def is_camel_case_first_down(token):
        return re.search('^[a-z][a-zA-Z0-9]*$', token.second_value)

    def replace_to_camel_case_first_down(self, token):
        if Formatter.is_camel_case_first_down(token) or token.token_type != TokenType.identifier:
            return

        if Formatter.is_upper_case(token):
            token.second_value = token.second_value.lower()

        Formatter.replace_underscore_to_uppercase(token)
        token.second_value = Formatter.to_lower(token.second_value, 0)

        if not Formatter.is_camel_case_first_down(token):
            print('wtf in token case_first_down: ' + token)

        self.replace_all_tokens_like_this(token)

    @staticmethod
    def is_upper_case(token):
        return re.search('^([A-Z0-9]*_*)*$', token.second_value)

    def replace_to_upper_case(self, token):
        if Formatter.is_upper_case(token) or token.token_type != TokenType.identifier:
            return

        token.second_value = Formatter.to_lower(token.second_value, 0)

        i = 1
        while i < len(token.second_value):
            if token.second_value[i].isupper():
                token.second_value = Formatter.to_lower(token.second_value, i)
                token.second_value = Formatter.insert_into_string(token.second_value, i, '_')
            i += 1

        for i in range(len(token.second_value)):
            token.second_value = Formatter.to_upper(token.second_value, i)

        if token.second_value[0] == '_':
            token.second_value = token.second_value[1:]
        if token.second_value[-1] == '_':
            token.second_value = token.second_value[:-1]

        self.replace_all_tokens_like_this(token)

    @staticmethod
    def is_method_return(token):
        if token.token_type == TokenType.identifier:
            return True
        return token.value in ('void', 'byte', 'int', 'boolean', 'char', 'long', 'short')


    def replace_to_snake_case(self, token):
        self.replace_to_upper_case(token)
        token.second_value = token.second_value.lower()
        self.replace_all_tokens_like_this(token)

    # fix
    def fix_names(self, file):
        stack = []
        i = 0
        while i < len(file.tokens):
            token = file.tokens[i]

            if token.value == 'package':
                while token.value != ';':
                    i += 1
                    token = file.tokens[i]
                    if token.token_type == TokenType.identifier:
                        self.replace_to_snake_case(token)
                        file.packages.insert(0, (token.value, token.second_value))

            if token.value in class_interface_enum and \
                    file.tokens[Formatter.get_next_no_whitespace_token_id(file, i)].token_type == TokenType.identifier:
                stack.append(token.value)
                class_id = self.get_next_no_whitespace_token_id(file, i)
                self.replace_to_camel_case_first_up(file.tokens[class_id])

            elif ((len(stack) > 0 and stack[-1] in class_interface_enum) or
                  (len(stack) > 1 and stack[-2] in class_interface_enum and stack[-1] == '{')) and token.value == '<':
                generic_stack = [token]
                while len(generic_stack) != 0:
                    i += 1
                    token = file.tokens[i]
                    if token.value == '>':
                        generic_stack.pop()
                    elif token.value == '<':
                        generic_stack.append(token)
                    elif token.token_type == TokenType.identifier:
                        self.replace_to_camel_case_first_up(token)

            elif token.value == '{':
                stack.append(token.value)
            elif token.value == '}':
                stack.pop()
                if len(stack) > 0 and stack[-1] in class_interface_enum:
                    stack.pop()
            elif token.value == '(':
                stack.append(token.value)
            elif token.value == ')':
                stack.pop()

            if token.token_type == TokenType.identifier:
                next_token = file.tokens[self.get_next_no_whitespace_token_id(file, i)]
                prev_token = file.tokens[self.get_prev_no_whitespace_token_id(file, i)]

                if len(stack) > 1 and stack[-2] in class_interface_enum and stack[-1] == '{':  # in class

                    if next_token.value == '(' and Formatter.is_method_return(prev_token):  # is method declaration
                        self.replace_to_camel_case_first_down(token)
                    elif next_token.value in (';', '='):  # is variable
                        end_of_search = Formatter.get_previous_token_id_with_such_value(file.tokens, i, ('{', '}', ';'))
                        if Formatter.get_previous_token_id_with_such_value(file.tokens, i, ('final',)) > end_of_search:
                            # final variable
                            self.replace_to_upper_case(token)
                        else:
                            self.replace_to_camel_case_first_down(token)

                elif len(stack) > 1 and next_token.value == '->':  # in lambda
                    self.replace_to_camel_case_first_down(token)

                elif len(stack) > 2 and stack[-2] == '{' and stack[-1] in ('(', '{'):  # in method
                    if stack[-1] == '(':
                        after_tokens = (')', ',', '[')
                    else:
                        after_tokens = (';', '=', ':')

                    if (prev_token.value in ('>', ']',) or Formatter.is_method_return(prev_token)) and \
                            next_token.value in after_tokens:
                        self.replace_to_camel_case_first_down(token)
            i += 1

    @staticmethod
    def insert_new_line(file, index):
        file.tokens.insert(index, Token(TokenType.whitespace, '\n', file.tokens[index].position))

    @staticmethod
    def add_indents(file, index, indent):
        for i in range(indent):
            file.tokens.insert(index, Token(TokenType.whitespace, ' ', file.tokens[index + i].position))

    @staticmethod
    def fix_documentation_comment(token, indent):
        token.second_value = token.second_value[3:]
        token.second_value = token.second_value[:-2]
        while token.second_value[0].isspace():
            token.second_value = token.second_value[1:]
        while token.second_value[-1].isspace():
            token.second_value = token.second_value[:-1]
        token.second_value = '/**\n' + token.second_value + '\n*/'


        i = 3
        was_newline = False
        while i + 2 < len(token.second_value):
            char = token.second_value[i]
            if char == '\n':
                was_newline = True
                second_part = token.second_value[i:]
                local_i = 0
                while second_part[local_i].isspace():
                    local_i += 1
                if second_part[local_i] == '*':
                    local_i += 1
                while second_part[local_i]== ' ':
                    local_i += 1

                token.second_value = token.second_value[:i + 1] + ' ' * indent + ' *' + second_part[local_i:]
            elif char == '*' and was_newline:
                token.second_value = token.second_value[:i + 1] + ' ' + token.second_value[i + 1:]
                was_newline = False

            i += 1

    @staticmethod
    def fix_beginning_comment(file):
        first_token = file.tokens[Formatter.get_next_no_whitespace_token_id(file, -1)]
        if first_token.value[0:2] != '/*':
            new_token = Token(TokenType.comment, '''/*
 * %W% %E% Firstname Lastname
 *
 * Copyright (c) 1995-2020 %your company name%
 *
 * This software is the confidential and proprietary information of 
 * %your company name%.  You shall not
 * disclose such Confidential Information and shall use it only in
 * accordance with the terms of the license agreement you entered into
 * with %your company name%.
 *
 * %your company name% MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF
 * THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE, OR NON-INFRINGEMENT. SUN SHALL NOT BE LIABLE FOR
 * ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR
 * DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 */''', Position(1, 1))
            file.tokens.insert(0, new_token)
            Formatter.insert_new_line(file, 1)

    @staticmethod
    def get_first_token_id_of_statement(file, index):
        while True:
            whitespace_id = Formatter.get_previous_token_id_with_such_value(file.tokens, index, ('\n',))
            previous_no_whitespace_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, whitespace_id)]
            if not (previous_no_whitespace_token.token_type == TokenType.annotation
                    or previous_no_whitespace_token.value == ')'):
                return Formatter.get_next_no_whitespace_token_id(file, whitespace_id)
            index = whitespace_id

    @staticmethod
    def fix_comment_before_class_declaration(file, class_index):
        class_token = file.tokens[Formatter.get_next_no_whitespace_token_id(file, class_index)]
        class_name = class_token.second_value
        class_type = file.tokens[class_index].value

        first_token_of_statement_id = Formatter.get_first_token_id_of_statement(file, class_index)
        first_token_of_statement = file.tokens[first_token_of_statement_id]
        indent = first_token_of_statement.position.column - 1

        previous_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, first_token_of_statement_id)]

        if previous_token.second_value[0:3] == '/**':  # validate

            previous_token.second_value = previous_token.second_value.replace(class_token.value, class_name)
            if class_name not in previous_token.second_value:
                new_line = '' if previous_token.second_value[3] == '\n' else '\n'
                previous_token.second_value = '/**\n' + ' ' * indent + f' * The {class_name} {class_type} provides ' + \
                                              new_line + previous_token.second_value[3:]

            Formatter.fix_documentation_comment(previous_token, indent)
        else:  # create
            token = Token(TokenType.comment, '', first_token_of_statement.position)
            token.second_value = '/**\n' + ' ' * indent + f' * The {class_name} {class_type} provides \n' + ' ' \
                                 * indent + ' */'

            file.tokens.insert(first_token_of_statement_id, token)
            Formatter.insert_new_line(file, first_token_of_statement_id + 1)
            Formatter.add_indents(file, first_token_of_statement_id + 2, indent)

        while file.tokens[class_index].value != class_type:
            class_index += 1
        return class_index

    @staticmethod
    def fix_comment_before_method_declaration(file, method_name_index):
        i = method_name_index

        def get_method_params():
            local_method_params = []
            nonlocal i
            i = Formatter.get_next_no_whitespace_token_id(file, i)
            token = file.tokens[i]
            local_previous_token = token

            while local_previous_token.value != ')':

                if token.value in (',', ')') and local_previous_token.token_type == TokenType.identifier:
                    local_method_params.append((local_previous_token.value, local_previous_token.second_value))
                elif token.value == '[' and local_previous_token.token_type == TokenType.identifier and \
                        file.tokens[i + 2].value in (',', ')'):
                    local_method_params.append((local_previous_token.value, local_previous_token.second_value))
                elif token.value == '<':
                    count_open = 1
                    while count_open != 0:
                        i += 1
                        if file.tokens[i].value == '<':
                            count_open += 1
                        elif file.tokens[i].value == '>':
                            count_open -= 1

                i += 1
                local_previous_token = token
                token = file.tokens[i]

            return local_method_params

        def get_method_throws():
            local_method_throws = []
            nonlocal i
            i = Formatter.get_next_no_whitespace_token_id(file, i)
            token = file.tokens[i]
            local_previous_token = token
            if token.value == 'throws':

                while local_previous_token.value not in (';', '{'):
                    if token.value in (',', ';', '{'):
                        local_method_throws.append((local_previous_token.value, local_previous_token.second_value))
                    i = Formatter.get_next_no_whitespace_token_id(file, i)
                    local_previous_token = token
                    token = file.tokens[i]

            return local_method_throws

        method_params = get_method_params()
        method_throws = get_method_throws()

        first_token_of_statement_id = Formatter.get_first_token_id_of_statement(file, method_name_index)
        first_token_of_statement = file.tokens[first_token_of_statement_id]
        indent = first_token_of_statement.position.column - 1

        previous_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, first_token_of_statement_id)]
        if previous_token.second_value[0:3] == '/**':  # validate

            for param in method_params:
                previous_token.second_value = previous_token.second_value.replace(param[0], param[1])
            for exception in method_throws:
                previous_token.second_value = previous_token.second_value.replace(exception[0], exception[1])

            Formatter.fix_documentation_comment(previous_token, indent)

        else:  # create
            previous_token = Token(TokenType.comment, f'/**\n{" " * indent} */',
                                   first_token_of_statement.position)
            file.tokens.insert(first_token_of_statement_id, previous_token)
            Formatter.insert_new_line(file, first_token_of_statement_id + 1)
            Formatter.add_indents(file, first_token_of_statement_id + 2, indent)

        separator = ' ' * indent + ' * @'
        blocks = previous_token.second_value.split(separator)
        for i in range(1, len(blocks)):
            blocks[i] = separator + blocks[i]
        end = ' ' * indent + ' */'
        if blocks[-1].endswith(end):
            blocks[-1] = blocks[-1][:-len(end)]
        else:
            blocks[-1] = blocks[-1][:-2]

        blocks.append(end)
        # sort
        new_blocs = [blocks[0]]
        blocks.pop(0)

        def refactor_block_return_name(_block, _name):
            _i = len(separator) + len(_name)
            while _i < len(_block) and _block[_i].isspace():
                _block = _block[:_i] + _block[_i + 1:]
            _block = _block[:_i] + ' ' + _block[_i:]
            next_space = _block.find(' ', _i + 1)
            return _block, _block[_i + 1:next_space].split()[0]

        # @param
        i = 0
        while i < len(blocks):
            if blocks[i].startswith(separator + 'param'):
                block, name = refactor_block_return_name(blocks[i], 'param')
                new_blocs.append(block)
                blocks.pop(i)
                i -= 1

                for _i in range(len(method_params)):
                    if method_params[_i][1] == name:
                        method_params.pop(_i)
                        break

            i += 1

        for param_name in method_params:
            new_blocs.append(separator + 'param ' + param_name[1] + '\n')

        # @return
        i = 0
        current_block = separator + 'return\n'
        while i < len(blocks):
            if blocks[i].startswith(separator + 'return'):
                current_block = blocks[i]
                blocks.pop(i)
                i -= 1
            i += 1
        new_blocs.append(current_block)

        # @throws
        i = 0
        while i < len(blocks):
            if blocks[i].startswith(separator + 'throws'):
                block, name = refactor_block_return_name(blocks[i], 'throws')
                new_blocs.append(block)
                blocks.pop(i)
                i -= 1

                for _i in range(len(method_throws)):
                    if method_throws[_i][1] == name:
                        method_throws.pop(_i)
                        break
            i += 1

        for param_name in method_throws:
            new_blocs.append(separator + 'throws ' + param_name[1] + '\n')

        # other
        for block in blocks:
            new_blocs.append(block)

        previous_token.second_value = ''.join(new_blocs)
        Formatter.fix_documentation_comment(previous_token, indent)

    @staticmethod
    def fix_comment_before_field(file, field_name_id):
        field_token = file.tokens[field_name_id]
        field_name = field_token.second_value
        first_token_of_statement_id = Formatter.get_first_token_id_of_statement(file, field_name_id)
        first_token_of_statement = file.tokens[first_token_of_statement_id]
        indent = first_token_of_statement.position.column - 1

        previous_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, first_token_of_statement_id)]
        if previous_token.second_value[0:3] == '/**':  # validate

            previous_token.second_value = previous_token.second_value.replace(field_token.value, field_name)
            if field_name not in previous_token.second_value:
                new_line = '' if previous_token.second_value[3] == '\n' else '\n'
                previous_token.second_value = '/**\n' + ' ' * indent + f' * The {field_name} documentation comment ' + \
                                              new_line + previous_token.second_value[3:]

            Formatter.fix_documentation_comment(previous_token, indent)
        else:  # create
            token = Token(TokenType.comment, '', first_token_of_statement.position)
            token.second_value = '/**\n' + ' ' * indent + f' * The {field_name} documentation comment \n' + ' ' \
                                 * indent + ' */'

            file.tokens.insert(first_token_of_statement_id, token)
            Formatter.insert_new_line(file, first_token_of_statement_id + 1)
            Formatter.add_indents(file, first_token_of_statement_id + 2, indent)

    @staticmethod
    def fix_another_comments(file):
        stack = []
        i = 0
        while i < len(file.tokens):
            token = file.tokens[i]
            next_token = file.tokens[Formatter.get_next_no_whitespace_token_id(file, i)]
            prev_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, i)]
            if token.value in class_interface_enum and next_token.token_type == TokenType.identifier:
                stack.append(token.value)
                i = Formatter.fix_comment_before_class_declaration(file, i)

            elif token.value == '{':
                stack.append(token.value)
            elif token.value == '}':
                stack.pop()
                if len(stack) > 0 and stack[-1] in class_interface_enum:
                    stack.pop()
            elif token.value == '(':
                stack.append(token.value)
            elif token.value == ')':
                stack.pop()

            if len(stack) > 1 and stack[-2] in class_interface_enum and stack[-1] == '{':  # in class
                if token.token_type == TokenType.identifier:  # identifier (method name or value)

                    if next_token.value == '(' and Formatter.is_method_return(prev_token):  # method declaration
                        Formatter.fix_comment_before_method_declaration(file, i)
                    elif next_token.value in (';', '='):  # is variable
                        Formatter.fix_comment_before_field(file, i)

            i += 1

    @staticmethod
    def fix_comments(file):
        Formatter.fix_beginning_comment(file)
        Formatter.fix_another_comments(file)

    def format_files(self):
        for file in self.files:
            print(file)
            self.fix_names(file)
            Formatter.fix_comments(file)
            Formatter.fix_filename(file)
