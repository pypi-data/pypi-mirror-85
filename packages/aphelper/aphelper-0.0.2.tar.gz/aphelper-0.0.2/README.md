# APHelper

## Getting Started

To use APHeler, add the following import statement to your code
```python
from aphelper import core
```

Then, make sure your program has a main class with whatever functions you want to the commands to run contained in it. For example, here is a file with a `Test` class that has a `test` function inside it which our command will call.
```python
from aphelper import core

class Test:
    def __init__(self):
        ah = core.ArgparseHelper(def_file='test/test.jsonc', parent=self)
        ah.execute()

    def test(self, args):
        print('test')

if __name__ == '__main__':
    Test()
```

You'll see that in the class' init function we create a `core.ArgparseHelper` object and pass the location of a definition file along with 'self'. You can pass a file location with the `def_file` keyword or you can pass the contents of a file with the `def_data` keyword.
Following the creation of the object, we call `ah.execute()` to create and parse the CLI.

The definition file used in this example is below:
```jsonc
{
    // the meta section defines information about the parser/subparser
    // for this first meta section you don't need the parser_help key/field
    "meta": {
        "parser_description": "Foo bar",
        "subparser_title": "subcommands",
        "subparser_dest": "command",
        "subparser_description": "valid subcommands"
    },
    // the subparsers key is used to define any parsers that need to be created
    "subparsers": {
        // in this case "hello" is the name of the first command
        "hello": {
            "meta": {
                "parser_description": "hello description",
                "parser_help": "hello help",
                "subparser_title": "subcommands",
                "subparser_dest": "subcommand",
                "subparser_description": "valid subcommands"
            },
            // once again we have a subparsers section which means we want another command
            // underneath "hello" which is not a final subcommand
            "subparsers": {
                "world": {
                    "meta": {
                        "parser_description": "world description",
                        "parser_help": "world help",
                        "subparser_title": "subcommands",
                        "subparser_dest": "subsubcommand",
                        "subparser_description": "valid subcommands"
                    },
                    // subcommands are for defining the "lowest level" commands which actually
                    // have arguments
                    // in this case, we are defining the "test" in the command string "hello world test"
                    "subcommands": {
                        "test": {
                            "meta": {
                                "description": "test help",
                                "help": "test description",
                                "function": {
                                    "name": "test",
                                    "args": {}
                                },
                                "requires": {
                                    "foo1": {
                                        "AND": ["bar1", "bar2"],
                                        "message": "the 'foo1' argument requires '--bar1' and '--bar2'"
                                    },
                                    "foo2": {
                                        "OR": ["bar1", "bar2"],
                                        "message": "the 'foo2' argument requires either '--bar1' or '--bar2'"
                                    },
                                    "foo3": {
                                        "NAND": ["bar1", "bar2"],
                                        "message": "the 'foo3' argument requires either '--bar1' or '--bar2' or neither, but not both"
                                    },
                                    "foo4": {
                                        "NOR": ["bar1", "bar2"],
                                        "message": "the 'foo4' argument requires '--bar1' and '--bar2' to be false"
                                    },
                                    "foo5": {
                                        "NOT": ["bar1"],
                                        "message": "the 'foo5' argument requires '--bar1' to be false"
                                    },
                                    "foo6": {
                                        "XOR": ["bar1", "bar2"],
                                        "message": "the 'foo6' argument requires '--bar1' or '--bar2', but not both"
                                    }
                                }
                            },
                            "args": {
                                "foo1": {
                                    "short": "-f",
                                    "long": "--foo1",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                },
                                "foo2": {
                                    "long": "--foo2",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                },
                                "foo3": {
                                    "long": "--foo3",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                },
                                "foo4": {
                                    "long": "--foo4",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                },
                                "foo5": {
                                    "long": "--foo5",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                },
                                "foo6": {
                                    "long": "--foo6",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                },
                                "bar1": {
                                    "long": "--bar1",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                },
                                "bar2": {
                                    "long": "--bar2",
                                    "choices": null,
                                    "default": null,
                                    "help": null,
                                    "action": "store_true",
                                    "nargs": null
                                }
                            }
                        }
                    }
                } 
            }
        }
    }
}
```

## Definition File Structure

`APHelper` allows for nested definitions within the definition file in order to create a multi-layered command line interface.  The two main object types that can be defined are `subparsers` and `subcommands`.  `Subparsers` are any CLI level that does not handle arguments directly and instead is a parent to other `subparsers` or `subcommands`. `subcommands` are different in that they are the final children of `subparsers` and cannot contain any other `subcommands`, instead they hold the argument definitions for the command.

When writing a definition file, you must always start with this template:
```
{
    // the meta section defines information about the parser/subparser
    // for this first meta section you don't need the parser_help key/field
    "meta": {
        "parser_description": "",
        "subparser_title": "",
        "subparser_dest": "",
        "subparser_description": ""
    }
}
```

On the same level as the "meta" command you can then add a `subaparsers` or `subcommands` section depending on your needs. 

The structure of a `subparsers` section is shown below.
``` jsonc
 "subparsers": {
    // in this case "hello" is the name of the first command
    "hello": {
        "meta": {
            // these five fields are required for any subparser
            // However, you can always set them to an empty string
            "parser_description": "hello description",
            "parser_help": "hello help",
            "subparser_title": "subcommands",
            "subparser_dest": "subcommand",
            "subparser_description": "valid subcommands"
        },
        // if you want to have sub-subparsers, you can define another subparsers section
        // if not, then just don't add it
        "subparsers": {},
        // if you want to have subcommands, you can define a subcommandssection
        // if not, then just don't add it
        "subcommands": {}
    },
    // if you want more than one command on this level then you can just add another key
    // along with its "meta" section and any desired "subparsers" and "subcommands"
    "hello2": {
        // ...
    },
    // ...
 }
```

The structure of a `subcommands` section is shown below.
```jsonc
 "subcommands": {
    // in this case "hello" is the name of the first command
    "world": {
        "meta": {
            // command description (required)
            "description": "",
            // command help (required)
            "help": "",
            "function": { // (required)
                // name of the function inside the class that calls the ArgparseHelper object
                // that you want to call when the command is executed
                "name": ""
            },
            "requires": { // (required, but you can just leave it blank if you want)
                // here we define any arguments that require logic to make sure that combinations of arguments are valid
                // set the argument that you want to trigger the logical check as the key
                "foo1": { 
                    // then define any logical checks you want to be made
                    // The valid operators are:
                    //   - AND
                    //   - NAND
                    //   - NOR
                    //   - NOT
                    //   - OR
                    //   - XOR
                    "AND": ["bar1", "bar2"],
                    // the message to print out if the logical check fails
                    "message": "the 'foo1' argument requires '--bar1' and '--bar2'"
                }
            }
        },
        "args": {
            "foo1": {
                // you need either a "short" key or a "long" key or both
                "short": "-f", // this is the single-letter flag that can be used for this argument
                "long": "--foo1", // this is the long flag that can be used for this argument
                // you can define any argparse keyword for the `add_argument` functio as a key and for an agrument
                // and it will be added to your argument that is created in your applicatoin
                // for example, in this case we set the 'action' keyword to 'store_true' for a boolean flag
                "action": "store_true"
            },
            "bar1": {
                "long": "--bar1",
                "action": "store_true"
            },
            "bar2": {
                "long": "--bar2",
                "action": "store_true"
            }
        }
    },
    // if you want more than one command on this level then you can just add another key
    // along with its "meta" and "args" sections
    "world2": {
        // ...
    },
    // ...
 }
```

You can then nest these `subcommands` and `subparsers` sections together to create whatever structure you need