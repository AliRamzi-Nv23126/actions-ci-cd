# Alternative: Using Amazon ECR Instead of DockerHub

If you prefer to use Amazon ECR (Elastic Container Registry) instead of DockerHub, follow this guide.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **IAM User** with the following permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "ecr:GetAuthorizationToken",
           "ecr:BatchCheckLayerAvailability",
           "ecr:GetDownloadUrlForLayer",
           "ecr:PutImage",
           "ecr:InitiateLayerUpload",
           "ecr:UploadLayerPart",
           "ecr:CompleteLayerUpload",
           "ecr:DescribeRepositories",
           "ecr:DescribeImages"
         ],
         "Resource": "arn:aws:ecr:*:*:repository/*"
       }
     ]
   }
   ```

## Setup Steps

### Step 1: Create ECR Repository

```bash
# Using AWS CLI
aws ecr create-repository --repository-name todo-app --region us-east-1

# Response will include repository URI, e.g.:
# 123456789.dkr.ecr.us-east-1.amazonaws.com/todo-app
```

### Step 2: Create IAM Access Keys

1. Go to IAM Console → Users → Create user
2. Attach the permissions policy above
3. Create access key:
   - Go to user → Security credentials → Create access key
   - Select "Other"
   - Copy **Access Key ID** and **Secret Access Key**

### Step 3: Add GitHub Secrets

In your GitHub repo Settings → Secrets → New repository secret:

| Secret Name | Value |
|------------|-------|
| `AWS_ACCESS_KEY_ID` | Your IAM access key ID |
| `AWS_SECRET_ACCESS_KEY` | Your IAM secret access key |
| `AWS_REGION` | Your region (e.g., `us-east-1`) |

### Step 4: Update CD Workflow

Replace `.github/workflows/cd.yml` with:

```yaml
name: CD

on:
  release:
    types: [published]

jobs:
  build-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Log in to ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Extract version from tag
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push to ECR
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ steps.login-ecr.outputs.registry }}/todo-app:${{ steps.version.outputs.VERSION }}
            ${{ steps.login-ecr.outputs.registry }}/todo-app:latest

      - name: Image digest
        run: echo "Pushed image to ECR"
```

### Step 5: Test the Workflow

1. Create a GitHub Release: `v0.1.0`
2. CD workflow will build and push to ECR
3. Verify in AWS ECR Console:
   ```bash
   aws ecr describe-images --repository-name todo-app --region us-east-1
   ```

## ECR vs DockerHub Comparison

| Feature | DockerHub | Amazon ECR |
|---------|-----------|-----------|
| **Setup Time** | ~5 minutes | ~10 minutes (AWS account) |
| **Cost** | Free tier (1 private repo) | Pay per GB stored/transferred |
| **Regional** | Global CDN | Region-specific (configure replication) |
| **Integration** | GitHub Actions | Seamless AWS integration |
| **Best For** | Quick start, hobby projects | Production, AWS-native apps |
| **Security** | Basic (password/token) | IAM-based (more granular) |

---

## Troubleshooting ECR

### Issue: "InvalidUserID.NotFound" or "User: arn:... is not authorized"
**Solution:** Verify IAM permissions. User needs `ecr:GetAuthorizationToken`.

### Issue: "Repository not found"
**Solution:** Create the repository first:
```bash
aws ecr create-repository --repository-name todo-app --region us-east-1
```

### Issue: "Access Denied" when pushing
**Solution:** Check IAM policy has these actions:
- `ecr:PutImage`
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`

### Issue: "Unable to get image details"
**Solution:** Ensure secrets are set correctly and region matches where repo was created.
