#!/usr/bin/env bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
docker exec -it postgres bash
psql --user=postgres
"CREATE DATABASE perfeval"
