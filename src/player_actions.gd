'''
Helps with splitscreen or same-screen player input.

Create an instance of this class and feed it the player's controller index.
When you call any of the action functions on this resource, it will append the controller index to the action name.
Ensure your input mappings are set up correctly for this.
'''
extends RefCounted
class_name PlayerActions

var _controller_index: int

func _init(controller_index: int):
    _controller_index = controller_index

func is_action_pressed(action: String) -> bool:
    return Input.is_action_pressed(_get_action_name(action))

func is_action_just_pressed(action: String) -> bool:
    return Input.is_action_just_pressed(_get_action_name(action))

func is_action_just_released(action: String) -> bool:
    return Input.is_action_just_released(_get_action_name(action))

func get_action_strength(action: String) -> float:
    return Input.get_action_strength(_get_action_name(action))
    
func get_action_raw_strength(action: String) -> float:
    return Input.get_action_raw_strength(_get_action_name(action))

func _get_action_name(action: String) -> String:
    return action + str(_controller_index)
