# Getjob: Automate to jobs applications

This code is to send emails with different contexts depending on company info, language, postulation job, and recruiter info.

## Installation

Use the package manager [pip](https://pypi.org/project/getjobs/) to install getjob

```bash
pip install getjobs
```
## Requirements
* python <= 2.7

## Usage

### Module Import
```python
from getjobs import GetJob

#sent mail
mail = GetJob(profile, sms_path, bulk_path, doc_path) #replace values to paths
#send bulk email
mail.send()
```

## Comnand line
Sending out a bulk email.

Send mails with a custom profile:
```
$ ./getjob.py path/profile.json path/templates/ path/data.csv path/file.pdf
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU](https://www.gnu.org/licenses/)