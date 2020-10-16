import docblacketeer.code_formatter as code_formatter
from docblacketeer.code_formatter import ARROWS, DOTS


class TestParameters:

    list_of_valid_python_code = [
        "import math\nx = 2 + 10\ny = 5 / math.pi",
        "for i in range(10):\n    print(i)",
    ]

    list_of_prompt_code = [
        ">>> import math\n>>> x = 2 + 10\n>>> y = 5 / math.pi\n>>> x",
    ]

    list_of_prompt_code_with_return = [
        ">>> import math\n>>> x = 2 + 10\n>>> y = 5 / math.pi\n>>> x\n12",
    ]

    list_of_prompt_code_with_expected = [
        (
            ">>> import math\n>>> x = 2 + 10\n>>> y = 5 / math.pi\n>>> x\n12",
            ">>> import math\n>>> \n>>> x = 2 + 10\n>>> y = 5 / math.pi\n>>> x\n12",
        ),
        (
            ">>> import math\n>>> x =   2    + 10\n>>> y =    5 /  math.pi\n>>> x\n12",
            ">>> import math\n>>> \n>>> x = 2 + 10\n>>> y = 5 / math.pi\n>>> x\n12",
        ),
        (
            ">>> import math   \n>>> x =   2    + 10\n>>> y =    5 /  math.pi\n>>> x\n12",
            ">>> import math\n>>> \n>>> x = 2 + 10\n>>> y = 5 / math.pi\n>>> x\n12",
        ),
        (
            " >>> import math   \n>>> x =   2    + 10\n>>> y =    5 /  math.pi\n>>> x\n12",
            code_formatter.CodeParseError,
        ),
        (
            " >>> import math   \n>>> x =   2    + 10\n>>> y =    5 /  math.pi\n>>> x",
            code_formatter.CodeParseError,
        ),
        (
            ">>> import math   \n>>> x =   2    + 10\n>>> y =    5 /  math.pi\n>>> x",
            code_formatter.CodeParseError,
        ),
        (
            ">>> import math   \n >>> x =   2    + 10\n>>> y =    5 /  math.pi\n>>> x",
            code_formatter.CodeParseError,
        ),
    ]
    lines_of_code = [
        (">>> import math\n", ARROWS),
        (" >>> import math\n", ""),
        (" >>2> import math\n", ""),
        (" ...>>> import math\n", ""),
        ("... some_parameter\n", DOTS),
        (" ... some_parameter\n", ""),
        ("some_parameter\n", ""),
    ]
