ruleSet = {
    "className": "ConditionalRule",
    "args": [
        {
            "className": "ConditionalRule",
            "args": [
                {
                    "className": "ConstantRule",
                    "args": [
                        "b"
                    ]
                },
                {
                    "className": "ConstantRule",
                    "args": [
                        "w"
                    ]
                },
                {
                    "className": "BoolOperator",
                    "args": [
                        {
                            "className": "Comparator",
                            "args": [
                                {
                                    "className": "GridSelector",
                                    "args": [
                                        "bbbbbbbbb"
                                    ]
                                },
                                {
                                    "className": "ConstantSelector",
                                    "args": [
                                        3
                                    ]
                                },
                                "=="
                            ]
                        },
                        {
                            "className": "Comparator",
                            "args": [
                                {
                                    "className": "GridSelector",
                                    "args": [
                                        "bbbbbbbbb"
                                    ]
                                },
                                {
                                    "className": "ConstantSelector",
                                    "args": [
                                        4
                                    ]
                                },
                                "=="
                            ]
                        },
                        "or"
                    ]
                }
            ]
        },
        {
            "className": "ConditionalRule",
            "args": [
                {
                    "className": "ConstantRule",
                    "args": [
                        "b"
                    ]
                },
                {
                    "className": "ConstantRule",
                    "args": [
                        "w"
                    ]
                },
                {
                    "className": "Comparator",
                    "args": [
                        {
                            "className": "GridSelector",
                            "args": [
                                "bbbbwbbbb"
                            ]
                        },
                        {
                            "className": "ConstantSelector",
                            "args": [
                                4
                            ]
                        },
                        "=="
                    ]
                }
            ]
        },
        {
            "className": "Comparator",
            "args": [
                {
                    "className": "GridSelector",
                    "args": [
                        "****b****"
                    ]
                },
                {
                    "className": "ConstantSelector",
                    "args": [
                        1
                    ]
                },
                "=="
            ]
        }
    ]
}

function initWorld(){
    r = Rule.deserialize(ruleSet);
    world = new BWWorld(25, 25, "automata", r);
}