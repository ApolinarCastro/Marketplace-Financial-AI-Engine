# Paris DTE Matching Design

## Current State
- Paris has 96 DTE XML files in `01_Raw/PARIS/Facturacion/` (dteproveedor_*.xml)
- These are Chilean electronic tax documents with Folio, amounts, IVA, dates
- The DTE processing pipeline only works for ML marketplace:
  - `dte_indexer.py`: hardcoded to `01_Raw/ML/Facturacion/`
  - `xml_matcher.py`: matches DTEs to `meli_ledger_v1`
  - `surgical_xml_justifier.py`: validates folios against XML index
  - `marketplace_auditor.py`: checks for `cargo_sin_respaldo_legal` (unmatched folios)
- Paris transactions have `folio_xml` field populated from Excel's "número factura" column
- But no XML matching occurs for Paris, so tax validation is incomplete
- "Pendiente Tributaria" refers to pending tax reconciliation due to unmatched DTEs

## Problem
Extend the existing DTE pipeline to support Paris marketplace so that:
1. Paris DTE XMLs are indexed into `dte_truth_v1`
2. Paris transaction folios are matched against the XML index
3. Audit can validate Paris folio matches
4. Tax reconciliation is complete for Paris

## Proposed Solution (Option A - Recommended)

### Changes Required:

1. **Database Schema Update**
   ```sql
   -- Add marketplace column to dte_truth_v1
   ALTER TABLE dte_truth_v1 
   ADD COLUMN marketplace TEXT DEFAULT 'ML' NOT NULL;
   
   -- Create composite primary key (folio, marketplace)
   -- OR recreate table with proper PK (safer for production)
   ```

2. **DTEIndexer Enhancement**
   - Accept `marketplace` parameter in constructor
   - Determine raw directory based on marketplace:
     - ML: `01_Raw/ML/Facturacion/`
     - PARIS: `01_Raw/PARIS/Facturacion/`
   - Include `marketplace` in INSERT statements

3. **XML Matcher Enhancement**
   - Support multiple ledger tables (`meli_ledger_v1` and `paris_ledger_v1`)
   - Include marketplace in matching JOIN conditions
   - Handle Paris-specific date/amount variations if needed

4. **Surgical XML Justifier Enhancement**
   - Support Paris ledger table
   - Validate Paris folio formats if different from ML

5. **Audit Logic Enhancement**
   - Update folio validation JOIN to include marketplace:
     ```sql
     LEFT JOIN dte_truth_v1 t ON l.folio_xml LIKE '%' || t.folio 
        AND l.marketplace = t.marketplace
     ```
   - Apply marketplace-specific filters if needed

### Benefits:
- Minimal changes to existing code
- Backward compatible (ML continues to work)
- Clear separation of concerns by marketplace
- Extensible to other marketplaces in future

### Estimated Effort: 2-3 hours

---

## Alternative Options

### Option B: Separate Tables
- Create `dte_truth_v1_paris` table
- Duplicate all DTE logic for Paris
- Pros: Complete isolation
- Cons: Code duplication, harder to maintain

### Option C: No Marketplace Column
- Store all DTEs in same table with composite folio (e.g., "PARIS-12345")
- Pros: No schema change
- Cons: Breaks existing ML assumptions, complex parsing

**Recommendation: Option A** - cleanest, most maintainable approach.

---

## Next Steps
If approved, I will:
1. Backup current database and code
2. Implement the schema change
3. Update DTEIndexer, XML Matcher, and Justifier
4. Test with Paris data
5. Run validation audit
6. Provide before/after metrics