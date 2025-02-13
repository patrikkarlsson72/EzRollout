import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="EzRollout - Application Search", layout="wide")

st.title("Application Search")

# Application Search Section
col_search1, col_search2 = st.columns(2)

# Kolla om vi har ett selected_app_id från Home page
if 'selected_app_id' in st.session_state:
    app_id = st.session_state['selected_app_id']
    # Dölj sökfälten när vi kommer från Home
    st.write(f"**Showing details for application ID: {app_id}**")
    app_name = None
    # Rensa session state så att det inte finns kvar vid manuell sökning
    del st.session_state['selected_app_id']
else:
    # Visa sökfälten endast när vi kommer direkt till sidan
    with col_search1:
        app_id = st.text_input("Search by Application ID", placeholder="Enter App ID...")
    with col_search2:
        app_name = st.text_input("Search by Application Name", placeholder="Enter App Name...")

if app_id or app_name:
    try:
        params = {}
        if app_id:
            params['app_id'] = app_id
        if app_name:
            params['app_name'] = app_name
            
        response = requests.get("http://localhost:8000/api/search-applications", params=params)
        if response.status_code == 200:
            results = response.json()
            if results:
                # Filtrera resultaten för att bara visa den specifika appen
                filtered_results = []
                for device in results:
                    matching_apps = [
                        app for app in device['installedApplications']
                        if (app_id and app['id'] == app_id) or 
                           (app_name and app_name.lower() in app['name'].lower())
                    ]
                    if matching_apps:
                        device_copy = device.copy()
                        device_copy['installedApplications'] = matching_apps
                        filtered_results.append(device_copy)
                
                if filtered_results:
                    st.write("### Application Deployment Status")
                    df_results = pd.DataFrame(filtered_results)
                    
                    # Visa applikationsinformation
                    target_app = filtered_results[0]['installedApplications'][0]
                    col_app1, col_app2 = st.columns(2)
                    
                    with col_app1:
                        st.subheader("Application Details")
                        st.info(f"""
                        **Name:** {target_app['displayName']}
                        **Version:** {target_app['version']}
                        **Publisher:** {target_app['publisher']}
                        """)
                    
                    with col_app2:
                        st.subheader("Deployment Overview")
                        total_devices = len(df_results)
                        installed_devices = len([d for d in results if any(
                            app['installState'] == 'Installed' 
                            for app in d['installedApplications'] 
                            if (app_id and app['id'] == app_id) or (app_name and app_name.lower() in app['name'].lower())
                        )])
                        
                        deployment_rate = (installed_devices / total_devices * 100) if total_devices > 0 else 0
                        
                        st.metric("Total Target Devices", total_devices)
                        st.metric("Successfully Installed", installed_devices)
                        st.metric("Deployment Rate", f"{deployment_rate:.1f}%")

                    # Installation Status Breakdown
                    st.subheader("Installation Status")
                    install_status = []
                    for device in results:
                        for app in device['installedApplications']:
                            if (app_id and app['id'] == app_id) or (app_name and app_name.lower() in app['name'].lower()):
                                install_status.append({
                                    'Device': device['deviceName'],
                                    'Status': app['installState'],
                                    'User': device['userDisplayName'],
                                    'Primary User Email': device['userPrincipalName'],
                                    'Department': device['department'],
                                    'OS Version': device['osVersion'],
                                    'Windows Version': device['osDescription'],
                                    'Application Name': app['displayName'],
                                    'Application Version': app['version']
                                })
                    
                    df_status = pd.DataFrame(install_status)
                    # Ändra ordningen på kolumnerna för bättre läsbarhet
                    columns_order = [
                        'Device',
                        'Status',
                        'User',
                        'Primary User Email',
                        'Department',
                        'OS Version',
                        'Windows Version',
                        'Application Name',
                        'Application Version'
                    ]
                    df_status = df_status[columns_order]
                    col_stat1, col_stat2 = st.columns(2)
                    
                    with col_stat1:
                        status_counts = df_status['Status'].value_counts()
                        fig_status = px.pie(values=status_counts.values, 
                                          names=status_counts.index, 
                                          title='Installation Status Distribution')
                        st.plotly_chart(fig_status, use_container_width=True)
                    
                    with col_stat2:
                        dept_status = df_status.groupby('Department')['Status'].value_counts().unstack()
                        fig_dept = px.bar(dept_status, 
                                        title='Installation Status by Department',
                                        labels={'value': 'Number of Devices', 'Department': 'Department'})
                        st.plotly_chart(fig_dept, use_container_width=True)

                    # Detaljerad installationstabell
                    st.subheader("Detailed Installation Status")
                    st.dataframe(df_status)

                    # Lägg till knapp för rapportgenerering
                    st.subheader("Generate Report")
                    if st.button("Generate Application Deployment Report"):
                        try:
                            params = {}
                            if app_id:
                                params['app_id'] = app_id
                            if app_name:
                                params['app_name'] = app_name
                                
                            response = requests.get("http://localhost:8000/api/generate-report", params=params)
                            if response.status_code == 200:
                                st.success("New report generated successfully!")
                                # Hämta nedladdningslänk
                                download_response = requests.get("http://localhost:8000/api/download-report")
                                if download_response.status_code == 200:
                                    # Skapa nedladdningslänk
                                    content = download_response.content
                                    st.download_button(
                                        label="Download Excel Report",
                                        data=content,
                                        file_name=f"app_deployment_report_{app_id or app_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                    )
                            else:
                                st.error(f"Could not generate report: {response.text}")
                        except Exception as e:
                            st.error(f"Error generating report: {str(e)}")

                else:
                    st.warning("No devices found with the specified application")
            else:
                st.error("Failed to fetch deployment status")
        else:
            st.error("Failed to fetch deployment status")
    except Exception as e:
        st.error(f"Error analyzing deployment: {str(e)}") 