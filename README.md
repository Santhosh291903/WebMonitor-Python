# WebMonitor-Python


This Python project monitors website uptime and SSL certificate expiry.  
It sends real-time alerts to Google Chat if a website is down or its SSL certificate is about to expire.  
At the end of the day, it emails a report summarizing downtime events.  

## Features  

✅ Checks if websites are up or down.  
✅ Sends alerts to Google Chat for downtime.  
✅ Monitors SSL certificate expiry (alerts if less than 15 days).  
✅ Sends a daily email report with downtime details.  


Monitor Websites
Run the monitor.py script to check website status:
python monitor.py

Send Daily Report

Run report.py to send the end-of-day email:
python report.py


Configuration

Websites to Monitor: Update the URLS list in monitor.py.
Google Chat Webhook: Replace <WEBHOOK_URL> with your actual webhook.
Email Configuration: Modify EMAIL_USER and TO_EMAILS in report.py.
