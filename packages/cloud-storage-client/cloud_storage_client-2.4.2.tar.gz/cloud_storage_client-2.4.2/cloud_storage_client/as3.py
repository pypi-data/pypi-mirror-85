import boto3
import tarfile
import os
import shutil
from botocore.exceptions import ClientError

from cloud_storage_client.exceptions import IncorrectCredentialsException


class AS3Client:
    """
    Boto3 Client to connect with Amazon S3 storage
    """

    def __init__(self, bucket_name, access_key, secret_key, endpoint, is_secure):
        session = boto3.Session(access_key, secret_key)
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        if endpoint == None or endpoint == '':
            self.client = session.client('s3')
            self.resource = session.resource('s3')
        else:
            if is_secure == 'true' or is_secure == 'True' or is_secure:
                secure = True
            else:
                secure = False

            self.client = session.client('s3', endpoint_url=endpoint, use_ssl=secure)
            self.resource = session.resource('s3', endpoint_url=endpoint, use_ssl=secure)

    def delete_file(self, file_path):
        try:
            bucket = self.resource.Bucket(self.bucket_name)
            if file_path[0] == '/':
                file_path = file_path[1:len(file_path)]
            for obj in bucket.objects.filter(Prefix=file_path):
                obj.delete()
        except ClientError as e:
            self.handle_client_error(e)

    def delete_folder(self, folder_id):
        try:
            bucket = self.resource.Bucket(self.bucket_name)
            if folder_id[0] == '/':
                folder_id = folder_id[1:len(folder_id)]
            for obj in bucket.objects.filter(Prefix=folder_id + '/'):
                obj.delete()
        except ClientError as e:
            self.handle_client_error(e)

    def download_folder(self, folder_id, folder_output):
        try:
            bucket = self.resource.Bucket(self.bucket_name)
            if not os.path.exists(folder_output):
                os.makedirs(folder_output)
            if folder_id[0] == '/':
                folder_id = folder_id[1:len(folder_id)]
            for obj in bucket.objects.filter(Prefix=folder_id + '/'):
                splitted_name = obj.key.split('/')
                splitted_name = list(filter(None, splitted_name))
                bucket.download_file(obj.key, folder_output + '/' + splitted_name[len(splitted_name) - 1])
        except ClientError as e:
            self.handle_client_error(e)

    def upload_file(self, src_file, dst_file, options):
        if dst_file[0] == '/':
            dst_file = dst_file[1:len(dst_file)]
        if dst_file[-1] == '/':
            dst_file = dst_file[0:len(dst_file) - 1]
        dst_file = dst_file.replace('//', '/')

        self.client.upload_file(src_file, self.bucket_name, dst_file)

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
            self.client.upload_file(folder_compress, self.bucket_name, folder_id + '/' + folder_id + ext)
        else:
            for chunk in selected_chunks:
                self.client.upload_file(folder_chunks + '/' + chunk, self.bucket_name, folder_id + '/' + chunk)

    def download_file(self, folder_id, selected_chunk, folder_output):
        try:
            bucket = self.resource.Bucket(self.bucket_name)
            if not os.path.exists(folder_output):
                os.makedirs(folder_output)
            if folder_id == '' or folder_id == '/':
                file_path = selected_chunk
            else:
                file_path = folder_id + '/' + selected_chunk
            if file_path[0] == '/':
                file_path = file_path[1:len(file_path)]
            bucket.download_file(file_path, folder_output + '/' + selected_chunk)
        except ClientError as e:
            self.handle_client_error(e)


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
            self.client.upload_file(folder_compress, self.bucket_name, dst_folder + ext)
        else:
            dir = os.fsencode(src_folder)
            for file in os.listdir(dir):
                filePath = src_folder + '/' + file.decode('utf-8')
                if not os.path.isdir(filePath):
                    self.client.upload_file(filePath, self.bucket_name, dst_folder + '/' + file.decode('utf-8'))

    def list_files_folder(self, folder):
        try:
            bucket = self.resource.Bucket(self.bucket_name)
            if folder[0] == '/':
                folder = folder[1:len(folder)]
            objects = bucket.objects.filter(Prefix=folder + '/')
            file_list = []
            for obj in objects:
                file_list.append(obj.key)

            return file_list
        except ClientError as e:
            self.handle_client_error(e)

    def get_file_size(self, filename):
        try:
            return self.resource.Bucket(self.bucket_name).Object(filename.lstrip('/')).content_length
        except:
            return -1

    def handle_client_error(self, e):
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 403:
            raise IncorrectCredentialsException(code=403)
        else:
            raise e
