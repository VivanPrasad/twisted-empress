## The main class for enemy drops to be 
## collected by the player.
##
## Stores status, movement, and state of
## an enemy. Gives resources to handle behavior and AI.[br]
## Specific variants of this class allow for context, but
## the normal AI is not defined.[br][br]
## [i]Last Modified: May 25[/i][br]
class_name Drop
extends Area2D

## 
@export_enum("hp","mp","xp") var type : String = "hp"
