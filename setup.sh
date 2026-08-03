mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor = '#1B4F8C'\n\
backgroundColor = '#F5F7FA'\n\
secondaryBackgroundColor = '#DCE3EC'\n\
textColor = '#14213D'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml
