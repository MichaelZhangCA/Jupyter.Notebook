SELECT ema.symbol, ema.effective_date, ema.ema20, atr.atr14, 
	ema.ema20 + atr.atr14 AS atr1_upper, ema.ema20 - atr.atr14 AS atr1_lower,
	ema.ema20 + atr.atr14 *2 AS atr2_upper, ema.ema20 - atr.atr14 *2 AS atr2_lower,
	ema.ema20 + atr.atr14 *3 AS atr3_upper, ema.ema20 - atr.atr14 *3 AS atr3_lower
FROM
(SELECT symbol, effective_date, ema AS ema20 FROM `idc.ema` WHERE period = 20) ema
LEFT JOIN
(SELECT symbol, effective_date, atr AS atr14 FROM `idc.atr` WHERE period = 14) atr
ON atr.symbol = ema.symbol AND atr.effective_date = ema.effective_date