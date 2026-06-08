*&---------------------------------------------------------------------*
*& Report Z_PO_EXCEPTION_REPORT
*& SAP Business Object: Purchase Order
*& Purpose: Identify blocked or exception-heavy purchase orders before go-live.
*&---------------------------------------------------------------------*
REPORT z_po_exception_report.

SELECTION-SCREEN BEGIN OF BLOCK b1 WITH FRAME TITLE TEXT-001.
PARAMETERS: p_bukrs TYPE string DEFAULT '1000',
            p_werks TYPE string DEFAULT 'PL01',
            p_block AS CHECKBOX DEFAULT 'X'.
SELECTION-SCREEN END OF BLOCK b1.

TYPES: BEGIN OF ty_po,
         ebeln      TYPE string,
         lifnr      TYPE string,
         werks      TYPE string,
         status     TYPE string,
         net_value  TYPE i,
         exception  TYPE string,
       END OF ty_po.

DATA: lt_po TYPE STANDARD TABLE OF ty_po,
      ls_po TYPE ty_po.

START-OF-SELECTION.

  APPEND VALUE ty_po( ebeln = '4500001001' lifnr = 'VEND-ACME'   werks = 'PL01' status = 'APPROVED' net_value = 12000 exception = '' ) TO lt_po.
  APPEND VALUE ty_po( ebeln = '4500001002' lifnr = 'VEND-NOVA'   werks = 'PL01' status = 'BLOCKED'  net_value = 8800  exception = 'MISSING_VENDOR_MASTER' ) TO lt_po.
  APPEND VALUE ty_po( ebeln = '4500001003' lifnr = 'VEND-VERTEX' werks = 'PL01' status = 'BLOCKED'  net_value = 15400 exception = 'SHIPMENT_DELAY' ) TO lt_po.

  WRITE: / 'Purchase Order Exception Report'.
  WRITE: / 'Company Code:', p_bukrs, 'Plant:', p_werks.
  ULINE.

  LOOP AT lt_po INTO ls_po WHERE werks = p_werks.
    IF p_block = 'X' AND ls_po-status <> 'BLOCKED'.
      CONTINUE.
    ENDIF.

    IF ls_po-exception IS NOT INITIAL.
      WRITE: / 'BLOCK:', ls_po-ebeln, ls_po-lifnr, ls_po-exception, ls_po-net_value.
    ELSE.
      WRITE: / 'READY:', ls_po-ebeln, ls_po-lifnr, ls_po-net_value.
    ENDIF.
  ENDLOOP.
