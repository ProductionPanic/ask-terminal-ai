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
            'content': 'You shall respond in using the following format: <command> | <extra info>'
        },
        {
            'role': 'creator',
            'content': 'What is the command to list all files in a directory?'
        },
        {
            'role': 'gpt',
            'content': 'ls -la | list all files in a directory'
        },
        {
            'role': 'gpt',
            'content': 'Any other commands?'
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
    for response in responses:
        if '|' in response:
            output['command'] = sentence.strip()
            print()
            console.print('[bold][white]Description:[/white][/bold]')
            sentence = ""
        else:
            sentence += response
        sentence = sentence.strip()
        console.print('[green]' + sentence + '[/green]', end="\r")
    output['description'] = sentence.strip()
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
    copy_to_clipboard(command)
    console = Console()
    console.print('\n[bold][cyan]Copied to clipboard![/cyan][/bold]')

def close_client_session():
    g4f.ChatCompletion.close_client_session()

if __name__ == "__main__":
    main()
