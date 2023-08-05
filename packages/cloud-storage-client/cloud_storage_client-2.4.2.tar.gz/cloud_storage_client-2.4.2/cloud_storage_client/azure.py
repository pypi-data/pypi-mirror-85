from azure.storage.blob import BlobServiceClient
from shutil import copyfile
import os, tarfile


class AzureClient():
    """
    Azure Blob Storage Client to connect with Microsoft Azure
    """

    def __init__(self, bucket_name, access_key, secret_key):
        self.service = BlobServiceClient(account_url=f"https://{access_key}.blob.core.windows.net/",
                                         credential=secret_key)
        self.bucket_name = bucket_name

    def delete_file(self, file_path):
        file_path = file_path.lstrip("/")
        blob_client = self.service.get_blob_client(container=self.bucket_name, blob=file_path)
        blob_client.delete_blob()

    def delete_folder(self, folder_id):
        folder_id = folder_id.lstrip("/")
        container_client = self.service.get_container_client(container=self.bucket_name)
        blobs = container_client.list_blobs(name_starts_with=folder_id)
        for blob in blobs:
            if blob.name.find(folder_id + '/') == 0:
                blob_client = self.service.get_blob_client(container=self.bucket_name, blob=blob.name)
                blob_client.delete_blob()

    def download_folder(self, src_folder, dst_folder):
        src_folder = src_folder.lstrip("/")
        container_client = self.service.get_container_client(container=self.bucket_name)
        blobs = container_client.list_blobs(name_starts_with=src_folder)
        for blob in blobs:
            if blob.name.find(src_folder + '/') == 0:
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)
                splitted_name = blob.name.split('/')
                splitted_name = list(filter(None, splitted_name))
                blob_client = self.service.get_blob_client(container=self.bucket_name, blob=blob.name)
                with open(f"{dst_folder + '/' + splitted_name[len(splitted_name) - 1]}", "wb") as data:
                    data.write(blob_client.download_blob(validate_content=True, max_concurrency=4).readall())

    def upload_file(self, src_file, dst_file, options):
        if dst_file[0] == '/':
            dst_file = dst_file[1:len(dst_file)]
        if dst_file[-1] == '/':
            dst_file = dst_file[0:len(dst_file) - 1]
        dst_file = dst_file.replace('//', '/')
        blob_client = self.service.get_blob_client(container=self.bucket_name,
                                                   blob=dst_file)
        with open(src_file, "rb") as data:
            blob_client.upload_blob(data, max_concurrency=4, overwrite=True, validate_content=True)

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
                copyfile(folder_chunks + '/' + chunk, folder)

            folder_compress = '/tmp/' + folder_id + ext
            with tarfile.open(folder_compress, verb) as tar:
                tar.add(folder, recursive=True)
            tar.close()
            blob_client = self.service.get_blob_client(container=self.bucket_name, blob=f"{folder_id}/{folder_id}{ext}")
            with open(folder_compress, "rb") as data:
                blob_client.upload_blob(data, max_concurrency=4, overwrite=True, validate_content=True)
        else:
            for chunk in selected_chunks:
                blob_client = self.service.get_blob_client(container=self.bucket_name,
                                                           blob=f"{folder_id}/{chunk}")
                with open(f"{folder_chunks}/{chunk}", "rb") as data:
                    blob_client.upload_blob(data, max_concurrency=4, overwrite=True, validate_content=True)

    def download_file(self, folder_id, selected_chunk, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if folder_id == '' or folder_id == '/':
            file_path = selected_chunk
        else:
            file_path = folder_id + '/' + selected_chunk
        if file_path[0] == '/':
            file_path = file_path[1:len(file_path)]
        blob_client = self.service.get_blob_client(container=self.bucket_name, blob=file_path)
        with open(f"{output_folder}/{selected_chunk}", "wb") as data:
            data.write(blob_client.download_blob(validate_content=True, max_concurrency=4).readall())

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
            blob_client = self.service.get_blob_client(container=self.bucket_name, blob=f"{dst_folder}{ext}")
            with open(folder_compress, "rb") as data:
                blob_client.upload_blob(data, max_concurrency=4, overwrite=True, validate_content=validate)
        else:
            folder = os.fsencode(src_folder)
            for file in os.listdir(folder):
                file_path = src_folder + '/' + file.decode('utf-8')
                if not os.path.isdir(file_path):
                    blob_client = self.service.get_blob_client(container=self.bucket_name,
                                                               blob=f"{dst_folder}/{file.decode('utf-8')}")
                    with open(file_path, "rb") as data:
                        blob_client.upload_blob(data, max_concurrency=4, overwrite=True, validate_content=validate)

    def list_files_folder(self, folder):
        folder = folder.lstrip("/")
        container_client = self.service.get_container_client(container=self.bucket_name)
        blobs = container_client.list_blobs(name_starts_with=folder)
        return [blob.name for blob in blobs if blob.name.find(folder + '/') == 0]

    def get_file_size(self, filename):
        try:
            blob_client = self.service.get_blob_client(container=self.bucket_name, blob=filename.strip().lstrip("/"))
            return blob_client.get_blob_properties().size
        except Exception as e:
            print(f"Exception getting file_size {e}")
            return -1
