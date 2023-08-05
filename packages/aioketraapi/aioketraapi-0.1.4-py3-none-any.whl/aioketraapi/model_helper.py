


def model_to_json(model) -> dict:
    model_json = model.to_dict()
    for attr in list(model_json.keys()):
        if attr in model.attribute_map:
            model_json[model.attribute_map[attr]] = model_json.pop(attr)
    return model_json