from kivy.utils import platform
from android.permissions import request_permissions, Permission

def request_permissions():
    if platform == 'android':
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.CAMERA
        ]) 