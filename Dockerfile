FROM ubuntu:19.10
COPY ./dist/main /root/main
VOLUME ["/root/mathchat"]
EXPOSE 5000
EXPOSE 5277
CMD ["/root/main"]
