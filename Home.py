import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="EzRollout - Overview", layout="wide")

st.title("EzRollout System Overview")

# Latest Applications Section
st.write("### Latest Applications")

def get_latest_applications():
    try:
        response = requests.get("http://localhost:8000/api/device-status")
        if response.status_code == 200:
            devices = response.json()
            if isinstance(devices, list) and devices:
                # Samla alla unika applikationer och deras installationsstatus
                all_apps = {}
                for device in devices:
                    for app in device['installedApplications']:
                        app_id = app['id']
                        if app_id not in all_apps:
                            # Räkna installationsstatus för denna app över alla enheter
                            status_counts = {'Installed': 0, 'Failed': 0, 'N/A': 0}
                            total_installs = 0
                            for d in devices:
                                for a in d['installedApplications']:
                                    if a['id'] == app_id:
                                        total_installs += 1
                                        if a['installState'] == 'Installed':
                                            status_counts['Installed'] += 1
                                        elif a['installState'] in ['Failed', 'Error', 'Uninstall Failed']:
                                            status_counts['Failed'] += 1
                                        else:
                                            status_counts['N/A'] += 1
                            
                            # Beräkna procentandelar
                            status_percentages = {
                                k: (v / total_installs * 100) if total_installs > 0 else 0 
                                for k, v in status_counts.items()
                            }
                            
                            all_apps[app_id] = {
                                'name': app['displayName'],
                                'status_percentages': status_percentages,
                                'appId': app['id'],
                                'entraGroups': app.get('entraGroups', []),
                                'addedDate': app.get('addedDate', datetime.now().isoformat())
                            }
                
                # Sortera efter addedDate och ta de 5 senaste
                sorted_apps = sorted(all_apps.values(), 
                                  key=lambda x: x['addedDate'], 
                                  reverse=True)[:5]
                return sorted_apps
    except Exception as e:
        st.error(f"Error fetching latest applications: {str(e)}")
        return []

latest_apps = get_latest_applications()

if latest_apps:
    # Skapa en enkel tabell för applikationerna
    for app in latest_apps:
        success_rate = app['status_percentages']['Installed']
        status_color = "🟢" if success_rate > 90 else "🟡" if success_rate > 70 else "🔴"
        
        col1, col2 = st.columns([4, 1])
        with col1:
            # Skapa en klickbar länk av applikationsnamnet
            if st.button(f"📦 {app['name']}", key=app['appId']):
                # Spara app ID i session state för att användas i Application Search
                st.session_state['selected_app_id'] = app['appId']
                # Navigera till Application Search sidan
                st.switch_page("pages/1_Application_Search.py")
        with col2:
            st.write(f"{status_color} {success_rate:.1f}%")
        
        # Tunn separator mellan applikationerna
        st.markdown('<hr style="margin: 5px 0; border: none; border-top: 1px solid #eee;">', unsafe_allow_html=True)
else:
    st.info("No applications found")

# Lägg till en separator mellan sektionerna
st.markdown("---")
st.markdown("## System Overview")

# Fetch deployment analysis
def fetch_deployment_analysis():
    try:
        response = requests.get("http://localhost:8000/api/analyze-deployment")
        if response.status_code == 200:
            return response.json()
        return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

# Fetch device status
def fetch_device_status():
    try:
        response = requests.get("http://localhost:8000/api/device-status")
        if response.status_code == 200:
            return response.json()
        return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

# Dashboard layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Deployment Success Rate")
    analysis = fetch_deployment_analysis()
    if "error" not in analysis:
        st.metric("Success Rate", f"{analysis.get('success_rate', 0):.1f}%")
        st.metric("Total Devices", analysis.get('total_devices', 0))
    else:
        st.error(f"Failed to fetch analysis data: {analysis.get('error', 'Unknown error')}")

with col2:
    st.subheader("Device Status")
    devices = fetch_device_status()
    if isinstance(devices, list) and devices:
        try:
            df = pd.DataFrame(devices)
            if 'complianceState' in df.columns:
                fig = px.pie(df, names='complianceState', title='Device Compliance Status')
                st.plotly_chart(fig)
            else:
                st.warning("No compliance data available in device data")
        except Exception as e:
            st.error(f"Could not create chart: {str(e)}")
    else:
        error_msg = devices.get('error', 'No device data available') if isinstance(devices, dict) else 'No device data available'
        st.error(f"Failed to fetch device data: {error_msg}")

# Detaljerad statistik sektion
st.write("### Detailed Statistics")
if isinstance(devices, list) and devices:
    df = pd.DataFrame(devices)
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    with col_stats1:
        st.subheader("Device Statistics")
        total_devices = len(df)
        compliant_devices = len(df[df['complianceState'] == 'compliant'])
        noncompliant_devices = len(df[df['complianceState'] == 'noncompliant'])
        
        st.metric("Total Devices", total_devices)
        st.metric("Compliant Devices", compliant_devices)
        st.metric("Non-compliant Devices", noncompliant_devices)
        compliance_rate = (compliant_devices / total_devices * 100) if total_devices > 0 else 0
        st.metric("Compliance Rate", f"{compliance_rate:.1f}%")

    with col_stats2:
        st.subheader("OS Distribution")
        os_dist = df['operatingSystem'].value_counts()
        fig_os = px.pie(values=os_dist.values, names=os_dist.index, title='OS Distribution')
        st.plotly_chart(fig_os, use_container_width=True)
        
        # OS Version breakdown
        os_version_dist = df['osVersion'].value_counts()
        fig_version = px.bar(x=os_version_dist.index, y=os_version_dist.values, 
                           title='OS Version Distribution')
        st.plotly_chart(fig_version, use_container_width=True)

    with col_stats3:
        st.subheader("Department Analysis")
        dept_dist = df['department'].value_counts()
        fig_dept = px.pie(values=dept_dist.values, names=dept_dist.index, 
                         title='Department Distribution')
        st.plotly_chart(fig_dept, use_container_width=True)

    # Tidslinje för senaste synkronisering
    st.subheader("Device Sync Timeline")
    df['lastSyncDateTime'] = pd.to_datetime(df['lastSyncDateTime'])
    fig_timeline = px.scatter(df, 
                            x='lastSyncDateTime', 
                            y='deviceName',
                            color='complianceState',
                            title='Last Device Sync Timeline')
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Detaljerad enhetstabell
    st.subheader("Detailed Device Information")
    columns_to_display = ['deviceName', 'userDisplayName', 'department', 
                         'osVersion', 'complianceState', 'lastSyncDateTime']
    st.dataframe(df[columns_to_display]) 