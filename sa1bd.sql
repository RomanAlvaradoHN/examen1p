-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 29, 2024 at 04:06 AM
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

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`admin`@`%` PROCEDURE `ACTUALIZAR_SALDO` (IN `p_id_cliente` INT, IN `p_id_prestamo` INT)   BEGIN
    DECLARE mcuota DOUBLE;
    DECLARE sactual DOUBLE;
   
    SELECT MONTOCUOTA(p_id_cliente, p_id_prestamo) INTO mcuota;
    SELECT SALDOACTUAL(p_id_cliente, p_id_prestamo) INTO sactual;

    UPDATE prestamos SET saldo_pendiente = (sactual - mcuota)
    WHERE id_cliente = p_id_cliente AND id = p_id_prestamo;
      
END$$

CREATE DEFINER=`admin`@`%` PROCEDURE `PAGAR_SIGUIENTE_CUOTA` (IN `p_id_cliente` INT, IN `p_id_prestamo` INT)   BEGIN
    DECLARE ncuota INT;    
    SELECT SCUOTA(p_id_cliente, p_id_prestamo) INTO ncuota;

    UPDATE cuotas SET fecha = CURRENT_TIMESTAMP, estado = 1
    WHERE id_cliente = p_id_cliente AND id_prestamo = p_id_prestamo
    AND cuota = ncuota;      
END$$

CREATE DEFINER=`admin`@`%` PROCEDURE `PAGO_CUOTA_PRESTAMO` (IN `p_id_cliente` INT, IN `p_id_prestamo` INT)   BEGIN
    CALL PAGAR_SIGUIENTE_CUOTA(p_id_cliente, p_id_prestamo);
    CALL ACTUALIZAR_SALDO(p_id_cliente, p_id_prestamo);
END$$

--
-- Functions
--
CREATE DEFINER=`admin`@`%` FUNCTION `MONTOCUOTA` (`p_id_cliente` INT, `p_id_prestamo` INT) RETURNS DOUBLE(10,0)  BEGIN
    DECLARE ncuota INT;
    SET ncuota = UCPAGADA(p_id_cliente, p_id_prestamo);

RETURN (
    SELECT monto_cuota FROM cuotas WHERE
    id_cliente = p_id_cliente
    AND id_prestamo = p_id_prestamo
    AND cuota = ncuota
    AND estado = 1
);
END$$

CREATE DEFINER=`admin`@`%` FUNCTION `SALDOACTUAL` (`p_id_cliente` INT, `p_id_prestamo` INT) RETURNS DECIMAL(10,0)  BEGIN RETURN (
    SELECT saldo_pendiente FROM prestamos
    WHERE
    id_cliente = p_id_cliente
    AND id = p_id_prestamo
);
END$$

CREATE DEFINER=`admin`@`%` FUNCTION `SCUOTA` (`p_id_cliente` INT, `p_id_prestamo` INT) RETURNS INT(11)  BEGIN
RETURN (
    SELECT MIN(cuota) FROM cuotas WHERE
    id_cliente = p_id_cliente
    AND id_prestamo = p_id_prestamo
    AND estado = 2
);
END$$

CREATE DEFINER=`admin`@`%` FUNCTION `UCPAGADA` (`p_id_cliente` INT, `p_id_prestamo` INT) RETURNS INT(11)  BEGIN
RETURN (
    SELECT MAX(cuota) FROM cuotas WHERE
    id_cliente = p_id_cliente
    AND id_prestamo = p_id_prestamo
    AND estado = 1
);
END$$

