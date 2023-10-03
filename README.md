# weather-app
A weather app using Azure services, demonstrating the seamless integration of 
various Azure services to deliver a comprehensive weather information solution. 
Users can get accurate weather updates and subscribe to personalized alerts, 
while Azure services handle the heavy lifting behind the scenes.

Azure resources used: 
- **Azure Web App**: Hosts the weather application.
- **Azure Functions**: Provides serverless functions for email notifications and backend tasks.
- **Azure Maps Account**: Offers powerful geospatial capabilities for location data.
- **Azure Communication Service**: Enables automated subscription emails.
- **Azure Key Vault**: Securely stores connection strings and secrets.
- **Azure Entra ID (Azure AD)**: Manages Service Principals for secure access.

The above resources were created using both, CLI
and the Azure Portal.

### Creating Azure Resource Group in CLI
```commandline
#Logging in to Azure first
az login
az group create --name weatherapp-rg --location eastus
```
### Creating the Web App in Azure Portal
- In the left-hand menu, click on "Create a resource."
- In the search bar, type "Web App" and select "Web App" from the results.
- Click the "Create" button.
- Fill in the details for your Web App, including the App name, Subscription, Resource Group, and App Service plan.
Runtime stack is Python for this use-case.

Configure GitHub Actions to actively deploy your web app code to Azure, as you commit to
the main branch

### Creating Function App and Functions
```commandline
az functionapp create --resource-group RESOURCE_GROUP_NAME \
--name FUNCTION_APP_NAME --consumption-plan-location \
LOCATION --runtime LANGUAGE_RUNTIME
```
Replace with appropriate values.

Before creating a function, we have to install to Azure Functions Core Tools 
(func), you can do so using npm (Node Package Manager). 
Make sure you have Node.js and npm installed on your machine. 
Run the following command globally:
```commandline
npm install -g azure-functions-core-tools@3 --unsafe-perm true
```
Initialise the Function App in the IDE CLI and change to the function-app directory
Now, you can use the func new command to create a new function:
```commandline
func new --name MyHttpFunction --template "HttpTrigger" --authlevel "anonymous"
```
Maintain all the json config files generated to make sure your function works.
To deploy your function app to Azure:
```commandline
func azure functionapp publish FUNCTION_APP_NAME
```
### Azure Maps Account
In this web application, we use this service to:
- Get latitude and longitude data of the location entered by the user via fuzzy
search
- Get the address & temperature information by providing the correct latitude and longitude.

example code to get temperature data using Azure Maps API:
```commandline
https://atlas.microsoft.com/weather/currentConditions/json?" \
              f"api-version=1.0&query=47.60357,-122.32945&" \
              f"subscription-key={azMapKey.value}
```
### Azure Communication Services
This is used to send automatic subscription emails to users via Azure Functions
This is done using a connection-string from Comm Services.
```commandline
client = EmailClient.from_connection_string(connection_string)

message = {
     "senderAddress": <Sender email>,
      "recipients": {
           "to": [{"address": f"{user_email}"}],
          },
          "content": {
              "subject": "Weather Alerts",
              "plainText": "Welcome! Thank you for subscribing to weather alerts.",
                }
        }
poller = client.begin_send(message)
```
### Azure Key Vault & Entra ID (AD)
All connection strings required to communicate between the multiple Azure resources
are stored securely in Azure Key Vault.

Create the key vault using CLI:
```commandline
az keyvault create --name YOUR_KEY_VAULT_NAME --resource-group YOUR_RESOURCE_GROUP --location YOUR_REGION
```
You will have to use a Service Principal created from Azure AD to access the secrets in
the key vault from other Azure resources.

- Navigate to Azure Entra ID (AD) in the portal
- Under "Manage," click on "App registrations."
- Click the "+ New registration" button.
- Provide a name for your Service Principal in the "Name" field.
- Next, Create a Client Secret (Client Credential). After the client secret is generated, make sure to copy and save it securely. This secret will not be visible again.

To communicate with the Azure Key vault, you will need the Client Secret, 
Client ID and Tenant ID. All will can be noted down by following the above steps.
```commandline
credential = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)
client = SecretClient(vault_url=kvUri, credential=credential)
azMapKey = client.get_secret("map-key")
```
### Final output
Once all the Azure resources are up, running and working together, we can see their
application through a sample web app that gives us the weather for any location
and allows users to subscribe to weather alerts.
![](/images/web-app.PNG)
After the user enters any location and email:
![](/images/web-app-user.PNG)
The automated email that is generated to the user after subscribing to the 
alerts is sent using Azure Functions, with a HTTP trigger:
![](/images/alert-email.PNG)

### Deployment
Deployment of the web app is automated through GitHub Actions, with 
all specifications defined in a YAML file.