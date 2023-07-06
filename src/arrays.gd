extends Object
class_name Arrays

func _init():
    assert(false, "Do not create an instance of Arrays!")

static func find(array: Array, find_func: Callable) -> Variant:
    for item in array:
        if find_func.call(item):
            return item
    return null

static func random(array: Array) -> Variant:
    if array.size() == 0: return null
    if array.size() == 1: return array[0]

    var rng := RandomNumberGenerator.new()
    rng.randomize()
    var random_index = rng.randi_range(0, array.size() - 1)
    return array[random_index]

static func remove(array: Array, item_to_remove: Variant) -> bool:
    if array.size() == 0: return false

    var index := array.find(item_to_remove)
    if index != -1:
        array.remove_at(index)
    
    return index != -1