DELIMITER ;

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
  `fecha` timestamp NULL DEFAULT NULL,
  `monto_cuota` double NOT NULL,
  `estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `cuotas`
--

INSERT INTO `cuotas` (`id`, `id_cliente`, `id_prestamo`, `cuota`, `fecha`, `monto_cuota`, `estado`) VALUES
(1, 1, 1, 1, NULL, 5000, 2),
(2, 1, 1, 2, NULL, 5000, 2),
(3, 1, 1, 3, NULL, 5000, 2),
(4, 1, 1, 4, NULL, 5000, 2),
(5, 1, 1, 5, NULL, 5000, 2),
(6, 1, 1, 6, NULL, 5000, 2),
(7, 2, 2, 2, NULL, 7000, 2),
(8, 2, 2, 3, NULL, 7000, 2),
(9, 2, 2, 4, NULL, 7000, 2),
(10, 2, 2, 5, NULL, 7000, 2),
(11, 2, 2, 6, NULL, 7000, 2),
(12, 3, 3, 1, NULL, 4166.67, 2),
(13, 3, 3, 2, NULL, 4166.67, 2),
(14, 3, 3, 3, NULL, 4166.67, 2),
(15, 3, 3, 4, NULL, 4166.67, 2),
(16, 3, 3, 5, NULL, 4166.67, 2),
(17, 3, 3, 6, NULL, 4166.67, 2),
(18, 2, 2, 1, NULL, 7000, 2),
(19, 4, 4, 1, NULL, 20000, 2),
(20, 4, 4, 2, NULL, 20000, 2),
(21, 4, 4, 3, NULL, 20000, 2),
(22, 4, 4, 4, NULL, 20000, 2),
(23, 4, 4, 5, NULL, 20000, 2),
(24, 4, 4, 6, NULL, 20000, 2),
(25, 5, 5, 1, NULL, 1000, 2),
(26, 5, 5, 2, NULL, 1000, 2),
(27, 5, 5, 3, NULL, 1000, 2),
(28, 5, 5, 4, NULL, 1000, 2),
(29, 5, 5, 5, NULL, 1000, 2),
(30, 5, 5, 6, NULL, 1000, 2),
(31, 2, 6, 1, NULL, 10000, 2),
(32, 2, 6, 2, NULL, 10000, 2),
(33, 2, 6, 3, NULL, 10000, 2),
(34, 2, 6, 4, NULL, 10000, 2),
(35, 2, 6, 5, NULL, 10000, 2),
(36, 2, 5, 6, NULL, 10000, 2);

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

--
-- Dumping data for table `prestamos`
--

INSERT INTO `prestamos` (`id`, `id_cliente`, `monto_prestamo`, `cuotas`, `monto_cuota`, `saldo_pendiente`, `estado`) VALUES
(1, 1, 30000, 6, 5000, 30000, 1),
(2, 2, 49000, 6, 7000, 49000, 1),
(3, 3, 25000, 6, 4166.67, 25000, 1),
(4, 4, 100000, 6, 20000, 100000, 1),
(5, 5, 6000, 6, 1000, 6000, 1),
(6, 2, 60000, 6, 10000, 60000, 1);

-- --------------------------------------------------------

--
-- Table structure for table `reversiones`
--

CREATE TABLE `reversiones` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_prestamo` int(11) NOT NULL,
  `id_cuota` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `cod_usuario` varchar(20) NOT NULL,
  `clave` varchar(12) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id`, `id_cliente`, `cod_usuario`, `clave`, `estado`) VALUES
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
-- Indexes for table `reversiones`
--
ALTER TABLE `reversiones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `IdCuota` (`id_cuota`),
  ADD KEY `Idprestamo` (`id_prestamo`,`id_cuota`) USING BTREE,
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reversiones`
--
ALTER TABLE `reversiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
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
-- Constraints for table `reversiones`
--
ALTER TABLE `reversiones`
  ADD CONSTRAINT `reversiones_ibfk_1` FOREIGN KEY (`id_prestamo`) REFERENCES `prestamos` (`id`),
  ADD CONSTRAINT `reversiones_ibfk_2` FOREIGN KEY (`id_cuota`) REFERENCES `cuotas` (`id`),
  ADD CONSTRAINT `reversiones_ibfk_3` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`);

--
-- Constraints for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`estado`) REFERENCES `estados_cliente` (`id`),
  ADD CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
