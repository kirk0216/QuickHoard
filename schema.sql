-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema qh
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema qh
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `qh` DEFAULT CHARACTER SET utf8 ;
USE `qh` ;

-- -----------------------------------------------------
-- Table `qh`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qh`.`user` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Email` VARCHAR(50) NOT NULL,
  `Password` VARCHAR(102) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `qh`.`budget`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qh`.`budget` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(50) NOT NULL,
  `User_Id` INT NOT NULL,
  PRIMARY KEY (`Id`),
  INDEX `fk_Budget_User_idx` (`User_Id` ASC) VISIBLE,
  CONSTRAINT `fk_Budget_User`
    FOREIGN KEY (`User_Id`)
    REFERENCES `qh`.`user` (`Id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `qh`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qh`.`category` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(50) NOT NULL,
  `Goal` DECIMAL(10,2) NOT NULL,
  `Budget_Id` INT NOT NULL,
  PRIMARY KEY (`Id`),
  INDEX `fk_Category_Budget1_idx` (`Budget_Id` ASC) VISIBLE,
  CONSTRAINT `fk_Category_Budget1`
    FOREIGN KEY (`Budget_Id`)
    REFERENCES `qh`.`budget` (`Id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `qh`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qh`.`transaction` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Recipient` VARCHAR(45) NOT NULL,
  `Date` DATE NOT NULL,
  `Amount` DECIMAL(10,2) NOT NULL,
  `Category_Id` INT NOT NULL,
  PRIMARY KEY (`Id`),
  INDEX `fk_Transaction_Category1_idx` (`Category_Id` ASC) VISIBLE,
  CONSTRAINT `fk_Transaction_Category1`
    FOREIGN KEY (`Category_Id`)
    REFERENCES `qh`.`category` (`Id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
