import argparse
from aphelper import enums, jsonc

class ArgparseHelper:
    def __init__(self, def_data=None, def_file=None, parent=None):

        self.version = '0.0.1'

        if def_file:
            with open(def_file) as f:
                def_data = jsonc.load(f)

        self.parent = parent
        
        parser_description = def_data[enums.Keys.META.value][enums.SubparserMeta.PARSER_DESCRIPTION.value]
        subparser_title = def_data[enums.Keys.META.value][enums.SubparserMeta.SUBPARSER_TITLE.value]
        subparser_description = def_data[enums.Keys.META.value][enums.SubparserMeta.SUBPARSER_DESCRIPTION.value]
        subparser_dest = def_data[enums.Keys.META.value][enums.SubparserMeta.SUBPARSER_DEST.value]
        self.dests = [subparser_dest]

        self.parser = argparse.ArgumentParser(description=parser_description)
        self.subparser = self.parser.add_subparsers(title=subparser_title, description=subparser_description, dest=subparser_dest)
        self.subparser = self.parse(def_data, self.subparser)

    def parse(self, data, subparser, ):
        if enums.Keys.SUBPARSERS.value in data.keys():
            for k in data[enums.Keys.SUBPARSERS.value]:
                help_str = ''
                description_str = ''
                subparser_title = ''
                subparser_description = ''
                subparser_dest = ''
                
                if enums.SubparserMeta.PARSER_HELP.value in data[enums.Keys.SUBPARSERS.value][k][enums.Keys.META.value]:
                    help_str = data[enums.Keys.SUBPARSERS.value][k][enums.Keys.META.value][enums.SubparserMeta.PARSER_HELP.value]
                if enums.SubparserMeta.PARSER_DESCRIPTION.value in data[enums.Keys.SUBPARSERS.value][k][enums.Keys.META.value]:
                    description_str = data[enums.Keys.SUBPARSERS.value][k][enums.Keys.META.value][enums.SubparserMeta.PARSER_DESCRIPTION.value]
                subparser_title = data[enums.Keys.SUBPARSERS.value][k][enums.Keys.META.value][enums.SubparserMeta.SUBPARSER_TITLE.value]
                subparser_description = data[enums.Keys.SUBPARSERS.value][k][enums.Keys.META.value][enums.SubparserMeta.SUBPARSER_DESCRIPTION.value]
                subparser_dest = data[enums.Keys.SUBPARSERS.value][k][enums.Keys.META.value][enums.SubparserMeta.SUBPARSER_DEST.value]
                if not subparser_dest in self.dests:
                    self.dests.append(subparser_dest)

                parser_temp = subparser.add_parser(k, help=help_str, description=description_str)
                parser_temp.set_defaults(func=self.print_help)
                parser_temp.set_defaults(parser=parser_temp)

                subparser_temp = parser_temp.add_subparsers(title=subparser_title, description=subparser_description, dest=subparser_dest)
                subparser_temp = self.parse(data[enums.Keys.SUBPARSERS.value][k], subparser_temp)

        if enums.Keys.SUBCOMMANDS.value in data.keys():
            for k in data[enums.Keys.SUBCOMMANDS.value]:
                help_str = ''
                description_str = ''

                if enums.SubcommandMeta.SUBCOMMAND_HELP.value in data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value]:
                    help_str = data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value][enums.SubcommandMeta.SUBCOMMAND_HELP.value]
                if enums.SubcommandMeta.SUBCOMMAND_DESCRIPTION.value in data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value]:
                    description_str = data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value][enums.SubcommandMeta.SUBCOMMAND_DESCRIPTION.value]

                parser_temp = subparser.add_parser(k, help=help_str, description=description_str)
                if enums.SubcommandMeta.SUBCOMMAND_FUNCTION.value in data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value]:
                    parser_temp.set_defaults(func=self.run_command)
                    parser_temp.set_defaults(function=getattr(self.parent, data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value][enums.SubcommandMeta.SUBCOMMAND_FUNCTION.value]['name']))
                    parser_temp.set_defaults(parser=parser_temp)
                
                if enums.SubcommandMeta.SUBCOMMAND_REQUIRES.value in data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value]:
                    parser_temp.set_defaults(requires=data[enums.Keys.SUBCOMMANDS.value][k][enums.Keys.META.value][enums.SubcommandMeta.SUBCOMMAND_REQUIRES.value])

                for arg_name in data[enums.Keys.SUBCOMMANDS.value][k]['args']:
                    arg = data[enums.Keys.SUBCOMMANDS.value][k]['args'][arg_name]
                    kwargs = {}
                    command = []
                    if enums.Argument.ARGUMENT_SHORT.value in arg.keys():
                        command.append(arg[enums.Argument.ARGUMENT_SHORT.value])
                    if enums.Argument.ARGUMENT_LONG.value in arg.keys():
                        command.append(arg[enums.Argument.ARGUMENT_LONG.value])
                    kwargs = {k:v for k, v in arg.items() if (k != enums.Argument.ARGUMENT_SHORT.value and k != enums.Argument.ARGUMENT_LONG.value and v != None)}

                    if len(command) == 1:
                        parser_temp.add_argument(command[0], **kwargs)
                    elif len(command) == 2:
                        parser_temp.add_argument(command[0], command[1], **kwargs)

        return subparser

    def print_help(self, parser, *args):
        print(parser.print_help())

    def run_command(self, parser, args):
        requires = args.requires
        ignore = self.dests + ['func', enums.SubcommandMeta.SUBCOMMAND_FUNCTION, enums.SubcommandMeta.SUBCOMMAND_REQUIRES, 'parser']
        arg_list = [k for k, v in list(vars(args).items()) if not k in ignore]

        valid = True
        for a in arg_list:
            if a in requires.keys() and getattr(args, a):
                for operator in requires[a]:
                    if operator == enums.LogicalOperators.OR.value:
                        new_valid = False
                        for arg in requires[a][operator]:
                            if getattr(args, arg):
                                new_valid = True
                        valid = new_valid
                    if operator == enums.LogicalOperators.NOR.value:
                        new_valid = False
                        for arg in requires[a][operator]:
                            if getattr(args, arg):
                                new_valid = True
                        valid = not new_valid
                    elif operator == enums.LogicalOperators.AND.value:
                        new_valid = True
                        for arg in requires[a][operator]:
                            if not getattr(args, arg):
                                new_valid = False
                        valid = new_valid
                    elif operator == enums.LogicalOperators.NAND.value:
                        new_valid = True
                        for arg in requires[a][operator]:
                            if not getattr(args, arg):
                                new_valid = False
                        valid = not new_valid
                    elif operator == enums.LogicalOperators.NOT.value:
                        new_valid = True
                        for arg in requires[a][operator]:
                            if getattr(args, arg):
                                new_valid = False
                        valid = new_valid
                    elif operator == enums.LogicalOperators.XOR.value:
                        set_count = 0
                        for arg in requires[a][operator]:
                            if getattr(args, arg):
                                set_count += 1
                        valid = (set_count % 2 == 1)
                    elif operator == 'message':
                        continue
                    if not valid:
                        break
            if not valid:
                break
        if not valid:
            parser.error(requires[a]['message'])

    def execute(self):
        args = self.parser.parse_args()
        if not 'func' in vars(args):
            self.parser.print_help()
        else:
            args.func(args.parser, args)