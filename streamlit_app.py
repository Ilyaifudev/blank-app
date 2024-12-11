import streamlit as st

# Predefined solutions for common issues
TROUBLESHOOTING_GUIDE = {
    "slow computer": "Your computer might be slow due to background apps or insufficient resources. Try restarting your computer, closing unused programs, or upgrading RAM if possible.",
    "internet not working": "Check if your router is powered on. Restart the router, check for loose cables, and verify your Wi-Fi or Ethernet connection.",
    "software not installing": "Ensure you have enough disk space and administrator privileges. Check if the software is compatible with your OS version.",
    "blue screen of death": "This could be due to hardware issues or corrupted drivers. Try booting into safe mode and updating your drivers or running diagnostics.",
    "printer not working": "Ensure the printer is powered on and connected. Check if drivers are installed correctly and restart the printer and your computer.",
    "overheating": "Make sure your computer's fans are working and not clogged with dust. Place the computer in a well-ventilated area and consider using a cooling pad.",
    "keyboard not responding": "Check the connection (wired or wireless). Try plugging it into another port or restarting the computer.",
    "unable to boot": "Check if the power supply is working. Disconnect external devices and boot into safe mode to diagnose further.",
    "sound not working": "Check if the speakers are connected and powered. Verify the audio output settings on your computer.",
    "file not opening": "Ensure the file format is supported by the application you're using. If the file is corrupted, try using a repair tool.",
}

# Streamlit App
st.title("TekSupport 9000")
st.write("Hello! I'm your helpdesk. I can help troubleshoot common computer issues. How can I assist you today?")

# User Input
user_query = st.text_input("Describe your issue:", "")

# Process the user query
if user_query:
    user_query_lower = user_query.lower()
    response_found = False

    for issue, solution in TROUBLESHOOTING_GUIDE.items():
        if issue in user_query_lower:
            st.write(f"**Issue:** {issue.capitalize()}")
            st.write(f"**Solution:** {solution}")
            response_found = True
            break

    if not response_found:
        st.write("I'm sorry, I don't have a solution for that issue. Please provide more details or contact IT support.")

# Example Quick Queries
st.write("#### Common Issues You Can Ask About:")
for issue in TROUBLESHOOTING_GUIDE.keys():
    st.write(f"- {issue.capitalize()}")
