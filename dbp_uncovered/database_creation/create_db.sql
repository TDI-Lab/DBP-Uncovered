-- Create the database if it not already exists
CREATE DATABASE IF NOT EXISTS t_dbp;

USE t_dbp;

-- Create tables

-- 1. Users table
CREATE TABLE IF NOT EXISTS users (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  username       VARCHAR(100)    NOT NULL UNIQUE,
  password_hash  VARCHAR(255)    NOT NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Answers table
CREATE TABLE IF NOT EXISTS answers (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  user_id        INT             ,
  q1             VARCHAR(20),
  q2             VARCHAR(20),
  q3             VARCHAR(20),
  q4             VARCHAR(20),
  q5             VARCHAR(20),
  q6             VARCHAR(20),
  q7             VARCHAR(20),
  q8             VARCHAR(20),
  q9             VARCHAR(20),
  q10            VARCHAR(20),
  q11            VARCHAR(20),
  q12            VARCHAR(20),
  q13            VARCHAR(20),
  q14            VARCHAR(20),
  q15            VARCHAR(20),
  q16            VARCHAR(20),
  ti 			 VARCHAR(20),
  cost 			 VARCHAR(20),
  freq 			 VARCHAR(20),
  effc 			 VARCHAR(20),
  answered_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);