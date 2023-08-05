from cloud_storage_client import storage_adapter
from cloud_storage_client import gcloud
from cloud_storage_client import gcloud_access_secret
from cloud_storage_client import as3
from cloud_storage_client import azure
from cloud_storage_client import sftp
from cloud_storage_client import ftp
from cloud_storage_client import file_system
import time

from cloud_storage_client.exceptions import IncorrectCredentialsException, NotFoundException, UploadException

GOOGLE_CLOUD_STORAGE = 'GCS'
AMAZON_S3 = 'S3'
AZURE_BLOB_STORAGE = 'ABS'
FTP = 'FTP'
FILE_SYSTEM = 'FILE_SYSTEM'
NETSTORAGE = 'NETSTORAGE'
SSH = 'SSH'


class StorageClient(storage_adapter.StorageAdapter):

    def __init__(self, type=None, bucket_name=None, access_key=None, secret_key=None, region=None, username=None,
                 password=None, host=None, port=None, secure=None):
        if type == GOOGLE_CLOUD_STORAGE:
            if (access_key == None and secret_key == None) or (access_key == "" and secret_key == ""):
                self.client = gcloud.GCloudStorageClient(bucket_name)
            else:
                self.client = gcloud_access_secret.GCloudStorageClientAccessKeySecretKey(bucket_name, access_key,
                                                                                         secret_key, region=region)
        elif type == AMAZON_S3:
            self.client = as3.AS3Client(bucket_name, access_key, secret_key, host, secure)
        elif type == AZURE_BLOB_STORAGE:
            self.client = azure.AzureClient(bucket_name, access_key, secret_key)
        elif type == FTP or type == NETSTORAGE:
            if secure or secure == 'true' or secure == 'True':
                self.client = sftp.SFTPClient(host=host, port=port, username=username, password=password)
            else:
                self.client = ftp.FTPClient(host, port, username, password)
        elif type == FILE_SYSTEM:
            self.client = file_system.FileSystemClient()
        elif type == SSH:
            self.client = sftp.SFTPClient(host=host, port=port, username=username, secret_key=secret_key,
                                          password=password)
        else:
            raise NameError('Invalid Storage Type')

        self.bucket_name = bucket_name
        self.backoffValue = 2

    def _delete_file(self, file_path):
        ts = time.time()
        self.client.delete_file(file_path)

    def delete_file(self, file_path, total_retries=4, retries_count=0, seconds_wait=0.5):
        if retries_count < total_retries:
            try:
                self._delete_file(file_path)
            except IncorrectCredentialsException as e:
                raise e
            except:
                print('Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
                self.delete_file(file_path, total_retries=total_retries, retries_count=retries_count, seconds_wait=seconds_wait)
        else:
            raise Exception('Could not delete_file', file_path)

    def _delete_folder(self, folder_id):
        ts = time.time()
        self.client.delete_folder(folder_id)

    def delete_folder(self, folder_id, total_retries=4, retries_count=0, seconds_wait=0.5):
        if retries_count < total_retries:
            try:
                self._delete_folder(folder_id)
            except IncorrectCredentialsException as e:
                raise e
            except:
                print('Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
                self.delete_folder(folder_id, total_retries=total_retries, retries_count=retries_count, seconds_wait=seconds_wait)
        else:
            raise Exception('Could not delete_folder', folder_id)

    def _download_folder(self, src_folder, dst_folder):
        ts = time.time()
        self.client.download_folder(src_folder, dst_folder)

    def download_folder(self, src_folder, dst_folder, total_retries=4, retries_count=0, seconds_wait=0.5):
        if retries_count < total_retries:
            try:
                self._download_folder(src_folder, dst_folder)
            except IncorrectCredentialsException as e:
                raise e
            except:
                print('Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
                self.download_folder(src_folder, dst_folder, total_retries=total_retries, retries_count=retries_count, seconds_wait=seconds_wait)
        else:
            raise Exception('Could not download_folder', src_folder, dst_folder)

    def _upload_file(self, src_file, dst_file, options):
        ts = time.time()
        self.client.upload_file(src_file, dst_file, options)

    def upload_file(self, src_file, dst_file, total_retries=4, retries_count=0, seconds_wait=0.5, options=None):
        if retries_count < total_retries:
            try:
                self._upload_file(src_file, dst_file, options)
            except IncorrectCredentialsException as e:
                raise e
            except NotFoundException as e:
                raise e
            except UploadException as e:
                raise e
            except:
                print('Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
                self.upload_file(src_file, dst_file, total_retries=total_retries, retries_count=retries_count, seconds_wait=seconds_wait)
        else:
            raise UploadException(Exception('Could not upload_file', src_file, dst_file))

    def _upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
        ts = time.time()
        self.client.upload_files(folder_id, selected_chunks, folder_chunks, do_tar, do_compress)

    def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False, total_retries=4, retries_count=0, seconds_wait=0.5):
        if retries_count < total_retries:
            try:
                self._upload_files(folder_id, selected_chunks, folder_chunks, do_tar=do_tar, do_compress=do_compress)
            except IncorrectCredentialsException as e:
                raise e
            except:
                print('Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
                self.upload_files(folder_id, selected_chunks, folder_chunks, do_tar=do_tar, do_compress=do_compress, total_retries=total_retries, retries_count=retries_count, seconds_wait=seconds_wait)
        else:
            raise Exception('Could not upload_files', folder_id, selected_chunks, folder_chunks, do_tar, do_compress)

    def _download_file(self, folder_id, selected_chunk, output_folder):
        ts = time.time()
        self.client.download_file(folder_id, selected_chunk, output_folder)

    def download_file(self, folder_id, selected_chunk, output_folder, total_retries=4, retries_count=0, seconds_wait=0.5):
        if retries_count < total_retries:
            try:
                self._download_file(folder_id, selected_chunk, output_folder)
            except IncorrectCredentialsException as e:
                raise e
            except:
                print('Retriying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
                self.download_file(folder_id, selected_chunk, output_folder, total_retries=total_retries, retries_count=retries_count, seconds_wait=seconds_wait)
        else:
            raise Exception('Could not download_file', folder_id, selected_chunk, output_folder)

    def _upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False, validate=False):
        ts = time.time()
        self.client.upload_folder(dst_folder, src_folder, do_tar, do_compress, validate)

    def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False, total_retries=4, retries_count=0, seconds_wait=0.5, validate=False):
        if retries_count < total_retries:
            try:
                self._upload_folder(dst_folder, src_folder, do_tar=do_tar, do_compress=do_compress, validate=validate)
            except IncorrectCredentialsException as e:
                print(e)
                raise IncorrectCredentialsException
            except:
                print('Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
                self.upload_folder(dst_folder, src_folder, do_tar=do_tar, do_compress=do_compress, total_retries=total_retries, retries_count=retries_count, seconds_wait=seconds_wait, validate=validate)
        else:
            raise Exception('Could not upload_folder', dst_folder, src_folder, do_tar, do_compress)

    def _list_files_folder(self, folder):
        ts = time.time()
        files = self.client.list_files_folder(folder)
        return files

    def list_files_folder(self, folder, total_retries=4, retries_count=0, seconds_wait=0.5):
        while retries_count < total_retries:
            try:
                return self._list_files_folder(folder)
            except IncorrectCredentialsException as e:
                raise e
            except:
                print('Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue

        raise Exception('Could not list_files_folder', folder)

    def _get_file_size(self, filename):
        ts = time.time()
        s = self.client.get_file_size(filename)
        return s

    def get_file_size(self, filename, total_retries=4, retries_count=0, seconds_wait=0.5):
        file_size = -1

        while retries_count < total_retries:
            try:
                file_size = self._get_file_size(filename)
            except:
                file_size = -1

            if file_size == -1:
                print('Exception. Retrying request in', seconds_wait, ' seconds')
                time.sleep(seconds_wait)
                retries_count = retries_count + 1
                seconds_wait = seconds_wait * self.backoffValue
            else:
                return file_size
        return file_size

    def elapsed_time(self, init_time, end_time):
        return (int(end_time) - int(init_time))