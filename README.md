# PS-Upskilling

This is the upskilling gamification/tracker for Project Snowden. It consists of a Jinja-fied HTML template, some static assets, a flat-file database, and a Python script that transforms all of these into a static site showing the current status of the Project Snowden team member's directed upskilling progress. The intention is that this system can be used for the lifetime of the project.

## Update Process

The main Python code lives in `generate.py`, the data on modules, tasks, members and their progress lives in the equivalent `data/*.yml` files, the templated files live in `/templates`, while the current visible static site lives in `/docs`. In order to update the site, you should cut a new branch, update the YAML files with the new details, run `generate.py`, then commit the whole batch of changes. Once you push and merge that branch, the publicly visible website will have the updated information.

## Development process

The only difference here is that you *must* test your changes locally by passing in the "--test" argument. This places the output into a folder named `docs-test` that is in the `.gitignore` folder and can therefore never be added to the repository. Once you are happy with the changes to the python code, you can then proceed as above to update the "live" folder (`/docs`).