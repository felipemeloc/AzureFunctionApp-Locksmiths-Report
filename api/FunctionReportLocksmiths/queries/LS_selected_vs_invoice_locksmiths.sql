------------- Cases when the selected locksmith is not the same as the invoice's locksmith
SELECT
CAST(LD.ReportID AS VARCHAR(20)) AS ReportID,
LS.LocksmithName,
PF.RecipientName,
PF.NetCost
FROM [dbo].[Policy_LocksmithDetails] LD
LEFT JOIN [dbo].[Lookup_Locksmiths] LS
ON LD.LocksmithID = LS.ID
LEFT JOIN [dbo].[Policy_Financial] PF
ON LD.ReportID = PF.ReportID
WHERE LD.Selected = 1
AND (PF.RecipientName LIKE ('WGTK%') OR LS.LocksmithName LIKE ('WGTK%'))
AND PF.RecipientName NOT LIKE ('WGTK Cancellation%')
AND LD.ReportID IN (
	SELECT
	DISTINCT(PD.ReportID)
	FROM
	[dbo].[Policy_Diary] PD
	WHERE PD.Active = 0
	AND CAST(PD.ClosedDate AS DATE) = CAST(GETDATE() AS DATE)
)
AND LS.LocksmithName <> PF.RecipientName
AND CAST(LD.AvailableFromDate AS DATE) = CAST(GETDATE() AS DATE)
ORDER BY PF.NetCost DESC