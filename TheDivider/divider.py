import sys
import click
import pandas as pd
from io import StringIO
import subprocess as subp

@click.command()
@click.argument('command', required=False) #, help='command to be run on file')
@click.argument('input_file', required=False) #, help='file to be run/divided')
@click.option('-level', default=0)
#@click.option('-noerror', is_flag=True, default=True,
#    help='remove the default error message')
def cli(command, input_file, level):
    ### HELP DOCUMENTATION ###

    """
    DIVIDER takes a terminal command and a file as inputs.
    The command is tried on the file, and if the command fails (exit status does not equal 0) then the file is divided         20-fold by line number. The process is repeated on the new files until files of line size 1 are left.

    Ex: $ divider "SQL_Toxprint_Generator" "myDTXCIDS.tsv"
            This will $SQL_Toxprint Generator myDTXCIDs
            if the program fails it will divide myDTXCIDS into 20 parts and rerun SQL_Toxprint_generator on each file.
            This continues until 1 line files are created or the program no longer fails (exit code = 0)

    """

    # takes stdin if argument is not directly given

    #this doesnt work needs an actual file
    if not input_file:
        input_file = (sys.stdin.read())
        print(input_file)


    #     mytable = pd.read_csv(tsv_input, sep="\t")
    # elif tsv_input:
    #     mytable = pd.read_csv(tsv_input, sep="\t")


    try:
        a = subp.Popen('({} {})'.format(command, input_file), shell=True)
        a.communicate()
        exitstatus = a.returncode
        #this is still passing after a fail

    except:
        click.secho("Error: command execution failed", fg='red', bold=True)
        sys.exit(1)

    # click.secho('{}'.format(exitstatus))
    if exitstatus == 0:
        click.secho("{} {} was successful".format(command, input_file))
    elif exitstatus > 0:
        #get line number
        b = subp.Popen("wc -l {}".format(input_file), stdout=subp.PIPE, shell=True)
        linenumber = b.communicate()
        linenumber = linenumber[0].decode('utf-8')
        linenumber = int(linenumber.split(" ",1)[0])
        print(linenumber)

        if linenumber > 1:
            # split
            linenumber = int(linenumber/20) + (linenumber%20 > 0)
            #format input file
            try:
                input_file.decode('utf-8')
            except:
                pass

            input_file2 = input_file.split(".")[0]
            input_file2 = input_file2.split("/")
            input_file2.insert(-1, 'splits{}'.format(level))
            input_file2 = "/".join(input_file2)
            input_file3 = input_file2.split("/")[0:-1]
            input_file3 = "/".join(input_file3)
            print(input_file2)
            print(input_file3)

            c = subp.Popen("mkdir {}; csplit -k -f {}_part_ {}  '{}' '{{*}}'".format(input_file3, input_file2, input_file,linenumber), shell=True)
            c.communicate()
            #recurse divided files
            d = subp.Popen('ls {}'.format(input_file3),shell=True, stdout=subp.PIPE)
            splitfiles = d.communicate()
            splitfiles = splitfiles[0].decode('utf-8')
            splitfiles = splitfiles.split("\n")[0:-1]
            print(splitfiles)

            for i in splitfiles:
                #make path for new files
                level+=1
                e = subp.Popen("divider \"{}\" \"{}/{}\" -level {}".format(command, input_file3, i, level),shell=True)
                e.communicate()
        elif linenumber == 1:
            click.secho('{} failed with a 1 line file {}'.format(command, input_file), fg='red', bold=True)
            sys.exit(1)
        else:
            click.secho('Error: unknown error', fg='red', bold=True)
            sys.exit(1)

    else:
        click.secho('Error: unknown error', fg='red', bold=True)
        sys.exit(1)