mkdir -p ~/.streamlit

echo "SETUP RAN" >&2

cat > ~/.streamlit/config.toml <<EOF
[server]
headless = true
port = $PORT
address = "0.0.0.0"
enableCORS = false
EOF

echo "CONFIG CREATED" >&2
cat ~/.streamlit/config.toml >&2