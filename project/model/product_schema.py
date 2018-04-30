from project import ma

class product(ma.Schema):
    class Meta:
        fields = ('id','name', 'total_available','review','stars','details')
