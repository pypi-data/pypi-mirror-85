#!/usr/bin/env python
# -*-coding:utf-8-*-


import click
import opencc


@click.command()
@click.argument('input', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
@click.argument('op_type', type=click.Choice(['s2t', 't2s']))
def main(input, output, op_type):
    import opencc
    converter = opencc.OpenCC(f'{op_type}.json')

    content = input.read()
    new_content = converter.convert(content)
    output.write(new_content)


if __name__ == '__main__':
    main()
