from django.db.models import Model

def seed_users(model:Model, data_list: list, password:str):
    for user_obj in data_list:
        user = model.objects.create(**user_obj)
        user.set_password(password)
        user.save()
