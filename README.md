# AWS Serverless Real-Time Chat Application

## Project Overview

I built a real-time chat application using AWS serverless services to understand how different cloud components work together to deliver messages and store chat history.

The application uses WebSocket APIs for real-time communication. AWS Lambda processes chat events, DynamoDB keeps track of active connections and stores message history, and Amazon SQS handles message archiving asynchronously.

I created the resources, configured the connections between services, deployed the WebSocket API, and tested the application using a terminal-based chat client.

## Architecture

![See Image in The Architecture folder]

### How It Works

1. A user connects to the application through an Amazon API Gateway WebSocket API.
2. The `ChatHandler` Lambda function processes connection and disconnection events.
3. Active connection IDs and usernames are stored in the `ActiveConnections` DynamoDB table.
4. When a user sends a message, the Lambda function broadcasts it to connected clients through the API Gateway Management API.
5. The message is sent to the `ChatLogQueue` SQS queue for asynchronous processing.
6. The `ChatArchiver` Lambda function processes queued messages and saves them in the `ChatHistory` DynamoDB table.

This design separates real-time message delivery from message archiving, allowing the chat handler to hand off archival work to a separate process.

## AWS Services Used

- **Amazon API Gateway:** Created a WebSocket API for real-time, two-way communication.
- **AWS Lambda:** Used Python functions to handle chat events and archive messages.
- **Amazon DynamoDB:** Stored active connections and archived chat messages.
- **Amazon SQS:** Queued messages for asynchronous processing.
- **AWS IAM:** Configured permissions for Lambda functions to interact with other AWS services.
- **API Gateway Usage Plans and API Keys:** Configured API access controls and usage limits.
- **Python:** Used to implement the Lambda functions.
- **Linux Terminal:** Configured and launched the chat client for testing.

## What I Implemented

### 1. Database Setup

Created two DynamoDB tables:

- `ActiveConnections`: Stores WebSocket connection IDs and usernames.
- `ChatHistory`: Stores archived messages, including message IDs, timestamps, usernames, and message content.

Both tables use on-demand capacity mode.

### 2. Message Queue

Created an Amazon SQS Standard queue named `ChatLogQueue` to separate message archiving from real-time delivery.

### 3. Lambda Functions

Implemented two Python Lambda functions:

- `ChatHandler`: Handles WebSocket connection events, username registration, message broadcasting, and sending messages to SQS.
- `ChatArchiver`: Processes SQS events and writes chat messages to DynamoDB.

### 4. WebSocket API

Created and deployed the `RealTimeChatAPI` WebSocket API with these routes:

- `$connect`
- `$disconnect`
- `setName`
- `sendMessage`

Connected the routes to the `ChatHandler` Lambda function and deployed the API to the `production` stage.

### 5. Permissions and Access Configuration

Configured an IAM execution role for the Lambda functions and set up an API key and usage plan for the WebSocket API connection.

### 6. Application Testing

Configured the terminal chat client with the WebSocket endpoint and API key, then launched it from the terminal.

During testing, I encountered an executable permission issue and resolved it before launching the application.

I used the chat interface to test message delivery and the DynamoDB console to check whether messages were archived.


## Key Lessons

Working on this project helped me understand:

- How WebSocket APIs support persistent connections and real-time communication.
- How Lambda functions process events from API Gateway and SQS.
- How DynamoDB can store connection information and chat history.
- How SQS supports asynchronous processing between services.
- How IAM roles control access between AWS resources.
- How to configure and deploy a serverless application.
- How to troubleshoot issues when testing an application from a Linux terminal.

## Improvements I Would Make Next

There are several areas I would improve before using this architecture for a production application:

- Apply least-privilege IAM policies instead of broad managed permissions.
- Add stronger authentication and input validation.
- Improve error handling, logging, monitoring, and retry behaviour.
- Handle duplicate message processing safely.
- Add automated tests and a CI/CD pipeline.
- Use Terraform to manage the AWS infrastructure as code.
- Review AWS costs and document resource cleanup procedures.



## Conclusion

This project gave me practical experience building a serverless application by connecting AWS networking, compute, messaging, storage, and access-control services.

It also helped me understand how to separate real-time application behaviour from background processing and how to test a cloud application after deployment.

I plan to build on this foundation by managing the infrastructure with Terraform and introducing automated deployment and monitoring.

