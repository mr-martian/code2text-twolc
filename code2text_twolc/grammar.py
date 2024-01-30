from code2text.translate import Pattern
from tree_sitter_apertium import TWOLC

base_rules = [
    {'pattern': '[(comment) (semicolon)] @root', 'output': ''},
    {
        'pattern': '''
(source_file
  [(alphabet) (sets) (definitions) (diacritics) (rule_variables) (rules)] @thing_list
) @root''',
        'output': [
            {
                'lists': {'thing_list': {'join': '\n\n', 'html_type': 'p'}},
                'output': '{thing_list}\n'
            }
        ]
    },
    # handle empty files
    {'pattern': '(source_file) @root', 'output': ''},
    {
        'pattern': '(alphabet [(symbol) (symbol_pair)] @sym_list) @root',
        'output': [
            {
                'lists': {'sym_list': {'join': '\n', 'html_type': 'ul'}},
                'output': 'The following mappings are possible:\n{sym_list}',
            }
        ],
    },
    {
        'pattern': '(alphabet (symbol) @root_text)',
        'output': 'The symbol {root_text} remains unchanged',
    },
    {
        'pattern': '(alphabet (symbol_pair left: (symbol) @l_text right: (symbol) @r_text) @root (#eq? @r_text "0"))',
        'output': 'The symbol {l_text} is deleted',
    },
    {
        'pattern': '(alphabet (symbol_pair left: (symbol) @l_text right: (symbol) @r_text) @root)',
        'output': 'The symbol {l_text} is changed to {r_text}',
    },
    {
        'pattern': '(sets (set) @set_list) @root',
        'output': [
            {
                'lists': {'set_list': {'join': '\n', 'html_type': 'ul'}},
                'output': 'We define the following sets of mappings:\n{set_list}',
            }
        ],
    },
    {
        'pattern': '(set name: (symbol) @name_text [(symbol) (symbol_pair)] @thing_list) @root',
        'output': [
            {
                'lists': {'thing_list': {'join': ', '}},
                'output': 'The set {name_text} contains {thing_list}.',
            }
        ],
    },
    {
        'pattern': '(set (symbol) @root_text)',
        'output': '{root_text}',
    },
    {
        'pattern': '(rules (rule) @rule_list) @root',
        'output': [
            {
                'lists': {'rule_list': {'join': '\n\n', 'html_type': 'p'}},
                'output': 'The mappings are constrained by the following rules:\n\n{rule_list}',
            }
        ],
    },
    {
        'pattern': '(rule (rule_name) @name_text [(symbol) (symbol_pair)] @target (arrow) @arrow (positive_contexts) @pos) @root',
        'output': '{target} {arrow} it occurs in one of the following contexts:\n{pos}',
    },
    {
        'pattern': '((arrow) @root (#eq? @root "<=>"))',
        'output': 'if and only if',
    },
    {
        'pattern': '(rule (symbol_pair left: (symbol) @l_text right: (symbol) @r_text) @root (#eq? @r_text "0"))',
        'output': '{l_text} is deleted',
    },
    {
        'pattern': '(rule (symbol_pair left: (symbol) @l_text right: (symbol) @r_text) @root (#eq? @l_text "0"))',
        'output': '{r_text} is inserted',
    },
    {
        'pattern': '(rule (symbol_pair left: (symbol) @l_text right: (symbol) @r_text) @root)',
        'output': '{l_text} becomes {r_text}',
    },
    {
        'pattern': '(positive_contexts (context) @ctx_list) @root',
        'output': [
            {
                'lists': {'ctx_list': {'join': '\n -', 'html_type': 'ul'}},
                'output': '- {ctx_list}',
            },
        ],
    },
    {'pattern': '(pattern (symbol) @s) @root', 'output': '{s}'},
    {'pattern': '(pattern (symbol_pair) @s) @root', 'output': '{s}'},
    {'pattern': '(pattern (word_boundary) @s) @root', 'output': '{s}'},
    {'pattern': '(pattern (any) @s) @root', 'output': '{s}'},
    {'pattern': '(pattern (lpar) (pattern) @s (rpar)) @root', 'output': '({s})'},
    {'pattern': '(pattern (loptional) (pattern) @s (roptional)) @root', 'output': 'optional ({s})'},
    {
        'pattern': '(pattern (prefix_op) @o (pattern) @s) @root',
        'output': '{o} {s}',
    },
    {
        'pattern': '(pattern (pattern) @s (suffix_op) @o) @root',
        'output': '{o} {s}',
    },
    {
        'pattern': '(pattern (pattern) @p1 [(ignore_op) (bool_op) (replace_op) (compose_op)] @o (pattern) @p2) @root',
        'output': '{p1} {o} {p2}',
    },
    {
        'pattern': '(pattern (pattern) @p1 (pattern) @p2) @root',
        'output': '{p1}, {p2}',
    },
    {
        'pattern': '(symbol) @root_text',
        'output': '{root_text}',
    },
    {
        'pattern': '((symbol_pair left: (symbol) @l right: (symbol) @r) @root (#eq? @r "0"))',
        'output': '{l} which is deleted',
    },
    {
        'pattern': '(symbol_pair left: (symbol) @l right: (symbol) @r) @root',
        'output': '{l} which becomes {r}',
    },
    {
        'pattern': '(symbol_pair right: (symbol) @r) @root',
        'output': 'any symbol which becomes {r}',
    },
    {
        'pattern': '(symbol_pair left: (symbol) @l) @root',
        'output': '{l} which becomes anything',
    },
    {'pattern': '((bool_op) @root (#eq? @root "|"))', 'output': 'or'},
    {'pattern': '((bool_op) @root (#eq? @root "&"))', 'output': 'and'},
    {'pattern': '((bool_op) @root (#eq? @root "-"))', 'output': 'but not'},
    {'pattern': '(locus) @root', 'output': 'the locus of the rule'},
    {
        'pattern': '(context left: (pattern) @l (locus) @_ right: (pattern) @r) @root',
        'output': '{l}, {_}, {r}',
    },
    {
        'pattern': '(context (locus) @_ right: (pattern) @r) @root',
        'output': '{_}, {r}',
    },
    {
        'pattern': '(context left: (pattern) @l (locus) @_) @root',
        'output': '{l}, {_}',
    },
    {
        'pattern': '(context (locus) @_) @root',
        'output': 'anywhere',
    },
]

rules = [Pattern.from_json(TWOLC, rl) for rl in base_rules]
