Summarizing

**Overall thoughts on the refactor**
- The separation of responsibilitiesis fine enough. There is overlap between input handling and displaying 
- There are many minor things that need adjusting to clean up the code


**How this helps development UI Overhaul**
- UI changes can happen everywhere because the UI is being drawn by one object

**How this helps development Levels**
- Each level can just import game and UI and most of the game will be done. (this makes the unique elements easier to add)

**How can I mix this with the scenes and scene manager I implemented?**
- This can be implemented with the scene manager with reasonable amount of time and effort. 
- This is only the game itself and has no actual navigable interface (Where the scene manager is most important)
- It is still valuable to work on it


**What can be improved**
- Main game loop can be simplified to only having to call updates and keep a counter (I don't think the main loop should handle logic)
	- Something like game.update() & UI.update
	- However with the scene manager only scene updates need to be called and the individual scenes will update their game and UI
- Input handling should be more general
	- Playing a key directly calls a function, but there will be different screens that use those buttons differently