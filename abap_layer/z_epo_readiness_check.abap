*&---------------------------------------------------------------------*
*& Report Z_EPO_READINESS_CHECK
*&---------------------------------------------------------------------*
*& Enterprise Process Lab
*& SAP-style readiness validation for purchase orders, inventory,
*& vendors, shipments, and implementation go-live status.
*&---------------------------------------------------------------------*

REPORT z_epo_readiness_check.

TYPES: BEGIN OF ty_po_status,
         process_id       TYPE string,
         purchase_order   TYPE string,
         vendor_id        TYPE string,
         inventory_status TYPE string,
         shipment_status  TYPE string,
         approval_status  TYPE string,
         exception_type   TYPE string,
         readiness_status TYPE string,
       END OF ty_po_status.

DATA: lt_po_status TYPE STANDARD TABLE OF ty_po_status,
      ls_po_status TYPE ty_po_status.

START-OF-SELECTION.

  APPEND VALUE ty_po_status(
    process_id       = 'PRC-1001'
    purchase_order   = 'PO-9001'
    vendor_id        = 'VEND-ACME'
    inventory_status = 'AVAILABLE'
    shipment_status  = 'DELIVERED'
    approval_status  = 'APPROVED'
    exception_type   = ''
    readiness_status = 'READY'
  ) TO lt_po_status.

  APPEND VALUE ty_po_status(
    process_id       = 'PRC-1002'
    purchase_order   = 'PO-9002'
    vendor_id        = 'VEND-NOVA'
    inventory_status = 'LOW_STOCK'
    shipment_status  = 'DELAYED'
    approval_status  = 'BLOCKED'
    exception_type   = 'SHIPMENT_DELAY'
    readiness_status = 'BLOCKED'
  ) TO lt_po_status.

  APPEND VALUE ty_po_status(
    process_id       = 'PRC-1004'
    purchase_order   = 'PO-9004'
    vendor_id        = 'VEND-VERTEX'
    inventory_status = 'STOCKOUT'
    shipment_status  = 'PENDING'
    approval_status  = 'FAILED_VALIDATION'
    exception_type   = 'INVENTORY_MISMATCH'
    readiness_status = 'BLOCKED'
  ) TO lt_po_status.

  LOOP AT lt_po_status INTO ls_po_status.
    IF ls_po_status-readiness_status = 'BLOCKED'.
      WRITE: / 'BLOCK:', ls_po_status-process_id,
               ls_po_status-purchase_order,
               ls_po_status-exception_type.
    ELSE.
      WRITE: / 'READY:', ls_po_status-process_id,
               ls_po_status-purchase_order.
    ENDIF.
  ENDLOOP.
