
docker run -it ^
-v ./src:/knot-dns-web/src ^
-p 8080:80/tcp ^
-p 443:443/tcp ^
--name knot-dns-web knot-dns-web