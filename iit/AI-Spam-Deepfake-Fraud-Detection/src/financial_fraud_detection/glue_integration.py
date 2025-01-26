import boto3
import json

# Initialize AWS Glue client
glue_client = boto3.client("glue", region_name="your-region")

def start_glue_job(job_name, arguments=None):
    """
    Starts an AWS Glue job.

    Parameters:
        job_name (str): The name of the Glue job to start.
        arguments (dict): Additional arguments to pass to the Glue job.

    Returns:
        dict: Details about the job run, including the JobRunId.
    """
    try:
        response = glue_client.start_job_run(
            JobName=job_name,
            Arguments=arguments or {}
        )
        job_run_id = response.get("JobRunId")
        print(f"Glue job '{job_name}' started successfully with JobRunId: {job_run_id}")
        return {"status": "success", "job_run_id": job_run_id}
    except Exception as e:
        print(f"Error starting Glue job: {e}")
        return {"status": "error", "message": str(e)}

def get_glue_job_status(job_name, job_run_id):
    """
    Retrieves the status of a Glue job run.

    Parameters:
        job_name (str): The name of the Glue job.
        job_run_id (str): The JobRunId of the Glue job run.

    Returns:
        dict: Status details of the job run.
    """
    try:
        response = glue_client.get_job_run(
            JobName=job_name,
            RunId=job_run_id
        )
        status = response["JobRun"].get("JobRunState")
        print(f"Glue job '{job_name}' with JobRunId '{job_run_id}' is in state: {status}")
        return {"status": "success", "job_status": status}
    except Exception as e:
        print(f"Error fetching Glue job status: {e}")
        return {"status": "error", "message": str(e)}

def create_glue_job(job_name, script_location, role, s3_target_bucket, temp_dir, glue_version="3.0", worker_type="G.1X", num_workers=2):
    """
    Creates an AWS Glue job for ETL processing.

    Parameters:
        job_name (str): Name of the Glue job to create.
        script_location (str): S3 path to the ETL script.
        role (str): IAM role for the Glue job.
        s3_target_bucket (str): Target S3 bucket for transformed data.
        temp_dir (str): Temporary directory path in S3 for Glue job.
        glue_version (str): Glue version (default is 3.0).
        worker_type (str): Worker type (e.g., "G.1X" or "G.2X").
        num_workers (int): Number of workers to assign to the job.

    Returns:
        dict: Details about the created Glue job.
    """
    try:
        response = glue_client.create_job(
            Name=job_name,
            Role=role,
            ExecutionProperty={"MaxConcurrentRuns": 1},
            Command={
                "Name": "glueetl",
                "ScriptLocation": script_location,
                "PythonVersion": "3"
            },
            DefaultArguments={
                "--TempDir": temp_dir,
                "--enable-continuous-cloudwatch-log": "true",
                "--enable-metrics": "",
                "--job-bookmark-option": "job-bookmark-enable"
            },
            GlueVersion=glue_version,
            WorkerType=worker_type,
            NumberOfWorkers=num_workers,
            OutputLocation=f"s3://{s3_target_bucket}/transformed-data/"
        )
        print(f"Glue job '{job_name}' created successfully.")
        return {"status": "success", "job_details": response}
    except Exception as e:
        print(f"Error creating Glue job: {e}")
        return {"status": "error", "message": str(e)}

# Example usage
if __name__ == "__main__":
    # Replace with your AWS-specific parameters
    example_job_name = "fraud-detection-etl"
    example_script_location = "s3://your-bucket-name/scripts/fraud_etl_script.py"
    example_role = "arn:aws:iam::your-account-id:role/AWSGlueServiceRole"
    example_s3_target_bucket = "your-target-bucket-name"
    example_temp_dir = "s3://your-bucket-name/temp/"

    # Create a Glue job
    job_creation_response = create_glue_job(
        job_name=example_job_name,
        script_location=example_script_location,
        role=example_role,
        s3_target_bucket=example_s3_target_bucket,
        temp_dir=example_temp_dir
    )
    print(json.dumps(job_creation_response, indent=4))

    # Start the Glue job
    if job_creation_response["status"] == "success":
        job_start_response = start_glue_job(example_job_name)
        print(json.dumps(job_start_response, indent=4))

        # Get job status (replace with actual JobRunId from the response)
        if job_start_response["status"] == "success":
            job_run_id = job_start_response["job_run_id"]
            job_status_response = get_glue_job_status(example_job_name, job_run_id)
            print(json.dumps(job_status_response, indent=4))
