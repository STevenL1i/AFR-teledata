SELECT beginUnixTime, beginTime, packetFormat, gameMajorVersion, gameMinorVersion
FROM SessionList
WHERE beginTime < "DATETIME"
ORDER BY beginTime DESC
LIMIT queryNUM;