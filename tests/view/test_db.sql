-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema qhtest
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `qhtest`;
CREATE SCHEMA IF NOT EXISTS `qhtest` DEFAULT CHARACTER SET utf8 ;
USE `qhtest` ;

-- -----------------------------------------------------
-- Table `qhtest`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qhtest`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(102) NOT NULL,
  `failed_login` INT NOT NULL DEFAULT 0,
  `last_login` DATETIME,
  `reset_code` VARCHAR(45),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `Email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `qhtest`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qhtest`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_category_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_category_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `qhtest`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `qhtest`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qhtest`.`transaction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `recipient` VARCHAR(45) NOT NULL,
  `date` DATE NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Transaction_Category1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_Transaction_Category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `qhtest`.`category` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `qhtest`.`category_goal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qhtest`.`category_goal` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `goal` DECIMAL(10,2) NOT NULL,
  `year` INT NOT NULL,
  `month` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_table1_category1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_table1_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `qhtest`.`category` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
