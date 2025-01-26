# System Workflow: AI-Powered Fraud Detection System

This paper describes the AI-Powered Fraud Detection System, its components, and how they interact with each other. The workflow is broken into several stages to make it easier to understand and modular.

---

## **1. Data Ingestion**

- **Sources**:
  - Call recordings, VKYC videos, and transaction logs are stored in **Amazon S3** buckets.
- **ETL Process**:
- **AWS Glue** is used to clean and transform transaction data for analysis.

---

## **2. Spam Call Detection**
- **Audio Transcription**:
  - **AWS Transcribe** transcribes call recordings into text.
- **Transcript Analysis**:
  - **AWS Comprehend** analyzes transcripts for phishing keywords using NLP techniques.
- **Call Metadata Analysis**:
  - A custom Python-based solution analyzes metadata such as call frequency and duration to flag suspicious calls.

---

## **3. Deepfake Detection in VKYC**
- **Facial Recognition**:
  - **Amazon Rekognition** detects and analyzes faces in VKYC video sessions.
- **Deepfake Detection**:
  - **Amazon SageMaker** runs ML models to identify anomalies in facial features and voice patterns.
- **Results**:
  - VKYC sessions are marked as authentic or suspicious.

---

## **4. Financial Fraud Detection**
- **Data Preparation**:
  - **AWS Glue** prepares transaction data for machine learning analysis.
- **Anomaly Detection**:
- **Isolation Forest** or custom-trained SageMaker models detect irregularities in transaction patterns.
- **Results**:
  - Transactions are classified as normal or potentially fraudulent.

---

## **5. Real-Time Alerts and Feedback**
- **Notifications**:
  - **Amazon SNS** sends real-time alerts to users when suspicious activities are detected.
- **User Interface**:
  - A **Flask-based UI**, hosted using **AWS Amplify**, allows users to:
    - Report fraudulent activities.
- View real-time alerts and transaction status.

---

## **System Workflow Diagram**
![System Architecture](docs/workflow diagram.png)

---

## **Summary of AWS Services**
| Service         | Purpose                                                        |
| **Amazon S3**    | Storing call recording, VKYC videos, transaction log files in storage.                                |
| **AWS Glue**     | Transaction data - performing ETL processes.
| **AWS Lambda**   | Serverless workflows for fraud detection                       |
| **AWS Rekognition** | Facial and video analysis for VKYC sessions                 |
| **Amazon SageMaker** | Training and inference for anomaly detection models        |
| **Amazon SNS**   | Real-time notifications and alerts                             |
| **AWS Amplify**  | Hosting the UI for reporting and feedback                      |
| **AWS Transcribe** | Converts audio recordings to text for analysis               |
| **AWS Comprehend** | NLP for Call Transcripts Analysis                           |

---
## **Future Enhancements**
1. **Advanced Deepfake Detection**
   Incorporation of state-of-the-art voice and facial models.
2. **Domain Enlargement**
   Expanding fraud detection beyond the finance domain to include the healthcare and e-commerce domains.
3. **Improved User Feedback**:
   - Utilize user feedback to iteratively improve model accuracy.

---

## **Contributors**
- **Name**: Prashant yadav
- **Role**: Project Leader
- **Contact**: py3030223@gmail.com

---

## **How to Use**
1. Place this `System_Workflow.md` in the root of your GitHub repository.
2. Ensure all referenced files (like diagrams) are in the `docs/` directory.
3. Use this file as a comprehensive reference for understanding the project workflow.
