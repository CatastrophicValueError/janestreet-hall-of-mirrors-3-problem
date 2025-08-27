# Hall of Mirrors 3 — An Interactive Version in Python


## Description
This is an interactive recreation of the Jane Street monthly puzzle [*Hall of Mirrors 3*](https://www.janestreet.com/puzzles/hall-of-mirrors-3-index/) (March 2025) written in Python. The original description of the puzzle is as follows:
> The perimeter of a 10-by-10 square field is surrounded by lasers pointing into the field. (Each laser begins half a unit from the edge of the field, as indicated by the •’s.)
>
> Some of the lasers have numbers beside them. Place diagonal mirrors in some of the cells so that the product of the segment lengths of a laser’s path matches the clue numbers. (For instance, the segments for the “75” path in the example puzzle have lengths 5, 3, 5.) Mirrors may not be placed in orthogonally adjacent cells.
>
> Once finished, determine the missing clue numbers for the perimeter, and calculate the sum of these clues for each side of the square. The answer to this puzzle is the product of these four sums.

I originally made this project as a coding exercise, as I was unfamiliar with using Tkinter and needed an opportunity to work on my code readibility. As the project only uses the (*de-facto* standard) Tkinter library, it can be run on standard Linux/Windows/MacOS installs of Python without having to worry about installing packages.

In short, it's nothing too sophisticated.

## Features & Controls
The controls are fairly simple, and I also provide a short description of them in the code file. Towards the bottom of the file, there's a transcription of the solution to the puzzle. You can uncomment this section and restart the program to see the solution.

#### Adding/Removing Mirrors:
<kbd>left-click</kbd> on the squares in the grid.
- Clicking an empty square places a left-slanted mirror (provided it has no orthogonally adjacent neighbours).
- Clicking a left-slanted mirror turns it into a right-slanted mirror.
- Clicking a right-slanted mirror empties the square again.

#### Firing Lasers:
<kbd>left-click</kbd> on one of the dots to fire a laser. Click the same dot again to clear the laser(s).

#### Clearing the Screen:
Press <kbd>c</kbd> to clear all mirrors, lasers, and numbers from the screen. 

---
All credit for the puzzle concept goes to Jane Street. Have fun! 
