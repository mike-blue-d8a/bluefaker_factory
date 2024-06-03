# blue_fkdata_gen

blue_fkdata_gen is a versatile tool for generating fake data in CSV, Parquet, and JSON formats. It leverages the `faker` module to create realistic fake data and allows easy configuration through YAML files. With blue_fkdata_gen, you can quickly generate files containing anywhere from 100 to millions of rows, all within minutes, thanks to its concurrency capabilities. Additionally, you can append data to existing files.

### Why? 

If you ever need realistic data for testing a pipeline, database, or any other application, blue_fkdata_gen provides a safe and efficient way to create data without using sensitive production data, which can be vulnerable. 

blue_fkdata_gen uses faker functions as the dtypes that are mapped out in the function `get_fake_data()`. Here can see what the avaible mapped out faker types are. There are some  conditions added.  Like name and email I have combined them so you can have the same name as name and email.  ie Bob Smith and bob.smith@whatever.com 

Docs to the faker module:
https://faker.readthedocs.io/en/master/index.html

## Configuration

In your YAML configuration file, specify the columns you want and the corresponding `faker` data types. For example:

```yaml
columns:
  - column: Email_Id
    dtype: email
  - column: Name
    dtype: name
  - column: Gamer_Id
    dtype: user_name
  - column: Device
    dtype: user_agent
  - column: Phone_Number
    dtype: phone_number
```


## Example Usage:

```
python3 blue_fkdata_gen.py --file mytestdata --records 10000 --format parquet --schema test_schema.yml
```

## Sample output
```
Generating Fake Data with '10000' records....

100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10000/10000 [00:05<00:00, 1668.28it/s]

Sample Data:
+-----------------------------+----------------+---------------+-------------------------------------------------------------------------------------------------+--------------------+
|           Email_Id          |      Name      |    Gamer_Id   |                                              Device                                             |    Phone_Number    |
+-----------------------------+----------------+---------------+-------------------------------------------------------------------------------------------------+--------------------+
| roger.schwartz@ferguson.com | Roger Schwartz |   browneric   | Mozilla/5.0 (Windows NT 6.0; ht-HT; rv:1.9.1.20) Gecko/8189-08-02 16:57:46.645020 Firefox/3.6.4 |     9066232881     |
|   edward.james@walker.biz   |  Edward James  |  ravenparker  |                   Mozilla/5.0 (compatible; MSIE 5.0; Windows 95; Trident/3.0)                   | (958)521-2763x1161 |
|   douglas.garza@holmes.biz  | Douglas Garza  | johnsonjoshua |   Mozilla/5.0 (X11; Linux x86_64; rv:1.9.6.20) Gecko/7958-09-05 14:17:35.965302 Firefox/3.6.19  |    564-921-1439    |
+-----------------------------+----------------+---------------+-------------------------------------------------------------------------------------------------+--------------------+

Created file: mytestdata.parquet
Number of rows added: 10000
```

### If you want to  append rows to a file that exist:

```
python3 blue_fkdata_gen.py --file mytestdata --records 10000 --format parquet --schema test_schema.yml -a
```

## To Install

```
pip install -r requirements.txt
```
