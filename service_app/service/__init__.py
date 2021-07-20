import platform


def get_platform():
    return platform.node()


def update_model_instance(model, model_instance, filters):
    update_data = model_instance.__dict__.copy()
    del update_data["_state"]
    del update_data["id"]
    return model.objects.filter(**filters).update(**update_data)
