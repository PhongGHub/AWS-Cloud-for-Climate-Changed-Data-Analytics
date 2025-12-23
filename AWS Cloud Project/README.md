# AWS Cloud Project: Real-time Climate Data Analytics

This project simulates a Real-time Data Analytics pipeline for Climate Change monitoring.
It generates mock sensor data (Temperature, Humidity, CO2) from cities around the world, streams it to AWS Kinesis, processes it with Lambda, and stores it in S3 for analysis.

## Architecture
1.  **Producer (`producer/main.py`)**: Python script generating random climate data and sending it to **Amazon Kinesis Data Stream**.
2.  **Stream (`climate-stream`)**: Buffers real-time data.
3.  **Processor (`lambda/processor.py`)**: AWS Lambda function triggered by Kinesis. It extracts data, adds timestamps, checks for alerts (High Temp), and saves to **Amazon S3**.
4.  **Storage (`S3 Bucket`)**: Data Lake storing JSON files.
5.  **Analytics (QuickSight)**: *To be configured manually* for visualizing the data.

## Prerequisites
To deploy this project to the real AWS Cloud, you need to install the following tools:

1.  **AWS CLI** (Command Line Interface)
    - [Download for Windows (64-bit)](https://awscli.amazonaws.com/AWSCLIV2.msi)
    - After installing, open a new terminal and run: `aws configure`
    - Enter your **Access Key ID** and **Secret Access Key** (from your AWS IAM Console).
    - Default Region name: `us-east-1`
    - Default output format: `json`

2.  **Terraform** (Infrastructure as Code)
    - [Download for Windows (AMD64)](https://releases.hashicorp.com/terraform/1.9.0/terraform_1.9.0_windows_amd64.zip)
    - Extract the zip file.
    - Add the folder containing `terraform.exe` to your System **PATH** environment variable.
    - Verify by running: `terraform -version`

3.  **Python 3.9+** (Already installed)

## Deployment Instructions

### 1. Deploy Infrastructure (Terraform)
1.  Navigate to the `infrastructure` folder:
    ```bash
    cd infrastructure
    ```
2.  Initialize Terraform:
    ```bash
    terraform init
    ```
3.  Review plan and apply:
    ```bash
    terraform apply
    ```
    *Type `yes` to confirm.*
    *This will create the Kinesis Stream, S3 Bucket, and Lambda Function in your AWS account.*

4.  Note the **Outputs**:
    - `s3_bucket_name`: The created S3 bucket (e.g., `climate-analytics-lake-xxxx`)
    - `kinesis_stream_name`: `climate-stream`

### 2. Configure & Run Data Producer
1.  Open `producer/main.py`.
2.  **IMPORTANT**: Change `SIMULATION_MODE = True` to `False` on line 11.
    ```python
    SIMULATION_MODE = False
    ```
3.  Navigate to the `producer` folder:
    ```bash
    cd ../producer
    ```
4.  Run the producer:
    ```bash
    python main.py
    ```
    *You should see logs sending data to Kinesis.*

### 3. Verify Data Flow
1.  Go to the **AWS Console > S3**.
2.  Open the bucket created by Terraform.
3.  You should see a folder `climate_data/` containing JSON files organized by City and Timestamp.

## Dashboard Setup (Amazon QuickSight)
*Note: QuickSight incurs costs and requires manual setup.*

1.  **Sign up for QuickSight** (Standard or Enterprise).
2.  **Connect S3**:
    - Go to "Datasets" > "New Dataset" > "S3".
    - **DataSource Name**: `ClimateDataLake`.
    - **Upload Manifest**: Create a file named `manifest.json` locally with the following content (replace `YOUR_BUCKET_NAME`):
      ```json
      {
          "fileLocations": [
              {
                  "URIPrefixes": [
                      "s3://YOUR_BUCKET_NAME/climate_data/"
                  ]
              }
          ],
          "globalUploadSettings": {
              "format": "JSON"
          }
      }
      ```
    - Upload this `manifest.json`.
3.  **Visualize**:
    - Use the visualization area to drag-and-drop fields.
    - **X-axis**: `timestamp` (Aggregate by Minute/Hour).
    - **Y-axis**: `temperature` (or `humidity`).
    - **Filter**: `city`.

## Cleanup
To avoid charges, destroy the infrastructure when finished:
```bash
cd infrastructure
terraform destroy
```
