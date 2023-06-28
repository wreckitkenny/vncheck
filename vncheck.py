import yaml, sys, argparse, json, jsonschema

### ENV validation Functions
def checkDup(list):
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
                isDup = checkDup(name)
                return isDup
            except:
                return []
    except:
        return []

### Schema validation Functions
def validateValue(valueFile, schemaFile):
    try:
        print("Checking: {}".format(valueFile))
        with open(valueFile) as valueFile, open(schemaFile) as schemaFile:
            valueContent = yaml.load(valueFile, Loader=yaml.FullLoader)
            schemaContent = json.load(schemaFile)
            jsonschema.validate(instance=valueContent, schema=schemaContent)
            return True
    except jsonschema.exceptions.ValidationError as error:
        return error
    except FileNotFoundError:
        print("SKIPPED - File {} has not been available to check.".format(valueFile))
        return True

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''A tool to validate Helm value file''',
    epilog="""Author: _wiky""")
    parser.add_argument('--check-env', action="store_true", help='enable to check ENV variables in Helm value file')
    parser.add_argument('--check-schema', action="store_true", help='enable to check Helm value file based on schema')
    parser.add_argument('--schema-file', help='path to a schema file')
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
        schemaFile = args.schema_file
        if args.exclude:
            if valueFile in args.exclude.split(','): valueFile = ""
        if valueFile != "":
            valueValidation = validateValue(valueFile, schemaFile)
            if valueValidation != True: sys.exit(valueValidation)