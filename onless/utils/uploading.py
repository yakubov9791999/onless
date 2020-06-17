# import xlrd
#
# from user.models import User
#
#
# class UploadingPupils(object):
#     foreign_key_fields = ['school']
#     model = User
#
#     def __init__(self, data):
#         data = data
#         self.uploaded_file = data.get('file')
#         self.parsing()
#
#     def getting_related_model(self, field_name):
#         related_model = self.model._meta.get_field(field_name).rel.to
#         return related_model
#
#     def getting_headers(self):
#         a = self.s
#         headers = dict()
#         for column in range(s.ncols):
#             value = s.cell(0, colum)
#             n
