CREATE TABLE `offcputime` (
  `id` int(11) PRIMARY KEY,
  `hostname` varchar(256) NOT NULL,
  `time` datetime NOT NULL,
  `process` varchar(256) NOT NULL,
  `pid` int(11) NOT NULL,
  `stack` text NOT NULL,
  `elapsed` bigint(20) NOT NULL
);
