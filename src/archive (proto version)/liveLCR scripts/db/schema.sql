/*
Author: Austin Tabulog
last updated: 10/28/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

SQL schema file for LCR meter collected data.
*/

/*General table*/
DROP TABLE IF EXISTS general;
CREATE TABLE general(
  motorID INT,
  manufacturer CHAR(64),
  mass REAL
  PRIMARY KEY(motorID, manufacturer)
);


/*Parameter table for simple Zfit model (ONLY POPULATED FOR IMPEDANCE TESTS)*/
DROP TABLE IF EXISTS parameters;
CREATE TABLE parameters(
  testID CHAR(64) PRIMARY KEY,
  motorID INT,
  Cd REAL,
  Rd REAL,
  Lm REAL,
  Ro REAL,
  Cm REAL,
  resonantFrequency REAL,
  antiresonantFrequency REAL,
  K REAL,
  Q REAL
);


/*Test summary table */
DROP TABLE IF EXISTS testSummary;
CREATE TABLE testSummary(
  testID CHAR(64) PRIMARY KEY,
  motorID INT,
  channel CHAR(6),
  stage CHAR(6),
  description TEXT,
  primary CHAR(6),
  secondary CHAR(6),
  level REAL,
  start REAL,
  step REAL,
  dwell REAL
);


/*Measurement table*/
DROP TABLE IF EXISTS testData;
CREATE TABLE testData(
  testID CHAR(64),
  motorID INT,
  frequency REAL,
  primary REAL,
  secondary REAL
  PRIMARY KEY(testID, frequency)
);
