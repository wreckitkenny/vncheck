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
    try:
        print("Checking the file: {}".format(file))
        with open(file, 'r') as f:
            try:
                env = yaml.load(f, Loader=yaml.FullLoader)['env']
                name = [env[i]['name'] for i in range(len(env))]
                isDup = check_duplicate(name)
                return isDup
            except:
                return []
    except:
        return []

### Schema validation Functions
def validate_value(valueFile, schemaDir):
    print("[!] Checking: {}".format(valueFile))
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
    args=parser.parse_args()

    if len(sys.argv) == 1: parser.print_help()

    if args.check_env == True:
        # try:
        isDuplicated = validate(args.value_file)
        if isDuplicated != None and len(isDuplicated) != 0:
            sys.exit("{} duplicated ENV(s) {} in file [{}].".format(len(isDuplicated), isDuplicated, args.value_file))
        # except IndexError:
        #     print("Help: {} example.yaml".format(sys.argv[0]))

    if args.check_schema == True:
        valueFile = args.value_file
        schemaDir = args.schema_directory
        if args.exclude and valueFile in args.exclude.split(','): valueFile = ""
        if valueFile != "":
            valueValidation = validate_value(valueFile, schemaDir)
            if valueValidation != True: sys.exit(valueValidation)