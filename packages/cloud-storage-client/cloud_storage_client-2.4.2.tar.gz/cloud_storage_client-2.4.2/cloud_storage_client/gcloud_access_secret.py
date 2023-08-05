from boto3.session import Session
from botocore.client import Config
from botocore.handlers import set_list_objects_encoding_type_url
import tarfile
import os
import shutil

class GCloudStorageClientAccessKeySecretKey():
    """
    Boto3 Client to connect with Google cloud storage
    """

    def __init__(self, bucket_name, access_key, secret_key, region=None):
        if region == None or region == '':
            self.region = 'US-CENTRAL1'

        self.session = Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=self.region)
        self.session.events.unregister('before-parameter-build.s3.ListObjects', set_list_objects_encoding_type_url)
        self.s3 = self.session.resource('s3', endpoint_url='https://storage.googleapis.com', config=Config(signature_version='s3v4'))
        self.bucket = self.s3.Bucket(bucket_name)
        self.bucket_name = bucket_name

    def delete_file(self, file_path):
        if file_path[0] == '/':
            file_path = file_path[1:len(file_path)]
        for obj in self.bucket.objects.filter(Prefix=file_path):
            obj.delete()

    def delete_folder(self, folder_id):
        if folder_id[0] == '/':
            folder_id = folder_id[1:len(folder_id)]
        for obj in self.bucket.objects.filter(Prefix=folder_id + '/'):
            obj.delete()

    def download_folder(self, folder_id, folder_output):
        if not os.path.exists(folder_output):
            os.makedirs(folder_output)
        if folder_id[0] == '/':
            folder_id = folder_id[1:len(folder_id)]
        for obj in self.bucket.objects.filter(Prefix=folder_id + '/'):
            splitted_name = obj.key.split('/')
            splitted_name = list(filter(None, splitted_name))
            self.bucket.download_file(obj.key, folder_output + '/' + splitted_name[len(splitted_name) - 1])

    def upload_file(self, src_file, dst_file, options):
        if dst_file[0] == '/':
            dst_file = dst_file[1:len(dst_file)]
        if dst_file[-1] == '/':
            dst_file = dst_file[0:len(dst_file) - 1]
        dst_file = dst_file.replace('//', '/')

        with open(src_file, 'rb') as data:
            self.s3.Object(self.bucket_name, dst_file).put(Body=data)

    def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
        if folder_id[0] == '/':
            folder_id = folder_id[1:len(folder_id)]
        if folder_id[-1] == '/':
            folder_id = folder_id[0:len(folder_id) - 1]
        folder_id = folder_id.replace('//', '/')

        if do_tar:
            if do_compress:
                ext = '.tgz'
                verb = 'w:gz'
            else:
                ext = '.tar'
                verb = 'w'

            folder = '/tmp/' + folder_id
            for chunk in selected_chunks:
                shutil.copyfile(folder_chunks + '/' + chunk, folder)

            folder_compress = '/tmp/' + folder_id + ext
            with tarfile.open(folder_compress, verb) as tar:
                tar.add(folder, recursive=True)
            tar.close()

            with open(folder_compress, 'rb') as data:
                self.s3.Object(self.bucket_name, folder_id + '/' + folder_id + ext).put(Body=data)
        else:
            for chunk in selected_chunks:
                with open(folder_chunks + '/' + chunk, 'rb') as data:
                    self.s3.Object(self.bucket_name, folder_id + '/' + chunk).put(Body=data)

    def download_file(self, folder_id, selected_chunk, folder_output):
        if not os.path.exists(folder_output):
            os.makedirs(folder_output)
        if folder_id == '' or folder_id == '/':
            file_path = selected_chunk
        else:
            file_path = folder_id + '/' + selected_chunk
        if file_path[0] == '/':
            file_path = file_path[1:len(file_path)]
        self.bucket.download_file(file_path, folder_output + '/' + selected_chunk)

    def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False, validate=False):
        if dst_folder[0] == '/':
            dst_folder = dst_folder[1:len(dst_folder)]
        if do_tar:
            if do_compress:
                ext = '.tgz'
                verb = 'w:gz'
            else:
                ext = '.tar'
                verb = 'w'

            local_folder = '/tmp/{}'.format(dst_folder)
            os.makedirs(local_folder, exist_ok=True)

            folder_compress = '{}/result.{}'.format(local_folder, ext)
            with tarfile.open(folder_compress, verb) as tar:
                tar.add(src_folder, arcname=dst_folder, recursive=True)
            tar.close()
            with open(folder_compress, 'rb') as data:
                self.s3.Object(self.bucket_name, dst_folder + ext).put(Body=data)
        else:
            dir = os.fsencode(src_folder)
            for file in os.listdir(dir):
                filePath = src_folder + '/' + file.decode('utf-8')
                if not os.path.isdir(filePath):
                    with open(filePath, 'rb') as data:
                        self.s3.Object(self.bucket_name, dst_folder + '/' + file.decode('utf-8')).put(Body=data)

    def list_files_folder(self, folder):
        if folder[0] == '/':
            folder = folder[1:len(folder)]
        objects = self.bucket.objects.filter(Prefix=folder + '/')
        file_list = []
        for obj in objects:
            file_list.append(obj.key)

        return file_list

    def get_file_size(self, filename):
        try:
            return self.bucket.Object(filename.lstrip('/')).content_length
        except:
            return -1
