# Breakdown

1. general layout / menu
2. gameplay UI (readable gameplay)
3. other style and art things

## General layout

Menu requirements
- Screen switching 
	- One solution is filling the screen with black then laying over new buttons and images. The game loop will also need to change according with the screen. Use [video](https://www.youtube.com/watch?v=GMBqjxcKogA&t=55s) as a overview of this solution
- Buttons
	- Pygame doesn't have an inbuild button object so one will have to be created
- What fills the menu
	- Levels
	- Challenges
	- Settings
	- Quit

## Gameplay UI

Elements of the UI
- Name of level or challenge you are playing
- Next block(s)
- Blocks themselves
- Grid / What the blocks are on
- Pause button

UIs I found

![172](https://c8.alamy.com/comp/FMX9TG/tetris-device-interface-tetris-gaming-device-interface-game-block-FMX9TG.jpg)

This one has most of the elements I would like. It has a line score indicating how many lines you have cleared but I don't know if we are implementing this. 
What I like about this UI
- The scores are easy to read. 
- Blocks mesh together well after dropping them
What I don't like
- The grid is offset from the center.  
- No visible grid
I would improve this by 
- making the information on the right smaller 
- Maybe split the information to be on the left and right so you can have the grid in the center
- Brighten the next block to be more obvious when not directly looking at it
- Visible grid

![220](https://img.magnific.com/free-vector/brick-game-vector-template-mobile-app-play-computer-digital-retro-technology-illustration_1284-42796.jpg?semt=ais_hybrid&w=740&q=80)

This is very similar to the one before so it has most of the same complaints, however what I don't like about this one is the design of the blocks.

Why the blocks are bad
- Don't mesh well after drop
- Over designed
	- The blocks have an outline, shaded center, and bright top

All these make previous shapes are easy to identify, but I feel that they burst out too much and cause too much visual clutter

![268](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBzMFID2-MtBe2f-eB9BQ6kycsnAUzBTszA_rUsklFtZ6w23UmyKb5RWU&s=10)

What I like
- Next block is in the center
	- Your eyes travel a shorter distance on average

What I don't like
- Grid looks slightly off center
- No visible grid lines
- Statistics
	- Feels unnecessary, maybe can be after you quit or pause the level.

What I would change
- Lines is displayed in the same box as the score
- Level replaces lines at the top
- Removing or shrinking stats to put the grid center

![249](https://www.digitaltrends.com/tachyon/2019/02/randoms.jpeg?resize=720%2C720) ![248](https://assetsio.gnwcdn.com/tetris-99-hides-the-way-it-works-and-thats-brilliant-1550764447836.jpg?width=1200&height=1200&fit=crop&quality=100&format=png&enable=upscale&auto=webp)

I like this UI the most out of the other examples because
- Grid is minimal and visible
- Next blocks are different colors to better distinguish them
	- I don't think we are having multiple next blocks, but if it comes up in a challenge or level this is a good design
- Blocks already dropped mesh well and are readable

## Other style and art things

Not putting much thought into this now, will make the basic UI first then worry about this.

Other UI/UX elements
- Sound effects
- Line(s) clear animation
- Music