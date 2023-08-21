def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', action='store')
    parser.add_argument('output_file', action='store')
    args = parser.parse_args()
    from .grammar import rules
    from tree_sitter_apertium import TWOLC
    from code2text.translate import translate
    with open(args.input_file, 'rb') as fin:
        with open(args.output_file, 'w') as fout:
            fout.write(translate(rules, TWOLC, fin.read()))
