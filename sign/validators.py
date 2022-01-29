def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.3gp','.mp4','.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.xlsx', '.txt', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Siz faqat ko'rsatilgan kengaytmadagi fayllarni yuklay olasiz !")