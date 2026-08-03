mkdir -p ~/.streamlit/

cat > ~/.streamlit/config.toml <<EOF
[server]
headless = true
port = $PORT
enableCORS = false
address = "0.0.0.0"

[theme]
primaryColor = "#1B4F8C"
backgroundColor = "#F5F7FA"
secondaryBackgroundColor = "#DCE3EC"
textColor = "#14213D"
font = "sans serif"
EOF