#!/usr/bin/env python3

import sys
import g4f
import pyperclip
from rich.console import Console
import Bing

verbose = False


def log(message):
    if verbose:
        print(message)


def output(response):
    console = Console()
    console.print('[bold][white]Description:[/white][/bold]')
    console.print('[blue]' + response + '[/blue]', end="\n\n")

def guessCommand(message):
    message = message.strip()
    console = Console()
    log("Guessing command for: " + message)
    stream = True
    responses = g4f.ChatCompletion.create(provider=Bing, stream=stream, model=g4f.Model.gpt_4, messages=[
        {
            'role': 'creator',
            'content': 'Your purpose is to predict terminal commands. the user will ask a question and the bot will respond with a command. If you need more information start the message with request:info'
        },
        {
            'role': 'creator',
            'content': 'You shall respond in using the following format: <command> | <extra info> |'
        },
        {
            'role': 'creator',
            'content': 'how to: What is the command to list all files in a directory?'
        },
        {
            'role': 'gpt',
            'content': 'ls -la | list all files in a directory |'
        },
        {
            'role': 'user',
            'content': "how to: " + message
        }
    ])

    if not stream:
        responses = responses.split(' ')
        responses = [' ' + x for x in responses]

    console.print('[underline][red][bold]WARNING[/bold] use at your own risk![/red][/underline]', end="\n")
    console.print('[bold][blue]Guessing command...[/blue][/bold]', end="\n\n")
    console.print('[bold][white]Command:[/white][/bold]', end="\n")
    sentence = ""
    output = {
        'command': "",
        'description': ""
    }
    command_printed = False
    end_reached = False
    for response in responses:
        if end_reached:
            continue

        if '|' in response and not command_printed:
            command_printed = True
            output['command'] = sentence.strip()
            sentence = ""
            print('\n')
            console.print('[bold][white]Description:[/white][/bold]')
            continue
        elif '|' in response and command_printed:
            output['description'] = sentence.strip()
            end_reached = True
            continue

        sentence += response
        sentence = sentence.strip()

        if command_printed:
            console.print('[blue]' + sentence + '[/blue]', end="\r")
        else:
            console.print('[green]' + sentence + '[/green]', end="\r")

    print()
    return output


def copy_to_clipboard(text):
    log("Copying to clipboard: " + text)
    pyperclip.copy(text)


def main():
    global verbose
    args = sys.argv[1:]
    if '-v' in args or '--verbose' in args:
        verbose = True
        if '-v' in args:
            args.remove('-v')
        if '--verbose' in args:
            args.remove('--verbose')
    arg_string = ' '.join(args)
    resp = guessCommand(arg_string)
    command = resp['command']
    print()
    console = Console()
    console.print('[bold][cyan]Do you want to copy the command to clipboard?[/cyan][/bold] (y/n)', end=" ")
    response = input()
    if response == 'y':
        copy_to_clipboard(command)
        console.print('[bold][green]Copied to clipboard![/green][/bold]')


if __name__ == "__main__":
    console = Console()
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        console.print('[bold][white]Usage:[/white][/bold]', end="\n")
        console.print('[magenta]ask[/magenta][cyan] [options] <question>[/cyan]', end="\n\n")
        console.print('[bold][white]options:[/white][/bold]', end="\n")
        console.print('[cyan]--path <path>[/cyan]', end="\n\n")
        console.print('[bold][white]Description:[/white][/bold]', end="\n")
        console.print('[magenta]ask[/magenta] [white]is a command line tool that guesses terminal commands based on a question or input[/white]', end="\n\n")
        console.print('[bold][white]Examples:[/white][/bold]', end="\n")
        console.print('[cyan][magenta]ask[/magenta] how to list all files in a directory[/cyan]', end="\n")
        console.print('[blue]->\tls -la[/blue]', end="\n\n")
        console.print('[cyan][magenta]ask[/magenta] how to list all files in a directory --path /home/user[/cyan]', end="\n")
        console.print('[blue]->\tls -la /home/user[/blue]', end="\n\n")
        console.print('[cyan][magenta]ask[/magenta] delete all files in a directory[/cyan]', end="\n")
        console.print('[blue]->\trm -rf *[/blue]', end="\n\n")

        sys.exit(0)

        print("Options:")
        print("  --path <path>  Path to execute from")

        sys.exit(0)

    if '--path' in args:
        path = args[args.index('--path') + 1]
        args.remove('--path')
        args.remove(path)
        sys.path.insert(0, path)
    main()
