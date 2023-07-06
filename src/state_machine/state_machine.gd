'''
Cool state machine system by DevDuck
Source: https://youtu.be/vxRzLf4PdgY?t=486
'''
extends Node
class_name StateMachine

var current_state: State

func change_state(new_state: State):
    if current_state != null:
        current_state.set_process(false)
        current_state.set_physics_process(false)
        current_state.exit()

    current_state = new_state
    current_state.enter()
    current_state.set_process(true)
    current_state.set_physics_process(true)
