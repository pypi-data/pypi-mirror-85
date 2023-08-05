# lib-template

This is a template repo for creating libs in shuttl

This template comes with dependabot and github workflows integrated in it.

Dependabot:
- To raise prs for updating dependencies with minor version bump

Github workflows:
- Close stale prs
- Python package : run black, flake8 and pytest coverage on every pull request and push to master
- Python publish : Publishes package corresponding to a tag at Pypi. Triggered by `release` step in `Makefile`
- Auto approve pr: to approve safe-to-merge dependabot prs.

Checkout the status of the workflows through the Actions tab on your repository

![Alt text](readme/actions.png?raw=true "Actions in Action")


Add your lib as a submodule in [monorepo-libs](https://github.com/Shuttl-Tech/monorepo-libs)


## Releasing 


####Steps to follow:
- `make bump_version`
- Update [the Changelog]
- Commit changes to `Changelog`, `setup.py` and `setup.cfg`.
- `make push_tag` (this'll push a tag that will trigger python package checks)
- `make release` (this will release the tag)

####Note 

If this is your first release, make sure you visit the `realease` rule in the  `Makefile`.
You are expected to change the `REPO_URL` to github url of your repository.
