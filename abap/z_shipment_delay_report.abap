*&---------------------------------------------------------------------*
*& Report Z_SHIPMENT_DELAY_REPORT
*& SAP Business Object: Shipment Event / Logistics Execution
*& Purpose: Identify delayed shipment events and SLA risk before go-live.
*&---------------------------------------------------------------------*
REPORT z_shipment_delay_report.

SELECTION-SCREEN BEGIN OF BLOCK b1 WITH FRAME TITLE TEXT-001.
PARAMETERS: p_route TYPE string DEFAULT 'US-EAST',
            p_sla   TYPE i DEFAULT 3.
SELECTION-SCREEN END OF BLOCK b1.

TYPES: BEGIN OF ty_ship,
         tknum       TYPE string,
         ebeln       TYPE string,
         route       TYPE string,
         carrier     TYPE string,
         delay_days  TYPE i,
         status      TYPE string,
         exception   TYPE string,
       END OF ty_ship.

DATA: lt_ship TYPE STANDARD TABLE OF ty_ship,
      ls_ship TYPE ty_ship.

START-OF-SELECTION.

  APPEND VALUE ty_ship( tknum = 'SHIP-1001' ebeln = '4500001001' route = 'US-EAST' carrier = 'DHL' delay_days = 0 status = 'DELIVERED' exception = '' ) TO lt_ship.
  APPEND VALUE ty_ship( tknum = 'SHIP-1002' ebeln = '4500001002' route = 'US-EAST' carrier = 'UPS' delay_days = 5 status = 'DELAYED' exception = 'SLA_BREACH' ) TO lt_ship.
  APPEND VALUE ty_ship( tknum = 'SHIP-1003' ebeln = '4500001003' route = 'US-EAST' carrier = 'FDX' delay_days = 4 status = 'DELAYED' exception = 'CARRIER_DELAY' ) TO lt_ship.

  WRITE: / 'Shipment Delay Exception Report'.
  WRITE: / 'Route:', p_route, 'SLA days:', p_sla.
  ULINE.

  LOOP AT lt_ship INTO ls_ship WHERE route = p_route.
    IF ls_ship-delay_days > p_sla.
      WRITE: / 'BLOCK:', ls_ship-tknum, ls_ship-ebeln, ls_ship-carrier, ls_ship-exception.
    ELSE.
      WRITE: / 'ON_TIME:', ls_ship-tknum, ls_ship-ebeln, ls_ship-carrier.
    ENDIF.
  ENDLOOP.
