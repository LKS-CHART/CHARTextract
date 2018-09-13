import re

class ASTNode:
    operators = {"OR", "..."}

    @staticmethod
    def _identity(val):
        return val

    @staticmethod
    def _text_replace(val):
        wildcards = val.replace("...", ".*?")
        dictionaries = re.sub("{(.*?)}", r"dict:'\(\1\)'", wildcards)

        return dictionaries

    @staticmethod
    def _advanced_compile(val):
        pass

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

        self._tag_compiler = ASTNode._text_replace

        if self.val in ASTNode.operators:
            if val == "...":
                self._compiled = ".*?"
            elif val == "OR":
                self._compiled = "|"
        else:
            self._compiled = self._tag_compiler(self.val)

    def __str__(self):
        if self.val[0] == "(" and self.val[-1] == ")":
            return "(" + (str(self.left) if self.left else "") + self._compiled[1:-1] + (
                str(self.right) if self.right else "") + ")"
        else:
            return "(?:" + (str(self.left) if self.left else "") + self._compiled + (
                str(self.right) if self.right else "") + ")"

    def __repr__(self):
        return "ASTNode(" + "\"" + self.val + "\"" + "," + repr(self.left) + "," + repr(self.right) + ")"
