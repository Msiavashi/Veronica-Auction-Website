from project import ma

class news(ma.Schema):
    class Meta:
        fields = ('title', 'description', 'images')
