# nbcourse: publish your course based on Jupyter notebooks

## Features

`nbcourse` helps you building a static website to publish your course content in the form of jupyter notebooks (one notebook for one chapter).

Main features:

- all the configuration is described by a single `nbcourse.yml` file
- it is based on [doit](https://pydoit.org) in order to build efficently the html files
- chapters can be displayed in *preview mode* only so attendees can see the whole course program without being able to access content of the lessons to come
- notebooks can be:
    - rendered as static html files,
    - rendered as static reveal slideshows,
    - packaged with all their material in a downloadable archive,
    - compiled in a single pdf book using [bookbook](https://github.com/takluyver/bookbook)
- the theme can be easily customized (html files are templated using jinja)

See [this python course](https://mm2act.pages.math.unistra.fr/cours-python/) (in French) as an example.

## Installation

```bash
pip install nbcourse
```

## Usage

### Initiate an empty nbcourse project

```bash
nbcourse --init
```

### Configure your website

- Put your notebooks file in the `notebook/` directory
- Edit the `nbcourse.yml` file created by the `nbcourse --init` command.

### Build your website

```bash
nbcourse
```

Resulting files are in the `build/` directory.

### Get help

```bash
nbcourse --help
```

### Publish

Publishing with [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/) is as simple as adding a `.gitlab-ci.yml` file such as:

```yaml
pages:
  image: boileaum/jupyter
  script:
    - pip install nbcourse
    - nbcourse -n 5
    - mv build public
  artifacts:
    paths:
      - public
```
