# Cubing Tools
A python gui and toolset for speedcubing

## Features

### Timer
- Under the Timer tab
- Press space to prime the timer
- Let go of space to start the timer
- Solve the twisty puzzle!
- Press space to stop the timer
- Times and averages are logged under Logs

### Logs
- Under the Logs tab
- Lists the single, ao5, and ao12 times for each solves
- aox times are averages of the last x solves

### Solver
- Under the solver tab
- Click on a sticker to change it to the current active color
- Use U, R, F, D, L, and B keys to change the current active color
- Press G to find the shortest solution
- Solutions are found to a depth of 10moves/phase (python port of kociemba's algorithm)