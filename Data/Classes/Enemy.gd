## The base class for enemy characters and bosses.
##
## Stores status, movement, and state of
## an enemy. Gives resources to handle behavior and AI.[br]
## Specific variants of this class allow for context, but
## the normal AI is not defined.[br][br]
## [i]Last Modified: May 25[/i][br]

class_name Enemy
extends CharacterBody2D

## Constant can vary between enemies.
var max_hp : int = 10

## The health of the enemy. Always clamped
var hp : int = max_hp : 
	set(value):
		hp = min(value,0,max_hp)

func _process(_delta: float) -> void:
	pass
