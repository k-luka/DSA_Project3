class Scene:
    # Class that stores the models for objects to be rendered on the GPU
    def __init__(self, app):
        self.app = app
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def render(self):
        for obj in self.objects:
            obj.render()
