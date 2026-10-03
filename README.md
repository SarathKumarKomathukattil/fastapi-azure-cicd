# FastAPI CI/CD Deployment on Azure

A production-style FastAPI application demonstrating automated testing, Docker containerization, secure GitHub Actions CI/CD, Azure Container Registry, and cloud deployment using Azure Container Apps.

The primary goal of this project is to demonstrate how an application moves from **source code to a live cloud deployment through an automated CI/CD pipeline**.

---

## 🚀 Project Overview

This project started as a FastAPI application and was progressively converted into a containerized, tested, and cloud-deployed service.

The final solution includes:

- FastAPI REST API
- Pytest automated testing
- Docker containerization
- Git and GitHub
- GitHub Actions Continuous Integration
- GitHub Actions Continuous Deployment
- Azure authentication using OpenID Connect (OIDC)
- Azure Container Registry (ACR)
- Azure Container Apps
- Managed Identity for secure ACR access
- Azure RBAC
- Git commit SHA-based Docker image versioning
- Public HTTPS endpoint
- FastAPI Swagger documentation

The key focus of this project is **automation, secure cloud authentication, container deployment, and CI/CD**.

---

# 🔄 End-to-End Workflow

```text
Developer changes code
        ↓
Git Push
        ↓
GitHub Repository
        ↓
GitHub Actions CI
        ↓
Install dependencies
        ↓
Run Pytest
        ↓
Build Docker image
        ↓
CI succeeds
        ↓
GitHub Actions CD
        ↓
Authenticate GitHub → Azure using OIDC
        ↓
Build versioned Docker image
        ↓
Push image to Azure Container Registry
        ↓
Update Azure Container App
        ↓
Azure creates a new revision
        ↓
FastAPI application is live
```

---

# 🏗️ Architecture

> Add the main CI/CD workflow infographic here.

```markdown
![CI/CD Architecture](docs/images/cicd-architecture.png)
```

Recommended infographic title:

**Automated FastAPI CI/CD Pipeline on Azure**

The diagram should show:

```text
Developer / VS Code
        ↓
GitHub
        ↓
┌─────────────────────────────┐
│ GitHub Actions - CI         │
│                             │
│ Checkout                    │
│ Install dependencies        │
│ Pytest                      │
│ Docker Build                │
└──────────────┬──────────────┘
               │
          CI Successful
               ↓
┌─────────────────────────────┐
│ GitHub Actions - CD         │
│                             │
│ OIDC Authentication         │
│ Docker Build                │
│ Docker Push                 │
│ Container App Update        │
└──────────────┬──────────────┘
               │
               ▼
      Azure Container Registry
               │
               ▼
       Azure Container Apps
               │
               ▼
        FastAPI / Swagger
```

---

# 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Programming Language | Python |
| API Framework | FastAPI |
| API Server | Uvicorn |
| Testing | Pytest |
| Database ORM | SQLAlchemy |
| Database | MySQL |
| Authentication | JWT / OAuth2 |
| Containerization | Docker |
| Version Control | Git |
| Source Repository | GitHub |
| CI/CD | GitHub Actions |
| Cloud Platform | Microsoft Azure |
| Container Registry | Azure Container Registry |
| Application Hosting | Azure Container Apps |
| GitHub → Azure Authentication | OpenID Connect (OIDC) |
| Container App → ACR Authentication | Managed Identity |
| Authorization | Azure RBAC |

---

# 📁 Project Structure

```text
fastapi_tutorial/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── auth/
├── tests/
│
├── main.py
├── crud.py
├── database.py
├── model.py
├── create_table.py
├── project.py
│
├── Dockerfile
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

Sensitive environment variables are excluded from Git using `.gitignore`.

---

# ⚡ FastAPI Application

The application demonstrates common REST API development concepts including:

- GET endpoints
- POST endpoints
- PUT endpoints
- DELETE endpoints
- Path parameters
- Query parameters
- JSON request bodies
- Pydantic validation
- Exception handling
- HTTP status codes
- SQLAlchemy integration
- MySQL database connectivity
- User authentication
- JWT authorization

FastAPI automatically generates Swagger documentation at:

```text
/docs
```

Example:

```text
https://<container-app-domain>/docs
```

---

# 🧪 Automated Testing with Pytest

Automated tests were added before implementing CI/CD.

Testing concepts used in the project include:

- Basic assertions
- `pytest.raises()`
- Parameterized tests
- Fixtures
- `yield` fixtures
- `conftest.py`
- FastAPI `TestClient`
- Monkeypatching
- Test coverage

Example:

```python
def test_greet_name():
    response = client.get("/greet/sarath?age=25")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Hey sarath, you are 25 years old"
    }
