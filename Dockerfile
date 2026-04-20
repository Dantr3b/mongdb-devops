FROM mongo:7.0-jammy

COPY docker-entrypoint-initdb.d/init-blog.js /docker-entrypoint-initdb.d/init-blog.js

RUN chmod 644 /docker-entrypoint-initdb.d/init-blog.js

USER mongodb

EXPOSE 27017