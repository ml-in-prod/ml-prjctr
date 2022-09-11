FROM golang:1.16-alpine

WORKDIR /app

COPY go.mod ./
COPY *.go ./
RUN go build -o /server

RUN addgroup -S group && adduser -S user -G group
USER user

EXPOSE 8080

CMD [ "/server" ]