```

Run tests locally:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

# 🐳 Docker Containerization

The FastAPI application is packaged into a Docker image.

Dockerfile:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The application runs inside the container using:

```text
Uvicorn
Host: 0.0.0.0
Port: 8000
```

Build locally:

```bash
docker build -t fastapi-app .
```

Run locally:

```bash
docker run -p 8000:8000 fastapi-app
```

Then access:

```text
http://localhost:8000/docs
```

---

# ✅ Continuous Integration

The CI workflow automatically validates the application whenever code is pushed or a pull request is created.

CI performs:

```text
Checkout repository
        ↓
Set up Python
        ↓
Install dependencies
        ↓
Run Pytest
        ↓
Build Docker image
```

Example CI workflow:

```yaml
name: FastAPI CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest httpx

      - name: Run tests
        run: python -m pytest

  build:
    needs: test

    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t fastapi-app .
```

The Docker build depends on:

```yaml
needs: test
```

Therefore:

```text
Tests fail ❌
→ Docker build does not continue

Tests pass ✅
→ Docker build runs
```

This prevents broken application code from progressing further through the pipeline.

---

# 🚀 Continuous Deployment

The Continuous Deployment workflow starts after the CI workflow finishes successfully.

```text
CI succeeds
      ↓
CD starts
      ↓
Checkout tested commit
      ↓
Authenticate to Azure
      ↓
Login to ACR
      ↓
Build Docker image
      ↓
Push image to ACR
      ↓
Update Azure Container App
      ↓
Create new revision
```

---

# 🔐 GitHub → Azure Authentication using OIDC

GitHub Actions authenticates to Azure using **OpenID Connect (OIDC)**.

This avoids storing a long-lived Azure client secret inside GitHub.

GitHub Actions requests permission to generate an OIDC token:

```yaml
permissions:
  contents: read
  id-token: write
```

Azure authentication:

```yaml
- name: Login to Azure
  uses: azure/login@v3
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

The following values are stored securely in GitHub repository secrets:

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

No Azure client password is required.

The authentication flow is:

```text
GitHub Actions
       ↓
Temporary OIDC token
       ↓
Microsoft Entra ID
       ↓
Federated Identity Credential
       ↓
Azure identity
       ↓
Azure resources
```

---

# 🔒 Secretless Authentication Architecture

> Recommended second infographic.

```markdown
![Security Architecture](docs/images/security-architecture.png)
```

Suggested diagram:

```text
DEPLOYMENT IDENTITY

GitHub Actions
      │
      │ OIDC
      ▼
Microsoft Entra ID
      │
      │ Federated Credential
      ▼
github-fastapi-cd
      │
      ├───────────────→ ACR
      │
      └───────────────→ Container Apps


RUNTIME IDENTITY

Azure Container App
      │
      │ System-Assigned Managed Identity
      ▼
Azure Container Registry
      │
      ▼
Pull Docker Image
```

This project therefore uses different identities for different responsibilities.

```text
GitHub identity
→ Push / deploy

Container App identity
→ Pull / run
```

---

# 📦 Azure Container Registry

Docker images are stored inside a private Azure Container Registry.

Registry:

```text
sarathfastapiacr
```

Repository:

```text
fastapi-app
```

During manual testing, Docker images were created using version tags:

```text
fastapi-app:v1
fastapi-app:v2
```

The automated CD pipeline uses **Git commit SHAs** instead.

Example:

```text
fastapi-app:32a166d9...
```

---

# 🏷️ Docker Image Versioning

The CD pipeline does not depend on:

```text
latest
```

Instead, each Docker image is tagged using the Git commit SHA.

Example:

```yaml
${{ github.event.workflow_run.head_sha }}
```

Suppose the commit is:

```text
32a166d9
```

The generated image becomes:

