# Dropbox File Searcher

A small Python tool for searching Dropbox for configured file names, checking each result against a set of file criteria, and moving the first matching file into a target Dropbox folder. 

The search list is supplied as a CSV file, and the matching rules are supplied as JSON.

## Usage

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DROPBOX_KEY=your_dropbox_access_token
TESTMODE=1
MOVEFOLDER=YOUR_FOLDER_NAME
```

Create the search input file:

```text
resources/active_files.csv
```

The file must contain a `Name` column:

```csv
Name
example-file
another-file
```

Run the searcher:

```bash
python app.py
```

With `TESTMODE=1`, matching files are logged but not moved. Remove `TESTMODE` or set it to another value when you are ready to move files in Dropbox.

`MOVEFOLDER` will determine the folder to which the matched file will be moved. If there is no folder then a new one will be created.

## Configuration

The matching rules live in:

```text
config/criteria.json
```

The default criteria are:

```json
{
   "criteria": [
      {
         "name": "File Type",
         "properties": ["extension"],
         "operations": ["=="],
         "description": "Filter images by their file type.",
         "values": ["psd"]
      },
      {
         "name": "Size",
         "properties": ["size"],
         "operations": [">"],
         "description": "Filter images based on their file size.",
         "values": [1048576]
      }
   ]
}
```

Each criterion has:

`name`: Name for criterion (Only for logs).

`properties`: One or more fields to read from the file record.

`operations`: Operators used to compare, combine, or calculate values. The final operator MUST be a comparison operator.

`description`: A human-readable note explaining what the rule is for.

`values`: One or more accepted comparison values.

All criteria must pass for a file to be moved.

## Supported File Fields

The main script builds a `FileRecord` from Dropbox metadata with these fields:

```python
FileRecord(
    name=metadata.name,
    path=metadata.path_display,
    size=metadata.size,
    modified_time=metadata.server_modified,
    extension=os.path.splitext(metadata.name)[1].lstrip(".").lower(),
    metadata={
        "id": metadata.id,
        "client_modified": metadata.client_modified,
        "rev": metadata.rev,
    }
)
```

Criteria can refer directly to:

```text
name
path
size
modified_time
extension
```

They can also refer to values inside the metadata dictionary:

```text
id
client_modified
rev
```

Please add more criteria from metadata inside this dict as needed.

## Supported Operators

The criteria loader supports these operators:

```text
==   equal
!=   not equal
>    greater than
<    less than
>=   greater than or equal
<=   less than or equal
/    division
*    multiplication
+    addition
-    subtraction
%    modulo
```

Simple criteria use one property and one comparison operator:

```json
{
   "name": "Only Photoshop Files",
   "properties": ["extension"],
   "operations": ["=="],
   "description": "Only move PSD files.",
   "values": ["psd"]
}
```

Multiple-property criteria calculate a value from the listed properties, then compare the calculated result with `values`.

For example, a rule with:

```json
{
   "name": "Example Calculated Rule",
   "properties": ["size", "some_other_value"],
   "operations": ["/", ">"],
   "description": "Divide size by another value, then compare the result.",
   "values": [100]
}
```

would calculate:

```text
size / some_other_value
```

then check whether the result is greater than `100`.

You can also add other operators inside the helpers/operators.py


## Moving Files

When a file passes all criteria, it is moved to:

```text
/{os.getenv(MOVEFOLDER)}/{file_name}
```

Before moving, the Dropbox client verifies that the destination folder exists. If it does not exist, the folder is created automatically.

Only the first valid match for each search name is moved. Once a file passes the configured criteria and is either logged in test mode or moved in live mode, the script stops checking additional matches for that search term.

## Test Mode

Use test mode before running against real Dropbox files:

```env
TESTMODE=1
```

In test mode, the script logs what would happen:

```text
File example.psd passed all criteria and would be moved to /YOUR_FOLDER_NAME/
```

No Dropbox files are moved while `TESTMODE` is set to `1`.

## Requirements

The project depends on:

```text
python-dotenv
requests
dropbox
```

