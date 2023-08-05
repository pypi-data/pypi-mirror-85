from typing import Any

from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame


def read(self):  # Have to add self since this will become a method
    return EasyDynamicFrameReader(glue_context=self)


setattr(GlueContext, 'read', read)


class EasyDynamicFrameReader:

    connection_options_dict = {}
    format_options_dict = {}
    additional_options_dict = {}
    data_format = ''

    def __init__(self, glue_context: GlueContext):
        self.glue_context = glue_context

    def csv(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
            **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='csv', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def json(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
             **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='json', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def avro(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
             **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='avro', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def ion(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
            **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='ion', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def groklog(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
                **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='grokLog', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def orc(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
            **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='orc', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def parquet(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
                **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='parquet', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def glueparquet(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
                    **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='glueparquet', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def xml(self, s3_paths, transformation_ctx: str = "", push_down_predicate: str = "",
            **kwargs: Any) -> DynamicFrame:
        return self._read_from_s3(data_format='xml', s3_paths=s3_paths, transformation_ctx=transformation_ctx,
                                  push_down_predicate=push_down_predicate, kwargs=kwargs)

    def _read_from_s3(self, data_format: str, s3_paths: str = "", transformation_ctx: str = "",
                      push_down_predicate: str = "", **kwargs: Any) -> DynamicFrame:
        if s3_paths:
            if isinstance(s3_paths, str):
                self.connection_options_dict['paths'] = [s3_paths]
            elif isinstance(s3_paths, list):
                self.connection_options_dict['paths'] = s3_paths
            # TODO Add else with an error message if s3_path is not str or list

        return self.glue_context.create_dynamic_frame.from_options(connection_type='s3',
                                                                   connection_options=self.connection_options_dict,
                                                                   format=data_format,
                                                                   format_options=self.format_options_dict,
                                                                   transformation_ctx=transformation_ctx,
                                                                   push_down_predicate=push_down_predicate,
                                                                   kwargs=kwargs
                                                                   )

    def table(self, database_name: str, table_name: str, redshift_tmp_dir: str = "", transformation_ctx: str = "",
              push_down_predicate: str = "", catalog_id: int = None, **kwargs: Any) -> DynamicFrame:
        return self.glue_context.create_dynamic_frame.from_catalog(database=database_name,
                                                                   table_name=table_name,
                                                                   redshift_tmp_dir=redshift_tmp_dir,
                                                                   transformation_ctx=transformation_ctx,
                                                                   push_down_predicate=push_down_predicate,
                                                                   additional_options=self.additional_options_dict,
                                                                   catalog_id=catalog_id,
                                                                   kwargs=kwargs)

    def format_option(self, key: str, value: str):
        self.format_options_dict.update({key: value})
        return self

    def format_options(self, options: dict):
        self.format_options_dict = options
        return self

    def connection_option(self, key: str, value: str):
        self.format_options_dict.update({key: value})
        return self

    def connection_options(self, options: dict):
        self.connection_options_dict = options
        return self

    def additional_option(self, key: str, value: str):
        self.format_options_dict.update({key: value})
        return self

    def additional_options(self, options: dict):
        self.additional_options_dict = options
        return self

    def option(self, key: str, value: str):
        return self.connection_option(key, value)

    def options(self, options: dict):
        return self.connection_options(options)
