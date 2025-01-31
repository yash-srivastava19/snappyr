# Snappyr - Setup Projects Blazingly Fast.

[PyPI](https://pypi.org/project/snappyr/)
[Repo](https://github.com/yash-srivastava19/snappyr)

## Introduction
I'm someone who works a lot on different projects, especially in python. Having to manually set up things that takes me sometime to do, takes away the fun from it. Tools like poetry or uv are preferred for project management, but in my case, I require just the project setup, I can manage other things. 

That's why I created Snappyr. It is a basic tool that just does it for me. With this tool in my arsenal, I focus my energy on creating projects, not worrying about other things. Snappyr is hardly 100 LOC, in pure python without any external dependencies, but it helps me a ton.

## Features
Snappyr does a lot of redundant tasks, especially the ones we do in the start of a new python project. These include:

1. **Create the directory structure**. Snappyr sets up the project directory. Snappyr can be made to adjust as per your need. Just fork the project, and create your own version. The format that works for me is:

```python
project_name
|__ src/
|__ tests/
|__ scripts/
|__ docs/
|__ venv
|__ .env
|__ .gitignore
|__ main.py
|__ README.md
|__ requirements.txt
```


2. **Setting up virtual environment**. Snappyr uses python virtual environment behind the scenes and creates a venv so that we don't run into dependency conflicts.

3. **Setup Git Repository for the project**. By default, git is initialized in the project working directory. This can also be connected to a remote repository, or can be later configured using Git CLI.

4. **Package Mode**. If I'm working on developing a library(which is often the case), I can specify in the Snappyr CLI and it'll configure the `setuptools` and other necessary requirements to be used for your project.

5. **Pre-commit hooks**. Snappyr also add a boilerplate pre-commit hooks for the project.

## Usage
Using snappyr is pretty easy. First, download the package through PyPI:

```bash
pip install snappyr
```
Snappyr is available through CLI, which can be run using poetry. After installing, use the commands to run:

```bash
poetry run snappyr --project_name="severance" --is_package=False
```

The options available in the CLI are
`--project_name`: This is your project name. You can set this whatever you want.
`--is_package`: If the project you are working on is a package, Snappyr will add additional things too.

### Get it to work.
I feel the right way to use Snappyr is not through package, but setting this up in your machine so you can call it from anywhere. You just need to copy the `main.py` (renamed to snappyr), and follow the instructions as per your machine.

#### Windows

1. Save the Script: Save the code as `snappyr.py` in a directory, e.g., C:\my_scripts.

2. Add the script to PATH:

- Open the Start Menu and search for "Environment Variables.
- Click Edit the system environment variables > Environment Variables.
- In the System Variables section, find the Path variable, select it, and click Edit.
- Add the path to your directory (e.g., C:\my_scripts) and click OK.
- Make It Callable: In C:\my_scripts, create a batch file (e.g., `snappyr.bat`) with the following content:

```bat
@echo off
python %~dp0snappyr.py %*
```
3. This makes the script callable from anywhere in the command prompt as:

```cmd
snappyr <project_name>
```

#### Linux/Mac

1. Save the `main.py` as `snappyr.py`(or any other name you want)

2. Make the file Executable, run the following command:

```bash
chmod +x snappyr.py
```
3. Move it to a directory in your PATH (e.g., /usr/local/bin) so you can call it from anywhere:

```bash
mv snappyr.py /usr/local/bin/snappyr
```

4. From your terminal, run:

```bash
snapper <project_name>
```

After setting this up, you can set up your projects as(from anywhere!!):

```bash
snappyr my_python_project
```

## Contributing
This is a very small project, so it'll be very easy to add features. Get in touch with me if you have any ideas, and we can work on PRs.