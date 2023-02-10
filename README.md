# sword-and-scale-filter

A GCP Cloud Function that filters out all the Sword & Scale episodes that I don't care about.

## Deploying

After getting into a virtualenv with the projects dependencies (managed by poetry), deploy the
function from the root directory of this project:

```shell
make deploy
```

There's definitely some undocumented stuff. Snoop around and see what you can figure from beyond
this readme.