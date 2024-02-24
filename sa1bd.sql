-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 24, 2024 at 01:44 AM
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
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`id`, `nombre`, `estado`) VALUES
(1, 'Herber Roman Alvarado', 1),
(2, 'Jairo Vargas', 1),
(3, 'Eddy Caceres', 1),
(4, 'Carlos O.', 1),
(5, 'Jose Salasar', 1);

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
-- Table structure for table `estados_cliente`
--

CREATE TABLE `estados_cliente` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `estados_cliente`
--

INSERT INTO `estados_cliente` (`id`, `descripcion`) VALUES
(1, 'activo'),
(2, 'inactivo');

-- --------------------------------------------------------

--
-- Table structure for table `estados_cuota`
--

CREATE TABLE `estados_cuota` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `estados_cuota`
--

INSERT INTO `estados_cuota` (`id`, `descripcion`) VALUES
(1, 'aplicado'),
(2, 'pendiente');

-- --------------------------------------------------------

--
-- Table structure for table `estados_prestamo`
--

CREATE TABLE `estados_prestamo` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `estados_prestamo`
--

INSERT INTO `estados_prestamo` (`id`, `descripcion`) VALUES
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
-- Table structure for table `usuairos`
--

CREATE TABLE `usuairos` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `cod_usuario` varchar(20) NOT NULL,
  `clave` varchar(12) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `usuairos`
--

INSERT INTO `usuairos` (`id`, `id_cliente`, `cod_usuario`, `clave`, `estado`) VALUES
(1, 1, 'herbera', '123', 1),
(2, 2, 'jairov', '123', 1),
(3, 3, 'eddyc', '123', 1),
(4, 4, 'carloso', '123', 1),
(5, 5, 'joses', '123', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Estado` (`estado`) USING BTREE;

--
-- Indexes for table `cuotas`
--
ALTER TABLE `cuotas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Estado` (`estado`),
  ADD KEY `IdPrestamo` (`id_prestamo`),
  ADD KEY `IdCliente` (`id_cliente`,`id_prestamo`,`estado`) USING BTREE;

--
-- Indexes for table `estados_cliente`
--
ALTER TABLE `estados_cliente`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `estados_cuota`
--
ALTER TABLE `estados_cuota`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `estados_prestamo`
--
ALTER TABLE `estados_prestamo`
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
-- Indexes for table `usuairos`
--
ALTER TABLE `usuairos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `idCliente` (`id_cliente`),
  ADD UNIQUE KEY `cod_usuario` (`cod_usuario`),
  ADD KEY `Estado` (`estado`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `cuotas`
--
ALTER TABLE `cuotas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `estados_cliente`
--
ALTER TABLE `estados_cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `estados_cuota`
--
ALTER TABLE `estados_cuota`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `estados_prestamo`
--
ALTER TABLE `estados_prestamo`
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
-- AUTO_INCREMENT for table `usuairos`
--
ALTER TABLE `usuairos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`estado`) REFERENCES `estados_cliente` (`id`);

--
-- Constraints for table `cuotas`
--
ALTER TABLE `cuotas`
  ADD CONSTRAINT `cuotas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `cuotas_ibfk_3` FOREIGN KEY (`estado`) REFERENCES `estados_cuota` (`id`),
  ADD CONSTRAINT `cuotas_ibfk_4` FOREIGN KEY (`id_prestamo`) REFERENCES `prestamos` (`id`);

--
-- Constraints for table `prestamos`
--
ALTER TABLE `prestamos`
  ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `prestamos_ibfk_3` FOREIGN KEY (`estado`) REFERENCES `estados_prestamo` (`id`);

--
-- Constraints for table `reversion`
--
ALTER TABLE `reversion`
  ADD CONSTRAINT `reversion_ibfk_1` FOREIGN KEY (`id_prestamo`) REFERENCES `prestamos` (`id`),
  ADD CONSTRAINT `reversion_ibfk_2` FOREIGN KEY (`id_cuota`) REFERENCES `cuotas` (`id`);

--
-- Constraints for table `usuairos`
--
ALTER TABLE `usuairos`
  ADD CONSTRAINT `usuairos_ibfk_1` FOREIGN KEY (`estado`) REFERENCES `estados_cliente` (`id`),
  ADD CONSTRAINT `usuairos_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
