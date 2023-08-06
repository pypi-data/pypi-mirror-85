def format_type_name(type_name):
    """Type names start with a capital letter and have a capital letter for each new word, with no underscores:
    MyExcitingClass, MyExcitingEnum. The names of all types — classes, structs, type aliases, enums, and type
    template parameters — have the same naming convention. Type names should start with a capital letter and have
    a capital letter for each new word. No underscores."""
    need_upper_case = False
    first_letter = True
    formatted_type_name = ""
    for symbol in type_name:
        if first_letter and str.isalpha(symbol):
            formatted_type_name = formatted_type_name + str.upper(symbol)
        elif symbol == '_':
            need_upper_case = True
        elif str.isalpha(symbol):
            if need_upper_case:
                formatted_type_name = formatted_type_name + str.upper(symbol)
                need_upper_case = False
            else:
                formatted_type_name = formatted_type_name + symbol
        elif str.isdigit(symbol):
            formatted_type_name = formatted_type_name + symbol
            need_upper_case = True
        else:
            formatted_type_name = formatted_type_name + symbol
        first_letter = False
    return formatted_type_name


def format_common_var_name(var_name):
    """std::string table_name;  // OK - lowercase with underscore.
    std::string tableName;   // Bad - mixed case.
    Data members of structs, both static and non-static, are named like ordinary nonmember variables.
    They do not have the trailing underscores that data members in classes have.
    Also used for namespace names"""
    formatted_variable_name = ""
    for symbol in var_name:
        if str.isalpha(symbol):
            if str.islower(symbol):
                formatted_variable_name = formatted_variable_name + symbol
            else:
                if len(formatted_variable_name) > 0 and formatted_variable_name[-1] != '_':
                    formatted_variable_name = formatted_variable_name + '_'
                formatted_variable_name = formatted_variable_name + str.lower(symbol)
        else:
            formatted_variable_name = formatted_variable_name + symbol
    return formatted_variable_name


def format_class_var_name(class_var_name):
    """Data members of classes, both static and non-static, are named like ordinary nonmember variables, but with a
    trailing underscore. """
    return format_common_var_name(class_var_name) + '_'


def format_const_var_name(const_var_name):
    """Variables declared constexpr or const, and whose value is fixed for the duration of the program, are named
    with a leading "k" followed by mixed case. Underscores can be used as separators in the rare cases where
    capitalization cannot be used for separation.
    Also used for ENUMS"""
    first_letter = True
    need_upper_case = False
    formatted_const_var_name = ""
    i = 0
    while i < len(const_var_name):
        if first_letter:
            formatted_const_var_name = 'k'
            if const_var_name[i] == 'k':
                if len(const_var_name) > 1 and str.islower(const_var_name[1]):
                    need_upper_case = True
            elif const_var_name[i] == '_':
                need_upper_case = True
            else:
                formatted_const_var_name = formatted_const_var_name + str.upper(const_var_name[i])
        elif str.isalpha(const_var_name[i]):
            if need_upper_case:
                formatted_const_var_name = formatted_const_var_name + str.upper(const_var_name[i])
                need_upper_case = False
            else:
                formatted_const_var_name = formatted_const_var_name + const_var_name[i]
        elif const_var_name[i] == '_':
            if len(formatted_const_var_name) > 0 and str.isdigit(formatted_const_var_name[-1]) and \
                    i + 1 < len(const_var_name) and str.isdigit(const_var_name[i+1]):
                formatted_const_var_name = formatted_const_var_name + '_'
            else:
                need_upper_case = True
        elif str.isdigit(const_var_name[i]):
            need_upper_case = True
            formatted_const_var_name = formatted_const_var_name + const_var_name[i]
        else:
            formatted_const_var_name = formatted_const_var_name + const_var_name[i]
        first_letter = False
        i += 1
    return formatted_const_var_name


def format_func_name(func_name):
    """Regular functions have mixed case; accessors and mutators may be named like variables.
    Ordinarily, functions should start with a capital letter and have a capital letter for each new word."""
    if func_name == "main":
        return "main"
    return format_type_name(func_name)


def format_file_name(file_name):
    """Filenames should be all lowercase and can include underscores (_) or dashes (-). Follow the convention
     that your project uses. If there is no consistent local pattern to follow, prefer '_' """
    formatted_file_name = ""
    for symbol in file_name:
        if str.isalpha(symbol):
            if str.islower(symbol):
                formatted_file_name = formatted_file_name + symbol
            else:
                if len(formatted_file_name) > 0 and formatted_file_name[-1] != '_' and formatted_file_name[-1] != '-':
                    formatted_file_name = formatted_file_name + '_'
                formatted_file_name = formatted_file_name + str.lower(symbol)
        else:
            formatted_file_name = formatted_file_name + symbol
    return formatted_file_name


def format_macro_name(macro_name):
    """You're not really going to define a macro, are you? If you do, they're like this:
    MY_MACRO_THAT_SCARES_SMALL_CHILDREN_AND_ADULTS_ALIKE."""
    formatted_macro_name = ""
    i = 0
    while i < len(macro_name):
        if str.islower(macro_name[i]):
            formatted_macro_name = formatted_macro_name + str.upper(macro_name[i])
            if i+1 < len(macro_name) and str.isupper(macro_name[i+1]):
                formatted_macro_name = formatted_macro_name + '_'
        else:
            formatted_macro_name = formatted_macro_name + macro_name[i]
        i += 1
    return str.upper(formatted_macro_name)


def format_single_line_comment(comment):
    comment_parts = split_large_comment(comment, True)
    if len(comment_parts) == 1 and comment_parts[0] == "\n":
        return ""
    result_comment = ""
    was_space = False
    for comment_part in comment_parts:
        cur_comment_line = "//"
        for symbol in comment_part:
            if symbol == ' ':
                if not was_space:
                    was_space = True
                    cur_comment_line = cur_comment_line + ' '
            else:
                was_space = False
                cur_comment_line = cur_comment_line + symbol
        cur_comment_line = cur_comment_line.replace('\n', "")
        cur_comment_line = cur_comment_line + '\n'
        if cur_comment_line[2] != ' ':
            cur_comment_line = cur_comment_line[0:2] + ' ' + cur_comment_line[2:len(cur_comment_line)]
        result_comment = result_comment + cur_comment_line
    return result_comment


def format_multi_line_comment(comment):
    comment = comment.replace('\n', ' ')
    comment = comment.strip()
    comment_parts = split_large_comment(comment, False)
    result_comment = ""
    for single_comment in comment_parts:
        result_comment = result_comment + format_single_line_comment(single_comment)
    return result_comment


def split_large_comment(comment, single_line):
    max_comment_len = 80
    if single_line:
        if len(comment) >= 2 and comment[0:2] == "//":
            comment = comment[2:len(comment)]  # remove //
    else:
        comment = comment[2:-2]  # remove /**/
    comment_parts = []
    comment_len = len(comment)
    from_pos = 0
    while True:
        if from_pos + max_comment_len < comment_len:
            comment_part = comment[from_pos:from_pos + max_comment_len]
            comment_parts.append(comment_part)
            from_pos = from_pos + max_comment_len
        else:
            comment_part = comment[from_pos:comment_len]
            comment_parts.append(comment_part)
            break
    return comment_parts