```text
sarathfastapiacr.azurecr.io/fastapi-app:32a166d9
```

This provides:

- Traceability
- Reproducibility
- Easier debugging
- Deployment history
- Safer rollback
- Direct mapping between source code and deployed image

---

# 🔄 Traceable Image Lifecycle

> Recommended third infographic.

```markdown
![Image Lifecycle](docs/images/image-lifecycle.png)
```

Suggested process diagram:

```text
Git Commit
32a166d9
      ↓
Docker Build
      ↓
fastapi-app:32a166d9
      ↓
Azure Container Registry
      ↓
Azure Container App
      ↓
New Revision
      ↓
Production API
```

Main concept:

```text
Git SHA
=
Docker Image Tag
=
Deployment Version
```

---

# ☁️ Azure Container Apps

Azure Container Apps is used to run the Dockerized FastAPI application.

Azure Container Registry stores the image.

Azure Container Apps runs the image.

```text
Docker Image
      ↓
Azure Container Registry
      ↓
Azure Container Apps
      ↓
Uvicorn :8000
      ↓
HTTPS endpoint
```

Container Apps provides:

- Container hosting
- Managed HTTPS
- Autoscaling
- Scale-to-zero
- Revision management
- Traffic management
- Logging
- Application URLs

The FastAPI container listens on:

```text
8000
```

Therefore Azure Container Apps ingress is configured with:

```text
Target Port: 8000
```

---

# 🔑 Managed Identity for Private ACR

The Container App does not use an ACR username or password.

Instead, a **System-Assigned Managed Identity** is enabled on the Container App.

The identity receives:

```text
Container Registry Repository Reader
```

permission on the Azure Container Registry.

Runtime authentication:

```text
Azure Container App
       ↓
System-Assigned Managed Identity
       ↓
Azure RBAC
       ↓
Azure Container Registry
       ↓
Pull Docker Image
```

This allows the application to securely retrieve private container images without storing registry credentials.

---

# 🛡️ Azure RBAC

The project uses different Azure permissions depending on the responsibility.

### GitHub Deployment Identity

The GitHub Azure identity requires permissions to:

```text
Push images to ACR
Update Azure Container Apps
```

For the ABAC-enabled Azure Container Registry, image publishing uses:

```text
Container Registry Repository Writer
```

The deployment identity also requires access to update the Container App.

---

### Container App Runtime Identity

The FastAPI Container App requires only image pull access.

It receives:

```text
Container Registry Repository Reader
```

This follows the principle of least privilege.

---

# 🤖 Automated Deployment to Container Apps

After Docker builds and pushes the new image, GitHub Actions automatically updates Azure Container Apps.

Example:

```yaml
- name: Deploy to Container App
  run: az containerapp update --name ${{ env.CONTAINER_APP_NAME }} --resource-group ${{ env.RESOURCE_GROUP }} --image ${{ env.REGISTRY_URL }}/${{ env.IMAGE_NAME }}:${{ github.event.workflow_run.head_sha }}
```

Breakdown:

```text
az containerapp update
→ update an existing Container App

--name
→ identify the Container App

--resource-group
→ specify where the application exists

--image
→ specify the newly built Docker image
```

Example resolved command:

```bash
az containerapp update \
  --name fastapi-app \
  --resource-group rg-fastapi-cicd \
  --image sarathfastapiacr.azurecr.io/fastapi-app:32a166d9
```

Azure then creates a new Container App revision using that image.

---

# 🔁 Complete Automated CI/CD Flow

```text
Developer
    ↓
git push
    ↓
GitHub Repository
    ↓
GitHub Actions CI
    ↓
Run automated tests
    ↓
Docker build verification
    ↓
CI succeeds
    ↓
GitHub Actions CD
    ↓
Authenticate to Azure using OIDC
    ↓
Build versioned Docker image
    ↓
Push Docker image to ACR
    ↓
az containerapp update
    ↓
Container Apps pulls new image
    ↓
New revision
    ↓
FastAPI application live
```

After the initial Azure infrastructure exists, future deployments require no manual Docker build, push, or Container App image update.

---

# ☁️ Azure Runtime Architecture

> Recommended fourth infographic.

```markdown
![Azure Runtime Architecture](docs/images/azure-runtime-architecture.png)
```

Suggested diagram:

