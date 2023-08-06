# Smart Voice Hub Skill SDK - Python

[![pipeline status](https://smarthub-wbench.psst.t-online.corp/gitlab/smarthub_skills/skill_sdk_python/badges/master/pipeline.svg)](https://smarthub-wbench.psst.t-online.corp/gitlab/smarthub_skills/skill_sdk_python/commits/master) 
[![coverage report](https://smarthub-wbench.psst.t-online.corp/gitlab/smarthub_skills/skill_sdk_python/badges/master/coverage.svg)](https://smarthub-wbench.psst.t-online.corp/gitlab/smarthub_skills/skill_sdk_python/commits/master)
[![sonar gate](https://smarthub-wbench.wesp.telekom.net/sonar/api/badges/gate?key=de.telekom.smarthub.skill_sdk_python)](https://smarthub-wbench.wesp.telekom.net/sonar/dashboard?id=de.telekom.smarthub.skill_sdk_python)

You can find the docs here: [Python SDK Docu](docs/README.md)

# Quickstart
Make sure to have an actual version of <a href="https://docs.python.org/3/">**Python 3**</a> (3.7 is minimum required):
`apt-get install python3` if you don't or `brew install python3` if you're on MacOS.

1. Clone the repo: `git clone https://smarthub-wbench.wesp.telekom.net/gitlab/smarthub_skills/skill_sdk_python.git`
    > Alternatively if you have received a source distribution archive, unpack it with `tar xvzf smarthub_sdk-*.tar.gz` command   
2. Change to SDK dir: `cd skill_sdk_python`
3. Run *new-skill* install:   `python setup.py new_skill`

You'll be prompted for:
- The skill name. Give it an Awesome Name! 
- Programming language. Python is Awesome!
- The directory where the project will be created. Make sure it's writable. 

This script will:
- Create a new project in the directory of your choice.
- Add a virtual environment to `.venv` inside your project.
- Install required dependencies.
 
You may now open your skill directory as a project in PyCharm. 

> If you get an error `This package requires Python version >= 3.7 and Python's setuptools`, you happen to have an outdated Python version.
> Check it with `python --version` and make sure it is >= 3.7

*Happy coding!*

# Further reading:
- Please check the [installation guide](docs/install.md) for technical details.
- You can find the docs here: [Python SDK Documentation](docs/README.md) 
- Even more details are at [gitlab pages](https://smarthub-wbench.wesp.telekom.net/pages/smarthub_skills/docs/public/skill_sdk_python/README.html)
- Have a look at the [Contribution Guide](CONTRIBUTING.md)
- [Working with Demo Skill](docs/articles/demo_skill.md)
- [Creating a Custom Weather Skill](docs/articles/weather_skill.md)

Requires Python 3.7! [Type hints](https://docs.python.org/3/library/typing.html) FTW!
* [PEP 526: Syntax for variable annotations](https://docs.python.org/3.6/whatsnew/3.6.html#whatsnew36-pep526)
* [PEP 484: Type Hints](https://docs.python.org/3.5/whatsnew/3.5.html#whatsnew-pep-484)

# Remark:
This repository uses the `*_test.py` naming schema. PyCharm discovers everything automatically. But if you like to invoke unit tests from the command line, and you are not sure about how, please check `scripts/test`.
