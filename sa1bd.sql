-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 24, 2024 at 01:32 AM
-- Server version: 11.3.2-MariaDB-1:11.3.2+maria~deb12
-- PHP Version: 8.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sa1bd`
--

-- --------------------------------------------------------

--
-- Table structure for table `cliente`
--

CREATE TABLE `cliente` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `cliente`
--

INSERT INTO `cliente` (`id`, `nombre`, `estado`) VALUES
(1, 'Herber Roman Alvarado', 1),
(4, 'Jairo Vargas', 1),
(5, 'Eddy Caceres', 1),
(6, 'Carlos O.', 1),
(7, 'Jose Salasar', 1);

-- --------------------------------------------------------

--
-- Table structure for table `cuotaestado`
--

CREATE TABLE `cuotaestado` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `cuotaestado`
--

INSERT INTO `cuotaestado` (`id`, `descripcion`) VALUES
(1, 'aplicado'),
(2, 'pendiente');

-- --------------------------------------------------------

--
-- Table structure for table `cuotas`
--

CREATE TABLE `cuotas` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_prestamo` int(11) NOT NULL,
  `cuota` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `monto_cuota` double NOT NULL,
  `estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `estadocliente`
--

CREATE TABLE `estadocliente` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `estadocliente`
--

INSERT INTO `estadocliente` (`id`, `descripcion`) VALUES
(1, 'activo'),
(2, 'inactivo');

-- --------------------------------------------------------

--
-- Table structure for table `estadoprestamo`
--

CREATE TABLE `estadoprestamo` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `estadoprestamo`
--

INSERT INTO `estadoprestamo` (`id`, `descripcion`) VALUES
(1, 'activo'),
(2, 'cancelado');

-- --------------------------------------------------------

--
-- Table structure for table `prestamos`
--

CREATE TABLE `prestamos` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `monto_prestamo` int(11) NOT NULL,
  `cuotas` int(11) NOT NULL DEFAULT 6,
  `monto_cuota` double NOT NULL,
  `saldo_pendiente` double NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reversion`
--

CREATE TABLE `reversion` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `id_prestamo` int(11) NOT NULL,
  `id_cuota` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usuairo`
--

CREATE TABLE `usuairo` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `cod_usuario` varchar(20) NOT NULL,
  `clave` varchar(12) NOT NULL,
  `estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Estado` (`estado`) USING BTREE;

--
-- Indexes for table `cuotaestado`
--
ALTER TABLE `cuotaestado`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cuotas`
--
ALTER TABLE `cuotas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Estado` (`estado`),
  ADD KEY `IdPrestamo` (`id_prestamo`),
  ADD KEY `IdCliente` (`id_cliente`,`id_prestamo`,`estado`) USING BTREE;

--
-- Indexes for table `estadocliente`
--
ALTER TABLE `estadocliente`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `estadoprestamo`
--
ALTER TABLE `estadoprestamo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prestamos`
--
ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Estado` (`estado`) USING BTREE,
  ADD KEY `IdCliente` (`id_cliente`) USING BTREE;

--
-- Indexes for table `reversion`
--
ALTER TABLE `reversion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `IdCuota` (`id_cuota`),
  ADD KEY `Idprestamo` (`id_prestamo`,`id_cuota`) USING BTREE;

--
-- Indexes for table `usuairo`
--
ALTER TABLE `usuairo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `idCliente` (`id_cliente`),
  ADD KEY `Estado` (`estado`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `cuotaestado`
--
ALTER TABLE `cuotaestado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `cuotas`
--
ALTER TABLE `cuotas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `estadocliente`
--
ALTER TABLE `estadocliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `estadoprestamo`
--
ALTER TABLE `estadoprestamo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `prestamos`
--
ALTER TABLE `prestamos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reversion`
--
ALTER TABLE `reversion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usuairo`
--
ALTER TABLE `usuairo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`estado`) REFERENCES `estadocliente` (`id`);

--
-- Constraints for table `cuotas`
--
ALTER TABLE `cuotas`
  ADD CONSTRAINT `cuotas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `cuotas_ibfk_3` FOREIGN KEY (`estado`) REFERENCES `cuotaestado` (`id`),
  ADD CONSTRAINT `cuotas_ibfk_4` FOREIGN KEY (`id_prestamo`) REFERENCES `prestamos` (`id`);

--
-- Constraints for table `prestamos`
--
ALTER TABLE `prestamos`
  ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `prestamos_ibfk_3` FOREIGN KEY (`estado`) REFERENCES `estadoprestamo` (`id`);

--
-- Constraints for table `reversion`
--
ALTER TABLE `reversion`
  ADD CONSTRAINT `reversion_ibfk_1` FOREIGN KEY (`id_prestamo`) REFERENCES `prestamos` (`id`),
  ADD CONSTRAINT `reversion_ibfk_2` FOREIGN KEY (`id_cuota`) REFERENCES `cuotas` (`id`);

--
-- Constraints for table `usuairo`
--
ALTER TABLE `usuairo`
  ADD CONSTRAINT `usuairo_ibfk_1` FOREIGN KEY (`estado`) REFERENCES `estadocliente` (`id`),
  ADD CONSTRAINT `usuairo_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
