import os  
from openai import AzureOpenAI  
import json
from dotenv import load_dotenv

load_dotenv()
    
endpoint = os.getenv("ENDPOINT_URL")  
deployment = os.getenv("DEPLOYMENT_NAME")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY" )  
    
    # Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version="2024-05-01-preview",  
    )  
      
    # Prepare the chat prompt  
chat_prompt = [
    {
        "role": "system",
        "content": r"""
        Your are a helpful, cheerful database assistant. 
            Use the following database schema when creating your answers:

            - [SalesLT].[Address] (AddressID, AddressLine1, AddressLine2, City,StateProvince, CountryRegion, PostalCode,rowguid,ModifiedDate)
            - [SalesLT].[Customer](CustomerID,NameStyle, Title, FirstName, MiddleName, LastName, Suffix, CompanyName, SalesPerson, EmailAddress, Phone, PasswordHash, PasswordSalt, rowguid, ModifiedDate)
            - [SalesLT].[CustomerAddress](CustomerID, AddressID, AddressType, rowguid, ModifiedDate)
            - [SalesLT].[Product](ProductID, Name, ProductNumber, Color,StandardCost, ListPrice, Size,Weight, ProductCategoryID, ProductModelID, SellStartDate, SellEndDate, DiscontinuedDate, ThumbNailPhoto, ThumbnailPhotoFileName, rowguid, ModifiedDate)
            - [SalesLT].[ProductCategory](ProductCategoryID, ParentProductCategoryID, Name, rowguid, ModifiedDate)
            - [SalesLT].[ProductDescription](ProductDescriptionID, Description, rowguid, ModifiedDate)
            - [SalesLT].[ProductModel](ProductModelID, Name, CatalogDescription, rowguid, ModifiedDate)
            - [SalesLT].[ProductModelProductDescription](ProductModelID, ProductDescriptionID, Culture, rowguid, ModifiedDate)
            - [SalesLT].[SalesOrderDetail](SalesOrderID,SalesOrderDetailID,OrderQty,ProductID,UnitPrice,UnitPriceDiscount, LineTotal, rowguid, ModifiedDate)
            - [SalesLT].[SalesOrderHeader](SalesOrderID,RevisionNumber,OrderDate,DueDate,ShipDate,Status,OnlineOrderFlag, SalesOrderNumber, PurchaseOrderNumber, AccountNumber, CustomerID, ShipToAddressID, BillToAddressID, ShipMethod, CreditCardApprovalCode, SubTotal, TaxAmt, Freight,TotalDue, Comment, rowguid, ModifiedDate)

            Include column name headers in the query results.

            Always provide your answer in the JSON format below:
            
            { ""summary"": ""your-summary"", ""query"":  ""your-query"" }
            
            Output ONLY JSON.
            In the preceding JSON response, substitute ""your-query"" with Microsoft SQL Server Query to retrieve the requested data.
            In the preceding JSON response, substitute ""your-summary"" with a summary of the query.
            Always include all columns in the table.
            If the resulting query is non-executable, replace ""your-query"" with NA, but still substitute ""your-query"" with a summary of the query.
            Do not use MySQL syntax.
            Always limit the SQL Query to 100 rows.
        
        write a query that returns the best selling products top 3"""
    }
]  
    
    # Include speech result if speech is enabled  
speech_result = chat_prompt  
    
    # Generate the completion  
completion = client.chat.completions.create(  
        model=deployment,  
        messages=speech_result,  
      
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False  
    )  
      
result = completion.to_json()

y=json.loads(result)

print(y["choices"][0]["message"])  
    