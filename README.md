# SightMachine Python SDK

The Sight Machine software development kit (SDK) complements the Sight Machine platform by providing advanced users with the ability to retrieve and manipulate contextualized data from the platform.


## Terminologies
- SMSDK
  - An acronym name for SightMachine Software Development Kit.
- Entites
    - The collection of High Level objects(HLOs) which allows data manipulation via SMSDK. Ex - *MachineType, Machine, Part etxc*
- Utilities
  - The functions associated with each of the HLO entities which does the actual work of data updation or reterival from SM platform.
- Client
  - Any autheticated python objects through which the underlying *utility* of an *Entity* can be accessed.  
  
## Authetication
  - Inorder to have a secure connectivity between SM platform and SMSDK following authentication methods are supported 
    -  *basic* - Username/Password
       -  Contact Sightmachine Administrator to get a set of Username/Password.
    -  *apikeys* - API keys
       - The API keys can be generated from SM platform.  
    -  OAuth
       - Under Implementation
  
### Installation

##### via PiP from Github
```
pip install git+https://github.com/sightmachine/sightmachine-sdk.git
```

##### Confirmation
```
import smsdk
```
## Quick Start - Authenticating
- To authenticate
  - Initialize a Client: 
    ```
    from smsdk import client
    tenantname = 'demo'
    cli = clinet.Client(tenant)
    ```
- Log in using the authentication methods
  ```
    >>> cli.login('basic', email=user, password=passw)
  ```
  ```
    >>> cli.login('apikey', secret_id=secret_id, key_id=key_id)
  ```
- To view the list of registered entities
  ```
    >>> cli.list_entities()
    ['cycle', 'downtime', 'machine', 'machine_type', 'parts']
  ```
- To get the list of registered utilites for a given entity
  ```
  >>> cli.get_data('machine_type', 'get_utilities')

    get_utilities
    get_machine_types
  ```
### Retrieving Data
The SDK provides a simple interface for downloading data from models such as Cycles, Downtimes, Machine, MachineType etc.
- To retrieve data:
  -  Generate a query to limit the data returned.
The Sight Machine SDK supports a MongoEngine-like query syntax. See the MongoEngine Tutorial for examples. One notable limitation is that the Sight Machine API does not support logical OR when combining query parameters.
  ```
  params = {'_limit':1, '_only':'["source_type", "source_type_clean", "stats"]'}
  cli.get_data('machine_type', 'get_machine_types', **params)
  ```
  
  ```
  DATE_START = datetime(2017, 8, 6)
  DATE_END   = datetime(2017, 8, 7)
  QUERY = {'endtime__gte' : DATE_START, 
           'endtime__lte' : DATE_END, 
           'order_by': '-endtime'}
  cli.get_data('cycle', 'get_cycles', **QUERY)
  ```

IMPORTANT: We highly recommend setting time filters and ordering in all queries of the cycle model to ensure consistent data values are returned.  This minimizes the chances that changes to the database while the queries are running will result in data inconsistencies.

### Optional parameters for filtering 
The following optional parameters can be supplied as per the requirements
  
- normalize
  -  Type = Boolean
  -  Values = True/False
  -  Default = False
  -  If True, this option will normalize the nested data structure into separate columns in a data frame.
  ```
  QUERY = {'normalize':True}
  or
  QUERY = {'starttime__gte' : DATE_START, 'starttime__lte' : DATE_END, 'enable_pagination':True}
  cli.get_data('cycle', 'get_cycles',normalize=True, **QUERY)
  ```
### Todos

 - Write MORE Tests


License
----


