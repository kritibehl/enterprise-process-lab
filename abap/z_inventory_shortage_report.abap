*&---------------------------------------------------------------------*
*& Report Z_INVENTORY_SHORTAGE_REPORT
*& SAP Business Object: Inventory Item / Material Stock
*& Purpose: Detect stock shortages that should block implementation readiness.
*&---------------------------------------------------------------------*
REPORT z_inventory_shortage_report.

SELECTION-SCREEN BEGIN OF BLOCK b1 WITH FRAME TITLE TEXT-001.
PARAMETERS: p_werks TYPE string DEFAULT 'PL01',
            p_min   TYPE i DEFAULT 100.
SELECTION-SCREEN END OF BLOCK b1.

TYPES: BEGIN OF ty_stock,
         matnr       TYPE string,
         werks       TYPE string,
         available   TYPE i,
         required    TYPE i,
         exception   TYPE string,
       END OF ty_stock.

DATA: lt_stock TYPE STANDARD TABLE OF ty_stock,
      ls_stock TYPE ty_stock.

START-OF-SELECTION.

  APPEND VALUE ty_stock( matnr = 'MAT-CPU-001' werks = 'PL01' available = 500 required = 250 exception = '' ) TO lt_stock.
  APPEND VALUE ty_stock( matnr = 'MAT-SSD-002' werks = 'PL01' available = 40  required = 140 exception = 'SHORTAGE' ) TO lt_stock.
  APPEND VALUE ty_stock( matnr = 'MAT-NIC-003' werks = 'PL01' available = 75  required = 200 exception = 'SHORTAGE' ) TO lt_stock.

  WRITE: / 'Inventory Shortage Readiness Report'.
  WRITE: / 'Plant:', p_werks, 'Minimum threshold:', p_min.
  ULINE.

  LOOP AT lt_stock INTO ls_stock WHERE werks = p_werks.
    IF ls_stock-available < ls_stock-required OR ls_stock-available < p_min.
      WRITE: / 'BLOCK:', ls_stock-matnr, 'Available:', ls_stock-available, 'Required:', ls_stock-required.
    ELSE.
      WRITE: / 'READY:', ls_stock-matnr, 'Available:', ls_stock-available.
    ENDIF.
  ENDLOOP.
