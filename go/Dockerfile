FROM golang:1.22.3-alpine

EXPOSE 8080

WORKDIR /interrupting/go

COPY go.mod go.sum ./

RUN go mod download

COPY . .

CMD ["go", "run", "main.go"]
