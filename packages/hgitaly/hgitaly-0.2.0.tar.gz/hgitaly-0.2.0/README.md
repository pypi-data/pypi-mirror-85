# HGitaly

HGitaly is Gitaly server for Mercurial.


## Updating the Gitaly gRPC protocol

The virtualenv has to be activated

1. `pip install -r dev-requirements.txt`

2. Copy the new `proto` files from a Gitaly checkout with
   version matching the wanted GitLab upstream version.
   Example in a HDK context:

   ```
   rm protos/*.proto
   cp ../gitaly/proto/*.proto protos/  # we dont want the `go` subdir
   ```

3. run `./generate-stubs`

4. run the tests: `./run-all-tests`

5. perform necessary `hg add` after close inspection of `hg status`
