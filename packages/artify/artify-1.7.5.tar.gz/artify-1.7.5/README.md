
Upload to Nexus, Upload files to hooks, Modify version number, Sync to GitLab type repository, Generate template files, Extract commands from Git commit messages, Create SonarQube projects

Installation
============
You can download and install the latest version of this software from the Python package index (PyPI) as follows::

    pip install --upgrade artify

Usage
=====
    python -m artify --help=

    python -m artify --command <command> [Options]
or

`python -m artify -c <command> [Options]`


**Params**

command &nbsp; &nbsp; &nbsp; &nbsp; nexus, syncrepo, deploy, deltav, create
<br>

Upload to Nexus
===============

    python -m artify -c nexus -f <format> -n <artifact_name> -h <nexus_repository_base_url>

**Important**

Artifact name should include artifact id and version number. E.g example-ws-1.0.0.war

**Params**

-f, --format &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Nexus upload format. Types supported: raw, npm, maven

-w, --workdirectory  &nbsp;&nbsp; &nbsp; Working directory of artifact to be uploaded to Nexus repository

-n, --artifactname &nbsp;&nbsp;&nbsp; &nbsp; &nbsp; Artifact name

-r, --repository &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; Nexus repository to upload to: e.g <repository>-snapshots

-g, --groupid &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Group ID for Maven2 type repository, Environment variable: NEXUS_GROUP_ID

-d, --directory &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp;&nbsp;&nbsp; &nbsp; Directory for RAW type repository

-u, --username &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Username of nexus user, Environment variable: NEXUS_USERNAME

-p, --password &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; Password of nexus user, Environment variable: NEXUS_PASSWORD

--proxy &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;  Sets Http proxy

--proxysec  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Sets Https proxy


### Environment variables need
**NEXUS_GROUP_ID** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Group ID of the project e.g com.testing.testapplication
**NEXUS_USERNAME** &nbsp; &nbsp; &nbsp; &nbsp; Username of nexus user that will upload artifact
**NExUS_PASSWORD** &nbsp; &nbsp; &nbsp; &nbsp; Password of nexus user that will upload artifact

<br>

Deploy App using custom AWX host
================================

    python -m artify -c deploy -f <manifest_file.yml> -h <awx_host>

### Environment variables need
**DEPLOY_TOKEN** &nbsp; &nbsp; &nbsp; &nbsp; Token used to deploy application
<br>

Change Package version
======================

Artify uses semantic version 2.0.

`python -m artify -c deltav -t patch -a npm`

**Params**

-a, --archtype &nbsp; &nbsp; &nbsp; &nbsp; npm, gradle, flutter, maven, dotnet

-t, --type &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; major, minor, patch, prerelease

**Optional Params**
For Prerelease version change
--preValue          Prerelease version value e.g SNAPHOT, RELEASE, BUILD, beta, alpa
<br>

Push changes to GitLab repository
=================================

### Recommendation: You can create a feature branch, then perform your code changes before pushing changes to remote
    python -m artify -c syncrepo -m <message> -b 

**Params**
 
 -c, --message &nbsp; &nbsp; &nbsp; &nbsp; Commit message
 -b, --branch &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Optional, by default, it will push to 'develop' branch

### Environment variables need
**PRIVATE_TOKEN**, popularly known as personal access token is needed to perform the push. This can be created by following this guide:
[Creating a personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

N.B A commit is performed automatically followed by a push

Generate Template files
=======================

### Generate template .gitlab-ci.yml file
`python -m artify -c create -f gitlabci` 

### Geneate template manifest.yml file
`python -m artify -c create -f manifest`

**Params**
-f, --file &nbsp; &nbsp; &nbsp; &nbsp; File template to generate

**Supported files**
- .gitlab-ci.yml
- manifest.yml

Extract commands from GIT message
=================================
`python -m artify -c extract`

**N.B** If manifest.yml file is present, it will update version number in that file also.

**Parameters**

- version/deltav - specifies type of version change e.g "version": "patch", "deltav": "patch", "version": "minor"



- archtype - specifies project architecture e.g "archtype": "npm", "archtype": "gradle", "archtype": "flutter"



- branch - speficies branch you want to push changes. If branch is not specified, it push changes to 'develop' branch by default



**Sample commit messages**

1. Added login functionality {"version": "patch", "archtype": "npm", "branch": "release-1.0.0" } - Updates the patch version of npm type project, and push to branch called 'release-1.0.0' branch


2. Added search functionality {"deltav": "major", "archtype": "gradle" } - Updates the major version of a java project with Gradle build tool


3. Added edit functionality {"version": "minor", "a": "flutter" } - Updates the minor version of a flutter project  

<br/>

Initialize SonarQube project
============================

`python -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -a <arch_type/os> -l <language>`

**Sample command**

`python -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -l java -a gradle`

`python -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -l java -a maven`

<br />

**For Windows Runner, Other (JS, TS, Go, Python, PHP, ...)**  

python -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -l other -a windows

<br />

**For Linux/macOS runner, Other (JS, TS, Go, Python, PHP, ...)**

python -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -l other -a linux

<br />

**Parameters**

-l, --language =>  Possible values: JS, TS, Go, Python, PHP, other)

-a, --archtype =>  Architecture, OS (depends on usage)

-n, --projectname => Project name.

-k, --projectkey => Project key. This should be a unique identifier for project.

-u, --username => Username for SonarQube. 

-p, --password => Password for SonarQube. The user should be able to create projects.

**N.B**. The user should have the permission to create/modify projects.

python -m artify -c initialize -h <SonarQube_base_url> -u <username> -p <password> -a php

