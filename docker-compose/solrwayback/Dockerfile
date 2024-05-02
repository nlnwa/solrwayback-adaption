FROM ghcr.io/nlnwa/solrwayback:main

COPY solrwayback.properties solrwaybackweb.properties /root/

# Uncomment below to install google-chrome-stable to expirement with page preview functionality.
#
# RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/trusted.gpg.d/google.asc >/dev/null \
#     && echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/google.asc] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
#     && apt-get update && apt-get -y install google-chrome-stable \
#     && rm -rf /var/lib/apt/lists/*
