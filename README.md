# QtThree

A (very much) simplified version of the Three.js 3D editor written with PySide2 and PyQtGraph.

## Requirements

- Python 3.7+
- Python OpenGL bindings ([windows/osx](http://pyopengl.sourceforge.net/) / [linux](#linux-python-opengl-bindings))

## Setup & Usage

I recommend setting up a virtual environment for installation.

```sh
$ pip install -r requirements.txt
$ python -m qtthree
```



## Project Design

Please read below for all of my design decisions relating to the development of this project.

### Rendering

Rendering of the scene is handled via PyQtGraph's OpenGL widget.

### Object Transformation

Transformation of objects is maintained internally by PyQtGraph's `Transform3D` class. This class is simply
an extension of Qt's `QMatrix4x4` with some additional helper methods.

The `QMatrix4x4` class, and by extension the `Transform3D`, make it very simple to rotate and laterally transform
objects.

### In-Memory Object Storage

Internally, objects are all written as a subclass of an `AbstractShape`. This base class provides helper methods
that can be easily modified to include the additional fields implemented by the inhereting classes. This also enables
shape classes to be easily serialized without the duplication of code.

For instance, a `Box` is an extension of the `AbstractShape` with `length`, `width`, and `height` fields added.

### Type-Hinting

Originally, everything written was type-hinted, but the codebase was littered with `type: ignore`, simply because
the typings for PySide2 are not that great. Type validations were failing, even though the code was correct.
I've decided to disable Python type-checking in my workspace due to the poor typings of PySide2.

## Linux Python OpenGL Bindings

Installing the Python OpenGL bindings is dependent on your distribution.

Please refer to your package manager's version of the `python-opengl` package.