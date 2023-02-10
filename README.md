# sword-and-scale-filter

A GCP Cloud Function that filters out all the Sword & Scale episodes that I don't care about.

## Deploying

After getting into a virtualenv with the projects dependencies (managed by poetry), deploy the
function from the root directory of this project:

```shell
make deploy
```

After that's done, look at the GCP console for the URL, and bam! Bob's your uncle. Can throw that in
a supporting podcast app.

There's definitely some undocumented stuff here. Setting up cloud infra is easier in the web console
once than repeatably on the command line.
