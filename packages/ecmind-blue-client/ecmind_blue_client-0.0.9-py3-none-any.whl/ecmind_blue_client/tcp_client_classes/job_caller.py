# from protlib import 
import socket
import ssl
import pathlib
import hashlib
import base64
import os
from uuid import uuid4
from datetime import datetime
from typing import List, Optional
from tempfile import gettempdir
from ..param import Param
from ..result import Result
from ..result_file import ResultFile
from ..result_file import ResultFileType
from ..const import ParamTypes
from .call_job_parameters import CallJobParameters
from .job_header import JobHeader
from .file_header import FileHeader
from .file_footer import FileFooter
from .response_job_parameters import ResponseJobParameters
from .job_parameters import JobParameters
from .job_parameter_description import JobParameterDescription
from .job_parameter_data import JobParameterData


class JobCaller:
    def __init__(self, hostname, port, use_ssl:Optional[bool]=True, file_cache_byte_limit:Optional[int]=33554432):
        self.hostname = hostname
        self.port = port
        self.file_cache_byte_limit = file_cache_byte_limit
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        plain_text_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if use_ssl:
            self.socket = ssl.wrap_socket(
                plain_text_socket, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="AES256-SHA")
        else: 
            self.socket = plain_text_socket
        self.socket.connect((hostname, port))


    def close(self):
        self.socket.close()


    def execute(self, job):
        # Create internal parameter
        intern_params: List[Param] = []
        intern_params.append(Param("streams", ParamTypes.INTEGER, len(job.files)))
        internal_parameters = self.build_parameters(intern_params)

        #create parameter
        parameters = self.build_parameters(job.params)
       
        # create request parameters 
        request_parameters = CallJobParameters(method=job.name, internal_parameters=internal_parameters, parameters=parameters)
        request_parameters_binary = request_parameters.serialize()
        
        # calculate digest of request parameters
        request_digest = hashlib.sha1()
        request_digest.update(request_parameters_binary)

        # create request headers
        request_headers = JobHeader()
        request_headers.set_parameter_length(len(request_parameters_binary) + 20)
        request_header_binary= request_headers.serialize()

        # send request
        self.socket.send(request_header_binary)
        self.socket.send(request_parameters_binary)
        
        # for each file
        for file in job.files:
            # read file info
            with pathlib.Path(file) as p: 
                size = p.stat().st_size 
                extension = p.suffix[1:]

                # write file header 
                request_file_header = FileHeader()
                request_file_header.set_file_length(size)
                request_file_header.extension = extension
                request_file_header_binary = request_file_header.serialize()
            
                self.socket.send(request_file_header_binary)
                request_digest.update(request_file_header_binary)

                # stream file
                f = open(file,'rb')
                l = f.read(1024)
                while (l):
                    self.socket.send(l)
                    request_digest.update(l)
                    l = f.read(1024)
                f.close()

                # write fix file footer @0000000000@MAERTSSA
                request_file_footer = FileFooter()
                request_file_footer_binary = request_file_footer.serialize()
                self.socket.send(request_file_footer_binary)

                request_digest.update(request_file_footer_binary)

        # send request digest
        self.socket.send(request_digest.digest())

        #----------------------------------------------------------------------
        # Start read response
        #----------------------------------------------------------------------
        
        # read header
        response_header = JobHeader.parse(self.socket.recv(20))

        # read body
        response_digest = hashlib.sha1()
        body_raw = self.socket.recv(response_header.get_parameter_length() - 20)
        response_digest.update(body_raw)

        # parse body
        response_parameters = ResponseJobParameters.parse(body_raw)

        return_code = int(response_parameters.internal_parameters.get('return'))
        error_message = None
        if return_code != 0:
            error_message = ''
            errors = response_parameters.errors
            for error in errors.data:
                error_message += str(error.error_message, 'ascii') + '\n'

        result_values = {}
        param_index = 0
        for param_description in response_parameters.parameters.description:
            type_id = param_description.type
            data = response_parameters.parameters.data[param_index]
            name = str(data.name, encoding='ascii')
            infered_value = None
            if type_id == ParamTypes.STRING.value:
                infered_value = str(data.value, 'ascii')
            elif type_id == ParamTypes.INTEGER.value:
                infered_value = int(data.value)
            elif type_id == ParamTypes.BOOLEAN.value:
                infered_value = bool(data.value)
            elif type_id == ParamTypes.DOUBLE.value:
                infered_value = float(data.value)
            elif type_id == ParamTypes.DATE_TIME.value:
                infered_value = datetime(data.value)
            elif type_id == ParamTypes.BASE64.value:
                infered_value = base64.b64decode(data.value).decode('UTF-8')

            result_values[name] = infered_value
            param_index += 1

        # parse file streams

        result_files:List[ResultFile] = []

        streams = response_parameters.internal_parameters.get("streams")
        if streams != None:
            streams = int(streams)
            for i in range(0, int(streams)):
                header_raw = self.socket.recv(32)
                header = FileHeader.parse(header_raw)
                response_digest.update(header_raw)

                file_length = header.get_file_length()
                to_file = file_length <= self.file_cache_byte_limit
                remainder = file_length
                file_pointer = None
                byte_array = None
                file_path = None
                file_name =f'ecmind_{str(uuid4())}.{header.get_file_extension()}'
                if to_file:
                    file_path = os.path.join(gettempdir(), file_name)
                    file_pointer = open(file_path, 'wb')
                else:
                    byte_array = b''
                BUFFER_SIZE = 4096
                while remainder > 0:
                    file_part = self.socket.recv(min(remainder, BUFFER_SIZE))
                    response_digest.update(file_part)
                    remainder -= len(file_part)
                    if to_file:
                        file_pointer.write(file_part)
                    else:
                        byte_array += file_part

                if to_file:
                    file_pointer.close()
                    rf = ResultFile(
                        result_file_type=ResultFileType.FILE_PATH,
                        file_path=file_path
                    )
                else:
                    rf = ResultFile(
                        result_file_type=ResultFileType.BYTE_ARRAY,
                        byte_array=byte_array,
                        file_name=file_name,                        
                    )

                result_files.append(rf)
                
                footer_raw = self.socket.recv(20)
                response_digest.update(footer_raw)
                #footer = FileFooter.parse(footer_raw)

        response_digest_received = response_digest.digest()
        response_digest_expected = self.socket.recv(20)

        if(response_digest_received != response_digest_expected): 
            raise Exception("Digest for response does not match")

        return Result(result_values, result_files, return_code, error_message)


    def build_parameters(self, params: List[Param]):
        
        data_offset = 4 + (len(params) * 12)
        data_length = 0

        parameter_description_list=[]
        parameter_description_size=0

        parameter_data_list=[]
        parameter_data_size=0

        for param in params:
            parameter_description = JobParameterDescription(name_offset=data_offset + data_length, type=param.type.value, value_offset=data_offset + data_length + len(param.name) + 1)
            
            parameter_data = None
            if param.type == ParamTypes.STRING:
                parameter_data = JobParameterData(name=param.name, value=param.value)
            if param.type == ParamTypes.INTEGER:
                parameter_data = JobParameterData(name=param.name, value=str(param.value))
            if param.type == ParamTypes.BOOLEAN:
                parameter_data = JobParameterData(name=param.name, value="1" if param.value else "0")
            if param.type == ParamTypes.DOUBLE:
                parameter_data = JobParameterData(name=param.name, value=str(param.value))
            if param.type == ParamTypes.DATE_TIME:
                if isinstance(param.value, datetime):
                    JobParameterData(name=param.name, value=str(param.value.strftime("%d.%m.%y %H:%M:%S")))
                else:
                    JobParameterData(name=param.name, value=str(param.value))
            if param.type == ParamTypes.BASE64:
                if isinstance(param.value, (bytearray, bytes)):
                    parameter_data = JobParameterData(name=param.name, value=base64.b64encode(param.value))
                else:
                    parameter_data = JobParameterData(name=param.name, value=base64.b64encode(param.value.encode('UTF-8')))

            data_length += parameter_data.sizeof()
            
            parameter_description_list.append(parameter_description)
            parameter_description_size += parameter_description.sizeof() 

            parameter_data_list.append(parameter_data)
            parameter_data_size += parameter_data.sizeof()
        
        params_length = 4 + parameter_description_size + parameter_data_size
        
        return JobParameters(length=params_length, count=len(params), description=parameter_description_list, data=parameter_data_list)