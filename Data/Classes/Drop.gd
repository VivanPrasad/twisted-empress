## The main class for enemy drops to be 
## collected by the player.
##
## Stores status, movement, and state of
## an enemy. Gives resources to handle behavior and AI.[br]
## Specific variants of this class allow for context, but
## the normal AI is not defined.[br][br]
## Last Modified: June 30[br]
class_name Drop
extends Area2D

## The Drop Type
@export_enum("hp","mp","xp") var type : int = 0

