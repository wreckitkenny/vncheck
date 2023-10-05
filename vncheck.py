import yaml, sys, argparse, json, jsonschema

### ENV validation Functions
def check_duplicate(list):
    setOfName = set()
    listOfName = []
    for n in list:
        if n in setOfName: listOfName.append(n)
        else: setOfName.add(n)
    return listOfName

def validate(file):
    print("[!] Checking duplicated env: {}".format(file))
    with open(file, 'r') as f:
        valueContent = yaml.load(f, Loader=yaml.FullLoader)
        try:
            if "image" not in list(valueContent.keys()):
                isDup = []
                for container in valueContent['app']['containers']:
                    name = [container['env'][i]['name'] for i in range(len(container['env']))]
                    isDup += check_duplicate(name)
            else:
                name = [valueContent['env'][i]['name'] for i in range(len(valueContent['env']))]
                isDup = check_duplicate(name)
        except KeyError:
            print("--> [!] Yaml node 'env' not found")
        return isDup

### Schema validation Functions
def validate_value(valueFile, schemaDir):
    print("[!] Check schema: {}".format(valueFile))
    with open(valueFile) as valueFile:
        valueContent = yaml.load(valueFile, Loader=yaml.FullLoader)
        # Detect helm generic version
        if "image" not in list(valueContent.keys()):
            print("--> [+] Version 1.0.0 is detected.")
            with open(schemaDir + "/newSchema.json") as schemaFile:
                schemaContent = json.load(schemaFile)
        else:
            print("--> [+] Version <1.0.0 is detected.")
            with open(schemaDir + "/oldSchema.json") as schemaFile:
                schemaContent = json.load(schemaFile)
    try:
        jsonschema.validate(instance=valueContent, schema=schemaContent)
        print("--> [+] VALIDATED!!!")
        return True
    except jsonschema.exceptions.ValidationError as error:
        return "--> [-] Failed to validate: {}".format(error)
    except FileNotFoundError:
        print("--> [-] File {} has not been available to check.".format(valueFile))
        return True

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''A tool to validate Helm value file''',
    epilog="""Author: _wiky""")
    parser.add_argument('--check-env', action="store_true", help='enable to check ENV variables in Helm value file')
    parser.add_argument('--check-schema', action="store_true", help='enable to check Helm value file based on schema')
    parser.add_argument('--schema-directory', help='schema directory')
    parser.add_argument('--value-file', help='path to a Helm value file')
    parser.add_argument('--exclude', help='exclude files not needed to check')
    parser.add_argument('--middleware', help='define middleware application not needed to check')
    args=parser.parse_args()

    if len(sys.argv) == 1: parser.print_help()

    valueFile = args.value_file

    # Check excluded files
    if args.exclude and valueFile.split('/')[-1] in args.exclude.split(','):
        print("[!] Nothing to check")
        valueFile = ""

    # Check middleware helm value files
    if args.middleware:
        for m in args.middleware.split(','):
            if m in valueFile: valueFile = ""

    ## Main check
    if valueFile != "" and args.check_env == True:
        isDuplicated = validate(valueFile)
        if isDuplicated != None and len(isDuplicated) != 0:
            sys.exit("--> [-] Found {} duplicated ENV(s) {} in file [{}].".format(len(isDuplicated), isDuplicated, valueFile))
        else:
            print("--> [+] Everything OK")
    if valueFile != "" and args.check_schema == True:
        schemaDir = args.schema_directory
        valueValidation = validate_value(valueFile, schemaDir)
        if valueValidation != True: sys.exit(valueValidation)