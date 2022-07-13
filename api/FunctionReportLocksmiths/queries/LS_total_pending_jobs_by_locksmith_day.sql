------------- Today's pending jobs by locksmiths 
SELECT
SB.LocksmithName AS "Locksmith",
COUNT(*) AS "Pending jobs"
FROM 
(
SELECT
DISTINCT(LD.ReportID),
LS.LocksmithName,
PF.NetCost
FROM [dbo].[Policy_LocksmithDetails] LD
LEFT JOIN [dbo].[Lookup_Locksmiths] LS
ON LD.LocksmithID = LS.ID
LEFT JOIN [dbo].[Policy_Financial] PF
ON LD.ReportID = PF.ReportID
WHERE LD.Selected = 1
AND LS.LocksmithName LIKE ('WGTK%')
AND LD.ReportID IN (
	SELECT
	DISTINCT(PD.ReportID)
	FROM
	[dbo].[Policy_Diary] PD
	LEFT JOIN [dbo].[Policy_Details] DE
	ON PD.ReportID = DE.ReportID
	WHERE PD.Active = 1
	AND DE.StatusID <> 15
)
AND CAST(LD.AvailableFromDate AS DATE) = CAST(GETDATE() AS DATE)
) AS SB
WHERE SB.NetCost IS NULL
GROUP BY SB.LocksmithName
ORDER BY COUNT(*) DESC