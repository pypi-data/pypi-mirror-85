from enum import Enum, unique

class BaseEnum(Enum):
    @classmethod
    def values(cls) -> list:
        """Returns a list of raw values for the class"""
        values = [member.value for role, member in cls.__members__.items()]
        return values


@unique
class Keys(BaseEnum):
    """Represents categories of objects in cli definition files"""

    META        = "meta"
    SUBPARSERS  = "subparsers"
    SUBCOMMANDS = "subcommands"


@unique
class LogicalOperators(BaseEnum):
    """Represents logical operators that can be used in determining required arguments"""

    NOT  = "NOT"
    OR   = "OR"
    AND  = "AND"
    XOR  = "XOR"
    NAND = "NAND"
    NOR  = "NOR"

@unique
class SubparserMeta(BaseEnum):
    """Represents fields that are used to define subparser metadata"""

    PARSER_DESCRIPTION     = "parser_description"
    PARSER_HELP            = "parser_help"
    SUBPARSER_TITLE        = "subparser_title"
    SUBPARSER_DESCRIPTION  = "subparser_description"
    SUBPARSER_DEST         = "subparser_dest"

@unique
class SubcommandMeta(BaseEnum):
    """Represents fields that are used to define subcommand metadata"""

    SUBCOMMAND_DESCRIPTION = "description"
    SUBCOMMAND_HELP        = "help"
    SUBCOMMAND_FUNCTION    = "function"
    SUBCOMMAND_REQUIRES    = "requires"

class Argument(BaseEnum):
    ARGUMENT_SHORT = "short"
    ARGUMENT_LONG  = "long"