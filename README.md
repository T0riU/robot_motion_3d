# 3D Motion Visualizer

This is a university project. The code is straightforward but not clean. Everything lives in one file with global variables shared across functions and a background thread updating the matplotlib canvas directly, which is not thread safe. It works well enough to demonstrate the algorithm but you would not want to build on top of it.

A small desktop app that visualizes how a 3D Bresenham line algorithm moves a point from one coordinate to another. You set a target position, hit play, and watch the path get drawn step by step in a 3D chart.

## What it does

You give it a destination point anywhere in a 500x500x500 space and it calculates the path using the 3D Bresenham algorithm, which figures out which integer grid steps to take so the resulting line is as straight as possible. Each step gets drawn live on the chart so you can see the path build up in real time.

You can pause mid-animation, stop it early, change the speed, tweak the colors and marker size, and zoom in and out on the chart with the scroll wheel. Double clicking the middle mouse button resets the zoom back to default.

## Controls

The four buttons at the top do the following. Play starts the animation. The pause button freezes it mid-step so you can inspect where it is. Stop cancels the whole thing. The chart icon opens the coordinate picker where you drag sliders to set the X, Y, and Z target.

The Settings button at the bottom opens a panel where you can adjust animation speed in milliseconds per step, pick a color for the line and the point markers separately, and change the marker size.

## The algorithm

The core of the project is the step_3d function which implements one step of the 3D Bresenham algorithm at a time. It figures out which axis is dominant based on the distances to travel, advances along that axis by one, and uses error accumulators to decide whether to also step on the other two axes. Calling it in a loop from the current position to the target traces a straight line through integer coordinates.

## Files

```
motion.py          the whole application
motion.spec        PyInstaller config to build a standalone exe
icon.ico           window icon
```

## Requirements

```
tkinter
matplotlib
```

## Running it

Run motion.py directly with Python. If you want a standalone exe, PyInstaller is already configured via the spec file. Run pyinstaller motion.spec and the exe will appear in the dist folder.
