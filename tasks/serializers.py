from rest_framework import serializers
from .models import Task, Photo


# class ImageField(serializers.ImageField):
#     def to_representation(self, value):
#         # Serialize each image in the list individually
#         if isinstance(value, list):
#             return [super(ImageField, self).to_representation(item) for item in value]
#         return super(ImageField, self).to_representation(value)

class ImageAndPrimaryKeyField(serializers.ListField):
    def to_representation(self, data):
        return data.values_list('id', flat=True) if hasattr(data, 'values_list') else data
    def to_internal_value(self, data):
        # Deserialize the data and separate primary keys from image data.
        primary_keys = []
        images = []
        for item in data:
            if isinstance(item, int):
                primary_keys.append(item)
            else:
                images.append(item)
        return primary_keys, images
    

class TaskSerializer(serializers.ModelSerializer):
    # photos = serializers.ListField(
    #     child=serializers.ImageField(max_length=100000, allow_empty_file=False),
    #     required=False,
    # )

    # photos = serializers.PrimaryKeyRelatedField(many=True, queryset=Photo.objects.all(), required=False)
    photos = ImageAndPrimaryKeyField(required=False)
    
    class Meta:
        model = Task
        fields = '__all__'