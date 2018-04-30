from project import ma

class category(ma.Schema):
    class Meta:
        fields = ('id','name', 'description')
