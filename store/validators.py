from django.core.exceptions import ValidationError


def validate_image_size(image):
    # 5 Mb
    max_size_mb = 5

    if image.size > max_size_mb * 1024 * 1024:
        print(image.size)
        raise ValidationError(f'Files cannot be larger than {max_size_mb}MB!')
