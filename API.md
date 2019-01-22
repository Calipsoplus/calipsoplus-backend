# REST API interfaces

This backend uses a REST interface to communicate with several external services as explained in the [README.md](README.md) file. Currently, this interface is used for two services:

*  Local authentication provider (used both for local authentication, if enabled, and Umbrella hash validation)
*  Local authorization provider (used to determine access rights to privileged facility resources)
*  Local data provider (in case dynamic experiment data retrieval is enabled)

## Local authentication endpoints
### Local login (POST)
To support authentication of users against a local database, a login endpoint can be defined in the "BACKEND_UO_LOGIN" setting of the **calipsoplus/settings_[local|test|demo|prod].py** file (choose the one you will use according to your environment). The service that will provide this service must implement the endpoint as follows:

#### Arguments

*  **username**: String. The name of the account we attempt to authenticate.
*  **password**: String. The password of the account, unhashed.

#### Responses

*  **HTTP 200 OK**: The username/password combination exists, the authentication has succeeded.
*  **HTTP 401 Unauthorized**: The username/password combination does not exist, the authentication has not succeeded.
*  **HTTP 400 Bad Request**: Missing arguments or an error has occurred during processing.


### Umbrella hash validation (POST)
As part of the login operation of the Umbrella federated authentication service, an EAA hash is provided, identifying the local identity linked to the Umbrella account. This endpoint can be defined in the "BACKEND_UO_HASH" setting of the **calipsoplus/settings_[local|test|demo|prod].py** file. 

This endpoint **must** be implemented by a service that can check this hash against local records (eg.: a Web User Office application) for the Umbrella login feature to work properly.

#### Arguments
*  **eaa_hash**: String. Hash returned by the Umbrella SSO system.

#### Responses

*  **HTTP 200 OK**: An account exists with the provided EAA hash, the local username is returned.
*  **HTTP 404 Not Found**: An account does not exist with the provided EAA hash.
*  **HTTP 400 Bad Request**: Missing arguments or an error has occurred during processing.

## Authorization endpoints
### Authorization to use privileged facility resources (POST)
To validate access to other, permanent resources available for users this endpoint is called on demand with the account name. This endpoint can be defined in the "BACKEND_UO_IS_AUTHORIZED" setting of the **calipsoplus/settings_[local|test|demo|prod].py** file. The service providing this endpoint will need to decide if the user is authorized to access these resources.

This endpoint is secured with [HTTP Basic Authentication](https://www.django-rest-framework.org/api-guide/authentication/#basicauthentication).

#### Arguments
* **login**: String. Name of the account to check.

#### Responses

* **HTTP 200 OK**: All fine.
*  **HTTP 404 Not Found**: User not found.
*  **HTTP 400 Bad Request**: Missing arguments or an error has occurred during processing.
*  **HTTP 403 Forbidden**: Access credentials not provided.

#### Response contents (if OK)
The response is expected in JSON format, in the following structure:
* **result**: Boolean. If **true**, the user is authorized to access the privileged resources. Else, do not allow access.

## Local data provider endpoints
### Get experiments by login (GET)
If the dynamic retrieval of experimental data is enabled, the endpoint defined in the "DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL_ENDPOINT" of the **calipsoplus/settings_[local|test|demo|prod].py** file will be queried on demand to load the experiment data associated with a given account. The output of this endpoint is expected to be paginated.

This endpoint is secured with [HTTP Basic Authentication](https://www.django-rest-framework.org/api-guide/authentication/#basicauthentication).

#### Arguments
*  **username**: String. Name of the account to retrieve experiments from (is provided as part of the URL path).
*  **search**: String. Query argument (optional). String to be searched for in either experiment subject, body, beamline, or serial number.
*  **ordering**: String. Query argument (optional). Field by which to order ('-' preceding the name indicates descending order). The supported fields are:
    *  **serial_number**
    *  **subject**
    *  **body**
    *  **beam_line**
*  **page_size**: Integer. Query argument. Number of elements to return as maximum per request.
*  **page**: Integer. Query argument. Page number.

#### Responses

*  **HTTP 200 OK**: Account exists.
*  **HTTP 404 Not Found**: The specified account does not exist.
*  **HTTP 400 Bad Request**: Missing arguments or an error has occurred during processing.
*  **HTTP 403 Forbidden**: Access credentials not provided.

#### Response contents (if OK)
The response is expected in JSON format, in the following structure:
*  **count**: Integer. Number of elements of the total result set.
*  **next**: String. URL pointing to the next page (may be null if no further pages are available).
*  **previous**: String. URL pointing to the previous page (may be null if no previous pages are available).
*  **results**: List. Contains the experiments the user has participated in. The structure of each element is as follows:
    *  **subject**: String. Title or subject of the experiment.
    *  **serial_number**: String. Identifier of the experiment (must be unique).
    *  **body**: String. Abstract or description of the experiment.
    *  **beam_line**: String. Name of the beamline associated with the experiment.
    *  **sessions**: List. Contains the data collection sessions of this experiment. The structure of each element is as follows:
        *  **sesion_number**: String. Unique identifier for the session.
        *  **start_date**: Timestamp. Date of the start of the session.
        *  **end_date**: Timestamp. Date of the end of the session.
        *  **subject**: String. Subject of the session, if available.
        *  **body**: String. Description of the session, if available.
        *  **data_set_path**: String. (TOOD: unused?)