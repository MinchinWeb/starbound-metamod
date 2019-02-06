# Casual Game Mode Mod

I really like the food system of the normal difficulty but I hate losing everything on death. Is there a mod that can let me have the food system on casual difficulty?

---

I believe you could modify/patch the playermodes.config file to adjust this. That's where all those things should be configured.

ETA: Create a file named playermodes.config.patch:

	[
		{ "op": "replace", "path": "/survival/deathDropItemTypes", "value": "none"}
	]
	
That should work. This will remove the drop penalty from Survival Mode.

(Also, to get this to work, you'll need to set it up in a folder just like a normal mod)

ETA: Alternately, you could instead do this, to add hunger to Casual:

	[
		{ "op": "replace", "path": "/casual/hunger", "value": true}
	]

But I overlooked that simpler solution originally, because I'm an engineer. :3

*via [Reddit](https://www.reddit.com/r/starboundmods/comments/79qr7n/casual_game_mode_mod/)*
