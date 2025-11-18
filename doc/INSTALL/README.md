# Table of Contents

- [Table of Contents](#table-of-contents)
  - [How to create your doc environment](#how-to-create-your-doc-environment)
    - [Clone this CMM Team Standard Documentation GIT repo](#clone-this-cmm-team-standard-documentation-git-repo)
    - [Rename the cloned GIT repo](#rename-the-cloned-git-repo)
    - [Remove GIT repo information](#remove-git-repo-information)
    - [Install sphinx documentation system](#install-sphinx-documentation-system)
      - [Create a python virtual environment](#create-a-python-virtual-environment)
      - [Automatic installation using the requirements file](#automatic-installation-using-the-requirements-file)
      - [Manual installation](#manual-installation)
      - [Tune your environment](#tune-your-environment)
    - [Working with the CMM Team Standard Documentation System](#working-with-the-cmm-team-standard-documentation-system)
    - [Hosting your Project Documentation in GitLab Pages](#hosting-your-project-documentation-in-gitlab-pages)
    - [Hosting your Project Documentation in AWS S3](#hosting-your-project-documentation-in-aws-s3)
    - [Before starting your documentation project](#before-starting-your-documentation-project)

## How to create your doc environment

This documentation explains how to quickly integrate the latest CMM Team Standard Documentation system in your GIT project.

It is assumed that you have an existing GIT project named `my_project` and that you run the steps described in this document from within this project:

```shell
cd ${HOME}/somewhere/my_project
```

### Clone this CMM Team Standard Documentation GIT repo

1. Use the following command

   ```shell
   git clone https://gitlab.frval.fortinet-emea.com/support/cse-intl-cmm/sphinx_doc_template.git doc
   ```

   `doc` will be now the folder where you will place your documentation

> This is mandatory to use /doc folder to host your sphinx documentation

### Remove GIT repo information

1. Enter the `doc` folder and delete the `.git` file

   ```shell
   cd doc
   rm -rf .git
   ```

### Install sphinx documentation system

It is assumed you're now working from the `doc` folder:

```shell
cd ${HOME}/somewhere/my_project/doc
```

#### Create a python virtual environment

1. Enter the following commands

   ```shell
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install pip --upgrade
   deactivate
   ```

#### Automatic installation using the requirements file

> Using the `requirements.txt` file ensures that python libraries installed are the one that work *now* using specific version (ex Sphinx==7.2.6) and always use this release.

1. Enter the following commands

   ```shell
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

#### Manual installation

> Manual install use the last available release of packages and could potentially cause issues, using `requirements.txt` method is prefered.

1. Enter the following commands

   ```shell
   source .venv/bin/activate
   python -m pip install sphinx
   python -m pip install sphinx_copybutton
   python -m pip install sphinx_tabs
   python -m pip install sphinxcontrib.images
   python -m pip install sphinx_toolbox
   python -m pip install sphinx_togglebutton
   python -m pip install sphinx_design
   python -m pip install myst-parser
   python -m pip install sphinx_book_theme
   python -m pip install sphinx-autobuild
   python -m pip install awscliv2
   ```

#### Tune your environment

1. Edit `conf.py` file

   - You will certainly need to change the following variables:

     ```text
     project = 'Template_Project' << !! This template name will be used in the documentation public URL !!
     copyright = '2024, CMM_Team'
     author = 'CMM_Team'
     release = '0.1'
     ```

### Working with the CMM Team Standard Documentation System

1. Test the Sphinx doc generation process using `make html`

It is assumed you're now working from the `doc` folder within the python virtual
environment:

```shell
cd ${HOME}/somewhere/my_project/doc
source .venv/bin/activate
#generate static pages from the 000_hello_world.mdfile
make html

```

2. Run the `livehtml` command to start local webserver and see live your code changes ! 


```shell
cd ${HOME}/somewhere/my_project/doc
source .venv/bin/activate
#generate static pages from the 000_hello_world.mdfile
make livehtml

```



The following table give you the most useful commands that you can use to manage your sphinx documentation:

| Command           | Role                                                                                   | Notes                                                   |
| :---------------- | :------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `make html`       | Generate the HTML documentation                                                        | Point your browser to the `_build/html/index.html` file |
| `make clear`      | Delete the HTML documentation                                                          |                                                         |
| `make livehtml`   | Generate the HTML documentation and open your browser to point automatically to it     | Doc is also auto-refreshed!                             |
| `make upload`     | Upload HTML documentation to AWS S3 storage , create a doc.zip file for fortipoc usage | `Readme.md` file is auto-updated with generated links.  |
| `make cleanweb`   | Clean the published HTML documentation                                                 | `Readme.md` file is auto-updated to remove links.       |
| `make gitpages`   | Enable Gitlab pipeline to auto-generate and publish documentation on Gitlab server     | `Readme.md` file is auto-updated with generated links.  |
| `make nogitpages` | Disable Gitlab pipeline and stop generating and publish documentation on Gitlab server | `Readme.md` file is auto-updated to remove links.       |

### Hosting your Project Documentation in GitLab Pages

See [here](gitlab_pages_hosted_documentation.md)

### Hosting your Project Documentation in AWS S3

See [here](aws_s3_hosted_documentation.md)

### Before starting your documentation project

1. if needed, you can now delete the `INSTALL` folder

   ```shell
   rm -rf INSTALL
   ```
