# EzRollout - Product Requirements Document

## Översikt
EzRollout är ett verktyg för att övervaka och hantera utrullning av applikationer via Microsoft Intune.

## Huvudfunktioner

### 1. Dashboard
- Visar övergripande status för enheter och utrullningar
- Grafisk representation av compliance status
- Deployment success rate

### 2. Applikationssökning
- Sökning via:
  - Application ID (5-siffrigt)
  - Applikationsnamn
- Visar detaljerad information om sökresultaten

### 3. Rapportgenerering
- Genererar Excel-rapport för specifik applikation
- Rapporten innehåller en flik "Deployment Status" med:
  - App-specifik information:
    - Application Name
    - Version
    - Short Version
    - Publisher
    - Application Key
    - Install State
  - Enhetsinformation:
    - Device Name
    - User
    - Department
    - Platform
    - OS Version
    - Last Check-in

## Tekniska Specifikationer
- Backend: FastAPI
- Frontend: Streamlit
- Dataformat: Excel (.xlsx)
- Mock-data för utveckling och testning

## Ändringar 2024-03-14
1. Uppdaterat rapportgenerering för att fokusera på specifika applikationer
2. Förenklat rapportstruktur till en enda flik
3. Lagt till detaljerad applikationsinformation i rapporter
4. Uppdaterat filnamnsmönster för rapporter
5. Förbättrat sökfunktionalitet för applikationer

## Kommande Funktioner
- Jämförelse med tidigare versioner av samma applikation
- Historisk data för utrullningar

# Product Requirements Document (PRD)

## **Intune AI Agent**

### **1. Overview**
**Intune AI Agent** is an API-based service that automates the collection, analysis, and reporting of device and application deployment data from Microsoft Intune. It provides real-time insights, generates reports, and supports integration with AI-powered analysis tools.

### **2. Objectives**
- Automate data retrieval from Microsoft Graph API.
- Generate Excel reports summarizing device and application deployment status.
- Provide a REST API for real-time queries.
- Support AI-based analysis for troubleshooting and trend identification.
- Ensure secure and scalable deployment.

### **3. Features**
#### **3.1 API Endpoints**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/device-status` | GET | Fetches device status from Microsoft Intune. |
| `/generate-report` | GET | Generates an Excel report of the current deployment status. |
| `/download-report` | GET | Provides a downloadable link to the generated report. |

#### **3.2 Data Processing & Reporting**
- Extracts **device compliance, OS version, application installation state** from Intune.
- Stores data in an **Excel file (openpyxl)** for easy distribution.
- Ensures **error handling** for missing data and authentication failures.

#### **3.3 AI-Based Analysis (Future Scope)**
- **GPT-4 powered insights** on installation failures and trends.
- **Predictive analytics** for potential deployment issues.
- **Chatbot integration** for querying deployment reports via natural language.

### **4. Technical Requirements**
#### **4.1 Tech Stack**
| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python) |
| Data Retrieval | Microsoft Graph API |
| Database | SQLite (optional) |
| Report Generation | Pandas, OpenPyXL |
| AI Integration | GPT-4 API (future) |

#### **4.2 Authentication & Security**
- OAuth2 authentication for Microsoft Graph API.
- API key or JWT authentication for external access.
- Secure storage of API credentials using **environment variables**.

### **5. Deployment & Scalability**
- **Docker support** for containerized deployment.
- **Cloud-ready** for hosting on Azure Functions or AWS Lambda.
- **Logging & Monitoring** with built-in FastAPI logging.

### **6. Milestones & Roadmap**
#### **Phase 1: MVP (2 Weeks)**
✅ API development with `/device-status`, `/generate-report`, `/download-report` endpoints.
✅ Integration with Microsoft Graph API.
✅ Error handling & validation.

#### **Phase 2: Enhancements (4 Weeks)**
🔹 AI-based analysis of deployment success rates.
🔹 Dashboard integration with Streamlit.
🔹 Automate periodic report generation.

#### **Phase 3: AI-Powered Features (Future Scope)**
🚀 Chatbot-based report querying.
🚀 Predictive failure analysis.
🚀 Smart troubleshooting recommendations.

### **7. Open Questions & Risks**
- Do we need **real-time dashboard visualization** in addition to reports?
- What level of **data retention** is required?
- How should **API authentication** be managed for external clients?

---
### **8. Conclusion**
The **Intune AI Agent** will streamline application deployment analysis and reporting for IT teams. It will start as a **lightweight, API-driven tool**, with **AI-powered insights** added in future iterations. 🚀