```text
Azure Resource Group
rg-fastapi-cicd
│
├── Azure Container Registry
│   │
│   └── fastapi-app
│       ├── v1
│       ├── v2
│       └── <git-commit-sha>
│
├── Container Apps Environment
│   │
│   └── fastapi-app
│       │
│       ├── Uvicorn
│       ├── Port 8000
│       └── Managed Identity
│
└── Log Analytics Workspace

                 ↓

              HTTPS

                 ↓

          FastAPI /docs
```

---

# 🏢 Azure Resources

The project resources are organized inside:

```text
rg-fastapi-cicd
```

Main resources:

```text
rg-fastapi-cicd
│
├── Azure Container Registry
│   └── sarathfastapiacr
│
├── Container Apps Environment
│
├── Azure Container App
│   └── fastapi-app
│
└── Log Analytics Workspace
```

---

# 🏗️ Infrastructure vs Deployment

The initial Azure infrastructure is provisioned once.

For this project, infrastructure was created manually to understand each Azure component.

```text
Provisioning
=
Create infrastructure

Examples:
ACR
Container Apps Environment
Container App
Managed Identity
RBAC
```

Once infrastructure exists, application deployments are automated.

```text
Deployment
=
Release new application versions

GitHub Actions
→ Test
→ Build
→ Push
→ Deploy
```

In a larger production environment, initial infrastructure provisioning could also be automated using:

- Terraform
- Bicep
- ARM templates
- Infrastructure pipelines

This project intentionally focused first on understanding the Azure resources before automating application deployment.

---

# 🧯 Troubleshooting and Lessons Learned

This project included several real deployment issues that were investigated and resolved.

These troubleshooting steps were an important part of understanding cloud deployment.

---

## Azure CLI MFA Authentication

Azure CLI initially required MFA and explicit tenant authentication.

The correct Azure tenant and subscription were selected before accessing the Container Registry.

Verification:

```bash
az account show --output table
```

---

## GitHub OIDC Authentication Failure

Initial GitHub Actions error:

```text
AADSTS70025:
The client has no configured federated identity credentials
```

Cause:

```text
GitHub successfully generated an OIDC token
but
Microsoft Entra ID did not yet trust the repository.
```

Resolution:

A Federated Identity Credential was added to the Microsoft Entra App Registration.

```text
GitHub Repository
      ↓
main branch
      ↓
Federated Credential
      ↓
Microsoft Entra ID
```

---

## GitHub Azure Identity Permissions

OIDC authentication succeeded, but the GitHub identity initially lacked sufficient access to Azure resources.

Azure RBAC roles were added according to the operations required by the deployment pipeline.

---

## ACR Repository Permissions

The Azure Container Registry uses the newer repository permission model.

Repository responsibilities were separated:

```text
Repository Writer
→ GitHub pushes images

Repository Reader
→ Container App pulls images
```

The ACR admin account remained disabled.

---

## Container App Image Pull Failure

Container App deployment initially failed with:

```text
UNAUTHORIZED: authentication required
Action: pull
```

Cause:

```text
Container App
→ attempted to pull private image
→ identity did not have correct ACR permission
```

Resolution:

The Container App's System-Assigned Managed Identity was given:

```text
Container Registry Repository Reader
```

permission on ACR.

---

## Docker / Uvicorn Startup Error

Container logs showed:

```text
Error: Got unexpected extra argument (8000)
```

