# EasyGlue

This project aims to make the usage of AWS Glue's DynamicFrame more similar to that of Apache Spark's DataFrame, so that it's easier for newcomers to Glue to use the API. Let's take a simple S3 read of a CSV dataset with headers for instance:

DataFrame S3 read:
```
spark.read().csv('s3://test_path/', header=True)
```

DynamicFrame S3 read:
```
glue.create_dynamic_frame.from_options(connection_type='s3', connection_options={'paths': ['s3://test_path/']}, format='csv', format_options={'withHeader': True}, transformation_ctx='datasource0')
```

As you can see, the syntax here is quite different. With EasyGlue, you can turn the DynamicFrame read operation into something way more similar:
```
glue.read().format_option('withHeader', True).csv('s3://test_path/')
```

## Currently supported options

The project currently supports:

* Reading from S3 in any of the supported formats
* Read from Data Catalog tables

## Usage

To use EasyGlue in your projects, do the following:

1. Download the source code: `git clone https://github.com/albertquiroga/EasyGlue.git`
2. Go into the project's directory, and build it into a wheel file: `python setup.py build bdist_wheel`
3. A new `dist` directory will have been created, inside you'll find the built wheel file. Upload this to S3 and add it as a library to your Glue ETL Job
4. In your ETL Job code, simply add a `import easyglue` line at the top

## Roadmap

* Reading from JDBC sources
* Writes
* Turn format/connection options into method arguments for even more similar and compact method calls
