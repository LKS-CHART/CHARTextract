from util.datastructures import ASTNode

def _removeRedundantOps(tags):
    found_op = False
    new_tags = []
    operators = {"OR", "..."}

    for i, tag in enumerate(tags):
        if tag not in operators:
            found_op = False
            new_tags.append(tag)
        else:
            if found_op == False:
                new_tags.append(tag)
                found_op = True

    def remove_trailing(tags):
        start_index = 0
        end_index = len(tags)

        if tags[0] in operators:
            start_index += 1

        if tags[-1] in operators:
            end_index -= 1;

        return tags[start_index:end_index]

    new_tags = remove_trailing(new_tags)

    return new_tags


def _insertOperators(tags):
    new_tags = []
    operators = {"OR", "..."}

    for i, tag in enumerate(tags):
        if (i + 1) < len(tags) and (tag not in operators and tags[i + 1] not in operators):
            new_tags.append(tag)
            new_tags.append("...")
        else:
            new_tags.append(tag)

    return new_tags


def _ast_helper(tags):
    if len(tags) == 1:
        return ASTNode(tags[0])
    else:
        return ASTNode(tags[1], ASTNode(tags[0]), _ast_helper(tags[2:]))


def _find_first_or_group(tags, start_index=1):
    first_or_index = None
    end_or_index = None

    if len(tags) == 1:
        return [], None, None

    if "OR" not in tags[start_index:]:
        return [], None, None

    for i in range(start_index, len(tags), 2):
        if tags[i] == "OR" and not first_or_index:
            first_or_index = i
        elif tags[i] == "..." and first_or_index:
            break
        elif tags[i] == "OR":
            end_or_index = i + 1

    if first_or_index:
        if end_or_index:
            return tags[first_or_index + - 1:end_or_index + 1], first_or_index - 1, end_or_index + 1
        else:
            return tags[first_or_index - 1:first_or_index + 2], first_or_index - 1, first_or_index + 2
    else:
        return None


def _merge_ors(tags):
    or_group, first_index, end_index = _find_first_or_group(tags)
    new_tags = []
    appended = False
    for i in range(len(tags)):
        if (first_index and i < first_index) or (end_index and i >= end_index) or (first_index is None) or (
                end_index is None):
            new_tags.append(tags[i])
            if end_index and i >= end_index and end_index < len(tags):
                or_group, first_index, end_index = _find_first_or_group(tags, i)
                appended = False
        if or_group and not appended and (first_index is not None) and (end_index is not None) and \
                (first_index <= i < end_index):
            ast = _ast_helper(or_group)
            new_tags.append(str(ast))
            appended = True
    return new_tags

def construct_ast(tags):
    cleansed_tags = _removeRedundantOps(tags)
    tags_with_ops = _insertOperators(cleansed_tags)

    merged_ors = _merge_ors(tags_with_ops)
    return _ast_helper(merged_ors)

