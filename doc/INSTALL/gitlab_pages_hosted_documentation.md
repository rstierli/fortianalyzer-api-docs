# Hosting your Project Documentation with GitLab Pages

You can host your project documentation directly in GitLab using the GitLab Pages feature.

It is assumed you're now working from the `doc` folder within the python virtual
environment:

```shell
cd ${HOME}/somewhere/my_project/doc
source .venv/bin/activate
```

1. Create a CI/CI pipeline

   - Super easy! 
   - Just rename the `.gitlab-ci.yaml.no` file with `.gitlab-ci.yaml` (you can 
     also use `.gitlab-ci.yml`)

     ```text
     mv .gitlab-ci.yaml.no .gitlab-ci.yaml
     ```
   - Move `.gitlab-ci.yml` to the root of your project.  

2. Make sure your GIT project is using the shared runners that will be used to
   process the CI/CD pipeline

   - Login to the GIT server
   - Enter your project
   - Nagivate to *Settings* > *CI/CD*
   - Locate the *Runners* section and click its *Expand* button
   - Locate the *Shared runners* section and toggle on the *Enable shared 
     runners for this project*

3. Commit your work as usual

   ```text
   git add .
   git commit -m "wip"
   git push
   ```

4. Each time you will commit your work in the `main` branch (that's the
   one considered by your CI/CD pipeline), your project documentation will be
   created and reachable from this place:

   ```text
   https://support.pages.gitlab.frval.fortinet-emea.com/cse-intl-cmm/<PROJECT_NAME>
   ```

VARIABLES default VALUES
| $AWS_UPLOAD_MSG | $AWS_DOC_BUCKET |
| ------ | ------ |
|publish-to-aws   | cmm-doc|


.gitlab-ci.yaml
```
image: python:3.7-alpine

test:
  stage: test
  script:
  - pip install -U sphinx
  - pip install -U sphinx_copybutton
  - pip install -U sphinx_tabs
  - pip install -U sphinxcontrib.images
  - pip install -U sphinx_toolbox
  - pip install -U sphinx_togglebutton
  - pip install -U sphinx_design
  - pip install -U myst-parser
  - pip install -U sphinx_book_theme
  - sphinx-build -b html . public
  rules:
    - if: $CI_COMMIT_REF_NAME != $CI_DEFAULT_BRANCH
    
pages:
  stage: build
  script:
  - pip install -U sphinx
  - pip install -U sphinx_copybutton
  - pip install -U sphinx_tabs
  - pip install -U sphinxcontrib.images
  - pip install -U sphinx_toolbox
  - pip install -U sphinx_togglebutton
  - pip install -U sphinx_design
  - pip install -U myst-parser
  - pip install -U sphinx_book_theme
  - sphinx-build -b html . public
  artifacts:
    paths:
    - public
  rules:
    - if: $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH

aws:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - pwd
    - ls -la
    - aws --version
    - aws s3 sync --delete --acl public-read public s3://$AWS_DOC_BUCKET/$CI_PROJECT_NAME/
  rules:
    - if: '$CI_COMMIT_MESSAGE =~ $AWS_UPLOAD_MSG'
```
