*&---------------------------------------------------------------------*
*& Report Z_VENDOR_MASTER_VALIDATION
*& SAP Business Object: Vendor Master
*& Purpose: Validate supplier master data before procurement workflow release.
*&---------------------------------------------------------------------*
REPORT z_vendor_master_validation.

SELECTION-SCREEN BEGIN OF BLOCK b1 WITH FRAME TITLE TEXT-001.
PARAMETERS: p_lifnr TYPE string DEFAULT '*',
            p_onlye AS CHECKBOX DEFAULT 'X'.
SELECTION-SCREEN END OF BLOCK b1.

TYPES: BEGIN OF ty_vendor,
         lifnr        TYPE string,
         name1        TYPE string,
         payment_term TYPE string,
         tax_id       TYPE string,
         active       TYPE string,
         exception    TYPE string,
       END OF ty_vendor.

DATA: lt_vendor TYPE STANDARD TABLE OF ty_vendor,
      ls_vendor TYPE ty_vendor.

START-OF-SELECTION.

  APPEND VALUE ty_vendor( lifnr = 'VEND-ACME'   name1 = 'Acme Components' payment_term = 'NET30' tax_id = 'TX-1001' active = 'X' exception = '' ) TO lt_vendor.
  APPEND VALUE ty_vendor( lifnr = 'VEND-NOVA'   name1 = 'Nova Parts'      payment_term = ''      tax_id = 'TX-1002' active = 'X' exception = 'MISSING_PAYMENT_TERM' ) TO lt_vendor.
  APPEND VALUE ty_vendor( lifnr = 'VEND-VERTEX' name1 = 'Vertex Supply'   payment_term = 'NET45' tax_id = ''        active = 'X' exception = 'MISSING_TAX_ID' ) TO lt_vendor.

  WRITE: / 'Vendor Master Validation Report'.
  ULINE.

  LOOP AT lt_vendor INTO ls_vendor.
    IF p_onlye = 'X' AND ls_vendor-exception IS INITIAL.
      CONTINUE.
    ENDIF.

    IF ls_vendor-payment_term IS INITIAL OR ls_vendor-tax_id IS INITIAL.
      WRITE: / 'BLOCK:', ls_vendor-lifnr, ls_vendor-name1, ls_vendor-exception.
    ELSE.
      WRITE: / 'VALID:', ls_vendor-lifnr, ls_vendor-name1.
    ENDIF.
  ENDLOOP.
