DELETE FROM activities
WHERE id
IN (
    %(ids)s
)