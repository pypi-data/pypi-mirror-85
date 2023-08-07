# Changelog

## [0.3.3] - 2020-11-19

### Changed

* Fix bug in HTML template due to new nbconvert
* Fix bug in REVEAL url

## [0.3.2] - 2020-11-06

### Changed

* Handle bookbook import error

## [0.3.1] - 2020-11-06

### Changed

* Use flit instead of poetry

## [0.3.0] - 2020-11-05

### Changed

* `style_ipython.tplx` -> `style_ipython.tex.j2` in `/theme/default/templates/book.tplx`. Please update this file in your local `theme/` dir if you are using nbconvert >= 6.0
* Some code enhancement

### Fixed

* Fix issues with pdf generation using nbconvert >= 6.0
