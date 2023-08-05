import sys, getopt
import os
import requests
import base64
import json
from subprocess import Popen, PIPE

from artify import __version__

from artify import nexus
from artify import deploy
from artify import syncrepo
from artify import change_version
from artify import generate_file
from artify import extract_commands
from artify import initialize

debug = 0;

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxies = {
  "http": None,
  "https": None,
}

# Variables - Nexus
nexus_format = ''
artifact_name = ''
work_directory = ''
repository_name = ''
nexus_format = ''
repository_base_url = ''
repository_full_url = ''
username = ''
password = ''
directory = ''
group_id = ''
auth = ''

# Variables - Nexus

# Variables - Deploy AWX
encoded_string = ''  
url = ''
debug = 0
# Variables - Deploy AWX

# Variables - Change version
arch_type = ''
pre_value = ''
# Variables - Change version

# Variables - Sync repository
branch = ''
commit_message = ''
# Variables - sync repository

# Variables - create file
filename_gen = ''
# Variables - create file

# Variables - Initialize
sonarhost = ''
language = ''
project_key = ''
project_name = ''
# Variables - Initialize

def main(argv):  
    print("Copyright \N{COPYRIGHT SIGN} 2020 Stewartium ::: artify v{}\n".format(__version__))
    action = ''
    
    path = os.path.abspath(os.getcwd()) 
    
    # Variables - Deploy AWX
    global encoded_string 
    global url
    global debug
    # Variables - Deploy AWX
    
    # Variables - Nexus
    global nexus_format 
    global artifact_name
    global work_directory
    global repository_name
    global nexus_format
    global repository_base_url
    global repository_full_url
    global username
    global password
    global directory
    global group_id
    global auth
    # Variables - Nexus
    
    # Variables - Change version
    global arch_type
    global change_type
    global pre_value
    # Variables - Change version
    
    global branch
    global commit_message
    
    # Variables - generate file
    global filename_gen
    
    # Variables - Initialize
    global sonarhost
    global language
    global project_key
    global project_name
    # Variables - Initialize
   
    try:
        opts, args = getopt.getopt(argv, "a:b:c:d:f:h:k:l:m:n:u:p:r:g:t:w:", ["command=", "help=", 
                                                "artifactname=", "repository=","groupid=", "directory=", "nexushost=",
                                                "file=", "awxhost=","--host=",
                                                "format=",
                                                "type=", "archtype=", "prevalue=",
                                                "message=", "branch=",
                                                "projectkey=", "projectname="
                                                "debug"
                                               ])
    except getopt.GetoptError:
        print('Invalid syntax')
        print('To get help, type syntax below: ')
        print('python -m artify --help=')
        return sys.exit(2)
    
    for opt, arg in opts:
        if opt == "--help":
            if arg == "nexus":
                print("How to use Nexus Artifact Upload module\n")
                print("Usage: python -m artify -c nexus [OPTION] NEXUS_URL\n")
                print("Mandatory arguments: ")
                print("-f, --format    Nexus repository format e.g npm, maven, raw, nuget")
                print("-h, --nexushost   Nexus host base url e.g https://nexus.<yourcompany>.com")
                print("")
                print("Optional arguments i.e Some can be passed in the environment variables")
                print("-w, --workdirectory Working directory of artifact to be uploaded to Nexus repository")
                print("-n, --artifactname  Artifact name")
                print("-r, --repository    Nexus repository to upload to: e.g <repository>-snapshots")
                print("-g, --groupid       Group ID for Maven2 type repository")
                print("-d, --directory     Directory for RAW type repository")
                print("-u, --username      Username of nexus user")
                print("-p, --password      Password of nexus user")
                print("\n--proxy             Sets Http proxy")
                print("--proxysec          Sets Https proxy")
                return sys.exit(0)
            elif arg == "deploy":
                print("How to deploy app to AWX infrastructure")
                print('python -m artify -c deploy -f <manifest> -h <awx_host>')
                print("Or")
                print("python -m artify --command deploy --file <manifest> --awxhost <awx_host>")
                print("\n--proxy             Sets Http proxy")
                print("--proxysec          Sets Https proxy")
                return sys.exit(0)
            elif arg == "syncrepo":
                print('')
                print("How to Push and Commit changes\n")
                print("Usage: python -m artify -c syncrepo [OPTION] COMMIT_MESSAGE\n")
                print("Mandatory arguments: ")
                print("-m, --message     Commit message")
                print("\nOptional arguments: ")
                #print("-h, --host        Repository url")
                print("-b, --branch     Repository branch to sync changes")
                print("\n--proxy             Sets Http proxy")
                print("--proxysec          Sets Https proxy")
                return sys.exit(0)
            elif arg == "deltav":
                print('')
                print('python -m artify -c deltav -t <version_change> -a <architecture_type>')
                print("Or")
                print("python -m artify --command deltav --type <version_change> --archtype <architecture_type>")
                print("Mandatory argument(s): ")
                print("-t, --type          Type of version change: major, minor, patch")
                print("e.g --type major    1.0.0.0 => 2.0.0.0")
                print("e.g --type minor    1.0.0.0 => 1.1.0.0")
                print("e.g --type patch    1.0.0.0 => 1.0.1.0")
                print("e.g --type build    1.0.0.0 => 1.0.0.1   Experimental")
                
                print("e.g --archtype npm, gradle, maven, flutter, dotnet, netcore")
                print("\nOptional arguments: ")
                print("-b, --branch        Branch to commit code changes. Default: develop")
                print("--preValue          Prerelease version value e.g SNAPHOT, RELEASE, BUILD, beta, alpa")
               
                return sys.exit(0)
            elif arg == 'create':
                print('')
                print('python -m artify -c create -f <template_file>')
                print("Mandatory argument(s): ")
                print('-f, --file    Template file to create e.g manifest, gitlabci')
                return sys.exit(0)
            elif arg == 'extract':
                print('')
                print('python -m artify -c extract \n')
                print('Sample commit messages below: \n')
                print("Added login functionality {\"version\": \"patch\", \"archtype\": \"npm\", \"branch\": \"release\" } \n")
                print("Added edit functionality {\"version\": \"minor\", \"a\": \"flutter\" } \n")
                return sys.exit(0)
            elif arg == 'initialize':
                print('')
                print('python -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -a <arch_type/os> -l <language>')    
                print('\nExample command below for a java project that uses gradle build tool.')
                print('\npython -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -l java -a gradle\n')
                return sys.exit(0)
            else:
                print('python -m artify --help nexus        Help on how to deploy to Nexus Repository')
                print('python -m artify --help deploy       Help on how to deploy to AWX host')
                print('python -m artify --help syncrepo     Help on how to commit and push code to repository')
                print('python -m artify --help deltav       Help on how to change version number')
                print("python -m artify --help create       Help on how to generate template files")
                print("python -m artify --help extract      Help on how to use the extract command") 
                return sys.exit(0)
        elif opt == "--debug":
            debug = 1
        elif opt in ("-c", "--command"):
            action = arg
            if action == '':
                print("Invalid command specified")
                return sys.exit(2)
        elif opt == "--proxy":
            proxies['http'] = arg
        
        elif opt == "--proxysec":
            proxies['https'] = arg    
            
        ## Deploy-artifact-awx-host params START
        elif opt in ("-f", "--file", "--format"):
            if action == 'nexus':
                nexus_format = arg
                if nexus_format == '':
                    print("Please specify nexus repository format e.g npm, maven, raw, nuget")
                    return sys.exit(2) 
            elif action == 'deploy':
                file_path = os.path.join(path, arg)
                if os.path.exists(file_path):
                    with open(arg, "rb") as manifest_file:
                        encoded_string = base64.b64encode(manifest_file.read())
                else:
                    print("ERROR: File {} does not exist".format(arg))
                    return sys.exit(2)
            elif action == 'create':
                # Generate file START
                filename_gen = arg
                # Generate file END
            else:
                print("Invalid command specified: param: -f")
                     
        ## Deploy-artifact-awx-host params END
        
        ## Change-version-number params START
        elif opt in ("-t", "--type"):
            change_type = arg
             
        elif opt in ("-a", "--archtype"):
            arch_type = arg 
            
        elif opt == "--prevalue":
            pre_value = arg     
            
         ## Change-version-number params END
        
        ## Deploy-artifact-nexus params START
        ## -h 
        elif opt in ("-h", "--nexushost", "--awxhost", "--host"):
            if action == 'nexus':
                repository_base_url = arg
                if repository_base_url == '':
                    print("Nexus base url cannot be left blank")
                    return sys.exit(2)
            elif action == 'deploy':
                url = arg
            elif action == 'initialize':
                sonarhost = arg
            else:
                print("Invalid {} host specified".format(action))
                return sys.exit(2)
        ## -u
        elif opt in ("-u", "--username"):
            username = arg
            if username == '':
                print("Nexus username cannot be left blank")
        
        
        ## -p
        elif opt in ("-p", "--password"):
            password = arg
            if password == '':
                print("Nexus password cannot be left blank")
                return sys.exit(2)
        
        ## -d 
        elif opt in ("-d", "--directory"):
            directory = arg
            if directory == '':
                print("Please specify directory to store artifact for RAW respository")
                return sys.exit(2)
            
        
        ## -w
        elif opt in ("-w", "--workdirectory"):
            work_directory = arg
            if work_directory == '':
                work_directory = path
                if work_directory == '':
                    print("Please specify artifact current directory")
                    return sys.exit(2)
         
        ## -n  
        elif opt in ("-n", "--artifactname", "--projectname"):
            if action == 'initialize':
                project_name = arg
            else:
                artifact_name = arg
                if artifact_name == '':
                    print("Please specify artifact name")
                    return sys.exit(2)
        
        ## -g
        elif opt in ("-g", "--groupid"):
            group_id = arg
            if group_id == '':
                print("Please specify Group ID")
                return sys.exit(2)
                  
                  
        ## -r
        elif opt in ("-r", "--repository"):
            repository_name = arg
            if repository_name == '':
                print('Please specify repository name')
                return sys.exit(2)
        ## Deploy-artifact-nexus params START
        
        ## Change version (deltav) START
        elif opt in ("-t", "--type"):
            change_type = arg
            
        ## Change version (deltav) END
        elif opt in ("-m", "--message"):
            commit_message = arg
        elif opt in ("-b", "--branch"):
            branch = arg
        ## Commit-push changes repository START
        
        
        ## Commit-push changes repository END
        
        # Initialize START
        elif opt in ("-l", "--language"):
            language = arg
            
        elif opt in ("-k", "--projectkey"):
            project_key = arg
        # Initialize END       
         
    if debug == 1:
        print("Action entered: ", action)
    if action == 'nexus':
        nexus.setup_variables()
        print("Nexus Format entered: ", nexus_format)
        if nexus_format == 'raw':
            nexus.upload_nexus_raw()
        elif nexus_format == 'npm':
            nexus.upload_nexus_npm()
        elif nexus_format == 'maven':
            nexus.upload_nexus_maven()
        else:
            print("Invalid nexus format entered")
            return sys.exit(2)
            
    elif action == 'deltav':
        change_version.modify_version()
    elif action == 'syncrepo':
        syncrepo.commit_push_changes(commit_message)
    elif action == 'deploy':
        deploy.deploy_app_awx()
    elif action == 'create':
        generate_file.generator(filename_gen)
    elif action == 'document':
        #document artifact changes
        pass
    elif action == 'extract':
        extract_commands.extract()   
    elif action == 'initialize':
        #initialize.create_sonarq_project('test-frontend', 'goj-migration')   
        initialize.setup_variables()
        initialize.create_sonarq_project(project_name, project_key)
    elif action == '':
        print("Invalid action specified")
        return sys.exit(2)
    else:
        print("Action not supported")
        return sys.exit(2)
    
    return sys.exit(0) 
    
if __name__ == "__main__":
    main(sys.argv[1:])    
        
        