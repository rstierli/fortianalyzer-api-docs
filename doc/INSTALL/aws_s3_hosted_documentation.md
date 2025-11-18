# Hosting your Project Documentation with AWS S3

You can host your project documentation directly in AWS S3.

It is assumed you're now working from the `doc` folder within the python virtual
environment:

```shell
cd ${HOME}/somewhere/my_project/doc
source .venv/bin/activate
```

1. Look at the `aws` block in the `.gitlab-ci.yaml`

   - Enter following command:

     ```shell
     cat ../.gitlab-ci.yaml
     ```

   - You should see the `aws` block at the end of the file output:

     ```yaml
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

2. You can see a `if` condition

   ```yaml
   rules:
     - if: '$CI_COMMIT_MESSAGE =~ $AWS_UPLOAD_MSG' 
   ```

3. Basically this CI/CD stage will be run if the commit message (what you pass
   with the `-m` option) contains the keyword in the `AWS_UPLOAD_MSG`
   GITLAB variable

4. The `AWS_UPLOAD_MSG` has been set for `cse-int-cmm` GitLab group with the
   `publish-to-aws` value

5. Hence to publish your project documentation in a AWS S3, you just need to
   commit as usual but with a different message:

   ```shell
   git add .
   git commit -m "wip - publish-to-aws"
   git push
   ```

6. To reach your project documentation you will have to use the following URL

   ```text
   https://cmm-doc.s3.eu-west-1.amazonaws.com/<PROJECT_NAME>/index.html
   ```
