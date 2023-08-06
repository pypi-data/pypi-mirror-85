# OSMeterium
> The osmeterium is a defensive organ found in all papilionid larvae, in all stages. 

A simple wrapper for Popen to meet MapColonies org needs for running background processes and pipe the output.

## Usage
### Async
```py
t = run_command_async('ping -c 5 www.google.com',
        (lambda x: print('Hey this stdout output {0}'.format(x))),
        (lambda x: print('Hey this stderr output {0}'.format(x))),
        (lambda y: print('This is exit code ${0}'.format(y))),
        (lambda: print('Command success'))) #  return a Thread Object
t.join()
```
### Sync
```py
run_command('ping -c 5 www.google.com',
        (lambda x: print('Hey this stdout output {0}'.format(x))),
        (lambda x: print('Hey this stderr output {0}'.format(x))),
        (lambda y: print('This is exit code ${0}'.format(y))),
        (lambda: print('Command success')))
```