The Dockerfile originally contained:

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "8000"]
```

The `--port` argument was missing.

The command was corrected to:

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

A new Docker image version was then built:

```text
fastapi-app:v2
```

and deployed successfully.

---

## Container Apps Ingress Port

The public quickstart container initially listened on:

```text
80
```

The actual FastAPI container listens on:

```text
8000
```

Therefore Azure Container Apps ingress was updated to:

```text
Target Port: 8000
```

---

## Scale to Zero

Azure Container Apps showed:

```text
Scaled to 0
```

This was not an error.

The application was configured to allow Azure Container Apps to scale down when idle and automatically start a replica when traffic arrives.

---

# 📊 Deployment Evidence

Recommended screenshots to include in this section.

---

## 1. GitHub Actions

Show a successful CI/CD execution.

```markdown
![GitHub Actions](docs/images/github-actions-success.png)
```

The screenshot should show:

```text
CI ✅
CD ✅
```

---

## 2. Azure Container Registry

Show the `fastapi-app` repository with tags such as:

```text
v1
v2
<git-commit-sha>
```

```markdown
![Azure Container Registry](docs/images/acr-images.png)
```

This demonstrates both manual versioning and automated commit-based versioning.

---

## 3. Azure Container App

Show:

```text
Status: Running
Container App URL
Latest revision
```

```markdown
![Azure Container App](docs/images/container-app-running.png)
```

---

## 4. FastAPI Swagger UI

Show the publicly deployed Swagger interface:

```text
/docs
```

```markdown
![FastAPI Swagger](docs/images/swagger-cloud.png)
```

This provides visible proof that the containerized API is running successfully in Azure.

---

# 📸 Recommended Workflow Infographics

The repository should prioritize diagrams that explain the automation rather than using many Azure Portal screenshots.

Recommended diagrams:

### 1. Automated CI/CD Pipeline

```text
Developer
→ GitHub
→ CI
→ Pytest
→ Docker
→ CD
→ ACR
→ Container Apps
→ API
```

Filename:

```text
docs/images/cicd-architecture.png
```

---

### 2. Secretless Authentication Architecture

```text
GitHub
→ OIDC
→ Microsoft Entra ID
→ Azure

Container App
→ Managed Identity
→ ACR
```

Filename:

```text
docs/images/security-architecture.png
```

---

### 3. Docker Image Lifecycle

```text
Git Commit
→ Docker Image
→ ACR
→ Container App Revision
```

Filename:

```text
docs/images/image-lifecycle.png
```

---

### 4. Azure Runtime Architecture

```text
Resource Group
├── ACR
├── Container Apps Environment
├── FastAPI Container App
└── Log Analytics
```

Filename:

```text
docs/images/azure-runtime-architecture.png
```

---

# 🎯 Key Engineering Concepts Demonstrated

This project demonstrates practical experience with:

- REST API development
- Automated software testing
- Docker
- Container registries
- CI/CD
- GitHub Actions
- Azure
- OIDC authentication
- Microsoft Entra ID
- Federated identities
- Managed identities
- Azure RBAC
- Secure container deployment
- Container versioning
- Git SHA image tagging
- Cloud application deployment
- Container revisions
- Logging and troubleshooting
- Production-style deployment workflows

---

# ✅ Final Result

The final system provides an automated path from source code to a running cloud application.

```text
Developer
    ↓
GitHub
    ↓
Automated Testing
    ↓
Docker Build
    ↓
Azure Container Registry
    ↓
Azure Container Apps
    ↓
Public HTTPS API
    ↓
FastAPI Swagger
```

After the initial Azure infrastructure is created, new application versions can be automatically:

```text
Tested
→ Containerized
→ Versioned
→ Published
→ Deployed
```

through GitHub Actions.

---

# 🔮 Future Improvements

Future improvements to this project can include:

- Application Insights
- Azure Monitor
- Advanced Log Analytics
- Automated health checks
- Deployment verification
- Automatic rollback
- Staging and production environments
- Azure Key Vault
- MLflow
- Azure Machine Learning
- Model monitoring
- Model evaluation
- Continuous Training
- Model quality gates
- Infrastructure as Code using Terraform
- Infrastructure as Code using Bicep
- Kubernetes
- Azure Kubernetes Service (AKS)

---

# 📚 What I Learned

Through this project I gained hands-on experience building a complete application delivery workflow rather than only developing an API.

The project covered the full lifecycle:

```text
Code
→ Test
→ Package
→ Authenticate
→ Publish
→ Deploy
→ Run
→ Troubleshoot
```

A major focus was understanding how individual tools interact:

```text
GitHub
→ source control

Pytest
→ quality validation

Docker
→ application packaging

GitHub Actions
→ automation

Azure Container Registry
→ container image storage

Azure Container Apps
→ container execution

OIDC
→ secure deployment authentication

Managed Identity
→ secure runtime authentication
```

This project demonstrates how application development, DevOps, cloud infrastructure, security, and deployment automation come together in a real end-to-end workflow.

---

## Author

**Sarath Kumar Komathukattil**

AI/ML | Applied AI | MLOps | Cloud 