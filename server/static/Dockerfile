FROM nginx:latest
				COPY ./default.conf /etc/nginx/conf.d/default.conf
				RUN mkdir -p /var/www/static/
				COPY . /var/www/static/
				EXPOSE 80 443
				CMD ["nginx", "-g", "daemon off;"]
