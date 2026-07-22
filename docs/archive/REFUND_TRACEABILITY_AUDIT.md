# DIRECTIVA DE AUDITORÃ A DE TRAZABILIDAD DE DEVOLUCIONES

## FASE 1: ExtracciÃ³n desde Archivos Fuente

### AgrupaciÃ³n por Motivo y Flujo
```
      flow                                                                    reason_id                            reason_detail  operation_type       operation_status  count  total_amount
chargeback                                                                           10                                      nan regular_payment  ppv_covered_melienvio      1      21990.00
chargeback                                                                          104                                      nan regular_payment  ppv_covered_melienvio      2      69980.00
chargeback                                                                         4837                    INVALID_AUTHORIZATION regular_payment  ppv_covered_melienvio      1      38990.00
chargeback                                                                         4837                                      nan regular_payment  ppv_covered_melienvio      1      19990.00
chargeback                                                                         4860                     CREDIT_NOT_PROCESSED regular_payment              ppv_valid      1      21990.00
chargeback                                                                         4860                                      nan regular_payment              ppv_valid      1      39990.00
     claim                                                                      PDD9502                          repentant_buyer regular_payment                    nan      1      17490.00
     claim                                                                      PDD9536           not_expected_quality_different regular_payment                    nan      1      17490.00
     claim                                                                      PDD9570        item_not_useful_fashion_different regular_payment                    nan      1      18990.00
     claim                                                                      PDD9829                        bought_by_mistake regular_payment                    nan      1      53990.00
     claim                                                                      PDD9925 item_not_useful_fashion_different_change regular_payment                    nan     98    3444831.00
     claim                                                                      PDD9926   different_color_or_size_fashion_change regular_payment                    nan     37    1296844.00
     claim                                                                      PDD9931              different_item_other_change regular_payment                    nan      1      19990.00
     claim                                                                      PDD9939                          repentant_buyer regular_payment                    nan    656   19035239.00
     claim                                                                      PDD9941                  different_color_or_size regular_payment                    nan      4     227960.00
     claim                                                                      PDD9942                     different_item_other regular_payment                    nan     17     583330.00
     claim                                                                      PDD9944                 different_than_published regular_payment                    nan     48    1489530.00
     claim                                                                      PDD9952                      missing_accessories regular_payment                    nan      3     108970.00
     claim                                                                      PDD9955                             missing_item regular_payment                    nan      7     130930.00
     claim                                                                      PDD9958                                empty_box regular_payment                    nan      3      48970.00
     claim                                                                      PDD9960                          missing_invoice regular_payment                    nan      4      78384.00
     claim                                                                      PDD9962             not_match_size_guide_fashion regular_payment                    nan     93    2924703.00
     claim                                                                      PDD9963          different_color_or_size_fashion regular_payment                    nan    190    5916894.00
     claim                                                                      PDD9965                      broken_item_fashion regular_payment                    nan    104    3269365.00
     claim                                                                      PDD9966      damaged_package_broken_item_fashion regular_payment                    nan      1      63990.00
     claim                                                                      PDD9976             bigger_than_expected_fashion regular_payment                    nan   1925   60415610.00
     claim                                                                      PDD9977            smaller_than_expected_fashion regular_payment                    nan   1705   47074382.00
     claim                                                                      PDD9978       dont_want_it_another_cause_fashion regular_payment                    nan    518   16060632.00
     claim                                                                      PNR9501              undelivered_repentant_buyer regular_payment                    nan    282    7581587.00
     claim                                                                      PNR9502                    respondent_unanswered regular_payment                    nan      6     112150.00
     claim                                                                      PNR9503                             out_of_stock regular_payment                    nan      5     194040.00
     claim                                                                      PNR9504           estimated_delivery_out_of_time regular_payment                    nan     55    1392216.00
     claim                                                                      PNR9505                  change_receiver_address regular_payment                    nan     20     474042.00
     claim                                                                      PNR9506                            buy_out_of_ml regular_payment                    nan      1      23990.00
     claim                                                                      PNR9507                    unauthorized_purchase regular_payment                    nan     14     475110.00
     claim                                                                      PNR9508                        undelivered_other regular_payment                    nan     95    2448460.00
     claim                                                                      PNR9509              undelivered_repentant_buyer regular_payment                    nan    130    3843423.00
     claim                                                                      PNR9510           estimated_delivery_out_of_time regular_payment                    nan     26     716006.00
     claim                                                                      PNR9511                  change_receiver_address regular_payment                    nan      6     231940.00
     claim                                                                      PNR9512                    unauthorized_purchase regular_payment                    nan      9     351810.00
     claim                                                                      PNR9513                        undelivered_other regular_payment                    nan     48    1879236.00
     claim                                                                      PNR9521                delivery_date_was_not_met regular_payment                    nan     13     254308.00
     claim                                                                      PNR9560        delivered_but_not_receive_package regular_payment                    nan     11     305900.00
     claim                                                                      PNR9567        delivered_but_not_receive_package regular_payment                    nan     19     480470.00
    refund                                     Abrigo 4 Botones Azul Eléctrico Nicopoly                                      nan regular_payment           bpp_refunded      3     199970.00
    refund                                     Abrigo 4 Botones Azul Eléctrico Nicopoly                                      nan regular_payment            compensated      1      59990.00
    refund                                     Abrigo 4 Botones Azul Eléctrico Nicopoly                                      nan regular_payment         not_reconciled      1      59990.00
    refund                                     Abrigo 4 Botones Azul Eléctrico Nicopoly                                      nan regular_payment             reconciled      3     199970.00
    refund                                             Abrigo 4 Botones Morado Nicopoly                                      nan regular_payment           bpp_refunded      3     187970.00
    refund                                             Abrigo 4 Botones Morado Nicopoly                                      nan regular_payment            compensated      2     143980.00
    refund                                             Abrigo 4 Botones Morado Nicopoly                                      nan regular_payment             reconciled      9     519910.00
    refund                                              Abrigo 4 Botones Negro Nicopoly                                      nan regular_payment           bpp_refunded      4     247960.00
    refund                                              Abrigo 4 Botones Negro Nicopoly                                      nan regular_payment             reconciled      2     111980.00
    refund                                               Abrigo 4 Botones Rojo Nicopoly                                      nan regular_payment           bpp_refunded      4     247960.00
    refund                                               Abrigo 4 Botones Rojo Nicopoly                                      nan regular_payment            compensated      2     111980.00
    refund                                               Abrigo 4 Botones Rojo Nicopoly                                      nan regular_payment         not_reconciled      1      55990.00
    refund                                               Abrigo 4 Botones Rojo Nicopoly                                      nan regular_payment             reconciled      3     191970.00
    refund                                              Abrigo 4 Botones Óxido Nicopoly                                      nan regular_payment           bpp_refunded      1      55990.00
    refund                                              Abrigo 4 Botones Óxido Nicopoly                                      nan regular_payment             reconciled      1      79990.00
    refund                                               Abrigo Bouclé Grafito Nicopoly                                      nan regular_payment           bpp_refunded      9     417084.00
    refund                                               Abrigo Bouclé Grafito Nicopoly                                      nan regular_payment                    nan      2      89980.00
    refund                                               Abrigo Bouclé Grafito Nicopoly                                      nan regular_payment             reconciled      6     217778.00
    refund                                                 Abrigo Bouclé Khaki Nicopoly                                      nan regular_payment            bpp_covered      1      44990.00
    refund                                                 Abrigo Bouclé Khaki Nicopoly                                      nan regular_payment           bpp_refunded      9     404910.00
    refund                                                 Abrigo Bouclé Khaki Nicopoly                                      nan regular_payment             reconciled      6     262940.00
    refund                                                 Abrigo Bouclé Negro Nicopoly                                      nan regular_payment           bpp_refunded     15     640850.00
    refund                                                 Abrigo Bouclé Negro Nicopoly                                      nan regular_payment            compensated      1      40000.00
    refund                                                 Abrigo Bouclé Negro Nicopoly                                      nan regular_payment                    nan      1      41990.00
    refund                                                 Abrigo Bouclé Negro Nicopoly                                      nan regular_payment             reconciled      7     305430.00
    refund                                       Abrigo Básico 2 Botones Negro Nicopoly                                      nan regular_payment           bpp_refunded     17     886450.00
    refund                                       Abrigo Básico 2 Botones Negro Nicopoly                                      nan regular_payment             reconciled      3     159970.00
    refund                              Abrigo Cierre Lateral Café Nicopoly Café M Liso                                      nan regular_payment           bpp_refunded      1      71990.00
    refund                              Abrigo Cierre Lateral Café Nicopoly Café S Liso                                      nan regular_payment             reconciled      1      79990.00
    refund                            Abrigo Cierre Lateral Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      79990.00
    refund                            Abrigo Cierre Lateral Negro Nicopoly Negro L Liso                                      nan regular_payment            compensated      1      51790.00
    refund                            Abrigo Cierre Lateral Oliva Nicopoly Oliva L Liso                                      nan regular_payment           bpp_refunded      1      79990.00
    refund                            Abrigo Cierre Lateral Oliva Nicopoly Oliva M Liso                                      nan regular_payment           bpp_refunded      1      51990.00
    refund                            Abrigo Cierre Lateral Oliva Nicopoly Oliva M Liso                                      nan regular_payment             reconciled      1      47990.00
    refund                           Abrigo Cierre Lateral Oliva Nicopoly Oliva Xl Liso                                      nan regular_payment           bpp_refunded      1      79990.00
    refund                           Abrigo Cierre Lateral Oliva Nicopoly Oliva Xl Liso                                      nan regular_payment             reconciled      1      47990.00
    refund                       Abrigo Cinturón Y Solapa Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment             reconciled      1      94990.00
    refund                     Abrigo Con Solapa Y Cinturón Beige Nicopoly Beige M Liso                                      nan regular_payment             reconciled      1     136990.00
    refund                                                  Abrigo Corto Beige Nicopoly                                      nan regular_payment           bpp_refunded      6     179184.00
    refund                                                  Abrigo Corto Beige Nicopoly                                      nan regular_payment             reconciled      9     272086.00
    refund                                                  Abrigo Corto Khaki Nicopoly                                      nan regular_payment           bpp_refunded     13     453530.00
    refund                                                  Abrigo Corto Khaki Nicopoly                                      nan regular_payment             reconciled      6     188445.00
    refund                                                  Abrigo Corto Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     258222.00
    refund                                                  Abrigo Corto Negro Nicopoly                                      nan regular_payment             reconciled      4     119600.00
    refund                                                  Abrigo Cotelé Café Nicopoly                                      nan regular_payment           bpp_refunded      2      71980.00
    refund                                                  Abrigo Cotelé Café Nicopoly                                      nan regular_payment             reconciled      1      35990.00
    refund                                               Abrigo Cotelé Celeste Nicopoly                                      nan regular_payment           bpp_refunded      3     111970.00
    refund                                              Abrigo Cuadrillé Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     450660.00
    refund                                              Abrigo Cuadrillé Negro Nicopoly                                      nan regular_payment            compensated      1      64990.00
    refund                                              Abrigo Cuadrillé Negro Nicopoly                                      nan regular_payment             reconciled      3     124970.00
    refund                     Abrigo Cuello Pelo Sintético Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      79990.00
    refund                                      Abrigo Forro Tipo Piel Grafito Nicopoly                                      nan regular_payment           bpp_refunded     10     524127.00
    refund                                      Abrigo Forro Tipo Piel Grafito Nicopoly                                      nan regular_payment             reconciled      3     191970.00
    refund                                      Abrigo Gorro Desmontable Beige Nicopoly                                      nan regular_payment           bpp_refunded      3     143970.00
    refund                                      Abrigo Gorro Desmontable Beige Nicopoly                                      nan regular_payment             reconciled      1      47990.00
    refund                                       Abrigo Gorro Desmontable Café Nicopoly                                      nan regular_payment           bpp_refunded      2     127980.00
    refund                                       Abrigo Gorro Desmontable Café Nicopoly                                      nan regular_payment             reconciled      3     157970.00
    refund                      Abrigo Hombros Caídos Blanco Invierno Invierno Nicopoly                                      nan regular_payment           bpp_refunded      5     167956.00
    refund                      Abrigo Hombros Caídos Blanco Invierno Invierno Nicopoly                                      nan regular_payment            compensated      1      27996.00
    refund                      Abrigo Hombros Caídos Blanco Invierno Invierno Nicopoly                                      nan regular_payment             reconciled      6     269946.00
    refund                                          Abrigo Hombros Caídos Gris Nicopoly                                      nan regular_payment           bpp_refunded      7     236936.00
    refund                                          Abrigo Hombros Caídos Gris Nicopoly                                      nan regular_payment             reconciled      3      74980.00
    refund                                          Abrigo Hombros Caídos Moca Nicopoly                                      nan regular_payment           bpp_refunded     14     341037.00
    refund                                          Abrigo Hombros Caídos Moca Nicopoly                                      nan regular_payment             reconciled     13     439853.00
    refund                                         Abrigo Hombros Caídos Negro Nicopoly                                      nan regular_payment           bpp_refunded     15     382476.00
    refund                                         Abrigo Hombros Caídos Negro Nicopoly                                      nan regular_payment                    nan      1      34990.00
    refund                                         Abrigo Hombros Caídos Negro Nicopoly                                      nan regular_payment             reconciled      8     250890.00
    refund                                         Abrigo Hombros Caídos Negro Nicopoly                                      nan regular_payment   refund_account_money      1      34990.00
    refund                                      Abrigo Interior Corderito Café Nicopoly                                      nan regular_payment           bpp_refunded     10     527900.00
    refund                                      Abrigo Interior Corderito Café Nicopoly                                      nan regular_payment            compensated      1      63990.00
    refund                                      Abrigo Interior Corderito Café Nicopoly                                      nan regular_payment             reconciled      8     408723.00
    refund                                             Abrigo Largo Lazo Camel Nicopoly                                      nan regular_payment           bpp_refunded      1      56240.00
    refund                                             Abrigo Largo Lazo Camel Nicopoly                                      nan regular_payment            compensated      1      56240.00
    refund                                             Abrigo Largo Lazo Camel Nicopoly                                      nan regular_payment             reconciled      4     216210.00
    refund                                           Abrigo Largo Lazo Celeste Nicopoly                                      nan regular_payment           bpp_refunded      5     300700.00
    refund                                           Abrigo Largo Lazo Celeste Nicopoly                                      nan regular_payment             reconciled      1      46240.00
    refund                                             Abrigo Largo Lazo Negro Nicopoly                                      nan regular_payment           bpp_refunded      3     216220.00
    refund                                             Abrigo Largo Lazo Negro Nicopoly                                      nan regular_payment             reconciled      3     194970.00
    refund                                              Abrigo Largo Lazo Rojo Nicopoly                                      nan regular_payment           bpp_refunded      4     295960.00
    refund                                              Abrigo Largo Lazo Rojo Nicopoly                                      nan regular_payment            compensated      2     104230.00
    refund                                               Abrigo Largo Lazo Uva Nicopoly                                      nan regular_payment           bpp_refunded      3     176220.00
    refund                                 Abrigo Oversize Pied De Poule Khaki Nicopoly                                      nan regular_payment           bpp_refunded      2      35060.00
    refund                                 Abrigo Oversize Pied De Poule Khaki Nicopoly                                      nan regular_payment             reconciled      1      31420.00
    refund                                  Abrigo Oversize Pied De Poule Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3     107375.00
    refund                                  Abrigo Oversize Pied De Poule Rojo Nicopoly                                      nan regular_payment             reconciled      1      36490.00
    refund                                        Abrigo Patrón Espiga Grafito Nicopoly                                      nan regular_payment           bpp_refunded      8     358930.00
    refund                                        Abrigo Patrón Espiga Grafito Nicopoly                                      nan regular_payment             reconciled      6     312440.00
    refund                                          Abrigo Pied De Poule Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     414300.00
    refund                                          Abrigo Pied De Poule Negro Nicopoly                                      nan regular_payment             reconciled      4     168960.00
    refund                                       Abrigo Solapa Redonda Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2     108480.00
    refund                                       Abrigo Solapa Redonda Celeste Nicopoly                                      nan regular_payment             reconciled      2     111980.00
    refund                                          Abrigo Solapa Redonda Negronicopoly                                      nan regular_payment           bpp_refunded      8     491022.00
    refund                                          Abrigo Solapa Redonda Negronicopoly                                      nan regular_payment             reconciled      4     222562.00
    refund                                          Abrigo Solapa Redonda Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2     108480.00
    refund                                          Abrigo Solapa Redonda Rojo Nicopoly                                      nan regular_payment         not_reconciled      1      48990.00
    refund                                          Abrigo Solapa Redonda Rojo Nicopoly                                      nan regular_payment             reconciled      6     362440.00
    refund                                           Abrigo Solapa Redonda Uva Nicopoly                                      nan regular_payment           bpp_refunded      4     175628.00
    refund                                           Abrigo Solapa Redonda Uva Nicopoly                                      nan regular_payment            compensated      1      52490.00
    refund                                           Abrigo Solapa Redonda Uva Nicopoly                                      nan regular_payment             reconciled      3     130822.00
    refund                                    Abrigo Solapa Redonda Verde Lima Nicopoly                                      nan regular_payment           bpp_refunded      2     104980.00
    refund                                    Abrigo Solapa Redonda Verde Lima Nicopoly                                      nan regular_payment             reconciled      2     118980.00
    refund         Abrigo Solapa Redonda Verde Petróleo Nicopoly Verde Petróleo Xl Liso                                      nan regular_payment           bpp_refunded      1      71990.00
    refund                         Abrigo Solapa Y Cinturón Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      2     161980.00
    refund                         Abrigo Solapa Y Cinturón Negro Nicopoly Negro S Liso                                      nan regular_payment         not_reconciled      1      76990.00
    refund                        Abrigo Solapa Y Cinturón Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      1      76990.00
    refund                           Abrigo Solapa Y Cinturón Rojo Nicopoly Rojo L Liso                                      nan regular_payment           bpp_refunded      1      76990.00
    refund                           Abrigo Solapa Y Cinturón Rojo Nicopoly Rojo S Liso                                      nan regular_payment           bpp_refunded      1      76990.00
    refund                          Abrigo Solapa Y Cinturón Rojo Nicopoly Rojo Xl Liso                                      nan regular_payment           bpp_refunded      1      50990.00
    refund                                     Abrigo Tipo Paño 2 Botones Gris Nicopoly                                      nan regular_payment           bpp_refunded      3     175970.00
    refund                                     Abrigo Tipo Paño 2 Botones Gris Nicopoly                                      nan regular_payment             reconciled      1      63990.00
    refund                                     Abrigo Tipo Paño 2 Botones Negronicopoly                                      nan regular_payment           bpp_refunded      7     431930.00
    refund                                     Abrigo Tipo Paño 2 Botones Negronicopoly                                      nan regular_payment            compensated      1      55990.00
    refund                                     Abrigo Tipo Paño 2 Botones Negronicopoly                                      nan regular_payment             reconciled      6     333940.00
    refund                                    Abrigo Tipo Paño 2 Botones Óxido Nicopoly                                      nan regular_payment           bpp_refunded      2      55990.00
    refund                                  Blazer 4 Botones Decorativos Negro Nicopoly                                      nan regular_payment            bpp_covered      1      27990.00
    refund                                  Blazer 4 Botones Decorativos Negro Nicopoly                                      nan regular_payment           bpp_refunded     14     423552.00
    refund                                  Blazer 4 Botones Decorativos Negro Nicopoly                                      nan regular_payment            compensated      1      39990.00
    refund                                   Blazer 4 Botones Decorativos Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                Blazer 6 Botones Grafito - Grafito - M - Liso                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                      Blazer 6 Botones Grafito Grafito L Liso                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                      Blazer 6 Botones Grafito Grafito M Liso                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                      Blazer 6 Botones Grafito L Liso Grafito                                      nan regular_payment             reconciled      1      27990.00
    refund                               Blazer 6 Botones Marrón Nicopoly Marrón L Liso                                      nan regular_payment            bpp_covered      1      24070.00
    refund                               Blazer 6 Botones Marrón Nicopoly Marrón L Liso                                      nan regular_payment           bpp_refunded      2      55980.00
    refund                                 Blazer 6 Botones Marrón Nicopoly Marrón Liso                                      nan regular_payment           bpp_refunded      1      33590.00
    refund                                 Blazer 6 Botones Marrón Nicopoly Marrón Liso                                      nan regular_payment             reconciled      1      33590.00
    refund                               Blazer 6 Botones Marrón Nicopoly Marrón M Liso                                      nan regular_payment             reconciled      1      32990.00
    refund                                                Blazer 6 Botones Negro L Liso                                      nan regular_payment             reconciled      1      33590.00
    refund                                                Blazer 6 Botones Negro M Liso                                      nan regular_payment           bpp_refunded      1      33590.00
    refund                                                Blazer 6 Botones Negro M Liso                                      nan regular_payment             reconciled      1      33590.00
    refund                                          Blazer 6 Botones Negro Negro L Liso                                      nan regular_payment           bpp_refunded      2      83980.00
    refund                                          Blazer 6 Botones Negro Negro L Liso                                      nan regular_payment            compensated      1      27990.00
    refund                                          Blazer 6 Botones Negro Negro L Liso                                      nan regular_payment             reconciled      2      83980.00
    refund                                          Blazer 6 Botones Negro Negro M Liso                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                          Blazer 6 Botones Negro Negro S Liso                                      nan regular_payment           bpp_refunded      2      83980.00
    refund                                          Blazer 6 Botones Negro Negro S Liso                                      nan regular_payment             reconciled      1      27990.00
    refund                                         Blazer 6 Botones Negro Negro Xl Liso                                      nan regular_payment           bpp_refunded      2      59599.00
    refund                                         Blazer 6 Botones Negro Negro Xl Liso                                      nan regular_payment            compensated      1      27990.00
    refund                                         Blazer 6 Botones Negro Negro Xl Liso                                      nan regular_payment             reconciled      3      52371.00
    refund                                               Blazer 6 Botones Negro Xl Liso                                      nan regular_payment           bpp_refunded      1      55990.00
    refund                                            Blazer 6 Botones Rojo L Rojo Liso                                      nan regular_payment           bpp_refunded      1      32990.00
    refund                                            Blazer 6 Botones Rojo L Rojo Liso                                      nan regular_payment             reconciled      1      32990.00
    refund                                                 Blazer 6 Botones Rojo M Liso                                      nan regular_payment             reconciled      1      24070.00
    refund                                            Blazer 6 Botones Rojo Rojo L Liso                                      nan regular_payment           bpp_refunded      5      68100.00
    refund                                            Blazer 6 Botones Rojo Rojo M Liso                                      nan regular_payment           bpp_refunded      2      83980.00
    refund                                            Blazer 6 Botones Rojo Rojo M Liso                                      nan regular_payment             reconciled      1      32990.00
    refund                                            Blazer 6 Botones Rojo Rojo S Liso                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                           Blazer 6 Botones Rojo Rojo Xl Liso                                      nan regular_payment           bpp_refunded      2      83980.00
    refund                                           Blazer 6 Botones Rojo Rojo Xl Liso                                      nan regular_payment             reconciled      1      55990.00
    refund                                                 Blazer 6 Botones Rojo S Liso                                      nan regular_payment           bpp_refunded      1      33590.00
    refund                                                Blazer 6 Botones Rojo Xl Liso                                      nan regular_payment           bpp_refunded      1      33590.00
    refund                                           Blazer 6 Botones Rojo Xl Rojo Liso                                      nan regular_payment           bpp_refunded      1      32990.00
    refund                             Blazer Bolsillos Con Solapas Azul Medio Nicopoly                                      nan regular_payment           bpp_refunded      1      52990.00
    refund                                  Blazer Bolsillos Con Solapas Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      22000.00
    refund                                  Blazer Bolsillos Con Solapas Khaki Nicopoly                                      nan regular_payment             reconciled      2      49730.00
    refund                                     Blazer Bolsillos Y Botón  Negro Nicopoly                                      nan regular_payment           bpp_refunded      3     115970.00
    refund                                     Blazer Bolsillos Y Botón  Negro Nicopoly                                      nan regular_payment             reconciled      3      99970.00
    refund                                    Blazer Bolsillos Y Botón Celeste Nicopoly                                      nan regular_payment            bpp_covered      1      31990.00
    refund                                    Blazer Bolsillos Y Botón Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      59065.00
    refund                                    Blazer Bolsillos Y Botón Celeste Nicopoly                                      nan regular_payment             reconciled      2      36405.00
    refund                                       Blazer Bolsillos Y Botón Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      26490.00
    refund                                       Blazer Bolsillos Y Botón Rojo Nicopoly                                      nan regular_payment             reconciled      2      68280.00
    refund                                    Blazer Botones Decorativos Crema Nicopoly                                      nan regular_payment           bpp_refunded      6     166545.00
    refund                                    Blazer Botones Decorativos Crema Nicopoly                                      nan regular_payment             reconciled      4     114760.00
    refund                              Blazer Básico De Tope Azul Nicopoly Azul L Lisa                                      nan regular_payment           bpp_refunded      3      87980.00
    refund                              Blazer Básico De Tope Azul Nicopoly Azul L Lisa                                      nan regular_payment             reconciled      1      19990.00
    refund                              Blazer Básico De Tope Azul Nicopoly Azul S Lisa                                      nan regular_payment            bpp_covered      1      26990.00
    refund                             Blazer Básico De Tope Azul Nicopoly Azul Xl Lisa                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                   Blazer Básico De Tope Azul Nicopoly M Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                              Blazer Básico De Tope Azul Nicopoly S Azul Lisa                                      nan regular_payment           bpp_refunded      2      71980.00
    refund                                   Blazer Básico De Tope Azul Nicopoly S Lisa                                      nan regular_payment           bpp_refunded      1      26490.00
    refund                             Blazer Básico De Tope Azul Nicopoly Xl Azul Lisa                                      nan regular_payment             reconciled      1      35990.00
    refund                                  Blazer Básico De Tope Azul Nicopoly Xl Lisa                                      nan regular_payment           bpp_refunded      1      31490.00
    refund                            Blazer Básico De Tope Azul Nicopoly Xxl Azul Lisa                                      nan regular_payment             reconciled      1      35990.00
    refund                          Blazer Básico De Tope Blanco Nicopoly Blanco L Lisa                                      nan regular_payment           bpp_refunded      7     182195.00
    refund                          Blazer Básico De Tope Blanco Nicopoly Blanco L Lisa                                      nan regular_payment             reconciled      1      44990.00
    refund                         Blazer Básico De Tope Blanco Nicopoly Blanco Xl Lisa                                      nan regular_payment             reconciled      1      44990.00
    refund                        Blazer Básico De Tope Blanco Nicopoly Blanco Xxl Lisa                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                        Blazer Básico De Tope Blanco Nicopoly Blanco Xxl Lisa                                      nan regular_payment             reconciled      2      62980.00
    refund                          Blazer Básico De Tope Blanco Nicopoly L Lisa Blanco                                      nan regular_payment           bpp_refunded      2      71980.00
    refund                                 Blazer Básico De Tope Blanco Nicopoly M Lisa                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                                Blazer Básico De Tope Blanco Nicopoly Xl Lisa                                      nan regular_payment            compensated      1      44990.00
    refund                              Blazer Básico De Tope Café Nicopoly Café M Lisa                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                              Blazer Básico De Tope Café Nicopoly Café S Lisa                                      nan regular_payment             reconciled      1      44990.00
    refund                             Blazer Básico De Tope Café Nicopoly Café Xl Lisa                                      nan regular_payment           bpp_refunded      8     257920.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris L Lisa                                      nan regular_payment           bpp_refunded      9     293922.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris L Lisa                                      nan regular_payment             reconciled      1      29990.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris M Lisa                                      nan regular_payment           bpp_refunded      5     152780.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris M Lisa                                      nan regular_payment                    nan      1      29990.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris M Lisa                                      nan regular_payment             reconciled      2      37660.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris S Lisa                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris S Lisa                                      nan regular_payment             reconciled      1      26990.00
    refund                             Blazer Básico De Tope Gris Nicopoly Gris Xl Lisa                                      nan regular_payment           bpp_refunded      5     151450.00
    refund                             Blazer Básico De Tope Gris Nicopoly Gris Xl Lisa                                      nan regular_payment             reconciled      1      44990.00
    refund                            Blazer Básico De Tope Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment           bpp_refunded      7     131160.00
    refund                            Blazer Básico De Tope Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment             reconciled      1      29990.00
    refund                              Blazer Básico De Tope Gris Nicopoly L Gris Lisa                                      nan regular_payment             reconciled      1      35990.00
    refund                                   Blazer Básico De Tope Gris Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                      Blazer Básico De Tope Khaki Nicopoly - Khaki - S - Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                     Blazer Básico De Tope Khaki Nicopoly - Khaki - Xl - Lisa                                      nan regular_payment             reconciled      1      35990.00
    refund                            Blazer Básico De Tope Khaki Nicopoly Khaki L Lisa                                      nan regular_payment           bpp_refunded      2      61480.00
    refund                            Blazer Básico De Tope Khaki Nicopoly Khaki M Lisa                                      nan regular_payment           bpp_refunded      1      31490.00
    refund                            Blazer Básico De Tope Khaki Nicopoly Khaki M Lisa                                      nan regular_payment             reconciled      1      29990.00
    refund                            Blazer Básico De Tope Khaki Nicopoly Khaki S Lisa                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                           Blazer Básico De Tope Khaki Nicopoly Khaki Xl Lisa                                      nan regular_payment           bpp_refunded      5      39522.00
    refund                           Blazer Básico De Tope Khaki Nicopoly Khaki Xl Lisa                                      nan regular_payment   refund_account_money      2      48214.00
    refund                                 Blazer Básico De Tope Morado Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      1      31490.00
    refund                          Blazer Básico De Tope Morado Nicopoly L Lisa Morado                                      nan regular_payment             reconciled      1      35990.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado L Lisa                                      nan regular_payment           bpp_refunded      3     107970.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado L Lisa                                      nan regular_payment             reconciled      1      35990.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado M Lisa                                      nan regular_payment           bpp_refunded      6     133770.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado M Lisa                                      nan regular_payment         not_reconciled      1      35990.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado M Lisa                                      nan regular_payment             reconciled      2      78380.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado S Lisa                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                         Blazer Básico De Tope Morado Nicopoly Morado Xl Lisa                                      nan regular_payment           bpp_refunded      2      61480.00
    refund                         Blazer Básico De Tope Morado Nicopoly Morado Xl Lisa                                      nan regular_payment             reconciled      1      29990.00
    refund                         Blazer Básico De Tope Morado Nicopoly Xl Lisa Morado                                      nan regular_payment           bpp_refunded      1      30990.00
    refund                      Blazer Básico De Tope Negro Nicopoly - Negro - L - Lisa                                      nan regular_payment             reconciled      1      35990.00
    refund                                  Blazer Básico De Tope Negro Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                            Blazer Básico De Tope Negro Nicopoly M Lisa Negro                                      nan regular_payment           bpp_refunded      2      71980.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro L Lisa                                      nan regular_payment           bpp_refunded      4     143960.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro M Lisa                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro M Lisa                                      nan regular_payment                    nan      1      29990.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro M Lisa                                      nan regular_payment             reconciled      1      31490.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro S Lisa                                      nan regular_payment           bpp_refunded      3     104970.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro S Lisa                                      nan regular_payment             reconciled      1      44990.00
    refund                           Blazer Básico De Tope Negro Nicopoly Negro Xl Lisa                                      nan regular_payment           bpp_refunded      5     157450.00
    refund                           Blazer Básico De Tope Negro Nicopoly Negro Xl Lisa                                      nan regular_payment             reconciled      1      31490.00
    refund                          Blazer Básico De Tope Negro Nicopoly Negro Xxl Lisa                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                          Blazer Básico De Tope Negro Nicopoly Negro Xxl Lisa                                      nan regular_payment             reconciled      1      31490.00
    refund                                Blazer Básico De Tope Negro Nicopoly Xxl Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                                Blazer Básico De Tope Negro Nicopoly Xxl Lisa                                      nan regular_payment             reconciled      1      44990.00
    refund                        Blazer Básico De Tope Rojo Nicopoly - Rojo - M - Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                              Blazer Básico De Tope Rojo Nicopoly Rojo L Lisa                                      nan regular_payment             reconciled      1      36990.00
    refund                              Blazer Básico De Tope Rojo Nicopoly Rojo M Lisa                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                              Blazer Básico De Tope Rojo Nicopoly Rojo S Lisa                                      nan regular_payment             reconciled      2      61480.00
    refund                             Blazer Básico De Tope Rojo Nicopoly Rojo Xl Lisa                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                             Blazer Básico De Tope Rojo Nicopoly Rojo Xl Lisa                                      nan regular_payment             reconciled      4     112460.00
    refund                   Blazer Básico De Tope Rosado Nicopoly - Rosado - Xl - Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                                 Blazer Básico De Tope Rosado Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      2      71980.00
    refund                                 Blazer Básico De Tope Rosado Nicopoly L Lisa                                      nan regular_payment                    nan      1      35990.00
    refund                          Blazer Básico De Tope Rosado Nicopoly Rosado M Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                          Blazer Básico De Tope Rosado Nicopoly Rosado S Lisa                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                         Blazer Básico De Tope Rosado Nicopoly Rosado Xl Lisa                                      nan regular_payment             reconciled      1      35990.00
    refund                        Blazer Básico De Tope Rosado Nicopoly Rosado Xxl Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                        Blazer Básico De Tope Rosado Nicopoly Rosado Xxl Lisa                                      nan regular_payment             reconciled      1      29990.00
    refund                                Blazer Básico De Tope Rosado Nicopoly Xl Lisa                                      nan regular_payment           bpp_refunded      4      51473.00
    refund                                Blazer Básico De Tope Rosado Nicopoly Xl Lisa                                      nan regular_payment             reconciled      1      29329.00
    refund                         Blazer Básico De Tope Rosado Nicopoly Xl Lisa Rosado                                      nan regular_payment             reconciled      1      35990.00
    refund                               Blazer Básico De Tope Rosado Nicopoly Xxl Lisa                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                            Blazer Básico De Tope Verde Nicopoly Verde L Lisa                                      nan regular_payment           bpp_refunded      3     134970.00
    refund                            Blazer Básico De Tope Verde Nicopoly Verde M Lisa                                      nan regular_payment           bpp_refunded      6     260940.00
    refund                            Blazer Básico De Tope Verde Nicopoly Verde S Lisa                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                           Blazer Básico De Tope Verde Nicopoly Verde Xl Lisa                                      nan regular_payment           bpp_refunded      2      47791.00
    refund                           Blazer Básico De Tope Verde Nicopoly Verde Xl Lisa                                      nan regular_payment             reconciled      2      60179.00
    refund                            Blazer Básico De Tope Óxido Nicopoly Óxido M Lisa                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                           Blazer Básico De Tope Óxido Nicopoly Óxido Xl Lisa                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                                            Blazer Con Solapa Blanco Nicopoly                                      nan regular_payment           bpp_refunded      2      51480.00
    refund                                             Blazer Con Solapa Khaki Nicopoly                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                                             Blazer Con Solapa Khaki Nicopoly                                      nan regular_payment             reconciled      1      21490.00
    refund                                             Blazer Con Solapa Negro Nicopoly                                      nan regular_payment           bpp_refunded      5     116450.00
    refund                                             Blazer Con Solapa Negro Nicopoly                                      nan regular_payment             reconciled      8     242621.00
    refund                                                   Blazer Corto Rosa Nicopoly                                      nan regular_payment                    nan      1      39990.00
    refund                                                Blazer Cotelé Burdeo Nicopoly                                      nan regular_payment           bpp_refunded     16     521860.00
    refund                                                Blazer Cotelé Burdeo Nicopoly                                      nan regular_payment             reconciled      3      74480.00
    refund                                       Blazer Cruzado Ecocuero Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     280742.00
    refund                                       Blazer Cruzado Ecocuero Negro Nicopoly                                      nan regular_payment             reconciled      5     169818.00
    refund                           Blazer Cruzado Pied De Poule Blanco/negro Nicopoly                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                          Blazer Cruzado Sin Mangas Gris Nicopoly Gris M Liso                                      nan regular_payment           bpp_refunded      3      34990.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco L Lisa                                      nan regular_payment           bpp_refunded      3     114970.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco M Lisa                                      nan regular_payment           bpp_refunded      4     154960.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco M Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco S Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco S Lisa                                      nan regular_payment             reconciled      2      74980.00
    refund                         Blazer Cuello Cruzado Blanco Nicopoly Blanco Xl Lisa                                      nan regular_payment           bpp_refunded      4     144960.00
    refund                         Blazer Cuello Cruzado Blanco Nicopoly Blanco Xl Lisa                                      nan regular_payment             reconciled      3     109970.00
    refund                        Blazer Cuello Cruzado Blanco Nicopoly Blanco Xxl Lisa                                      nan regular_payment           bpp_refunded      3     119970.00
    refund                        Blazer Cuello Cruzado Blanco Nicopoly Blanco Xxl Lisa                                      nan regular_payment             reconciled      3     104970.00
    refund                                 Blazer Cuello Cruzado Blanco Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                 Blazer Cuello Cruzado Blanco Nicopoly L Lisa                                      nan regular_payment                    nan      1      39990.00
    refund                                 Blazer Cuello Cruzado Blanco Nicopoly M Lisa                                      nan regular_payment             reconciled      1      49990.00
    refund                                 Blazer Cuello Cruzado Blanco Nicopoly S Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly S Lisa Blanco                                      nan regular_payment             reconciled      1      31992.00
    refund                                Blazer Cuello Cruzado Blanco Nicopoly Xl Lisa                                      nan regular_payment            compensated      1      34990.00
    refund                  Blazer Cuello Cruzado Celeste Nicopoly - Celeste - L - Lisa                                      nan regular_payment             reconciled      1      39990.00
    refund                  Blazer Cuello Cruzado Celeste Nicopoly - Celeste - S - Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                 Blazer Cuello Cruzado Celeste Nicopoly - Celeste - Xl - Lisa                                      nan regular_payment            compensated      1      39990.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste L Lisa                                      nan regular_payment            bpp_covered      1      39990.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste L Lisa                                      nan regular_payment           bpp_refunded      3      99970.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste M Lisa                                      nan regular_payment           bpp_refunded      2      99980.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste M Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste S Lisa                                      nan regular_payment           bpp_refunded      2      34990.00
    refund                       Blazer Cuello Cruzado Celeste Nicopoly Celeste Xl Lisa                                      nan regular_payment           bpp_refunded      6     174940.00
    refund                       Blazer Cuello Cruzado Celeste Nicopoly Celeste Xl Lisa                                      nan regular_payment             reconciled      3      59990.00
    refund                      Blazer Cuello Cruzado Celeste Nicopoly Celeste Xxl Lisa                                      nan regular_payment           bpp_refunded      2      84980.00
    refund                      Blazer Cuello Cruzado Celeste Nicopoly Celeste Xxl Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly L Lisa Celeste                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly M Lisa Celeste                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                                Blazer Cuello Cruzado Celeste Nicopoly S Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                              Blazer Cuello Cruzado Celeste Nicopoly Xxl Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                       Blazer Cuello Cruzado Gris Nicopoly - Gris - Xl - Lisa                                      nan regular_payment             reconciled      1      39990.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly Gris L Lisa                                      nan regular_payment           bpp_refunded      2      69980.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly Gris M Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly Gris S Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly Gris S Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                             Blazer Cuello Cruzado Gris Nicopoly Gris Xl Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                            Blazer Cuello Cruzado Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment           bpp_refunded      2      69980.00
    refund                            Blazer Cuello Cruzado Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment partially_bpp_refunded      1      18000.00
    refund                            Blazer Cuello Cruzado Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly L Gris Lisa                                      nan regular_payment            bpp_covered      1      39990.00
    refund                      Blazer Cuello Cruzado Khaki Nicopoly - Khaki - M - Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                      Blazer Cuello Cruzado Khaki Nicopoly - Khaki - M - Lisa                                      nan regular_payment             reconciled      1      39990.00
    refund                            Blazer Cuello Cruzado Khaki Nicopoly Khaki L Lisa                                      nan regular_payment           bpp_refunded      2      79980.00
    refund                            Blazer Cuello Cruzado Khaki Nicopoly Khaki M Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                           Blazer Cuello Cruzado Khaki Nicopoly Khaki Xl Lisa                                      nan regular_payment           bpp_refunded      4      54967.00
    refund                           Blazer Cuello Cruzado Khaki Nicopoly Khaki Xl Lisa                                      nan regular_payment             reconciled      3     113311.00
    refund                           Blazer Cuello Cruzado Khaki Nicopoly Xl Lisa Khaki                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                                 Blazer Cuello Cruzado Morado Nicopoly M Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                          Blazer Cuello Cruzado Morado Nicopoly Morado L Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                          Blazer Cuello Cruzado Morado Nicopoly Morado L Lisa                                      nan regular_payment             reconciled      3      99980.00
    refund                          Blazer Cuello Cruzado Morado Nicopoly Morado M Lisa                                      nan regular_payment           bpp_refunded      4     174960.00
    refund                          Blazer Cuello Cruzado Morado Nicopoly Morado S Lisa                                      nan regular_payment             reconciled      1      49990.00
    refund                         Blazer Cuello Cruzado Morado Nicopoly Morado Xl Lisa                                      nan regular_payment           bpp_refunded      2      84980.00
    refund                         Blazer Cuello Cruzado Morado Nicopoly Morado Xl Lisa                                      nan regular_payment             reconciled      1      29990.00
    refund                      Blazer Cuello Cruzado Negro Nicopoly - Negro - M - Lisa                                      nan regular_payment             reconciled      2      79980.00
    refund                      Blazer Cuello Cruzado Negro Nicopoly - Negro - S - Lisa                                      nan regular_payment             reconciled      1      39990.00
    refund                   Blazer Cuello Cruzado Negro Nicopoly Blanco,negro Xxl Lisa                                      nan regular_payment           bpp_refunded      2      99980.00
    refund                                  Blazer Cuello Cruzado Negro Nicopoly L Lisa                                      nan regular_payment             reconciled      2      84980.00
    refund                                  Blazer Cuello Cruzado Negro Nicopoly M Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro L Lisa                                      nan regular_payment           bpp_refunded      7     279930.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro L Lisa                                      nan regular_payment             reconciled      3      84980.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro M Lisa                                      nan regular_payment           bpp_refunded      2      69980.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro M Lisa                                      nan regular_payment            compensated      1      34990.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro M Lisa                                      nan regular_payment             reconciled      2      64980.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro S Lisa                                      nan regular_payment           bpp_refunded      7     197950.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro S Lisa                                      nan regular_payment                    nan      1      34990.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro S Lisa                                      nan regular_payment             reconciled      2      61980.00
    refund                           Blazer Cuello Cruzado Negro Nicopoly Negro Xl Lisa                                      nan regular_payment           bpp_refunded      4     154960.00
    refund                           Blazer Cuello Cruzado Negro Nicopoly Negro Xl Lisa                                      nan regular_payment             reconciled      4     169960.00
    refund                                   Blazer Cuello Cruzado Rojo Nicopoly M Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                              Blazer Cuello Cruzado Rojo Nicopoly Rojo L Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                              Blazer Cuello Cruzado Rojo Nicopoly Rojo L Lisa                                      nan regular_payment             reconciled      2      99980.00
    refund                              Blazer Cuello Cruzado Rojo Nicopoly Rojo M Lisa                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                             Blazer Cuello Cruzado Rojo Nicopoly Rojo Xl Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                            Blazer Cuello Cruzado Verde Nicopoly Verde M Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                            Blazer Cuello Cruzado Verde Nicopoly Verde S Lisa                                      nan regular_payment             reconciled      1      49990.00
    refund                           Blazer Cuello Cruzado Verde Nicopoly Verde Xl Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                                 Blazer Cuello Cruzado Verde Nicopoly Xl Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                                             Blazer Cuello Mao Khaki Nicopoly                                      nan regular_payment           bpp_refunded      8     294920.00
    refund                                            Blazer Cuello Mao Morado Nicopoly                                      nan regular_payment           bpp_refunded      6     222940.00
    refund                                            Blazer Cuello Mao Morado Nicopoly                                      nan regular_payment            compensated      1      39990.00
    refund                                            Blazer Cuello Mao Morado Nicopoly                                      nan regular_payment             reconciled      6     234943.00
    refund                                             Blazer Cuello Mao Negro Nicopoly                                      nan regular_payment           bpp_refunded      9     344910.00
    refund                                             Blazer Cuello Mao Negro Nicopoly                                      nan regular_payment             reconciled      1      26990.00
    refund                                              Blazer Cuello Mao Rojo Nicopoly                                      nan regular_payment           bpp_refunded      6     224940.00
    refund                                              Blazer Cuello Mao Rojo Nicopoly                                      nan regular_payment             reconciled      4     131460.00
    refund                                      Blazer Cuello Mao Verde Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      8     304920.00
    refund                                      Blazer Cuello Mao Verde Oscuro Nicopoly                                      nan regular_payment             reconciled      3     104970.00
    refund                   Blazer Cuello Redondo Sin Solapa Gris Nicopoly Gris S Liso                                      nan regular_payment           bpp_refunded      1      43990.00
    refund                                     Blazer Cuello Sin Solapa Blanco Nicopoly                                      nan regular_payment           bpp_refunded      5     146950.00
    refund                                     Blazer Cuello Sin Solapa Blanco Nicopoly                                      nan regular_payment             reconciled      4     125960.00
    refund              Blazer Cuello Sin Solapa Celeste Nicopoly - Celeste - Xl - Liso                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                     Blazer Cuello Sin Solapa Celeste Nicopoly Celeste L Liso                                      nan regular_payment             reconciled      1      34990.00
    refund                    Blazer Cuello Sin Solapa Celeste Nicopoly Celeste Xl Liso                                      nan regular_payment           bpp_refunded      2      55980.00
    refund                             Blazer Cuello Sin Solapa Celeste Nicopoly L Liso                                      nan regular_payment             reconciled      1      34990.00
    refund                               Blazer Cuello Sin Solapa Celeste Nicopoly Liso                                      nan regular_payment           bpp_refunded      3       7545.00
    refund                               Blazer Cuello Sin Solapa Celeste Nicopoly Liso                                      nan regular_payment             reconciled      1      32475.00
    refund                             Blazer Cuello Sin Solapa Celeste Nicopoly M Liso                                      nan regular_payment                    nan      1      34990.00
    refund                     Blazer Cuello Sin Solapa Celeste Nicopoly M Liso Celeste                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                     Blazer Cuello Sin Solapa Celeste Nicopoly S Liso Celeste                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                      Blazer Cuello Sin Solapa Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     298900.00
    refund                                      Blazer Cuello Sin Solapa Negro Nicopoly                                      nan regular_payment            compensated      1      34990.00
    refund                                      Blazer Cuello Sin Solapa Negro Nicopoly                                      nan regular_payment                    nan      1      34990.00
    refund                                      Blazer Cuello Sin Solapa Negro Nicopoly                                      nan regular_payment             reconciled      6     139940.00
    refund                                       Blazer Cuello Sin Solapa Rojo Nicopoly                                      nan regular_payment           bpp_refunded      6     165940.00
    refund                                       Blazer Cuello Sin Solapa Rojo Nicopoly                                      nan regular_payment            compensated      1       3500.00
    refund                                       Blazer Cuello Sin Solapa Rojo Nicopoly                                      nan regular_payment             reconciled      1      24990.00
    refund                       Blazer Cuello Sin Solapa Rosado Nicopoly Rosado L Liso                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                       Blazer Cuello Sin Solapa Rosado Nicopoly Rosado M Liso                                      nan regular_payment           bpp_refunded      2      48980.00
    refund                       Blazer Cuello Sin Solapa Rosado Nicopoly Rosado M Liso                                      nan regular_payment             reconciled      2      41980.00
    refund                       Blazer Cuello Sin Solapa Rosado Nicopoly Rosado S Liso                                      nan regular_payment            bpp_covered      1      27990.00
    refund                            Blazer De Tope Botones Decorativos Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                            Blazer De Tope Botones Decorativos Negro Nicopoly                                      nan regular_payment             reconciled      1      44990.00
    refund                      Blazer De Tope Botones Decorativos Rojo Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      2      80980.00
    refund                      Blazer De Tope Botones Decorativos Rojo Oscuro Nicopoly                                      nan regular_payment             reconciled      1      44990.00
    refund                      Blazer De Tope Botones Decorativosverde Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                      Blazer De Tope Botones Decorativosverde Oscuro Nicopoly                                      nan regular_payment            compensated      2      89980.00
    refund                                      Blazer De Tope Manga 3/4 Beige Nicopoly                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                                     Blazer De Tope Manga 3/4 Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      5     249950.00
    refund                                     Blazer De Tope Manga 3/4 Burdeo Nicopoly                                      nan regular_payment            compensated      3     149970.00
    refund                                     Blazer De Tope Manga 3/4 Burdeo Nicopoly                                      nan regular_payment             reconciled      1      49990.00
    refund                                      Blazer De Tope Manga 3/4 Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      49990.00
    refund          Blazer De Tope Manga 3/4 Recogida Beige Nicopoly - Beige - L - Liso                                      nan regular_payment             reconciled      1      39990.00
    refund          Blazer De Tope Manga 3/4 Recogida Beige Nicopoly - Beige - M - Liso                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                Blazer De Tope Manga 3/4 Recogida Beige Nicopoly Beige L Liso                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                Blazer De Tope Manga 3/4 Recogida Beige Nicopoly Beige M Liso                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                Blazer De Tope Manga 3/4 Recogida Beige Nicopoly Beige S Liso                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                      Blazer De Tope Manga 3/4 Recogida Beige Nicopoly M Liso                                      nan regular_payment             reconciled      1      39990.00
    refund              Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment           bpp_refunded      1      29990.00
    refund              Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment             reconciled      1      43990.00
    refund              Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Burdeo S Liso                                      nan regular_payment           bpp_refunded      1      49990.00
    refund             Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                     Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly L Liso                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                    Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      2      89980.00
    refund                    Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Xl Liso                                      nan regular_payment             reconciled      1      34990.00
    refund            Blazer De Tope Manga 3/4 Recogida Celeste Nicopoly Celeste S Liso                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                  Blazer De Tope Manga 3/4 Recogida Rojo Nicopoly Rojo L Liso                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                  Blazer De Tope Manga 3/4 Recogida Rojo Nicopoly Rojo M Liso                                      nan regular_payment           bpp_refunded      3     109970.00
    refund                 Blazer De Tope Manga 3/4 Recogida Rojo Nicopoly Rojo Xl Liso                                      nan regular_payment             reconciled      1      49990.00
    refund                                       Blazer De Tope Manga 3/4 Rojo Nicopoly                                      nan regular_payment             reconciled      1      49990.00
    refund                                                Blazer Escocés Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      80172.00
    refund                                                Blazer Escocés Negro Nicopoly                                      nan regular_payment             reconciled      1       2298.00
    refund                                             Blazer Floreado Celeste Nicopoly                                      nan regular_payment           bpp_refunded      6     197940.00
    refund                                             Blazer Floreado Celeste Nicopoly                                      nan regular_payment             reconciled      2      65980.00
    refund                                               Blazer Floreado Negro Nicopoly                                      nan regular_payment            bpp_covered      1      32990.00
    refund                                               Blazer Floreado Negro Nicopoly                                      nan regular_payment           bpp_refunded     11     382987.00
    refund                                               Blazer Floreado Negro Nicopoly                                      nan regular_payment             reconciled      4     138673.00
    refund                                      Blazer Largo 4 Botones Celeste Nicopoly                                      nan regular_payment           bpp_refunded      5     135236.00
    refund                                        Blazer Largo 4 Botones Khaki Nicopoly                                      nan regular_payment           bpp_refunded      7     208730.00
    refund                                        Blazer Largo 4 Botones Khaki Nicopoly                                      nan regular_payment                    nan      1      27996.00
    refund                                        Blazer Largo 4 Botones Khaki Nicopoly                                      nan regular_payment             reconciled      4     133560.00
    refund                                        Blazer Largo 4 Botones Negro Nicopoly                                      nan regular_payment           bpp_refunded      4     107770.00
    refund                                        Blazer Largo 4 Botones Negro Nicopoly                                      nan regular_payment             reconciled      2      29580.00
    refund                  Blazer Largo 4 Botones Rosado Nicopoly - Rosado - Xl - Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                                Blazer Largo 4 Botones Rosado Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      3     129970.00
    refund                                Blazer Largo 4 Botones Rosado Nicopoly M Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                         Blazer Largo 4 Botones Rosado Nicopoly Rosado M Lisa                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                         Blazer Largo 4 Botones Rosado Nicopoly Rosado S Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                         Blazer Largo 4 Botones Rosado Nicopoly Rosado S Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                        Blazer Largo 4 Botones Rosado Nicopoly Rosado Xl Lisa                                      nan regular_payment           bpp_refunded      4      70978.00
    refund                        Blazer Largo 4 Botones Rosado Nicopoly Rosado Xl Lisa                                      nan regular_payment             reconciled      2      45988.00
    refund                       Blazer Largo 4 Botones Rosado Nicopoly Rosado Xxl Lisa                                      nan regular_payment           bpp_refunded      2      69980.00
    refund                       Blazer Largo 4 Botones Rosado Nicopoly Rosado Xxl Lisa                                      nan regular_payment         not_reconciled      1      39990.00
    refund                               Blazer Largo 4 Botones Rosado Nicopoly Xl Lisa                                      nan regular_payment             reconciled      1      39990.00
    refund                       Blazer Largo 4 Botones Rosado Nicopoly Xxl Lisa Rosado                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                       Blazer Largo 4 Botones Rosado Nicopoly Xxl Lisa Rosado                                      nan regular_payment             reconciled      1      39990.00
    refund                                               Blazer Largo Amarillo Nicopoly                                      nan regular_payment           bpp_refunded      4     119084.00
    refund                                               Blazer Largo Amarillo Nicopoly                                      nan regular_payment             reconciled      6     220826.00
    refund                                   Blazer Largo Cuello Cruzado Khaki Nicopoly                                      nan regular_payment           bpp_refunded      5     339930.00
    refund                                   Blazer Largo Cuello Cruzado Khaki Nicopoly                                      nan regular_payment            compensated      2      99980.00
    refund                                   Blazer Largo Cuello Cruzado Khaki Nicopoly                                      nan regular_payment             reconciled      7     329930.00
    refund                                  Blazer Largo Cuello Cruzado Morado Nicopoly                                      nan regular_payment           bpp_refunded      4     179960.00
    refund                                  Blazer Largo Cuello Cruzado Morado Nicopoly                                      nan regular_payment            compensated      1      39990.00
    refund                                  Blazer Largo Cuello Cruzado Morado Nicopoly                                      nan regular_payment                    nan      1      49990.00
    refund                                   Blazer Largo Cuello Cruzado Negro Nicopoly                                      nan regular_payment           bpp_refunded      5     249950.00
    refund                                   Blazer Largo Cuello Cruzado Negro Nicopoly                                      nan regular_payment             reconciled      3     149970.00
    refund                             Blazer Largo Cuello Cruzado Rojo Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      3     129970.00
    refund                             Blazer Largo Cuello Cruzado Rojo Oscuro Nicopoly                                      nan regular_payment            compensated      2      89980.00
    refund                             Blazer Largo Cuello Cruzado Rojo Oscuro Nicopoly                                      nan regular_payment             reconciled      2      89980.00
    refund                                          Blazer Largo De Tope Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     172342.00
    refund                                          Blazer Largo De Tope Negro Nicopoly                                      nan regular_payment            compensated      1      41990.00
    refund                                          Blazer Largo De Tope Negro Nicopoly                                      nan regular_payment             reconciled      1      39490.00
    refund                                           Blazer Largo De Tope Rojo Nicopoly                                      nan regular_payment           bpp_refunded      8     297636.00
    refund                                           Blazer Largo De Tope Rojo Nicopoly                                      nan regular_payment                    nan      1      41990.00
    refund                                           Blazer Largo De Tope Rojo Nicopoly                                      nan regular_payment             reconciled      4     140254.00
    refund                                   Blazer Largo Manga Drapeada Negro Nicopoly                                      nan regular_payment             reconciled      1      39990.00
    refund                                              Blazer Largo Terracota Nicopoly                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                              Blazer Largo Terracota Nicopoly                                      nan regular_payment             reconciled      1      34990.00
    refund                                         Blazer Lazo Delantero Negro Nicopoly                                      nan regular_payment           bpp_refunded      9     309910.00
    refund                                         Blazer Lazo Delantero Negro Nicopoly                                      nan regular_payment             reconciled      3      94970.00
    refund                                          Blazer Lazo Delantero Rojo Nicopoly                                      nan regular_payment           bpp_refunded      5     249930.00
    refund                                          Blazer Lazo Delantero Rojo Nicopoly                                      nan regular_payment             reconciled      3     104970.00
    refund            Blazer Manga 3/4 Ajustada Con Pliegues Blanco - Blanco - L - Lisa                                      nan regular_payment             reconciled      1      39990.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Blanco Blanco L Lisa                                      nan regular_payment             reconciled      1      49990.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Blanco M Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Blanco M Lisa                                      nan regular_payment             reconciled      1      49990.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Blanco S Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                      Blazer Manga 3/4 Ajustada Con Pliegues Celeste Nicopoly                                      nan regular_payment           bpp_refunded      3     139970.00
    refund            Blazer Manga 3/4 Ajustada Con Pliegues Marrón - Marrón - M - Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Marrón M Lisa Marrón                                      nan regular_payment             reconciled      1      39990.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Marrón Marrón S Lisa                                      nan regular_payment           bpp_refunded      3     134970.00
    refund                 Blazer Manga 3/4 Ajustada Con Pliegues Marrón Xl Lisa Marrón                                      nan regular_payment            compensated      1      39990.00
    refund              Blazer Manga 3/4 Ajustada Con Pliegues Negro - Negro - L - Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund              Blazer Manga 3/4 Ajustada Con Pliegues Negro - Negro - M - Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                    Blazer Manga 3/4 Ajustada Con Pliegues Negro L Lisa Negro                                      nan regular_payment             reconciled      1      39990.00
    refund                          Blazer Manga 3/4 Ajustada Con Pliegues Negro M Lisa                                      nan regular_payment           bpp_refunded      3     129970.00
    refund                    Blazer Manga 3/4 Ajustada Con Pliegues Negro Negro L Lisa                                      nan regular_payment           bpp_refunded      2      69980.00
    refund                    Blazer Manga 3/4 Ajustada Con Pliegues Negro Negro M Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                    Blazer Manga 3/4 Ajustada Con Pliegues Negro Negro M Lisa                                      nan regular_payment             reconciled      1      29990.00
    refund                   Blazer Manga 3/4 Ajustada Con Pliegues Negro Negro Xl Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                        Blazer Manga 3/4 Ajustada Con Pliegues Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Negro Xl Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Negro Xl Lisa                                      nan regular_payment             reconciled      1      34990.00
    refund                        Blazer Manga 3/4 Ajustada Con Pliegues Negro Xxl Lisa                                      nan regular_payment           bpp_refunded      2      79980.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Negro Xxl Lisa Negro                                      nan regular_payment             reconciled      1      39990.00
    refund                       Blazer Manga 3/4 Ajustada Con Pliegues Rosado Nicopoly                                      nan regular_payment           bpp_refunded      6     269940.00
    refund                       Blazer Manga 3/4 Ajustada Con Pliegues Rosado Nicopoly                                      nan regular_payment             reconciled      1      49990.00
    refund                                Blazer Manga Detalle Drapeado Blanco Nicopoly                                      nan regular_payment           bpp_refunded      2      56580.00
    refund                                Blazer Manga Detalle Drapeado Blanco Nicopoly                                      nan regular_payment             reconciled      2      67980.00
    refund                               Blazer Manga Detalle Drapeado Celeste Nicopoly                                      nan regular_payment            bpp_covered      1      26990.00
    refund                               Blazer Manga Detalle Drapeado Celeste Nicopoly                                      nan regular_payment           bpp_refunded      6     153540.00
    refund                                 Blazer Manga Detalle Drapeado Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      37990.00
    refund                                 Blazer Manga Detalle Drapeado Negro Nicopoly                                      nan regular_payment             reconciled      1      26590.00
    refund                              Blazer Manga Drapeada Gris Nicopoly Gris S Lisa                                      nan regular_payment           bpp_refunded      1      49990.00
    refund                            Blazer Manga Drapeada Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                                  Blazer Manga Drapeada Gris Nicopoly Xl Lisa                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                    Blazer Mangas 3/4 Solapa Púrpura Nicopoly                                      nan regular_payment           bpp_refunded      6     181140.00
    refund                                    Blazer Mangas 3/4 Solapa Púrpura Nicopoly                                      nan regular_payment         not_reconciled      1      29990.00
    refund                                    Blazer Mangas 3/4 Solapa Púrpura Nicopoly                                      nan regular_payment             reconciled     11     343290.00
    refund                                    Blazer Mangas Drapeadas 3/4 Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                        Blazer Oversize Tipo Gamuza Café Nicopoly Café L Liso                                      nan regular_payment           bpp_refunded      4      76717.00
    refund                        Blazer Oversize Tipo Gamuza Café Nicopoly Café L Liso                                      nan regular_payment             reconciled      1      49081.00
    refund                        Blazer Oversize Tipo Gamuza Café Nicopoly Café S Liso                                      nan regular_payment           bpp_refunded      1      55990.00
    refund                        Blazer Oversize Tipo Gamuza Café Nicopoly Café S Liso                                      nan regular_payment             reconciled      1      55990.00
    refund                                        Blazer Patrón Espiga Grafito Nicopoly                                      nan regular_payment           bpp_refunded      2      71553.00
    refund                                        Blazer Patrón Espiga Grafito Nicopoly                                      nan regular_payment             reconciled      3     122407.00
    refund                                     Blazer Patrón Espiga Gris Claro Nicopoly                                      nan regular_payment           bpp_refunded      9     389510.00
    refund                                     Blazer Patrón Espiga Gris Claro Nicopoly                                      nan regular_payment             reconciled      9     321320.00
    refund                                           Blazer Pied De Poule Café Nicopoly                                      nan regular_payment           bpp_refunded     20     727810.00
    refund                                           Blazer Pied De Poule Café Nicopoly                                      nan regular_payment             reconciled     13     449021.00
    refund                                              Blazer Pinceladas Azul Nicopoly                                      nan regular_payment           bpp_refunded      3     121970.00
    refund                                              Blazer Pinceladas Azul Nicopoly                                      nan regular_payment             reconciled      3      99970.00
    refund                   Blazer Sastrero Dos Botones Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment           bpp_refunded      3      69990.00
    refund                                  Blazer Sin Mangas Bolsillos Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      27590.00
    refund                                 Blazer Sin Mangas Bolsillos Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      2      55180.00
    refund                                 Blazer Sin Mangas Bolsillos Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                      Blazer Sin Mangas Bolsillos Marrón Nicopoly Café L Liso                                      nan regular_payment             reconciled      1      27590.00
    refund                        Blazer Sin Mangas Bolsillos Marrón Nicopoly Café Liso                                      nan regular_payment           bpp_refunded      1      27590.00
    refund                        Blazer Sin Mangas Bolsillos Marrón Nicopoly Café Liso                                      nan regular_payment             reconciled      1      27590.00
    refund                      Blazer Sin Mangas Bolsillos Marrón Nicopoly Café S Liso                                      nan regular_payment           bpp_refunded      1      27590.00
    refund                      Blazer Sin Mangas Bolsillos Marrón Nicopoly Café S Liso                                      nan regular_payment             reconciled      1      36990.00
    refund                                   Blazer Sin Mangas Bolsillos Negro Nicopoly                                      nan regular_payment           bpp_refunded      7     263504.00
    refund                      Blazer Sin Mangas Bolsillos Rosa Nicopoly Rosado L Liso                                      nan regular_payment           bpp_refunded      1      45990.00
    refund                      Blazer Sin Mangas Bolsillos Rosa Nicopoly Rosado M Liso                                      nan regular_payment             reconciled      2      43520.00
    refund                     Blazer Sin Mangas Bolsillos Rosa Nicopoly Rosado Xl Liso                                      nan regular_payment           bpp_refunded      2      55180.00
    refund                                     Blazer Sin Mangas Botón Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      2      52980.00
    refund                                     Blazer Sin Mangas Botón Burdeos Nicopoly                                      nan regular_payment             reconciled      2      63980.00
    refund                                      Blazer Sin Mangas Botón Lúcuma Nicopoly                                      nan regular_payment           bpp_refunded      2      61980.00
    refund                                      Blazer Sin Mangas Botón Lúcuma Nicopoly                                      nan regular_payment            compensated      1      20990.00
    refund                                      Blazer Solapa Manga 3/4 Rosado Nicopoly                                      nan regular_payment           bpp_refunded      3      80570.00
    refund                                      Blazer Solapa Manga 3/4 Rosado Nicopoly                                      nan regular_payment             reconciled      1      24990.00
    refund                                          Blazer Un Botón Azul Acero Nicopoly                                      nan regular_payment           bpp_refunded      9     314910.00
    refund                                          Blazer Un Botón Azul Acero Nicopoly                                      nan regular_payment             reconciled      3     114970.00
    refund                                               Blazer Un Botón Khaki Nicopoly                                      nan regular_payment           bpp_refunded      8     263920.00
    refund                                               Blazer Un Botón Khaki Nicopoly                                      nan regular_payment             reconciled      2      69980.00
    refund                                               Blazer Un Botón Negro Nicopoly                                      nan regular_payment           bpp_refunded      7     259930.00
    refund                                               Blazer Un Botón Negro Nicopoly                                      nan regular_payment            compensated      1      39990.00
    refund                                               Blazer Un Botón Negro Nicopoly                                      nan regular_payment             reconciled      4     159960.00
    refund                                                Blazer Un Botón Rojo Nicopoly                                      nan regular_payment           bpp_refunded      5     184950.00
    refund                                                Blazer Un Botón Rojo Nicopoly                                      nan regular_payment             reconciled      5     189950.00
    refund                                          Blusa Bolsillos Cargo Café Nicopoly                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                          Blusa Bolsillos Cargo Café Nicopoly                                      nan regular_payment             reconciled      1      27990.00
    refund                                         Blusa Bolsillos Cargo Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                Blusa Bolsillos Tipo Satín Palo Rosa Nicopoly                                      nan regular_payment           bpp_refunded      1      10490.00
    refund                                     Blusa Botonera Invisible Blanco Nicopoly                                      nan regular_payment           bpp_refunded      4      75572.00
    refund                                     Blusa Botonera Invisible Blanco Nicopoly                                      nan regular_payment             reconciled      1      16222.00
    refund                               Blusa Botonera Invisible Básica Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      19490.00
    refund                                    Blusa Botonera Invisible Celeste Nicopoly                                      nan regular_payment           bpp_refunded      8     163920.00
    refund                                    Blusa Botonera Invisible Celeste Nicopoly                                      nan regular_payment                    nan      1      27990.00
    refund                                    Blusa Botonera Invisible Celeste Nicopoly                                      nan regular_payment             reconciled      3      58770.00
    refund                                    Blusa Botonera Invisible Durazno Nicopoly                                      nan regular_payment           bpp_refunded      2      50133.00
    refund                                 Blusa Broderie Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                                 Blusa Broderie Blanco Nicopoly Blanco Liso M                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                                 Blusa Broderie Blanco Nicopoly Blanco Liso S                                      nan regular_payment             reconciled      1      21584.00
    refund                                     Blusa Básica Escote En V Blanco Nicopoly                                      nan regular_payment           bpp_refunded      5      93950.00
    refund                                    Blusa Básica Escote En V Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                      Blusa Básica Escote En V Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      29980.00
    refund                      Blusa Básica Escote En V Rosado Nicopoly Rosado Liso Xl                                      nan regular_payment           bpp_refunded      2      36980.00
    refund                      Blusa Básica Escote En V Rosado Nicopoly Xl Liso Rosado                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                                                   Blusa Cebra Beige Nicopoly                                      nan regular_payment           bpp_refunded      3      81370.00
    refund                                  Blusa Con Lazo Desmontable Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                                  Blusa Con Lazo Desmontable Celeste Nicopoly                                      nan regular_payment                    nan      1      24990.00
    refund                                    Blusa Con Lazo Desmontable Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      49980.00
    refund                                    Blusa Con Lazo Desmontable Negro Nicopoly                                      nan regular_payment                    nan      1      24990.00
    refund                                    Blusa Con Lazo Desmontable Negro Nicopoly                                      nan regular_payment             reconciled      5     114954.00
    refund                                     Blusa Con Lazo Desmontable Rojo Nicopoly                                      nan regular_payment           bpp_refunded      4      97960.00
    refund                                     Blusa Con Lazo Desmontable Rojo Nicopoly                                      nan regular_payment                    nan      1      24990.00
    refund                                     Blusa Con Lazo Desmontable Rojo Nicopoly                                      nan regular_payment             reconciled      1      25592.00
    refund                          Blusa Corbatín Y Vuelos Negro Nicopoly Negro Liso L                                      nan regular_payment            compensated      1      21990.00
    refund                          Blusa Corbatín Y Vuelos Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      27990.00
    refund          Blusa Corbatín Y Vuelos Verde Azulado Nicopoly Verde Azulado Liso S                                      nan regular_payment           bpp_refunded      2      52980.00
    refund                                     Blusa Cuello Mao Botones Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                    Blusa Cuello Mao Botones Celeste Nicopoly                                      nan regular_payment           bpp_refunded      6     108340.00
    refund                                      Blusa Cuello Mao Botones Negro Nicopoly                                      nan regular_payment           bpp_refunded      4      74560.00
    refund                                       Blusa Cuello Mao Floral Negro Nicopoly                                      nan regular_payment           bpp_refunded      4      71960.00
    refund                   Blusa Cuello Mao Manga Globo Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                    Blusa Cuello Mao Tipo Satín Gris Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                                    Blusa Cuello Mao Tipo Satín Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                            Blusa Cuello Mao Tipo Satín Verde Oscuro Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                      Blusa Cuello Tipo Corbata Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                    Blusa Cuello Tipo Corbata Celeste Nicopoly L Liso Celeste                                      nan regular_payment           bpp_refunded      1      23090.00
    refund                        Blusa Cuello Tipo Corbata Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      23090.00
    refund                       Blusa Cuello Tipo Corbata Negro Nicopoly Negro Liso Xl                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                     Blusa Cuello V Tipo Gasa Blanco Nicopoly                                      nan regular_payment           bpp_refunded      2      34980.00
    refund                                     Blusa Cuello V Tipo Gasa Blanco Nicopoly                                      nan regular_payment         not_reconciled      1      14990.00
    refund                                     Blusa Cuello V Tipo Gasa Blanco Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                                    Blusa Cuello V Tipo Gasa Celeste Nicopoly                                      nan regular_payment           bpp_refunded      5      89950.00
    refund                                       Blusa Drapeada Manga Larga Azul Lisa L                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                       Blusa Drapeada Manga Larga Azul Lisa M                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                        Blusa Drapeada Manga Larga Blanco - Blanco - Liso - S                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                      Blusa Drapeada Manga Larga Negro Lisa L                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                      Blusa Drapeada Manga Larga Negro Lisa S                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                Blusa Drapeada Manga Larga Negro Negro Lisa L                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                Blusa Drapeada Manga Larga Negro Negro Lisa M                                      nan regular_payment            compensated      1      22990.00
    refund                                Blusa Drapeada Manga Larga Negro Negro Lisa S                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                Blusa Drapeada Manga Larga Negro Negro Lisa S                                      nan regular_payment             reconciled      1      28990.00
    refund                              Blusa Efecto Cruzado Tipo Satín Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      12490.00
    refund                               Blusa Efecto Cruzado Tipo Satín Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      41970.00
    refund         Blusa Encaje Detalle Lentejuelas Blanco Nicopoly - Blanco - Liso - M                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                         Blusa Encaje Hombros Blanco Nicopoly                                      nan regular_payment            bpp_covered      1      16090.00
    refund                                         Blusa Encaje Hombros Blanco Nicopoly                                      nan regular_payment           bpp_refunded      8     145110.00
    refund                                         Blusa Encaje Hombros Blanco Nicopoly                                      nan regular_payment             reconciled      1      22990.00
    refund                                         Blusa Encaje Hombros Fucsia Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                          Blusa Encaje Hombros Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     135120.00
    refund                                          Blusa Encaje Hombros Negro Nicopoly                                      nan regular_payment             reconciled      1      22990.00
    refund                                    Blusa Escote V Sin Mangas Blanco Nicopoly                                      nan regular_payment           bpp_refunded      2      32780.00
    refund                                   Blusa Escote V Sin Mangas Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                     Blusa Escote V Sin Mangas Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      16790.00
    refund                                      Blusa Escote V Sin Mangas Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3      53364.00
    refund                                                 Blusa Leopard Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      19980.00
    refund                                                 Blusa Leopardo Café Nicopoly                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                     Blusa Manga Larga Con Corbatín Café Nicopoly Café Liso L                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                           Blusa Mangas Vuelos Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                      Blusa Nudo Delantero Encaje Negro Nicopoly Negro Lisa L                                      nan regular_payment           bpp_refunded      4      65960.00
    refund                      Blusa Nudo Delantero Encaje Negro Nicopoly Negro Lisa M                                      nan regular_payment                    nan      1      15990.00
    refund                                      Blusa Print Abstracto Azul Rey Nicopoly                                      nan regular_payment           bpp_refunded      3      63970.00
    refund                                      Blusa Print Abstracto Azul Rey Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                               Blusa Print Serpiente Morado Nicopoly Liso M/l                                      nan regular_payment             reconciled      1      22180.00
    refund                        Blusa Print Serpiente Morado Nicopoly Morado Liso M/l                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                        Blusa Print Serpiente Morado Nicopoly Morado Liso S/m                                      nan regular_payment           bpp_refunded      1      14390.00
    refund                                  Blusa Puntos Blancos Nicopoly Blanco Liso M                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                              Blusa Puntos Negros Nicopoly - Negro - Liso - L                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                                Blusa Rayada Lazo Desmontable Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                   Blusa Rayas Lazo Desmontable Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                     Blusa Rayas Lazo Desmontable Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                               Blusa Sin Mangas Lila Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund        Blusa Sin Mangas Negra Con Flores Blancas Nicopoly - Negro - Lisa - L                                      nan regular_payment           bpp_refunded      1      16990.00
    refund              Blusa Sin Mangas Negra Con Flores Blancas Nicopoly Negro Lisa L                                      nan regular_payment           bpp_refunded      1      16990.00
    refund              Blusa Sin Mangas Negra Con Flores Blancas Nicopoly Negro Lisa M                                      nan regular_payment           bpp_refunded      1      10190.00
    refund                                              Blusa Tipo Gasa Rosado Nicopoly                                      nan regular_payment           bpp_refunded      2      34980.00
    refund                                              Blusa Tipo Gasa Rosado Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                     Blusa Transparencia Nudo Cebra Café Nicopoly Café Liso M                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                     Blusa Transparencia Nudo Cebra Café Nicopoly Café Liso M                                      nan regular_payment                    nan      1      12990.00
    refund             Blusa Transparente Manga Globo Negro Nicopoly - Negro - Liso - L                                      nan regular_payment             reconciled      1      19990.00
    refund                                         Blusa Vuelos Hombros Fucsia Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                       Blusa Vuelos Manga Larga Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                       Blusa Vuelos Manga Larga Blanco Nicopoly Blanco Liso L                                      nan regular_payment             reconciled      1      28990.00
    refund                       Blusa Vuelos Manga Larga Blanco Nicopoly Blanco Liso M                                      nan regular_payment            bpp_covered      1      28990.00
    refund                       Blusa Vuelos Manga Larga Burdeo Nicopoly Burdeo Lisa L                                      nan regular_payment           bpp_refunded      2      47180.00
    refund                       Blusa Vuelos Manga Larga Burdeo Nicopoly Burdeo Lisa M                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                           Blusa Vuelos Manga Larga Café Nicopoly Café Lisa L                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                           Blusa Vuelos Manga Larga Café Nicopoly Café Lisa L                                      nan regular_payment             reconciled      1      28990.00
    refund                           Blusa Vuelos Manga Larga Café Nicopoly Café Lisa M                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                           Blusa Vuelos Manga Larga Café Nicopoly Café Lisa S                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                 Body Acanalado Manga Larga Amarillo Nicopoly                                      nan regular_payment           bpp_refunded      2      21980.00
    refund                                 Body Acanalado Manga Larga Amarillo Nicopoly                                      nan regular_payment partially_bpp_refunded      1      19980.00
    refund                                     Body Acanalado Manga Larga Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      10990.00
    refund                                           Body Escote Encaje Blanco Nicopoly                                      nan regular_payment           bpp_refunded      3      44970.00
    refund                                             Body Escote Encaje Rojo Nicopoly                                      nan regular_payment           bpp_refunded      5      72950.00
    refund                                        Body Escote V Acanalado Café Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                                     Body Escote V Acanalado Mostaza Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                           Body Escote Volantes Blanco Nicopoly Blanco Liso S                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                    Body Escote Volantes Café Nicopoly Liso L                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                             Body Escote Volantes Negro Nicopoly Negro Liso M                                      nan regular_payment                    nan      1      14990.00
    refund                             Body Escote Volantes Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                       Body Halter Tipo Satín Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                                        Body Halter Tipo Satín Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                  Body Texturizado Acanalado Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                                     Body Texturizado Acanalado Gris Nicopoly                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                                   Body Texturizado Acanalado Rosado Nicopoly                                      nan regular_payment           bpp_refunded      2      20980.00
    refund                                                Bomber Ecocuero Moca Nicopoly                                      nan regular_payment           bpp_refunded      2      65980.00
    refund                                               Bomber Ecocuero Negro Nicopoly                                      nan regular_payment           bpp_refunded      9     316478.00
    refund                                               Bomber Ecocuero Negro Nicopoly                                      nan regular_payment             reconciled      2      58172.00
    refund                         Bomber Tipo Gamuza Blanco Invierno Invierno Nicopoly                                      nan regular_payment           bpp_refunded      8     239920.00
    refund                         Bomber Tipo Gamuza Blanco Invierno Invierno Nicopoly                                      nan regular_payment             reconciled      5     132460.00
    refund                                            Bomber Tipo Gamuza Camel Nicopoly                                      nan regular_payment           bpp_refunded      8     186309.00
    refund                                            Bomber Tipo Gamuza Camel Nicopoly                                      nan regular_payment                    nan      1      34990.00
    refund                                            Bomber Tipo Gamuza Camel Nicopoly                                      nan regular_payment             reconciled      2      59527.00
    refund                                            Bomber Tipo Gamuza Oliva Nicopoly                                      nan regular_payment            bpp_covered      1      34990.00
    refund                                            Bomber Tipo Gamuza Oliva Nicopoly                                      nan regular_payment           bpp_refunded      3      99970.00
    refund                                            Bomber Tipo Gamuza Oliva Nicopoly                                      nan regular_payment                    nan      1      34990.00
    refund                                            Bomber Tipo Gamuza Oliva Nicopoly                                      nan regular_payment             reconciled      4     122962.00
    refund                                           Bomber Tipo Lanilla Negro Nicopoly                                      nan regular_payment            bpp_covered      1      26990.00
    refund                                           Bomber Tipo Lanilla Negro Nicopoly                                      nan regular_payment           bpp_refunded     17     517230.00
    refund                                           Bomber Tipo Lanilla Negro Nicopoly                                      nan regular_payment             reconciled      9     250532.00
    refund                                    Bufanda Cuadrillé Grande Celeste Nicopoly                                      nan regular_payment                    nan      1       9990.00
    refund                                    Bufanda Cuadrillé Grande Celeste Nicopoly                                      nan regular_payment             reconciled      1      15480.00
    refund                                       Bufanda Cuadrillé Grande Moca Nicopoly                                      nan regular_payment                    nan      1       9990.00
    refund                    Bufanda Cuadrillé Grande Moca Nicopoly Color Café Talla U                                      nan regular_payment             reconciled      1      13684.00
    refund                                      Bufanda Cuadrillé Pequeña Moca Nicopoly                                      nan regular_payment           bpp_refunded      1       9590.00
    refund                                   Bufanda Gruesa Azul Acero Nicopoly Talla U                                      nan regular_payment           bpp_refunded      1       5990.00
    refund                                              Bufanda Gruesa Grafito Nicopoly                                      nan regular_payment           bpp_refunded      1       7990.00
    refund                                                 Bufanda Gruesa Moca Nicopoly                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                                                 Bufanda Gruesa Moca Nicopoly                                      nan regular_payment                    nan      2      19980.00
    refund                                                 Bufanda Gruesa Moca Nicopoly                                      nan regular_payment             reconciled      1      11284.00
    refund                                                Bufanda Gruesa Negro Nicopoly                                      nan regular_payment           bpp_refunded      1       7490.00
    refund                                               Bufanda Gruesa Rosado Nicopoly                                      nan regular_payment                    nan      1       7990.00
    refund                                                Bufanda Suave Fucsia Nicopoly                                      nan regular_payment                    nan      1       5390.00
    refund                                               Bufanda Suave Grafito Nicopoly                                      nan regular_payment           bpp_refunded      1       6990.00
    refund                                          Bufanda Suave Gris Nicopoly Talla U                                      nan regular_payment            bpp_covered      1       5990.00
    refund                                                  Bufanda Suave Moca Nicopoly                                      nan regular_payment           bpp_refunded      1       6740.00
    refund                                           Bufanda Suave Moca Nicopoly Café U                                      nan regular_payment           bpp_refunded      1       5990.00
    refund                                                 Bufanda Suave Negro Nicopoly                                      nan regular_payment            bpp_covered      1       8990.00
    refund                                                 Bufanda Suave Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      20670.00
    refund                                                 Bufanda Suave Negro Nicopoly                                      nan regular_payment                    nan      1       6740.00
    refund                                          Bufanda Suave Rosado Claro Nicopoly                                      nan regular_payment           bpp_refunded      1       6990.00
    refund                                   Calza Cierres Decorativos Grafito Nicopoly                                      nan regular_payment             reconciled      1      26240.00
    refund                                     Calza Cierres Decorativos Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                   Calza Cuadrillé Pie De Poule Café Nicopoly                                      nan regular_payment           bpp_refunded      2      45980.00
    refund                                   Calza Cuadrillé Pie De Poule Café Nicopoly                                      nan regular_payment             reconciled      1      22990.00
    refund                       Calza Elasticada Skinny Tipo Encerada Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                          Calza Elasticada Skinny Tipo Encerada Café Nicopoly                                      nan regular_payment           bpp_refunded      2      51980.00
    refund                         Calza Elasticada Skinny Tipo Encerada Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                                 Calza Leopardo Café Nicopoly                                      nan regular_payment           bpp_refunded     11     229170.00
    refund                                                 Calza Leopardo Café Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                                       Calza Lisa Con Cierre Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                                          Calza Lisa Con Cierre Café Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                                    Calza Skinny Tipo Encerada Negro Nicopoly                                      nan regular_payment           bpp_refunded     13     277879.00
    refund                                    Calza Skinny Tipo Encerada Negro Nicopoly                                      nan regular_payment         not_reconciled      1      19990.00
    refund                                    Calza Skinny Tipo Encerada Negro Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                            Calza Skinny Vichy Con Cierre Azul/negro Nicopoly                                      nan regular_payment           bpp_refunded      2      35580.00
    refund                          Calza Skinny Vichy Con Cierre Blanco/negro Nicopoly                                      nan regular_payment           bpp_refunded     11     250860.00
    refund                          Calza Skinny Vichy Con Cierre Blanco/negro Nicopoly                                      nan regular_payment            compensated      1      25990.00
    refund                          Calza Skinny Vichy Con Cierre Blanco/negro Nicopoly                                      nan regular_payment                    nan      1      19990.00
    refund                          Calza Skinny Vichy Con Cierre Blanco/negro Nicopoly                                      nan regular_payment             reconciled      1      20272.00
    refund                                  Calza Skinny Vichy Con Cierre Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2      32980.00
    refund                                            Calza Tipo Gamuza Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      4      71960.00
    refund                                             Calza Tipo Gamuza Camel Nicopoly                                      nan regular_payment           bpp_refunded      8     167920.00
    refund                                             Calza Tipo Gamuza Camel Nicopoly                                      nan regular_payment             reconciled      1      20990.00
    refund                                             Calza Tipo Gamuza Negro Nicopoly                                      nan regular_payment           bpp_refunded      7     151540.00
    refund                                             Calza Tipo Gamuza Negro Nicopoly                                      nan regular_payment                    nan      2      40980.00
    refund                                             Calza Tipo Gamuza Negro Nicopoly                                      nan regular_payment             reconciled      2      42980.00
    refund                                Calza Vichy Con Cierre Burdeos/negro Nicopoly                                      nan regular_payment           bpp_refunded      4      79960.00
    refund                        Camisa Botonera Espalda Blanco Nicopoly Blanco Lisa M                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                          Camisa Botonera Espalda Khaki Nicopoly Khaki Lisa L                                      nan regular_payment           bpp_refunded      2      41980.00
    refund                          Camisa Botonera Espalda Khaki Nicopoly Khaki Lisa M                                      nan regular_payment           bpp_refunded      2      35980.00
    refund                          Camisa Botonera Espalda Khaki Nicopoly Khaki Lisa S                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                                        Camisa Básica Algodón Blanco Nicopoly                                      nan regular_payment             reconciled      2      24990.00
    refund                                         Camisa Básica Algodón Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                                                 Camisa Básica Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      62970.00
    refund                                                  Camisa Básica Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3      63358.00
    refund                          Camisa Básica Tipo Lino Beige Nicopoly Óxido Lisa M                                      nan regular_payment                    nan      1      18990.00
    refund                  Camisa Básica Tipo Lino Blanco Nicopoly - Blanco - Lisa - M                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                               Camisa Básica Tipo Lino Blanco Nicopoly Lisa S                                      nan regular_payment           bpp_refunded      1      53980.00
    refund                      Camisa Básica Tipo Lino Celeste Nicopoly Celeste Lisa L                                      nan regular_payment                    nan      1      16190.00
    refund                              Camisa Básica Tipo Lino Celeste Nicopoly Lisa M                                      nan regular_payment           bpp_refunded      1      18890.00
    refund                          Camisa Básica Tipo Lino Verde Oliva Nicopoly Lisa M                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                    Camisa Básica Tipo Lino Verde Oliva Nicopoly Oliva Lisa L                                      nan regular_payment            bpp_covered      1      15990.00
    refund                    Camisa Básica Tipo Lino Verde Oliva Nicopoly Oliva Lisa L                                      nan regular_payment                    nan      1      15990.00
    refund                                      Camisa Básica Tipo Satín Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      47980.00
    refund                                       Camisa Básica Tipo Satín Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                     Camisa Básica Tipo Satín Rosado Nicopoly                                      nan regular_payment             reconciled      1      27990.00
    refund                                        Camisa Manga Ajustable Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      24740.00
    refund                                       Camisa Pliegues Cintura Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      71970.00
    refund                                       Camisa Pliegues Cintura Negro Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                                        Camisa Pliegues Cintura Rojo Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                                      Camisa Rayas Café Nicopoly Café Liso Xl                                      nan regular_payment           bpp_refunded      1      27190.00
    refund                                                Camisa Rayas Celeste Nicopoly                                      nan regular_payment           bpp_refunded      5     121350.00
    refund                                                Camisa Rayas Celeste Nicopoly                                      nan regular_payment             reconciled      3      81970.00
    refund                                                  Camisa Rayas Negro Nicopoly                                      nan regular_payment           bpp_refunded      5     116950.00
    refund                   Camisa Satinada Transparente Blanco Nicopoly Blanco Liso M                                      nan regular_payment           bpp_refunded      2      40980.00
    refund                   Camisa Satinada Transparente Blanco Nicopoly Blanco Liso M                                      nan regular_payment             reconciled      1      13990.00
    refund                            Camisa Satinada Transparente Gris Nicopoly Gris L                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                            Camisa Satinada Transparente Gris Nicopoly M Gris                                      nan regular_payment           bpp_refunded      1      18990.00
    refund          Camisa Sin Mangas Tipo Lino Azul Marino Nicopoly Azul Marino Liso L                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                      Chaleco Cuello V Oversize Rosa Nicopoly                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                                      Chaleco Cuello V Oversize Rosa Nicopoly                                      nan regular_payment             reconciled      1      12930.00
    refund                                          Chaleco Pied De Poule Café Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                               Chaqueta Barn Jacket Café Nicopoly Café L Liso                                      nan regular_payment             reconciled      1      51990.00
    refund                             Chaqueta Barn Jacket Oliva Nicopoly Oliva S Liso                                      nan regular_payment             reconciled      1      51990.00
    refund                                                 Chaqueta Biker Café Nicopoly                                      nan regular_payment           bpp_refunded      1      38990.00
    refund                                                 Chaqueta Biker Café Nicopoly                                      nan regular_payment            compensated      1      41240.00
    refund                                                 Chaqueta Biker Café Nicopoly                                      nan regular_payment             reconciled      5     191200.00
    refund                                  Chaqueta Biker Ecocuero Corta Café Nicopoly                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                                  Chaqueta Biker Ecocuero Corta Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                  Chaqueta Biker Ecocuero Corta Gris Nicopoly                                      nan regular_payment         not_reconciled      2      55980.00
    refund                                  Chaqueta Biker Ecocuero Corta Gris Nicopoly                                      nan regular_payment             reconciled      1      37990.00
    refund                                Chaqueta Biker Ecocuero Corta Negro  Nicopoly                                      nan regular_payment           bpp_refunded      9     345910.00
    refund                                Chaqueta Biker Ecocuero Corta Negro  Nicopoly                                      nan regular_payment                    nan      1     113970.00
    refund                                Chaqueta Biker Ecocuero Corta Negro  Nicopoly                                      nan regular_payment             reconciled      2      63980.00
    refund                                        Chaqueta Biker Ecocuero Gris Nicopoly                                      nan regular_payment             reconciled      2      82980.00
    refund                                                Chaqueta Biker Negro Nicopoly                                      nan regular_payment           bpp_refunded     13     489380.00
    refund                                                Chaqueta Biker Negro Nicopoly                                      nan regular_payment            compensated      1      41240.00
    refund                                                Chaqueta Biker Negro Nicopoly                                      nan regular_payment             reconciled     11     456760.00
    refund                             Chaqueta Bomber Broches Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                       Chaqueta Bomber Broches Camel Nicopoly                                      nan regular_payment           bpp_refunded      2      51980.00
    refund                                       Chaqueta Bomber Broches Camel Nicopoly                                      nan regular_payment            compensated      1      25990.00
    refund                                       Chaqueta Bomber Broches Camel Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                            Chaqueta Bouclé Blanco Invierno Invierno Nicopoly                                      nan regular_payment           bpp_refunded      6     207690.00
    refund                            Chaqueta Bouclé Blanco Invierno Invierno Nicopoly                                      nan regular_payment             reconciled      2      59980.00
    refund                                                Chaqueta Bouclé Gris Nicopoly                                      nan regular_payment           bpp_refunded     15     539350.00
    refund                                                Chaqueta Bouclé Gris Nicopoly                                      nan regular_payment                    nan      1      27190.00
    refund                                                Chaqueta Bouclé Gris Nicopoly                                      nan regular_payment             reconciled      2      71980.00
    refund                                                Chaqueta Bouclé Moca Nicopoly                                      nan regular_payment           bpp_refunded      4     129960.00
    refund                                                Chaqueta Bouclé Moca Nicopoly                                      nan regular_payment             reconciled      3      97170.00
    refund                                               Chaqueta Bouclé Negro Nicopoly                                      nan regular_payment           bpp_refunded      7     201491.00
    refund                                               Chaqueta Bouclé Negro Nicopoly                                      nan regular_payment             reconciled      2      64315.00
    refund                                    Chaqueta Corta Impermeable Khaki Nicopoly                                      nan regular_payment           bpp_refunded      4     101426.00
    refund                                    Chaqueta Corta Impermeable Khaki Nicopoly                                      nan regular_payment             reconciled      2      57609.00
    refund                                    Chaqueta Corta Impermeable Negro Nicopoly                                      nan regular_payment           bpp_refunded     14     534360.00
    refund                                    Chaqueta Corta Impermeable Negro Nicopoly                                      nan regular_payment            compensated      1      43490.00
    refund                                    Chaqueta Corta Impermeable Negro Nicopoly                                      nan regular_payment partially_bpp_refunded      1      91980.00
    refund                                    Chaqueta Corta Impermeable Negro Nicopoly                                      nan regular_payment             reconciled      6     237440.00
    refund                                    Chaqueta Corta Impermeable Negro Nicopoly                                      nan regular_payment   refund_account_money      1      39990.00
    refund                                    Chaqueta Corta Impermeable Oliva Nicopoly                                      nan regular_payment           bpp_refunded      8     279722.00
    refund                                    Chaqueta Corta Impermeable Oliva Nicopoly                                      nan regular_payment             reconciled      5     193192.00
    refund                          Chaqueta Corta Tipo Gamuza Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      4     124462.00
    refund                          Chaqueta Corta Tipo Gamuza Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      22490.00
    refund                         Chaqueta Corta Tipo Gamuza Café Nicopoly Café L Liso                                      nan regular_payment             reconciled      1      51990.00
    refund                                    Chaqueta Corta Tipo Gamuza Camel Nicopoly                                      nan regular_payment           bpp_refunded     12     375884.00
    refund                                    Chaqueta Corta Tipo Gamuza Camel Nicopoly                                      nan regular_payment            compensated      2      67480.00
    refund                                    Chaqueta Corta Tipo Gamuza Camel Nicopoly                                      nan regular_payment             reconciled      4     130460.00
    refund                                    Chaqueta Corta Tipo Gamuza Oliva Nicopoly                                      nan regular_payment           bpp_refunded      5     123960.00
    refund                                    Chaqueta Corta Tipo Gamuza Oliva Nicopoly                                      nan regular_payment             reconciled      5     153829.00
    refund                              Chaqueta Cuello Camisero Ecocuero Café Nicopoly                                      nan regular_payment           bpp_refunded      2      66980.00
    refund                              Chaqueta Cuello Camisero Ecocuero Café Nicopoly                                      nan regular_payment             reconciled      1      36990.00
    refund                             Chaqueta Cuello Camisero Ecocuero Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     340900.00
    refund                             Chaqueta Cuello Camisero Ecocuero Negro Nicopoly                                      nan regular_payment             reconciled      1      29990.00
    refund                             Chaqueta Cuello Camisero Ecocuero Oliva Nicopoly                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                            Chaqueta Cuello Mao Café Nicopoly                                      nan regular_payment           bpp_refunded      8     262920.00
    refund                                            Chaqueta Cuello Mao Café Nicopoly                                      nan regular_payment             reconciled      2      69480.00
    refund                                  Chaqueta Cuello Mao Ecocuero Khaki Nicopoly                                      nan regular_payment           bpp_refunded      2      55980.00
    refund                                   Chaqueta Cuello Mao Ecocuero Lila Nicopoly                                      nan regular_payment             reconciled      1      34990.00
    refund                            Chaqueta Cuello Mao Ecocuero Rosa Chicle Nicopoly                                      nan regular_payment             reconciled      1      27990.00
    refund                                           Chaqueta Cuello Mao Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     318422.00
    refund                                           Chaqueta Cuello Mao Negro Nicopoly                                      nan regular_payment             reconciled      2      74980.00
    refund           Chaqueta Ecocuero Acolchado Cuello Mao Negro Nicopoly Negro L Liso                                      nan regular_payment            compensated      1      34790.00
    refund                                        Chaqueta Ecocuero Lazo Camel Nicopoly                                      nan regular_payment           bpp_refunded     10     271157.00
    refund                                        Chaqueta Ecocuero Lazo Camel Nicopoly                                      nan regular_payment             reconciled      4     137551.00
    refund                                        Chaqueta Ecocuero Lazo Negro Nicopoly                                      nan regular_payment           bpp_refunded     11     527692.00
    refund                                        Chaqueta Ecocuero Lazo Negro Nicopoly                                      nan regular_payment             reconciled      1      41990.00
    refund                                   Chaqueta Ecocuero Tipo Biker Café Nicopoly                                      nan regular_payment           bpp_refunded      4     139710.00
    refund                                   Chaqueta Ecocuero Tipo Biker Café Nicopoly                                      nan regular_payment             reconciled      6     233348.00
    refund                                  Chaqueta Ecocuero Tipo Biker Negro Nicopoly                                      nan regular_payment             reconciled      1      41990.00
    refund                                    Chaqueta Ecocuero/tipo Piel Café Nicopoly                                      nan regular_payment           bpp_refunded      8     226943.00
    refund                                    Chaqueta Ecocuero/tipo Piel Café Nicopoly                                      nan regular_payment             reconciled      5     253987.00
    refund                           Chaqueta Larga Impermeable Mostaza Oscuro Nicopoly                                      nan regular_payment           bpp_refunded     32    1322234.00
    refund                           Chaqueta Larga Impermeable Mostaza Oscuro Nicopoly                                      nan regular_payment             reconciled     22     852742.00
    refund                                    Chaqueta Larga Impermeable Negro Nicopoly                                      nan regular_payment           bpp_refunded     15     707850.00
    refund                                    Chaqueta Larga Impermeable Negro Nicopoly                                      nan regular_payment            compensated      1      42740.00
    refund                                    Chaqueta Larga Impermeable Negro Nicopoly                                      nan regular_payment                    nan      3     128220.00
    refund                                    Chaqueta Larga Impermeable Negro Nicopoly                                      nan regular_payment             reconciled      5     222950.00
    refund                              Chaqueta Larga Impermeable Oliva Claro Nicopoly                                      nan regular_payment           bpp_refunded     17     682958.00
    refund                              Chaqueta Larga Impermeable Oliva Claro Nicopoly                                      nan regular_payment             reconciled      8     320484.00
    refund                                             Chaqueta Leñadora Beige Nicopoly                                      nan regular_payment           bpp_refunded      3      92970.00
    refund                                             Chaqueta Leñadora Beige Nicopoly                                      nan regular_payment             reconciled      4     119000.00
    refund                                             Chaqueta Leñadora Camel Nicopoly                                      nan regular_payment           bpp_refunded      1      30990.00
    refund                                          Chaqueta Mao Ecocuero Café Nicopoly                                      nan regular_payment           bpp_refunded      2      43990.00
    refund                                          Chaqueta Mao Ecocuero Café Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                                         Chaqueta Mao Ecocuero Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                       Chaqueta Mitad Chiporro/parka Blanco Invierno Nicopoly                                      nan regular_payment            bpp_covered      1      22990.00
    refund                       Chaqueta Mitad Chiporro/parka Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      3      84970.00
    refund                       Chaqueta Mitad Chiporro/parka Blanco Invierno Nicopoly                                      nan regular_payment            compensated      1      22990.00
    refund                       Chaqueta Mitad Chiporro/parka Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      2      44980.00
    refund                                 Chaqueta Mitad Chiporro/parka Khaki Nicopoly                                      nan regular_payment           bpp_refunded     17     305911.00
    refund                                 Chaqueta Mitad Chiporro/parka Khaki Nicopoly                                      nan regular_payment            compensated      2      64780.00
    refund                                 Chaqueta Mitad Chiporro/parka Khaki Nicopoly                                      nan regular_payment         not_reconciled      1      29990.00
    refund                                 Chaqueta Mitad Chiporro/parka Khaki Nicopoly                                      nan regular_payment             reconciled      6     147933.00
    refund                                 Chaqueta Mitad Chiporro/parka Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     247920.00
    refund                                 Chaqueta Mitad Chiporro/parka Negro Nicopoly                                      nan regular_payment             reconciled      4     114960.00
    refund                                  Chaqueta Mitad Chiporro/parka Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3      73975.00
    refund                                  Chaqueta Mitad Chiporro/parka Rojo Nicopoly                                      nan regular_payment             reconciled      3      68475.00
    refund                              Chaqueta Puffer Cotelé Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      6     167015.00
    refund                              Chaqueta Puffer Cotelé Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      3      75295.00
    refund                                        Chaqueta Puffer Cotelé Camel Nicopoly                                      nan regular_payment            bpp_covered      1      39740.00
    refund                                        Chaqueta Puffer Cotelé Camel Nicopoly                                      nan regular_payment           bpp_refunded      7     164760.00
    refund                                        Chaqueta Puffer Cotelé Camel Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                                 Chaqueta Quilt Tipo Camisera Fucsia Nicopoly                                      nan regular_payment           bpp_refunded      9     189910.00
    refund                                 Chaqueta Quilt Tipo Camisera Fucsia Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                                 Chaqueta Quilt Tipo Camisera Marrón Nicopoly                                      nan regular_payment           bpp_refunded      5     129950.00
    refund                                  Chaqueta Quilt Tipo Camisera Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     206514.00
    refund                                  Chaqueta Quilt Tipo Camisera Negro Nicopoly                                      nan regular_payment             reconciled      5      90846.00
    refund                                  Chaqueta Quilt Tipo Camisera Oliva Nicopoly                                      nan regular_payment           bpp_refunded      3      61161.00
    refund                                            Chaqueta Reversible Moca Nicopoly                                      nan regular_payment           bpp_refunded      4     158760.00
    refund                                           Chaqueta Reversible Negro Nicopoly                                      nan regular_payment           bpp_refunded     21     763842.00
    refund                                           Chaqueta Reversible Negro Nicopoly                                      nan regular_payment             reconciled      4     136970.00
    refund                                           Chaqueta Reversible Oliva Nicopoly                                      nan regular_payment           bpp_refunded      2      94730.00
    refund                                           Chaqueta Reversible Oliva Nicopoly                                      nan regular_payment             reconciled      3     102972.00
    refund                              Chaqueta Tipo Barbour Café Nicopoly Café L Liso                                      nan regular_payment           bpp_refunded      1      55990.00
    refund                            Chaqueta Tipo Barbour Mocca Nicopoly Mocca L Liso                                      nan regular_payment           bpp_refunded      3     195970.00
    refund                            Chaqueta Tipo Barbour Mocca Nicopoly Mocca L Liso                                      nan regular_payment             reconciled      2     125980.00
    refund                                  Chaqueta Tipo Biker Ecocuero Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      43990.00
    refund                                  Chaqueta Tipo Biker Ecocuero Khaki Nicopoly                                      nan regular_payment            compensated      1      43990.00
    refund                                                   Crop Encaje Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      30470.00
    refund                                                   Crop Encaje Negro Nicopoly                                      nan regular_payment            compensated      1      15490.00
    refund                                 Crop Top Espalda Elasticada Magenta Nicopoly                                      nan regular_payment           bpp_refunded      3      54970.00
    refund                                 Crop Top Espalda Elasticada Magenta Nicopoly                                      nan regular_payment                    nan      1      11990.00
    refund                                 Crop Top Espalda Elasticada Magenta Nicopoly                                      nan regular_payment             reconciled      1      14990.00
    refund                  Crop Top Espalda Elasticada Mostaza Nicopoly Mostaza M Liso                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                 Crop Top Espalda Elasticada Mostaza Nicopoly Mostaza Xl Liso                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                                   Crop Top Espalda Elasticada Negro Nicopoly                                      nan regular_payment           bpp_refunded      5      76950.00
    refund                                   Crop Top Espalda Elasticada Verde Nicopoly                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                                           Crop Top Jaspeado Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      19980.00
    refund                                            Crop Top Jaspeado Rosado Nicopoly                                      nan regular_payment           bpp_refunded      2      31980.00
    refund                                               Cuello Tipo Piel Gris Nicopoly                                      nan regular_payment            bpp_covered      1       5990.00
    refund                                               Cuello Tipo Piel Gris Nicopoly                                      nan regular_payment                    nan      1       4990.00
    refund                                    Cárdigan Botones Acanalado Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                               Cárdigan Básico Azul  Nicopoly Azul Tejido M/l                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                               Cárdigan Básico Azul  Nicopoly Azul Tejido S/m                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                    Cárdigan Básico Azul  Nicopoly Tejido S/m                                      nan regular_payment                    nan      1      17990.00
    refund                                       Cárdigan Básico Botones Negro Nicopoly                                      nan regular_payment           bpp_refunded      6     133840.00
    refund                           Cárdigan Básico Morado  Nicopoly Morado Tejido M/l                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                           Cárdigan Básico Morado  Nicopoly Morado Tejido S/m                                      nan regular_payment           bpp_refunded      2      47970.00
    refund                                      Cárdigan Corto Botones Mostaza Nicopoly                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                                          Cárdigan Crop Flores Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                Cárdigan Crop Perlas Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      4      47982.00
    refund                                          Cárdigan Crop Perlas Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                          Cárdigan Crop Perlas Negro Nicopoly                                      nan regular_payment            compensated      1      22490.00
    refund                                           Cárdigan Crop Perlas Rojo Nicopoly                                      nan regular_payment            compensated      2      44980.00
    refund                                           Cárdigan Crop Perlas Rojo Nicopoly                                      nan regular_payment                    nan      2      52480.00
    refund                Cárdigan Cuello V Con 3 Botones Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment             reconciled      1      22490.00
    refund                                             Cárdigan Floreado Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      43980.00
    refund                                             Cárdigan Floreado Negro Nicopoly                                      nan regular_payment                    nan      1      21990.00
    refund                                            Cárdigan Flores 3d Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                       Cárdigan Manga Globo Ladrillo Nicopoly Ladrillo Liso S                                      nan regular_payment           bpp_refunded      1      34390.00
    refund                                  Cárdigan Multicolor Flores 3d Café Nicopoly                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                        Cárdigan Punto Fantasía Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                     Cárdigan Punto Fantasía Magenta Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                  Cárdigan Punto Fino Cadenetas Café Nicopoly                                      nan regular_payment           bpp_refunded      2      31980.00
    refund                                  Cárdigan Punto Fino Cadenetas Gris Nicopoly                                      nan regular_payment           bpp_refunded      2      30677.00
    refund                                  Cárdigan Punto Fino Cadenetas Gris Nicopoly                                      nan regular_payment             reconciled      1       4897.00
    refund                                 Cárdigan Punto Fino Cadenetas Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                               Cárdigan Rayado Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      40115.00
    refund                                               Cárdigan Rayado Negro Nicopoly                                      nan regular_payment             reconciled      1       4265.00
    refund                                                 Cárdigan Rayas Rojo Nicopoly                                      nan regular_payment             reconciled      1      20180.00
    refund              Cárdigan Tipo Crochet Botones Dorados Café Nicopoly Café Liso L                                      nan regular_payment           bpp_refunded      1      22990.00
    refund              Cárdigan Tipo Crochet Botones Dorados Café Nicopoly Café Liso M                                      nan regular_payment           bpp_refunded      1      31990.00
    refund        Cárdigan Tipo Crochet Botones Dorados Celeste Nicopoly Celeste Liso M                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                   Cárdigan Tipo Crochet Hilo Celeste Nicopoly Celeste Liso M                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                   Cárdigan Tipo Crochet Hilo Celeste Nicopoly Celeste Liso S                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                       Cárdigan Tipo Crochet Hilo Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                     Cárdigan Tipo Crochet Hilo Rosado Nicopoly Rosado Liso L                                      nan regular_payment           bpp_refunded      1      10995.00
    refund                     Cárdigan Tipo Crochet Hilo Rosado Nicopoly Rosado Liso L                                      nan regular_payment             reconciled      1      10995.00
    refund                                       Enterito Bustier Encaje Negro Nicopoly                                      nan regular_payment           bpp_refunded      7     195930.00
    refund                                       Enterito Bustier Encaje Negro Nicopoly                                      nan regular_payment            compensated      1      27990.00
    refund                                       Enterito Bustier Encaje Negro Nicopoly                                      nan regular_payment             reconciled      2      55980.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly Morado Liso M                                      nan regular_payment            bpp_covered      3       9300.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly Morado Liso M                                      nan regular_payment           bpp_refunded      2      61580.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly Morado Liso M                                      nan regular_payment             reconciled      1      31890.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly Morado Liso S                                      nan regular_payment           bpp_refunded      2      70180.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly Morado Liso S                                      nan regular_payment             reconciled      1      35190.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly S Liso Morado                                      nan regular_payment           bpp_refunded      1      43990.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly M Liso Negro                                      nan regular_payment           bpp_refunded      1      43990.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      35190.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso M                                      nan regular_payment             reconciled      1      35190.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      1      26390.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso S                                      nan regular_payment             reconciled      1      29990.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly S Liso Negro                                      nan regular_payment           bpp_refunded      1      43990.00
    refund         Enterito Cinturón Ajustable Verde Oscuro Nicopoly - Verde - Liso - L                                      nan regular_payment             reconciled      1      43990.00
    refund         Enterito Cinturón Ajustable Verde Oscuro Nicopoly - Verde - Liso - M                                      nan regular_payment             reconciled      1      43990.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly L Liso Verde                                      nan regular_payment             reconciled      2      87980.00
    refund                     Enterito Cinturón Ajustable Verde Oscuro Nicopoly Liso L                                      nan regular_payment           bpp_refunded      1      43990.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly M Liso Verde                                      nan regular_payment             reconciled      1      43990.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly S Liso Verde                                      nan regular_payment           bpp_refunded      1      43990.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly S Liso Verde                                      nan regular_payment             reconciled      2      87980.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly Verde Liso S                                      nan regular_payment             reconciled      1      35190.00
    refund                                          Enterito Con Encaje Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                           Enterito Con Encaje Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      92970.00
    refund                                    Enterito Con Solapa Y Lazo Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                                     Enterito Corto Flores Lazo Lila Nicopoly                                      nan regular_payment           bpp_refunded      4      91360.00
    refund                                     Enterito Corto Flores Lazo Lila Nicopoly                                      nan regular_payment             reconciled      2      41980.00
    refund                                  Enterito Corto Flores Lazo Naranjo Nicopoly                                      nan regular_payment           bpp_refunded      1      20990.00
    refund                                    Enterito Cruzado 2 Botones Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      84980.00
    refund                                    Enterito Cruzado 2 Botones Negro Nicopoly                                      nan regular_payment            compensated      2      74980.00
    refund                                    Enterito Cruzado 2 Botones Negro Nicopoly                                      nan regular_payment             reconciled      1      34990.00
    refund                                     Enterito Cruzado 2 Botones Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2      74980.00
    refund                                     Enterito Cruzado 2 Botones Rojo Nicopoly                                      nan regular_payment             reconciled      1      34990.00
    refund                                           Enterito Cuello Mock Azul Nicopoly                                      nan regular_payment           bpp_refunded      7     279730.00
    refund                                           Enterito Cuello Mock Azul Nicopoly                                      nan regular_payment            compensated      1      42990.00
    refund                                           Enterito Cuello Mock Azul Nicopoly                                      nan regular_payment                    nan      1      40490.00
    refund                                           Enterito Cuello Mock Azul Nicopoly                                      nan regular_payment             reconciled      2      85980.00
    refund                                         Enterito Cuello Mock Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      5     169826.00
    refund                                         Enterito Cuello Mock Burdeo Nicopoly                                      nan regular_payment             reconciled      6     188196.00
    refund                                  Enterito Cut Out Escote Azul Acero Nicopoly                                      nan regular_payment           bpp_refunded      6     245440.00
    refund                                  Enterito Cut Out Escote Azul Acero Nicopoly                                      nan regular_payment             reconciled      3     112970.00
    refund                                       Enterito Cut Out Escote Cobre Nicopoly                                      nan regular_payment           bpp_refunded      6     226940.00
    refund                                       Enterito Cut Out Escote Cobre Nicopoly                                      nan regular_payment            compensated      1      37990.00
    refund                                       Enterito Cut Out Escote Cobre Nicopoly                                      nan regular_payment             reconciled      3     108872.00
    refund                                 Enterito Cut Out Escote Rojo Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      4     151960.00
    refund                                 Enterito Cut Out Escote Rojo Oscuro Nicopoly                                      nan regular_payment                    nan      2      75980.00
    refund                                 Enterito Cut Out Escote Rojo Oscuro Nicopoly                                      nan regular_payment             reconciled      3     112970.00
    refund                            Enterito Detalles Dorados Hombros Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                            Enterito Detalles Dorados Hombros Burdeo Nicopoly                                      nan regular_payment            compensated      1      21990.00
    refund                            Enterito Detalles Dorados Hombros Burdeo Nicopoly                                      nan regular_payment             reconciled      2      43980.00
    refund                             Enterito Detalles Dorados Hombros Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                  Enterito Efecto Dos Piezas Celeste Nicopoly                                      nan regular_payment           bpp_refunded      8     272530.00
    refund                                  Enterito Efecto Dos Piezas Celeste Nicopoly                                      nan regular_payment             reconciled      5     172950.00
    refund               Enterito Efecto Dos Piezas Morado Nicopoly - Morado - Liso - L                                      nan regular_payment           bpp_refunded      1      45990.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly M Liso Morado                                      nan regular_payment             reconciled      1      45990.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso L                                      nan regular_payment           bpp_refunded      2      55180.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso L                                      nan regular_payment             reconciled      4     126160.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso M                                      nan regular_payment                    nan      1      27590.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso M                                      nan regular_payment             reconciled      2      71980.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso S                                      nan regular_payment            bpp_covered      1      36790.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso S                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                                    Enterito Efecto Dos Piezas Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     261930.00
    refund                                    Enterito Efecto Dos Piezas Negro Nicopoly                                      nan regular_payment             reconciled      4     166360.00
    refund                                     Enterito Efecto Dos Piezas Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      22490.00
    refund                                      Enterito Escote Cruzado Blanco Nicopoly                                      nan regular_payment           bpp_refunded      3     104974.00
    refund                                      Enterito Escote Cruzado Blanco Nicopoly                                      nan regular_payment             reconciled      2      67980.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment           bpp_refunded      2      61482.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment             reconciled      1      29990.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment           bpp_refunded      2      62984.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment             reconciled      2      61482.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso S                                      nan regular_payment           bpp_refunded      3      99472.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso S                                      nan regular_payment             reconciled      2      59980.00
    refund                                       Enterito Escote Cruzado Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     242630.00
    refund                                       Enterito Escote Cruzado Negro Nicopoly                                      nan regular_payment             reconciled      2      63980.00
    refund                                      Enterito Escote V Y Lazo Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                                      Enterito Escote V Y Lazo Negro Nicopoly                                      nan regular_payment             reconciled      1      31990.00
    refund                            Enterito Halter Con Cinturón Lazo Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      9     362510.00
    refund                            Enterito Halter Con Cinturón Lazo Burdeo Nicopoly                                      nan regular_payment             reconciled      7     277340.00
    refund                             Enterito Halter Con Cinturón Lazo Negro Nicopoly                                      nan regular_payment           bpp_refunded      5     222150.00
    refund                             Enterito Halter Con Cinturón Lazo Negro Nicopoly                                      nan regular_payment             reconciled      1      35990.00
    refund                    Enterito Halter Con Cinturón Lazo Verde Petróleo Nicopoly                                      nan regular_payment           bpp_refunded      6     264540.00
    refund                    Enterito Halter Con Cinturón Lazo Verde Petróleo Nicopoly                                      nan regular_payment             reconciled      1      29390.00
    refund                                 Enterito Lazo Y Hebilla Verde Oliva Nicopoly                                      nan regular_payment           bpp_refunded     13     318120.00
    refund                                 Enterito Lazo Y Hebilla Verde Oliva Nicopoly                                      nan regular_payment            compensated      1      22990.00
    refund                                 Enterito Lazo Y Hebilla Verde Oliva Nicopoly                                      nan regular_payment             reconciled      2      45980.00
    refund                            Falda Asimétrica Animal Print Cafe Animal Print S                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                                 Falda Denim Tajo Frontal Azul Medio Nicopoly                                      nan regular_payment           bpp_refunded      3      52860.00
    refund                                 Falda Denim Tajo Frontal Azul Medio Nicopoly                                      nan regular_payment             reconciled      1      19820.00
    refund                                       Falda Denim Tajo Frontal Azul Nicopoly                                      nan regular_payment           bpp_refunded      2      35980.00
    refund                               Falda Larga Animal Print Marrón Animal Print L                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                               Falda Larga Animal Print Marrón Animal Print M                                      nan regular_payment           bpp_refunded      4      87960.00
    refund                               Falda Larga Animal Print Marrón Animal Print M                                      nan regular_payment             reconciled      1      21990.00
    refund                               Falda Larga Animal Print Marrón Animal Print S                                      nan regular_payment           bpp_refunded      5     133950.00
    refund                               Falda Larga Animal Print Marrón Animal Print S                                      nan regular_payment             reconciled      1      21990.00
    refund                             Falda Midi Ecocuero Negro Nicopoly Negro Liso Xl                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                    Falda Midi Negra Con Flores Blancas Nicopoly Negro Lisa M                                      nan regular_payment             reconciled      1      20980.00
    refund                    Falda Midi Negra Con Flores Blancas Nicopoly Negro Lisa S                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                    Falda Satín Encaje En Ruedo Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                    Falda Satín Encaje En Ruedo Burdeo Nicopoly Burdeo Liso S                                      nan regular_payment           bpp_refunded      1      20790.00
    refund                                Falda Short Tipo Gamuza Oliva Nicopoly Liso S                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                          Falda Short Tipo Gamuza Oliva Nicopoly Oliva Liso M                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                            Gilet 4 Botones Beige Nicopoly - Beige - Lisa - L                                      nan regular_payment             reconciled      1      19990.00
    refund                                        Gilet 4 Botones Beige Nicopoly Lisa S                                      nan regular_payment           bpp_refunded      2      51980.00
    refund                          Gilet 4 Botones Blanco Nicopoly - Blanco - M - Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                       Gilet 4 Botones Blanco Nicopoly S Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                       Gilet 4 Botones Blanco Nicopoly S Lisa                                      nan regular_payment             reconciled      1      25990.00
    refund                        Gilet 4 Botones Celeste Nicopoly - Celeste - L - Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                             Gilet 4 Botones Celeste Nicopoly Celeste Xl Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                      Gilet 4 Botones Celeste Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                              Gilet 4 Botones Celeste Nicopoly M Lisa Celeste                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                    Gilet 4 Botones Gris Nicopoly Gris L Lisa                                      nan regular_payment             reconciled      1      19990.00
    refund                                    Gilet 4 Botones Gris Nicopoly Gris M Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                   Gilet 4 Botones Gris Nicopoly Gris Xl Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                    Gilet 4 Botones Gris Nicopoly L Gris Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                 Gilet 4 Botones Lila Nicopoly Violeta Lisa M                                      nan regular_payment           bpp_refunded      4      67960.00
    refund                                Gilet 4 Botones Lila Nicopoly Violeta Lisa Xl                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                Gilet 4 Botones Morado Nicopoly Morado S Lisa                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                            Gilet 4 Botones Negro Nicopoly - Negro - Lisa - L                                      nan regular_payment           bpp_refunded      4      79960.00
    refund                            Gilet 4 Botones Negro Nicopoly - Negro - Lisa - M                                      nan regular_payment             reconciled      1      19990.00
    refund                            Gilet 4 Botones Negro Nicopoly - Negro - Lisa - S                                      nan regular_payment           bpp_refunded      3      29970.00
    refund                                        Gilet 4 Botones Negro Nicopoly Lisa S                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                        Gilet 4 Botones Negro Nicopoly Lisa S                                      nan regular_payment             reconciled      2      20790.00
    refund                                       Gilet 4 Botones Negro Nicopoly Lisa Xl                                      nan regular_payment                    nan      1      25990.00
    refund                                       Gilet 4 Botones Negro Nicopoly Lisa Xl                                      nan regular_payment             reconciled      1      20790.00
    refund                                  Gilet 4 Botones Negro Nicopoly Negro L Lisa                                      nan regular_payment           bpp_refunded      1      20990.00
    refund                                  Gilet 4 Botones Negro Nicopoly Negro Lisa M                                      nan regular_payment             reconciled      1      10000.00
    refund                                 Gilet 4 Botones Negro Nicopoly Negro Lisa Xl                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                 Gilet 4 Botones Negro Nicopoly Negro Xl Lisa                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                                 Gilet 4 Botones Negro Nicopoly Xl Lisa Negro                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                 Gilet 4 Botones Negro Nicopoly Xl Lisa Negro                                      nan regular_payment             reconciled      1      19990.00
    refund                                  Gilet 4 Botones Rosa Nicopoly M Lisa Rosado                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                  Gilet 4 Botones Rosa Nicopoly Rosado M Lisa                                      nan regular_payment           bpp_refunded      2      40780.00
    refund                                  Gilet 4 Botones Rosa Nicopoly Rosado M Lisa                                      nan regular_payment                    nan      1      19990.00
    refund                                  Gilet 4 Botones Rosa Nicopoly Rosado S Lisa                                      nan regular_payment           bpp_refunded      2      51980.00
    refund                                 Gilet 4 Botones Rosa Nicopoly Xl Lisa Rosado                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                            Gilet 4 Botones Verde Nicopoly - Verde - Lisa - M                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                       Gilet 4 Botones Verde Nicopoly Lisa Xl                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                  Gilet 4 Botones Verde Nicopoly Verde Lisa M                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                 Gilet 4 Botones Verde Nicopoly Verde Xl Lisa                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                                        Gilet Básico 4 Botones Khaki Nicopoly                                      nan regular_payment           bpp_refunded      4     155940.00
    refund                                        Gilet Básico 4 Botones Khaki Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                                       Gilet Básico 4 Botones Morado Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                                        Gilet Básico 4 Botones Negro Nicopoly                                      nan regular_payment           bpp_refunded      2     103960.00
    refund                                        Gilet Básico 4 Botones Negro Nicopoly                                      nan regular_payment            compensated      2      46780.00
    refund                                        Gilet Básico 4 Botones Negro Nicopoly                                      nan regular_payment             reconciled      1      20790.00
    refund                                  Gilet Básico 4 Botones Rojo Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                 Gilet Básico 4 Botones Verde Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      2      51980.00
    refund                                 Gilet Básico 4 Botones Verde Oscuro Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                             Gilet Básico Ajustable Azul Nicopoly Azul L Liso                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                   Gilet Básico Ajustable Burdeo Nicopoly - Burdeo - L - Liso                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                   Gilet Básico Ajustable Burdeo Nicopoly - Burdeo - S - Liso                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                         Gilet Básico Ajustable Burdeo Nicopoly Burdeo L Liso                                      nan regular_payment             reconciled      1      28990.00
    refund                         Gilet Básico Ajustable Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                Gilet Básico Ajustable Burdeo Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      23190.00
    refund                               Gilet Básico Ajustable Burdeo Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      1      23190.00
    refund                       Gilet Básico Ajustable Celeste Nicopoly Celeste M Liso                                      nan regular_payment           bpp_refunded      2      58980.00
    refund                       Gilet Básico Ajustable Celeste Nicopoly Celeste M Liso                                      nan regular_payment             reconciled      1      28990.00
    refund                               Gilet Básico Ajustable Celeste Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      23190.00
    refund                     Gilet Básico Ajustable Negro Nicopoly - Negro - S - Liso                                      nan regular_payment             reconciled      1      22990.00
    refund                    Gilet Básico Ajustable Negro Nicopoly - Negro - Xl - Liso                                      nan regular_payment             reconciled      1      22990.00
    refund                           Gilet Básico Ajustable Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                           Gilet Básico Ajustable Negro Nicopoly Negro M Liso                                      nan regular_payment           bpp_refunded      1      17390.00
    refund                           Gilet Básico Ajustable Negro Nicopoly Negro M Liso                                      nan regular_payment             reconciled      2      52270.00
    refund                           Gilet Básico Ajustable Negro Nicopoly Negro S Liso                                      nan regular_payment           bpp_refunded      2      57980.00
    refund                          Gilet Básico Ajustable Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      4     104360.00
    refund                       Gilet Básico Ajustable Rojo Nicopoly - Rojo - M - Liso                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                       Gilet Básico Ajustable Rojo Nicopoly - Rojo - S - Liso                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                                  Gilet Básico Ajustable Rojo Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      23190.00
    refund                                  Gilet Básico Ajustable Rojo Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                             Gilet Básico Ajustable Rojo Nicopoly Rojo M Liso                                      nan regular_payment           bpp_refunded      2      45980.00
    refund                                  Gilet Básico Ajustable Rojo Nicopoly S Liso                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                          Gilet Básico Blanco Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      23190.00
    refund                                          Gilet Básico Blanco Nicopoly M Liso                                      nan regular_payment             reconciled      1      22990.00
    refund                                         Gilet Básico Blanco Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      1      23190.00
    refund                          Gilet Básico Celeste Nicopoly - Celeste - Xl - Lisa                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                                 Gilet Básico Celeste Nicopoly M Lisa Celeste                                      nan regular_payment           bpp_refunded      2      45980.00
    refund                                 Gilet Básico Gris Nicopoly - Gris - L - Lisa                                      nan regular_payment             reconciled      1      22990.00
    refund                                Gilet Básico Gris Nicopoly - Gris - Xl - Lisa                                      nan regular_payment             reconciled      1      22990.00
    refund                                      Gilet Básico Gris Nicopoly Gris Xl Lisa                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                                            Gilet Básico Gris Nicopoly S Lisa                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                      Gilet Básico Gris Nicopoly Xl Gris Lisa                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                              Gilet Básico Hilo Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      2      53980.00
    refund                              Gilet Básico Hilo Blanco Nicopoly Blanco M Liso                                      nan regular_payment             reconciled      1      21990.00
    refund                              Gilet Básico Hilo Blanco Nicopoly L Liso Blanco                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                     Gilet Básico Hilo Blanco Nicopoly M Liso                                      nan regular_payment           bpp_refunded      2      57580.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - L - Liso                                      nan regular_payment           bpp_refunded      4       5588.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - L - Liso                                      nan regular_payment             reconciled      2      31186.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - M - Liso                                      nan regular_payment             reconciled      1      13990.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - S - Liso                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - S - Liso                                      nan regular_payment            compensated      1      20000.00
    refund                              Gilet Básico Hilo Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment             reconciled      1      21924.00
    refund                              Gilet Básico Hilo Burdeo Nicopoly Burdeo S Liso                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                     Gilet Básico Hilo Burdeo Nicopoly M Liso                                      nan regular_payment           bpp_refunded      2      57580.00
    refund                            Gilet Básico Hilo Café Nicopoly - Cafe - L - Liso                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                          Gilet Básico Hilo Negro Nicopoly - Negro - L - Liso                                      nan regular_payment           bpp_refunded      2      43980.00
    refund                                Gilet Básico Hilo Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                Gilet Básico Hilo Negro Nicopoly Negro L Liso                                      nan regular_payment             reconciled      1      21990.00
    refund                                Gilet Básico Hilo Negro Nicopoly Negro M Liso                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                          Gilet Básico Rosado Nicopoly M Liso                                      nan regular_payment             reconciled      1      20290.00
    refund                                   Gilet Básico Rosado Nicopoly Rosado S Liso                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                  Gilet Básico Rosado Nicopoly Xl Liso Rosado                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                              Gilet Con Drapeado Lateral Blanco Blanco M Lisa                                      nan regular_payment           bpp_refunded      1      18890.00
    refund                              Gilet Con Drapeado Lateral Blanco Blanco S Lisa                                      nan regular_payment           bpp_refunded      3      72870.00
    refund                          Gilet Con Drapeado Lateral Negro - Negro - L - Liso                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                                Gilet Con Drapeado Lateral Negro Negro L Liso                                      nan regular_payment           bpp_refunded      3      57770.00
    refund                                Gilet Con Drapeado Lateral Negro Negro L Liso                                      nan regular_payment             reconciled      1      19990.00
    refund                                Gilet Con Drapeado Lateral Negro Negro S Liso                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                  Gilet Con Drapeado Lateral Rojo Rojo S Liso                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                    Gilet Crop Con Solapa Blanco Nicopoly - Blanco - L - Liso                                      nan regular_payment           bpp_refunded      3       7605.00
    refund                    Gilet Crop Con Solapa Blanco Nicopoly - Blanco - L - Liso                                      nan regular_payment             reconciled      1      23455.00
    refund                            Gilet Crop Con Solapa Caqui Nicopoly Khaki M Liso                                      nan regular_payment           bpp_refunded      1      19790.00
    refund                            Gilet Crop Con Solapa Caqui Nicopoly Khaki S Liso                                      nan regular_payment             reconciled      1      16990.00
    refund                                  Gilet Espalda Ajustable Azul Acero Nicopoly                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                       Gilet Espalda Ajustable Beige Nicopoly                                      nan regular_payment           bpp_refunded      4     202930.00
    refund                                       Gilet Espalda Ajustable Beige Nicopoly                                      nan regular_payment            compensated      2      57980.00
    refund                                       Gilet Espalda Ajustable Beige Nicopoly                                      nan regular_payment             reconciled      1      28990.00
    refund                                      Gilet Espalda Ajustable Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      2      57980.00
    refund                                      Gilet Espalda Ajustable Burdeo Nicopoly                                      nan regular_payment partially_bpp_refunded      1      57980.00
    refund                                       Gilet Espalda Ajustable Negro Nicopoly                                      nan regular_payment            bpp_covered      1      28990.00
    refund                                       Gilet Espalda Ajustable Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      86970.00
    refund                                       Gilet Espalda Ajustable Negro Nicopoly                                      nan regular_payment            compensated      5     144950.00
    refund                                        Gilet Espalda Ajustable Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3      86970.00
    refund               Gilet Halter Espalda Descubierta Blanco Nicopoly Blanco M Lisa                                      nan regular_payment           bpp_refunded      2      44980.00
    refund               Gilet Halter Espalda Descubierta Blanco Nicopoly Blanco S Lisa                                      nan regular_payment           bpp_refunded      1      18840.00
    refund               Gilet Halter Espalda Descubierta Blanco Nicopoly Blanco S Lisa                                      nan regular_payment                    nan      1      22990.00
    refund              Gilet Halter Espalda Descubierta Blanco Nicopoly Blanco Xl Lisa                                      nan regular_payment             reconciled      1      21990.00
    refund                 Gilet Halter Espalda Descubierta Negro Nicopoly Negro L Lisa                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                Gilet Halter Espalda Descubierta Negro Nicopoly Negro Xl Lisa                                      nan regular_payment           bpp_refunded      2      40830.00
    refund                      Gilet Halter Espalda Descubierta Negro Nicopoly Xl Lisa                                      nan regular_payment           bpp_refunded      1      23190.00
    refund                           Gilet Largo Con Botones Blanco - Blanco - M - Liso                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                 Gilet Largo Con Botones Blanco Blanco M Liso                                      nan regular_payment           bpp_refunded      5      59590.00
    refund                                 Gilet Largo Con Botones Blanco Blanco M Liso                                      nan regular_payment            compensated      1       9237.00
    refund                                 Gilet Largo Con Botones Blanco Blanco M Liso                                      nan regular_payment             reconciled      1      19471.00
    refund                                 Gilet Largo Con Botones Blanco Blanco S Liso                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                        Gilet Largo Con Botones Blanco S Liso                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                Gilet Largo Con Botones Burdeo Burdeos L Liso                                      nan regular_payment           bpp_refunded      1      20990.00
    refund                                Gilet Largo Con Botones Burdeo Burdeos M Liso                                      nan regular_payment            compensated      1      29990.00
    refund                                     Gilet Largo Con Botones Café Cafe M Liso                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                     Gilet Largo Con Botones Café Cafe S Liso                                      nan regular_payment             reconciled      1      29990.00
    refund                                   Gilet Largo Con Botones Negro Negro M Liso                                      nan regular_payment                    nan      1      29990.00
    refund                          Gilet Largo Con Botones Negro Nicopoly Negro M Liso                                      nan regular_payment           bpp_refunded      1      20990.00
    refund                         Gilet Largo Con Botones Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      1      14276.00
    refund                         Gilet Largo Con Botones Negro Nicopoly Negro Xl Liso                                      nan regular_payment             reconciled      1       6714.00
    refund                                         Gilet Largo Con Botones Negro S Liso                                      nan regular_payment           bpp_refunded      1      19192.00
    refund                                         Gilet Largo Con Botones Negro S Liso                                      nan regular_payment             reconciled      1      23990.00
    refund                                         Gilet Lazo Ajustable Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                             Gilet Lazo Ajustable Café Nicopoly Marrón S Lisa                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                              Gilet Lazo Ajustable Café Nicopoly Mocca S Liso                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                        Gilet Leopard Café Nicopoly - Cafe - Animal Print - L                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                        Gilet Leopard Café Nicopoly - Cafe - Animal Print - M                                      nan regular_payment           bpp_refunded      3      59970.00
    refund                              Gilet Leopard Café Nicopoly Cafe Animal Print L                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                              Gilet Leopard Café Nicopoly Cafe Animal Print M                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                             Gilet Mezcla Lino Beige Nicopoly                                      nan regular_payment           bpp_refunded      6     107440.00
    refund                                             Gilet Mezcla Lino Beige Nicopoly                                      nan regular_payment             reconciled      1      20990.00
    refund                                            Gilet Mezcla Lino Blanco Nicopoly                                      nan regular_payment           bpp_refunded      6     119340.00
    refund                            Gilet Mezcla Lino Celeste Nicopoly Celeste M Liso                                      nan regular_payment           bpp_refunded      2      33980.00
    refund                            Gilet Mezcla Lino Celeste Nicopoly Celeste S Liso                                      nan regular_payment           bpp_refunded      2      36980.00
    refund                         Gilet Negro Rayas Diplomáticas Nicopoly Negro S Liso                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                 Gilet Rayas Diplomáticas Blanco Nicopoly - Blanco - M - Liso                                      nan regular_payment             reconciled      1      26990.00
    refund                       Gilet Rayas Diplomáticas Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      1      22390.00
    refund                       Gilet Rayas Diplomáticas Blanco Nicopoly Blanco M Liso                                      nan regular_payment           bpp_refunded      2      47980.00
    refund                       Gilet Rayas Diplomáticas Blanco Nicopoly Blanco S Liso                                      nan regular_payment             reconciled      1      23990.00
    refund                      Gilet Rayas Diplomáticas Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                     Gilet Rayas Diplomáticas Celeste Nicopoly Celeste M Liso                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                     Gilet Rayas Diplomáticas Gris Nicopoly - Gris - M - Liso                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                           Gilet Rayas Diplomáticas Gris Nicopoly Gris L Liso                                      nan regular_payment           bpp_refunded      2      46380.00
    refund                           Gilet Rayas Diplomáticas Gris Nicopoly Gris S Liso                                      nan regular_payment           bpp_refunded      3      68770.00
    refund                                Gilet Rayas Diplomáticas Gris Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                   Gilet Sastre Entallado Blanco Nicopoly - Blanco - L - Liso                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                   Gilet Sastre Entallado Blanco Nicopoly - Blanco - M - Liso                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      4     107464.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco L Liso                                      nan regular_payment             reconciled      1      25990.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco M Liso                                      nan regular_payment           bpp_refunded      4     101360.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco M Liso                                      nan regular_payment             reconciled      1      22990.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco S Liso                                      nan regular_payment           bpp_refunded      3      80970.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco S Liso                                      nan regular_payment             reconciled      2      55980.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly S Liso Blanco                                      nan regular_payment           bpp_refunded      2      51980.00
    refund                         Gilet Sastre Entallado Burdeo Nicopoly Burdeo S Liso                                      nan regular_payment           bpp_refunded      1      26390.00
    refund                                 Gilet Sastre Entallado Negro Nicopoly L Liso                                      nan regular_payment             reconciled      1      26390.00
    refund                           Gilet Sastre Entallado Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      32990.00
    refund                                            Gilet Tejido Hilo Blanco Nicopoly                                      nan regular_payment           bpp_refunded      3      89570.00
    refund                                            Gilet Tejido Hilo Blanco Nicopoly                                      nan regular_payment            compensated      1      31990.00
    refund                                            Gilet Tejido Hilo Blanco Nicopoly                                      nan regular_payment             reconciled      2      63980.00
    refund                                            Gilet Tejido Hilo Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                                            Gilet Tejido Hilo Burdeo Nicopoly                                      nan regular_payment             reconciled      1      31990.00
    refund                                             Gilet Tejido Hilo Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      95970.00
    refund                                             Gilet Tejido Hilo Negro Nicopoly                                      nan regular_payment             reconciled      2      63980.00
    refund                      Gilet Tipo Crepé Animal Print Café Nicopoly Café L Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                     Gilet Tipo Crepé Animal Print Café Nicopoly Café Xl Lisa                                      nan regular_payment           bpp_refunded      2      35980.00
    refund                      Gilet Tipo Crepé Animal Print Café Nicopoly L Café Lisa                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                           Gilet Tipo Crepé Animal Print Café Nicopoly L Lisa                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                 Gilet Tipo Crepé Khaki Nicopoly Khaki L Liso                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                       Gilet Tipo Crepé Khaki Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                                       Gilet Tipo Crepé Negro Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1      16790.00
    refund                                 Gilet Tipo Crepé Negro Nicopoly Negro L Liso                                      nan regular_payment            compensated      1      19990.00
    refund                                Gilet Tipo Crepé Negro Nicopoly Negro Xl Liso                                      nan regular_payment                    nan      1      19990.00
    refund                     Jeans Básico Pierna Acampanada - Azul Marino - Liso - 40                                      nan regular_payment             reconciled      1      32990.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 36                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 38                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 40                                      nan regular_payment           bpp_refunded      3     113970.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 40                                      nan regular_payment             reconciled      1      33590.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 42                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                          Jeans Básico Pierna Ancha - Azul Marino - Liso - 42                                      nan regular_payment             reconciled      1      33990.00
    refund                                Jeans Básico Pierna Ancha Azul Marino Liso 36                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                Jeans Básico Pierna Ancha Azul Marino Liso 38                                      nan regular_payment           bpp_refunded      2      53980.00
    refund                                Jeans Básico Pierna Ancha Azul Marino Liso 40                                      nan regular_payment           bpp_refunded      2      68980.00
    refund                                Jeans Básico Pierna Ancha Azul Marino Liso 40                                      nan regular_payment             reconciled      1      19990.00
    refund                                      Jeans Básico Recto Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      8     181756.00
    refund                                      Jeans Básico Recto Azul Marino Nicopoly                                      nan regular_payment             reconciled      6     143157.00
    refund                                            Jeans Básico Recto Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     205920.00
    refund                                            Jeans Básico Recto Negro Nicopoly                                      nan regular_payment         not_reconciled      1      24990.00
    refund                                            Jeans Básico Recto Negro Nicopoly                                      nan regular_payment             reconciled      3      83970.00
    refund                                 Jeans Corte Barrel Azul Nicopoly Azul Liso M                                      nan regular_payment           bpp_refunded      1      44990.00
    refund                                  Jeans Corte Recto Café Nicopoly Café Liso L                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                                  Jeans Corte Recto Café Nicopoly Café Liso S                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                  Jeans Corte Recto Café Nicopoly Café Liso S                                      nan regular_payment             reconciled      1      39990.00
    refund                                Jeans Corte Recto Khaki Nicopoly Khaki Liso L                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                             Jeans Flare Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      4      34173.00
    refund                                             Jeans Flare Azul Marino Nicopoly                                      nan regular_payment             reconciled      2      39924.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly 36 Azul Liso                                      nan regular_payment             reconciled      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly 38 Azul Liso                                      nan regular_payment           bpp_refunded      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly 42 Azul Liso                                      nan regular_payment           bpp_refunded      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 34                                      nan regular_payment             reconciled      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 36                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 36                                      nan regular_payment             reconciled      3      95970.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 38                                      nan regular_payment           bpp_refunded      3      86970.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 38                                      nan regular_payment             reconciled      5     163150.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 40                                      nan regular_payment           bpp_refunded      2      74980.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 40                                      nan regular_payment             reconciled      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 42                                      nan regular_payment           bpp_refunded      4     133160.00
    refund                                  Jeans Pierna Wide Leg Azul Nicopoly Liso 36                                      nan regular_payment           bpp_refunded      1      32990.00
    refund                                  Jeans Pierna Wide Leg Azul Nicopoly Liso 38                                      nan regular_payment             reconciled      2      65980.00
    refund                                  Jeans Pierna Wide Leg Azul Nicopoly Liso 40                                      nan regular_payment           bpp_refunded      2      74980.00
    refund                                  Jeans Pierna Wide Leg Azul Nicopoly Liso 40                                      nan regular_payment             reconciled      1      41990.00
    refund                                                  Jeans Recto Rosado Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                            Jeans Rectos Tiro Alto Café Nicopoly Café Liso 34                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                            Jeans Rectos Tiro Alto Café Nicopoly Café Liso 38                                      nan regular_payment           bpp_refunded      2      83980.00
    refund                            Jeans Rectos Tiro Alto Café Nicopoly Café Liso 38                                      nan regular_payment             reconciled      1      41990.00
    refund                            Jeans Rectos Tiro Alto Café Nicopoly Café Liso 42                                      nan regular_payment           bpp_refunded      1      33990.00
    refund                         Jeans Wide Leg Blancos Nicopoly - Blanco - Liso - 42                                      nan regular_payment             reconciled      1      32990.00
    refund                               Jeans Wide Leg Blancos Nicopoly 42 Liso Blanco                                      nan regular_payment           bpp_refunded      1      32990.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 38                                      nan regular_payment           bpp_refunded      1      25190.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 40                                      nan regular_payment           bpp_refunded      3      92970.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 40                                      nan regular_payment                    nan      1      32990.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 40                                      nan regular_payment             reconciled      1      29990.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 42                                      nan regular_payment           bpp_refunded      3      92970.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 42                                      nan regular_payment             reconciled      1      32990.00
    refund                                      Jeans Wide Leg Blancos Nicopoly Liso 38                                      nan regular_payment           bpp_refunded      1      41990.00
    refund                              Kimono Negro Detalles Flecos Nicopoly Negro M/l                                      nan regular_payment            compensated      1      29990.00
    refund                             Legging Ecocuero Cierre Lateral Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                 Legging Tiro Alto Aberturas Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                              Maxi Vestido Corte Imperio Floral Azul Nicopoly                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                              Maxi Vestido Corte Imperio Floral Azul Nicopoly                                      nan regular_payment             reconciled      3     114970.00
    refund                                   Maxi Vestido Tajo Y Costuras Café Nicopoly                                      nan regular_payment            compensated      1      16990.00
    refund                                   Maxi Vestido Tajo Y Costuras Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                                            Mini Falda Leopardo Café Nicopoly                                      nan regular_payment           bpp_refunded      7     106924.00
    refund                                            Mini Falda Leopardo Café Nicopoly                                      nan regular_payment             reconciled      2      40470.00
    refund                                       Minifalda Ecocuero Tajo Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      40980.00
    refund                                       Minifalda Ecocuero Tajo Negro Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                          Pantalón Básico Blanco Nicopoly - Blanco - Liso - L                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                          Pantalón Básico Blanco Nicopoly - Blanco - Liso - S                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                         Pantalón Básico Blanco Nicopoly - Blanco - Liso - Xl                                      nan regular_payment             reconciled      1      27990.00
    refund                                Pantalón Básico Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                Pantalón Básico Blanco Nicopoly Blanco Liso L                                      nan regular_payment             reconciled      1      24490.00
    refund                                Pantalón Básico Blanco Nicopoly Blanco Liso M                                      nan regular_payment             reconciled      1      34990.00
    refund                                       Pantalón Básico Blanco Nicopoly Liso M                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                    Pantalón Básico Café Nicopoly Café Liso M                                      nan regular_payment           bpp_refunded      2      75980.00
    refund                                    Pantalón Básico Café Nicopoly Café Liso S                                      nan regular_payment           bpp_refunded      1      37990.00
    refund                                   Pantalón Básico Café Nicopoly Café Liso Xl                                      nan regular_payment           bpp_refunded      1      37990.00
    refund                        Pantalón Básico Celeste Nicopoly - Celeste - Liso - S                                      nan regular_payment           bpp_refunded      2      55980.00
    refund                              Pantalón Básico Celeste Nicopoly Celeste Liso M                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                      Pantalón Básico Celeste Nicopoly Liso M                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                    Pantalón Básico Gris Nicopoly Gris Liso L                                      nan regular_payment           bpp_refunded      1      24490.00
    refund                                    Pantalón Básico Gris Nicopoly Gris Liso M                                      nan regular_payment           bpp_refunded      1      24490.00
    refund                                    Pantalón Básico Gris Nicopoly L Gris Liso                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                         Pantalón Básico Gris Nicopoly Liso L                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                         Pantalón Básico Gris Nicopoly Liso M                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                    Pantalón Básico Gris Nicopoly M Gris Liso                                      nan regular_payment             reconciled      1      27990.00
    refund                            Pantalón Básico Khaki Nicopoly - Khaki - Liso - M                                      nan regular_payment           bpp_refunded      1      15000.00
    refund                            Pantalón Básico Khaki Nicopoly - Khaki - Liso - M                                      nan regular_payment             reconciled      1      12990.00
    refund                                  Pantalón Básico Khaki Nicopoly Khaki Liso S                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                        Pantalón Básico Khaki Nicopoly Liso M                                      nan regular_payment           bpp_refunded      2      62980.00
    refund                                Pantalón Básico Morado Nicopoly Morado Liso L                                      nan regular_payment           bpp_refunded      2      72980.00
    refund                                Pantalón Básico Morado Nicopoly Morado Liso M                                      nan regular_payment           bpp_refunded      2      58980.00
    refund                                Pantalón Básico Morado Nicopoly Morado Liso S                                      nan regular_payment           bpp_refunded      2      72980.00
    refund                               Pantalón Básico Morado Nicopoly Morado Liso Xl                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                        Pantalón Básico Negro Nicopoly Liso L                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                        Pantalón Básico Negro Nicopoly Liso L                                      nan regular_payment             reconciled      1      27990.00
    refund                                        Pantalón Básico Negro Nicopoly Liso M                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                        Pantalón Básico Negro Nicopoly Liso S                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                        Pantalón Básico Negro Nicopoly Liso S                                      nan regular_payment             reconciled      1      20000.00
    refund                                       Pantalón Básico Negro Nicopoly Liso Xl                                      nan regular_payment           bpp_refunded      2      69980.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      1      37990.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso L                                      nan regular_payment             reconciled      2      69980.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso M                                      nan regular_payment             reconciled      1      34990.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                 Pantalón Básico Negro Nicopoly Negro Liso Xl                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                 Pantalón Básico Negro Nicopoly Negro Liso Xl                                      nan regular_payment             reconciled      1      34990.00
    refund                                  Pantalón Básico Pierna Ancha Beige Nicopoly                                      nan regular_payment           bpp_refunded      2      57180.00
    refund                                  Pantalón Básico Pierna Ancha Beige Nicopoly                                      nan regular_payment             reconciled      2      56730.00
    refund                       Pantalón Básico Pierna Ancha Gris Nicopoly Gris Liso L                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                       Pantalón Básico Pierna Ancha Gris Nicopoly Gris Liso M                                      nan regular_payment                    nan      1      28990.00
    refund                            Pantalón Básico Pierna Ancha Gris Nicopoly Liso S                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                                  Pantalón Básico Pierna Ancha Khaki Nicopoly                                      nan regular_payment           bpp_refunded      4     124710.00
    refund                                  Pantalón Básico Pierna Ancha Khaki Nicopoly                                      nan regular_payment             reconciled      1      27740.00
    refund                   Pantalón Básico Pierna Ancha Marrón Nicopoly Marrón Lisa S                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                                  Pantalón Básico Pierna Ancha Negro Nicopoly                                      nan regular_payment           bpp_refunded      4     133960.00
    refund                                  Pantalón Básico Pierna Ancha Negro Nicopoly                                      nan regular_payment             reconciled      7     204233.00
    refund                              Pantalón Básico Rojo Nicopoly - Rojo - Liso - L                                      nan regular_payment             reconciled      1      27990.00
    refund                              Pantalón Básico Rojo Nicopoly - Rojo - Liso - M                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                         Pantalón Básico Rojo Nicopoly Liso M                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                    Pantalón Básico Rojo Nicopoly Rojo Liso L                                      nan regular_payment           bpp_refunded      2      49980.00
    refund                                    Pantalón Básico Rojo Nicopoly Rojo Liso L                                      nan regular_payment             reconciled      1      20990.00
    refund                           Pantalón Básico Rosa Nicopoly - Rosado - Liso - Xl                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                                  Pantalón Básico Rosa Nicopoly Rosado Liso L                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                  Pantalón Básico Rosa Nicopoly Rosado Liso M                                      nan regular_payment           bpp_refunded      4     132960.00
    refund                                  Pantalón Básico Rosa Nicopoly Rosado Liso S                                      nan regular_payment             reconciled      1      34990.00
    refund                                 Pantalón Básico Rosa Nicopoly Rosado Liso Xl                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                  Pantalón Básico Verde Nicopoly Verde Liso L                                      nan regular_payment           bpp_refunded      3     104970.00
    refund                                  Pantalón Básico Verde Nicopoly Verde Liso M                                      nan regular_payment           bpp_refunded      1      34990.00
    refund                                 Pantalón Básico Verde Nicopoly Verde Liso Xl                                      nan regular_payment           bpp_refunded      2      55980.00
    refund                                              Pantalón Carrot Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                               Pantalón Carrot Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      31490.00
    refund                                               Pantalón Carrot Khaki Nicopoly                                      nan regular_payment             reconciled      1      29390.00
    refund                                               Pantalón Carrot Negro Nicopoly                                      nan regular_payment           bpp_refunded      5     159553.00
    refund                    Pantalón Con Costuras Frontales Recto Azul Acero Nicopoly                                      nan regular_payment           bpp_refunded      6     106950.00
    refund                       Pantalón Con Costuras Frontales Recto Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      7     157940.00
    refund                       Pantalón Con Costuras Frontales Recto Burdeos Nicopoly                                      nan regular_payment             reconciled      2      43920.00
    refund                        Pantalón Con Costuras Frontales Recto Lúcuma Nicopoly                                      nan regular_payment           bpp_refunded      6     127950.00
    refund                                    Pantalón Con Pinzas Recto Blanco Nicopoly                                      nan regular_payment           bpp_refunded      4     119160.00
    refund                                    Pantalón Con Pinzas Recto Blanco Nicopoly                                      nan regular_payment partially_bpp_refunded      1      75980.00
    refund                                    Pantalón Con Pinzas Recto Blanco Nicopoly                                      nan regular_payment             reconciled      1      28790.00
    refund                                   Pantalón Con Pinzas Recto Celeste Nicopoly                                      nan regular_payment            bpp_covered      1      21590.00
    refund                                   Pantalón Con Pinzas Recto Celeste Nicopoly                                      nan regular_payment           bpp_refunded     11     310090.00
    refund                                   Pantalón Con Pinzas Recto Celeste Nicopoly                                      nan regular_payment             reconciled      1      28990.00
    refund                                     Pantalón Con Pinzas Recto Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      49470.00
    refund                                    Pantalón Con Pinzas Recto Rosado Nicopoly                                      nan regular_payment           bpp_refunded      4     111960.00
    refund                                    Pantalón Con Pinzas Recto Rosado Nicopoly                                      nan regular_payment             reconciled      1      28990.00
    refund                            Pantalón Costuras Frontales Recto Lúcuma Nicopoly                                      nan regular_payment           bpp_refunded      4      81800.00
    refund                              Pantalón Costuras Frontales Recto Rosa Nicopoly                                      nan regular_payment           bpp_refunded      5     112950.00
    refund                              Pantalón Costuras Frontales Recto Rosa Nicopoly                                      nan regular_payment             reconciled      2      45980.00
    refund         Pantalón De Pierna Recta Raya Diplomática Blanco - Blanco - Liso - L                                      nan regular_payment           bpp_refunded      2      61180.00
    refund         Pantalón De Pierna Recta Raya Diplomática Blanco - Blanco - Liso - M                                      nan regular_payment             reconciled      1      35990.00
    refund               Pantalón De Pierna Recta Raya Diplomática Blanco Blanco Liso S                                      nan regular_payment           bpp_refunded      1      37990.00
    refund      Pantalón De Pierna Recta Raya Diplomática Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment           bpp_refunded      2      75980.00
    refund             Pantalón De Pierna Recta Raya Diplomática Celeste Celeste Liso L                                      nan regular_payment           bpp_refunded      1      26990.00
    refund             Pantalón De Pierna Recta Raya Diplomática Gris - Gris - Liso - M                                      nan regular_payment           bpp_refunded      1      35990.00
    refund             Pantalón De Pierna Recta Raya Diplomática Gris - Gris - Liso - S                                      nan regular_payment           bpp_refunded      1      25190.00
    refund                   Pantalón De Pierna Recta Raya Diplomática Gris Gris Liso M                                      nan regular_payment           bpp_refunded      1      25190.00
    refund                   Pantalón De Pierna Recta Raya Diplomática Gris Gris Liso M                                      nan regular_payment             reconciled      1      35990.00
    refund                   Pantalón De Pierna Recta Raya Diplomática Gris Gris Liso S                                      nan regular_payment           bpp_refunded      2      63180.00
    refund                        Pantalón De Pierna Recta Raya Diplomática Gris Liso L                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                        Pantalón De Pierna Recta Raya Diplomática Gris Liso M                                      nan regular_payment           bpp_refunded      1      35990.00
    refund        Pantalón De Pierna Recta Raya Diplomática Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      1      37990.00
    refund        Pantalón De Pierna Recta Raya Diplomática Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      37990.00
    refund       Pantalón De Pierna Recta Raya Diplomática Negro Nicopoly Negro Liso Xl                                      nan regular_payment           bpp_refunded      1      37990.00
    refund                                Pantalón Dos Botones Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      21590.00
    refund                                        Pantalón Dos Botones Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      49980.00
    refund                     Pantalón Dos Botones Rosado Nicopoly - Rosado - Liso - M                                      nan regular_payment           bpp_refunded      1      25190.00
    refund                       Pantalón Dos Botones Verde Oliva Nicopoly Oliva Liso M                                      nan regular_payment           bpp_refunded      2      55980.00
    refund   Pantalón Entallado Costuras Delanteras Blanco Nicopoly - Blanco - Liso - S                                      nan regular_payment           bpp_refunded      1      25990.00
    refund         Pantalón Entallado Costuras Delanteras Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      19790.00
    refund             Pantalón Entallado Costuras Delanteras Café Nicopoly Café Liso L                                      nan regular_payment           bpp_refunded      2      45980.00
    refund             Pantalón Entallado Costuras Delanteras Café Nicopoly Café Liso S                                      nan regular_payment           bpp_refunded      1      22990.00
    refund       Pantalón Entallado Costuras Delanteras Celeste Nicopoly Celeste Liso M                                      nan regular_payment             reconciled      1      25990.00
    refund             Pantalón Entallado Costuras Delanteras Gris Nicopoly Gris Liso L                                      nan regular_payment           bpp_refunded      1      22990.00
    refund             Pantalón Entallado Costuras Delanteras Gris Nicopoly Gris Liso M                                      nan regular_payment           bpp_refunded      2      42780.00
    refund                          Pantalón Estampado Cebra Café Nicopoly Café Liso Xl                                      nan regular_payment           bpp_refunded      3      55970.00
    refund           Pantalón Estilo Japonés Pierna Ancha Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment           bpp_refunded      1      35990.00
    refund           Pantalón Estilo Japonés Pierna Ancha Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment             reconciled      1      35990.00
    refund          Pantalón Estilo Japonés Pierna Ancha Burdeo Nicopoly Burdeo Liso Xl                                      nan regular_payment           bpp_refunded      1      35990.00
    refund               Pantalón Estilo Japonés Pierna Ancha Café Nicopoly Café Liso L                                      nan regular_payment           bpp_refunded      1      35990.00
    refund              Pantalón Estilo Japonés Pierna Ancha Café Nicopoly Café Liso Xl                                      nan regular_payment            compensated      1      44990.00
    refund             Pantalón Estilo Japonés Pierna Ancha Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      5      91532.00
    refund             Pantalón Estilo Japonés Pierna Ancha Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      1      35990.00
    refund            Pantalón Estilo Japonés Pierna Ancha Negro Nicopoly Negro Liso Xl                                      nan regular_payment           bpp_refunded      2      80980.00
    refund            Pantalón Estilo Japonés Pierna Ancha Negro Nicopoly Negro Liso Xl                                      nan regular_payment                    nan      1      35990.00
    refund                                Pantalón Holgado Pretina Alta Blanco Nicopoly                                      nan regular_payment           bpp_refunded      2      41980.00
    refund                                Pantalón Holgado Pretina Alta Blanco Nicopoly                                      nan regular_payment             reconciled      2      41980.00
    refund                                       Pantalón Lazo De Hebilla Café Nicopoly                                      nan regular_payment           bpp_refunded      2      90980.00
    refund                                       Pantalón Lazo De Hebilla Café Nicopoly                                      nan regular_payment                    nan      1      40490.00
    refund                                       Pantalón Lazo De Hebilla Café Nicopoly                                      nan regular_payment             reconciled      3     118470.00
    refund                                      Pantalón Lazo De Hebilla Khaki Nicopoly                                      nan regular_payment           bpp_refunded      2      96102.00
    refund                                      Pantalón Lazo De Hebilla Khaki Nicopoly                                      nan regular_payment             reconciled      1      36990.00
    refund                            Pantalón Leopardo Café Nicopoly - Café - Liso - L                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                            Pantalón Leopardo Café Nicopoly - Café - Liso - M                                      nan regular_payment           bpp_refunded      3      77970.00
    refund                                  Pantalón Leopardo Café Nicopoly Café Liso L                                      nan regular_payment           bpp_refunded      1      18190.00
    refund                                  Pantalón Leopardo Café Nicopoly Café Liso M                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                 Pantalón Leopardo Café Nicopoly Café Liso Xl                                      nan regular_payment             reconciled      1      19990.00
    refund                                          Pantalón Mezcla Lino Beige Nicopoly                                      nan regular_payment           bpp_refunded      8     195920.00
    refund                                          Pantalón Mezcla Lino Beige Nicopoly                                      nan regular_payment             reconciled      3      69001.00
    refund                                         Pantalón Mezcla Lino Blanco Nicopoly                                      nan regular_payment           bpp_refunded      4     106960.00
    refund                                         Pantalón Mezcla Lino Blanco Nicopoly                                      nan regular_payment             reconciled      2      48980.00
    refund                         Pantalón Mezcla Lino Celeste Nicopoly Celeste Liso M                                      nan regular_payment            bpp_covered      3      49419.00
    refund                         Pantalón Mezcla Lino Celeste Nicopoly Celeste Liso S                                      nan regular_payment           bpp_refunded      2      43980.00
    refund                                Pantalón Negro Flores Blancas Nicopoly Lisa L                                      nan regular_payment           bpp_refunded      2      49980.00
    refund                                Pantalón Negro Flores Blancas Nicopoly Lisa M                                      nan regular_payment             reconciled      1      24990.00
    refund                          Pantalón Negro Flores Blancas Nicopoly Negro Lisa M                                      nan regular_payment           bpp_refunded      3      49970.00
    refund                          Pantalón Negro Flores Blancas Nicopoly Negro Lisa S                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                Pantalón Palazzo Lazo Frontal Blanco Nicopoly                                      nan regular_payment             reconciled      1      37990.00
    refund                                         Pantalón Palazzo Tajos Café Nicopoly                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                                         Pantalón Palazzo Tajos Café Nicopoly                                      nan regular_payment             reconciled      1      26990.00
    refund                                      Pantalón Palazzo Tajos Magenta Nicopoly                                      nan regular_payment            bpp_covered      1      26990.00
    refund                                      Pantalón Palazzo Tajos Magenta Nicopoly                                      nan regular_payment           bpp_refunded     12     358989.00
    refund                                      Pantalón Palazzo Tajos Magenta Nicopoly                                      nan regular_payment             reconciled      2      43481.00
    refund                       Pantalón Palazzo Tajos Mostaza Nicopoly M Liso Mostaza                                      nan regular_payment           bpp_refunded      1      36990.00
    refund                       Pantalón Palazzo Tajos Mostaza Nicopoly Mostaza Liso L                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                      Pantalón Palazzo Tajos Mostaza Nicopoly Mostaza Liso Xl                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                                        Pantalón Palazzo Tajos Negro Nicopoly                                      nan regular_payment           bpp_refunded     13     338900.00
    refund                                        Pantalón Palazzo Tajos Negro Nicopoly                                      nan regular_payment             reconciled      3     100970.00
    refund                                        Pantalón Palazzo Tajos Verde Nicopoly                                      nan regular_payment           bpp_refunded      5     100600.00
    refund                                        Pantalón Palazzo Tajos Verde Nicopoly                                      nan regular_payment             reconciled      5     132510.00
    refund                                        Pantalón Pierna Ancha Blanco Nicopoly                                      nan regular_payment             reconciled      1      26490.00
    refund                                       Pantalón Pierna Ancha Celeste Nicopoly                                      nan regular_payment           bpp_refunded      4     103460.00
    refund                             Pantalón Pierna Ancha Con Pasador Khaki Nicopoly                                      nan regular_payment            bpp_covered      1      34990.00
    refund                             Pantalón Pierna Ancha Con Pasador Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      26240.00
    refund                             Pantalón Pierna Ancha Con Pasador Khaki Nicopoly                                      nan regular_payment             reconciled      1      26240.00
    refund                            Pantalón Pierna Ancha Con Pasador Morado Nicopoly                                      nan regular_payment           bpp_refunded      3      82220.00
    refund                            Pantalón Pierna Ancha Con Pasador Morado Nicopoly                                      nan regular_payment            compensated      1      27292.00
    refund                            Pantalón Pierna Ancha Con Pasador Morado Nicopoly                                      nan regular_payment             reconciled      3      79772.00
    refund                             Pantalón Pierna Ancha Con Pasador Negro Nicopoly                                      nan regular_payment            bpp_covered      1      34990.00
    refund                             Pantalón Pierna Ancha Con Pasador Negro Nicopoly                                      nan regular_payment           bpp_refunded      4     125960.00
    refund                             Pantalón Pierna Ancha Con Pasador Negro Nicopoly                                      nan regular_payment             reconciled      1      34990.00
    refund                       Pantalón Pierna Ancha Con Pasador Rojo Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      3      97970.00
    refund                                         Pantalón Pierna Ancha Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                                         Pantalón Pierna Ancha Khaki Nicopoly                                      nan regular_payment             reconciled      1      32990.00
    refund                                         Pantalón Pierna Ancha Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      16490.00
    refund                                          Pantalón Pierna Ancha Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2      49980.00
    refund                                          Pantalón Pierna Ancha Rojo Nicopoly                                      nan regular_payment             reconciled      1      26990.00
    refund                                           Pantalón Pierna Ancha Rojonicopoly                                      nan regular_payment           bpp_refunded      2      46480.00
    refund                                       Pantalón Pinzas Recto Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      5     115950.00
    refund                                       Pantalón Pinzas Recto Burdeos Nicopoly                                      nan regular_payment             reconciled      2      47980.00
    refund                                          Pantalón Pinzas Recto Gris Nicopoly                                      nan regular_payment           bpp_refunded      3      68950.00
    refund                                         Pantalón Pinzas Recto Óxido Nicopoly                                      nan regular_payment           bpp_refunded      3      51970.00
    refund                                         Pantalón Pinzas Recto Óxido Nicopoly                                      nan regular_payment             reconciled      1      16980.00
    refund                                    Pantalón Pinzas Tiro Alto Blanco Nicopoly                                      nan regular_payment           bpp_refunded      3      75970.00
    refund                                    Pantalón Pinzas Tiro Alto Blanco Nicopoly                                      nan regular_payment             reconciled      1      21990.00
    refund                                   Pantalón Pinzas Tiro Alto Celeste Nicopoly                                      nan regular_payment           bpp_refunded      3      68970.00
    refund                                     Pantalón Pinzas Tiro Alto Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1      19190.00
    refund                                     Pantalón Pinzas Tiro Alto Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                      Pantalón Pinzas Tiro Alto Rojo Nicopoly                                      nan regular_payment             reconciled      1      24990.00
    refund                                Pantalón Pretina Ancha Azul Grisáceo Nicopoly                                      nan regular_payment             reconciled      1      20990.00
    refund                                  Pantalón Pretina Ancha Verde Musgo Nicopoly                                      nan regular_payment           bpp_refunded      2      41980.00
    refund                                  Pantalón Pretina Ancha Verde Musgo Nicopoly                                      nan regular_payment             reconciled      2      41980.00
    refund                                      Pantalón Recto Botones Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      2      42100.00
    refund                           Pantalón Recto Con Pinza Azul Nicopoly Azul Liso L                                      nan regular_payment           bpp_refunded      1      75980.00
    refund                        Pantalón Recto Con Pinza Oliva Nicopoly Oliva Liso Xl                                      nan regular_payment           bpp_refunded      1      37990.00
    refund                                Pantalón Recto Con Pinzas Azul Acero Nicopoly                                      nan regular_payment           bpp_refunded      6     185740.00
    refund                                Pantalón Recto Con Pinzas Azul Acero Nicopoly                                      nan regular_payment                    nan      1      35990.00
    refund                                Pantalón Recto Con Pinzas Azul Acero Nicopoly                                      nan regular_payment             reconciled      2      62980.00
    refund                                     Pantalón Recto Con Pinzas Beige Nicopoly                                      nan regular_payment           bpp_refunded      2      50380.00
    refund                                     Pantalón Recto Con Pinzas Beige Nicopoly                                      nan regular_payment             reconciled      1      35990.00
    refund                                    Pantalón Recto Con Pinzas Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      5     172750.00
    refund                                    Pantalón Recto Con Pinzas Burdeo Nicopoly                                      nan regular_payment            compensated      4     129560.00
    refund                                    Pantalón Recto Con Pinzas Burdeo Nicopoly                                      nan regular_payment                    nan      2      57580.00
    refund                                    Pantalón Recto Con Pinzas Burdeo Nicopoly                                      nan regular_payment             reconciled      1      35990.00
    refund                                     Pantalón Recto Con Pinzas Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     271720.00
    refund                                     Pantalón Recto Con Pinzas Negro Nicopoly                                      nan regular_payment            compensated      1      35990.00
    refund                                     Pantalón Recto Con Pinzas Negro Nicopoly                                      nan regular_payment             reconciled      2      62980.00
    refund                                     Pantalón Recto Con Pinzas Negro Nicopoly                                      nan regular_payment   refund_account_money      1      26990.00
    refund                                      Pantalón Recto Con Pinzas Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3     100970.00
    refund                             Pantalón Recto Costura Frontal  Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      37980.00
    refund                              Pantalón Recto Costura Frontal Burdeos Nicopoly                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                                Pantalón Recto Costura Frontal Negro Nicopoly                                      nan regular_payment           bpp_refunded      4      67868.00
    refund                                Pantalón Recto Costura Frontal Negro Nicopoly                                      nan regular_payment             reconciled      3      61996.00
    refund                                    Pantalón Recto Rayas Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                        Pantalón Sastrero Recto Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                        Pantalón Sastrero Recto Blanco Nicopoly Blanco Liso L                                      nan regular_payment             reconciled      1      31990.00
    refund                        Pantalón Sastrero Recto Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                            Pantalón Sastrero Recto Café Nicopoly Café Liso M                                      nan regular_payment           bpp_refunded      1      31990.00
    refund             Pantalón Tipo Crepé Ajustable Khaki Nicopoly - Khaki - Lisa - Xl                                      nan regular_payment             reconciled      1      23990.00
    refund                    Pantalón Tipo Crepé Ajustable Khaki Nicopoly Khaki Lisa M                                      nan regular_payment                    nan      1      17990.00
    refund                    Pantalón Tipo Crepé Ajustable Khaki Nicopoly Khaki Lisa S                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                   Pantalón Tipo Crepé Ajustable Khaki Nicopoly Khaki Lisa Xl                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                    Pantalón Tipo Crepé Ajustable Khaki Nicopoly L Lisa Khaki                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                          Pantalón Tipo Crepé Ajustable Negro Nicopoly Lisa M                                      nan regular_payment           bpp_refunded      1      16790.00
    refund                                    Pantalón Tiro Alto Básico Blanco Nicopoly                                      nan regular_payment           bpp_refunded      4      85650.00
    refund                                    Pantalón Tiro Alto Básico Blanco Nicopoly                                      nan regular_payment             reconciled      1      20990.00
    refund                                   Pantalón Tiro Alto Básico Celeste Nicopoly                                      nan regular_payment           bpp_refunded      7     140480.00
    refund                                   Pantalón Tiro Alto Básico Celeste Nicopoly                                      nan regular_payment             reconciled      2      41980.00
    refund                                     Pantalón Tiro Alto Básico Khaki Nicopoly                                      nan regular_payment            bpp_covered      1      20990.00
    refund                                     Pantalón Tiro Alto Básico Khaki Nicopoly                                      nan regular_payment           bpp_refunded     15     306150.00
    refund                                     Pantalón Tiro Alto Básico Khaki Nicopoly                                      nan regular_payment             reconciled      2      41980.00
    refund                                     Pantalón Tiro Alto Básico Negro Nicopoly                                      nan regular_payment           bpp_refunded      7     243330.00
    refund                                     Pantalón Tiro Alto Básico Negro Nicopoly                                      nan regular_payment             reconciled      1      17490.00
    refund                                      Pantalón Tiro Alto Básico Rojo Nicopoly                                      nan regular_payment           bpp_refunded     11     226340.00
    refund                                      Pantalón Tiro Alto Básico Rojo Nicopoly                                      nan regular_payment             reconciled      3      62970.00
    refund                                  Pantalón Tiro Alto Jaspeado Blanco Nicopoly                                      nan regular_payment           bpp_refunded      5      85950.00
    refund                                 Pantalón Tiro Alto Jaspeado Celeste Nicopoly                                      nan regular_payment           bpp_refunded      5      82950.00
    refund                                 Pantalón Tiro Alto Jaspeado Celeste Nicopoly                                      nan regular_payment             reconciled      1      19490.00
    refund                                  Pantalón Tiro Alto Jaspeado Rosado Nicopoly                                      nan regular_payment           bpp_refunded      3      50970.00
    refund                                  Pantalón Tiro Alto Jaspeado Rosado Nicopoly                                      nan regular_payment             reconciled      1      22944.00
    refund                            Pantalón Vestir Costuras Frontales Camel Nicopoly                                      nan regular_payment           bpp_refunded      2      35980.00
    refund                            Pantalón Vestir Costuras Frontales Camel Nicopoly                                      nan regular_payment             reconciled      1      20990.00
    refund                            Pantalón Vestir Costuras Frontales Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      19790.00
    refund                            Pantalón Vestir Costuras Frontales Negro Nicopoly                                      nan regular_payment                    nan      1      32990.00
    refund                                 Pantalón Vestir Recto Blanco Nicopoly Liso M                                      nan regular_payment           bpp_refunded      1      28790.00
    refund                                 Pantalón Vestir Recto Blanco Nicopoly Liso M                                      nan regular_payment             reconciled      1      35990.00
    refund                                 Pantalón Vestir Recto Blanco Nicopoly Liso S                                      nan regular_payment           bpp_refunded      1      28790.00
    refund                                 Pantalón Vestir Recto Blanco Nicopoly Liso S                                      nan regular_payment             reconciled      1      28790.00
    refund                         Pantalón Vestir Recto Blanco Nicopoly Xl Liso Blanco                                      nan regular_payment             reconciled      1      23390.00
    refund                          Pantalón Vestir Recto Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment           bpp_refunded      1      38990.00
    refund                          Pantalón Vestir Recto Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment             reconciled      1      38990.00
    refund                        Pantalón Vestir Recto Café Nicopoly - Café - Liso - L                                      nan regular_payment             reconciled      1      35990.00
    refund                        Pantalón Vestir Recto Café Nicopoly - Café - Liso - S                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso L                                      nan regular_payment           bpp_refunded      4     152960.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso L                                      nan regular_payment                    nan      1      35990.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso M                                      nan regular_payment           bpp_refunded      3      86370.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso M                                      nan regular_payment             reconciled      1      35990.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso S                                      nan regular_payment           bpp_refunded      3      71570.00
    refund                             Pantalón Vestir Recto Café Nicopoly Café Liso Xl                                      nan regular_payment           bpp_refunded      1      23390.00
    refund                      Pantalón Vestir Recto Khaki Nicopoly - Khaki - Liso - L                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly Khaki Liso M                                      nan regular_payment           bpp_refunded      3      83970.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly Khaki Liso S                                      nan regular_payment           bpp_refunded      2      48380.00
    refund                           Pantalón Vestir Recto Khaki Nicopoly Khaki Liso Xl                                      nan regular_payment           bpp_refunded      1      23390.00
    refund                                  Pantalón Vestir Recto Khaki Nicopoly Liso M                                      nan regular_payment           bpp_refunded      2      61180.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly M Liso Khaki                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly S Liso Khaki                                      nan regular_payment           bpp_refunded      1      23390.00
    refund                            Pantalón Vestir Recto Mocca Nicopoly Mocca Liso L                                      nan regular_payment           bpp_refunded      1      38990.00
    refund                            Pantalón Vestir Recto Mocca Nicopoly Mocca Liso S                                      nan regular_payment           bpp_refunded      1      38990.00
    refund                    Parka Acolchada Bolsillos Grandes Celeste Pastel Nicopoly                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                              Parka Acolchada Midi Con Gorro Celeste Nicopoly                                      nan regular_payment           bpp_refunded      3      91470.00
    refund                              Parka Acolchada Midi Con Gorro Celeste Nicopoly                                      nan regular_payment             reconciled      5     137465.00
    refund                                Parka Acolchada Midi Con Gorro Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      91980.00
    refund                                 Parka Corta Acolchada Azul Grisáceo Nicopoly                                      nan regular_payment           bpp_refunded      2      56980.00
    refund                                 Parka Corta Acolchada Azul Grisáceo Nicopoly                                      nan regular_payment             reconciled      2      59980.00
    refund                               Parka Corta Acolchada Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      3      95970.00
    refund                               Parka Corta Acolchada Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      29990.00
    refund                                          Parka Corta Acolchada Café Nicopoly                                      nan regular_payment           bpp_refunded     15     298753.00
    refund                                          Parka Corta Acolchada Café Nicopoly                                      nan regular_payment             reconciled      6     177659.00
    refund                             Parka Corta Quilt Con Gorro Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                             Parka Corta Quilt Con Gorro Azul Marino Nicopoly                                      nan regular_payment             reconciled      2      37980.00
    refund                                   Parka Corta Quilt Con Gorro Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      28490.00
    refund                                    Parka Corta Quilt Con Gorro Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      28490.00
    refund                                    Parka Corta Quilt Con Gorro Rojo Nicopoly                                      nan regular_payment             reconciled      1      21990.00
    refund                                   Parka Corta Quilt Con Gorro Óxido Nicopoly                                      nan regular_payment           bpp_refunded      2      23485.00
    refund                                   Parka Corta Quilt Con Gorro Óxido Nicopoly                                      nan regular_payment             reconciled      2      23485.00
    refund                     Parka Corta Sin Mangas Tipo Ecocuero Azul Cielo Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                    Parka Corta Tipo Ecocuero  Khaki Nicopoly                                      nan regular_payment           bpp_refunded      2      69980.00
    refund                           Parka Corta Tipo Ecocuero Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      2      95980.00
    refund                           Parka Corta Tipo Ecocuero Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      35990.00
    refund                             Parka Corta Tipo Ecocuero Gris Metálico Nicopoly                                      nan regular_payment           bpp_refunded      2      71980.00
    refund                                     Parka Corta Tipo Ecocuero Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      71980.00
    refund                                     Parka Corta Tipo Ecocuero Negro Nicopoly                                      nan regular_payment             reconciled      2      61980.00
    refund                             Parka Corta Tipo Ecocuero Rosado Chicle Nicopoly                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                           Parka Larga Acolchada Cuello Alto Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      41990.00
    refund                            Parka Larga Quilt Cintura Ajustable Gris Nicopoly                                      nan regular_payment           bpp_refunded      9     280010.00
    refund                            Parka Larga Quilt Cintura Ajustable Gris Nicopoly                                      nan regular_payment             reconciled      4     115960.00
    refund                           Parka Larga Quilt Cintura Ajustable Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      56280.00
    refund                           Parka Larga Quilt Cintura Ajustable Negro Nicopoly                                      nan regular_payment             reconciled      6     245440.00
    refund                           Parka Larga Quilt Cintura Ajustable Oliva Nicopoly                                      nan regular_payment           bpp_refunded      6     178443.00
    refund                           Parka Larga Quilt Cintura Ajustable Oliva Nicopoly                                      nan regular_payment             reconciled      4     120967.00
    refund                                Parka Midi Tipo Quilt Bolsillos Gris Nicopoly                                      nan regular_payment           bpp_refunded      8     223920.00
    refund                                Parka Midi Tipo Quilt Bolsillos Gris Nicopoly                                      nan regular_payment             reconciled      1      17990.00
    refund                              Parka Midi Tipo Quilt Bolsillos Marrón Nicopoly                                      nan regular_payment           bpp_refunded      3     101870.00
    refund                              Parka Midi Tipo Quilt Bolsillos Marrón Nicopoly                                      nan regular_payment             reconciled      4     133740.00
    refund                               Parka Midi Tipo Quilt Bolsillos Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      30990.00
    refund                               Parka Midi Tipo Quilt Bolsillos Negro Nicopoly                                      nan regular_payment             reconciled      3      92970.00
    refund                                  Parka Quilt Broches Gris Brillante Nicopoly                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                                  Parka Quilt Broches Gris Brillante Nicopoly                                      nan regular_payment             reconciled      3      86270.00
    refund                                 Parka Quilt Broches Negro Brillante Nicopoly                                      nan regular_payment           bpp_refunded      7     227530.00
    refund                                 Parka Quilt Broches Negro Brillante Nicopoly                                      nan regular_payment             reconciled      1      26290.00
    refund                             Parka Sin Mangas Cordón Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      8     282604.00
    refund                             Parka Sin Mangas Cordón Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      47990.00
    refund                                        Parka Sin Mangas Cordón Café Nicopoly                                      nan regular_payment           bpp_refunded      5     204950.00
    refund                                        Parka Sin Mangas Cordón Café Nicopoly                                      nan regular_payment             reconciled      5     171550.00
    refund                                       Parka Sin Mangas Cordón Negro Nicopoly                                      nan regular_payment            bpp_covered      1      33590.00
    refund                                       Parka Sin Mangas Cordón Negro Nicopoly                                      nan regular_payment           bpp_refunded     12     409560.00
    refund                                       Parka Sin Mangas Cordón Negro Nicopoly                                      nan regular_payment            compensated      2      71980.00
    refund                                       Parka Sin Mangas Cordón Negro Nicopoly                                      nan regular_payment             reconciled      9     345501.00
    refund                                        Parka Sin Mangas Cordón Rojo Nicopoly                                      nan regular_payment           bpp_refunded      4     153960.00
    refund                                        Parka Sin Mangas Cordón Rojo Nicopoly                                      nan regular_payment             reconciled      3     105970.00
    refund                          Parka Sin Mangas Imán Cuello Azul Grisáceo Nicopoly                                      nan regular_payment           bpp_refunded      2      39990.00
    refund                          Parka Sin Mangas Imán Cuello Azul Grisáceo Nicopoly                                      nan regular_payment             reconciled      1       9990.00
    refund                        Parka Sin Mangas Imán Cuello Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      4      97460.00
    refund                        Parka Sin Mangas Imán Cuello Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      2      49980.00
    refund                                   Parka Sin Mangas Imán Cuello Café Nicopoly                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                                   Parka Sin Mangas Imán Cuello Café Nicopoly                                      nan regular_payment             reconciled      1      24990.00
    refund                                         Parka Sin Mangas Quilt Gris Nicopoly                                      nan regular_payment             reconciled      2      51980.00
    refund                                       Parka Sin Mangas Quilt Marrón Nicopoly                                      nan regular_payment           bpp_refunded      1      38990.00
    refund                                        Parka Sin Mangas Quilt Oliva Nicopoly                                      nan regular_payment             reconciled      1      38990.00
    refund                                             Peto Básico Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      1       4990.00
    refund                                      Peto Cuello Halter Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      1       4990.00
    refund                                             Peto Escote En V Rosado Nicopoly                                      nan regular_payment             reconciled      1       8990.00
    refund                       Polera Blanca Detalle De Encaje Nicopoly Blanco M Liso                                      nan regular_payment             reconciled      1      14990.00
    refund                       Polera Blanca Detalle De Encaje Nicopoly Blanco S Liso                                      nan regular_payment           bpp_refunded      2      27980.00
    refund                       Polera Blanca Detalle De Encaje Nicopoly Blanco S Liso                                      nan regular_payment             reconciled      2      32454.00
    refund        Polera Básica Cuello Redondo Azul Marino Nicopoly Azul Marino Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                   Polera Básica Cuello Redondo Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund Polera Básica Cuello Redondo Líneas Azul Marino Nicopoly Azul Marino Xl Liso                                      nan regular_payment           bpp_refunded      1       9690.00
    refund          Polera Básica Cuello Redondo Líneas Grafito Nicopoly Grafito M Liso                                      nan regular_payment                    nan      1      11990.00
    refund               Polera Básica Cuello Redondo Líneas Gris Claro Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                     Polera Básica Cuello Redondo Líneas Rojo Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                    Polera Básica Cuello Redondo Líneas Rojo Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      1      14184.00
    refund                        Polera Con Transparencias Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      18190.00
    refund                       Polera Con Transparencias Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      2      35980.00
    refund                                  Polera Cuello Alto Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      1       8240.00
    refund                                           Polera Cuello Alto Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      1      10990.00
    refund                                           Polera Cuello Alto Burdeo Nicopoly                                      nan regular_payment                    nan      1      10990.00
    refund                                             Polera Cuello Alto Café Nicopoly                                      nan regular_payment           bpp_refunded      1       8240.00
    refund                                          Polera Cuello Alto Grafito Nicopoly                                      nan regular_payment           bpp_refunded      1       8240.00
    refund                                          Polera Cuello Alto Grafito Nicopoly                                      nan regular_payment                    nan      1       7690.00
    refund                                             Polera Cuello Alto Gris Nicopoly                                      nan regular_payment           bpp_refunded      2      20980.00
    refund                                             Polera Cuello Alto Gris Nicopoly                                      nan regular_payment                    nan      1       8790.00
    refund                               Polera Cuello Redondo Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      2      20980.00
    refund                                        Polera Cuello Redondo Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      4      40210.00
    refund                                        Polera Cuello Redondo Burdeo Nicopoly                                      nan regular_payment                    nan      1      10990.00
    refund                                          Polera Cuello Redondo Café Nicopoly                                      nan regular_payment           bpp_refunded      2      20980.00
    refund                                          Polera Cuello Redondo Café Nicopoly                                      nan regular_payment                    nan      1      10990.00
    refund                                          Polera Cuello Redondo Café Nicopoly                                      nan regular_payment             reconciled      1      11784.00
    refund                                       Polera Cuello Redondo Grafito Nicopoly                                      nan regular_payment            bpp_covered      1       9990.00
    refund                                       Polera Cuello Redondo Grafito Nicopoly                                      nan regular_payment           bpp_refunded      2      20580.00
    refund                                         Polera Cuello Redondo Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      20980.00
    refund                                         Polera Cuello Redondo Negro Nicopoly                                      nan regular_payment                    nan      1       8790.00
    refund                     Polera Encaje Cuello Alto Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment             reconciled      1      19990.00
    refund                     Polera Encaje Cuello Alto Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                        Polera Encaje Cuello Alto Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      13190.00
    refund                        Polera Encaje Cuello Alto Negro Nicopoly Negro M Liso                                      nan regular_payment                    nan      1      13190.00
    refund                       Polera Encaje Cuello Alto Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                       Polera Encaje Cuello Alto Negro Nicopoly Negro Xl Liso                                      nan regular_payment             reconciled      1      21990.00
    refund                        Polera Encaje Escote Nudo Beige Nicopoly Beige Liso M                                      nan regular_payment           bpp_refunded      3      50770.00
    refund                        Polera Encaje Escote Nudo Beige Nicopoly Beige Liso S                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                              Polera Encaje Escote Nudo Negro Nicopoly Liso M                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                        Polera Encaje Escote Nudo Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                        Polera Encaje Escote Nudo Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      13790.00
    refund                Polera Encaje Escote Nudo Rosado Nicopoly - Rosado - Liso - M                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                      Polera Encaje Escote Nudo Rosado Nicopoly Rosado Liso M                                      nan regular_payment           bpp_refunded      3      59770.00
    refund                      Polera Encaje Manga Larga Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                      Polera Encaje Manga Larga Blanco Nicopoly Blanco Liso S                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                      Polera Encaje Manga Larga Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment           bpp_refunded      1      15590.00
    refund                             Polera Encaje Manga Larga Burdeo Nicopoly M Liso                                      nan regular_payment             reconciled      1      20790.00
    refund                              Polera Encaje Manga Larga Negro Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      20790.00
    refund                        Polera Encaje Manga Larga Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1        722.00
    refund                        Polera Encaje Manga Larga Negro Nicopoly Negro L Liso                                      nan regular_payment             reconciled      1      25268.00
    refund                        Polera Encaje Manga Larga Negro Nicopoly Negro S Liso                                      nan regular_payment           bpp_refunded      1      25990.00
    refund            Polera Escote En V Básica Azul Marino Nicopoly Azul Marino L Liso                                      nan regular_payment           bpp_refunded      4      89910.00
    refund            Polera Escote En V Básica Azul Marino Nicopoly Azul Marino M Liso                                      nan regular_payment           bpp_refunded      4      39960.00
    refund                      Polera Escote En V Básica Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      4      35702.00
    refund                      Polera Escote En V Básica Blanco Nicopoly Blanco L Liso                                      nan regular_payment             reconciled      1       7387.00
    refund                      Polera Escote En V Básica Blanco Nicopoly Blanco M Liso                                      nan regular_payment           bpp_refunded      2      29970.00
    refund                     Polera Escote En V Básica Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                             Polera Escote En V Básica Blanco Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      23980.00
    refund                      Polera Escote En V Básica Blanco Nicopoly L Liso Blanco                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                      Polera Escote En V Básica Blanco Nicopoly M Liso Blanco                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                            Polera Escote En V Básica Blanco Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                    Polera Escote En V Básica Café Nicopoly - Café - L - Liso                                      nan regular_payment           bpp_refunded      2      23070.00
    refund                          Polera Escote En V Básica Café Nicopoly Café M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                         Polera Escote En V Básica Café Nicopoly Café Xl Liso                                      nan regular_payment           bpp_refunded      3      29970.00
    refund                          Polera Escote En V Básica Café Nicopoly L Café Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                         Polera Escote En V Básica Café Nicopoly Xl Café Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                              Polera Escote En V Básica Café Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                    Polera Escote En V Básica Celeste Nicopoly Celeste L Liso                                      nan regular_payment             reconciled      1      12980.00
    refund                    Polera Escote En V Básica Celeste Nicopoly Celeste M Liso                                      nan regular_payment           bpp_refunded      2      19980.00
    refund                   Polera Escote En V Básica Celeste Nicopoly Celeste Xl Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                            Polera Escote En V Básica Celeste Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                   Polera Escote En V Básica Gris Nicopoly - Gris - Xl - Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                          Polera Escote En V Básica Gris Nicopoly Gris S Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                              Polera Escote En V Básica Gris Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                        Polera Escote En V Básica Negro Nicopoly L Liso Negro                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                        Polera Escote En V Básica Negro Nicopoly M Liso Negro                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                        Polera Escote En V Básica Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      3      29970.00
    refund                        Polera Escote En V Básica Negro Nicopoly Negro M Liso                                      nan regular_payment           bpp_refunded      2      19980.00
    refund                        Polera Escote En V Básica Negro Nicopoly Negro M Liso                                      nan regular_payment             reconciled      1      11844.00
    refund                       Polera Escote En V Básica Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                             Polera Escote En V Básica Negro Nicopoly Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                       Polera Escote En V Básica Negro Nicopoly Xl Liso Negro                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                      Polera Escote En V Básica Rosado Nicopoly Rosado L Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                      Polera Escote En V Básica Rosado Nicopoly Rosado M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                                 Polera Halter Calada Bicolor Fucsia Nicopoly                                      nan regular_payment             reconciled      1      17764.00
    refund                                         Polera Halter Calada Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                  Polera Hilo Cuello V Botones Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                       Polera Malla Cuello Alto Burdeo Nicopoly Burdeo L Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                   Polera Manga 3/4 Cuello Bote Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                      Polera Manga Corta Básica Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                      Polera Manga Corta Básica Blanco Nicopoly Blanco M Liso                                      nan regular_payment                    nan      1       9990.00
    refund                      Polera Manga Corta Básica Blanco Nicopoly Blanco S Liso                                      nan regular_payment           bpp_refunded      2      21980.00
    refund                     Polera Manga Corta Básica Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                             Polera Manga Corta Básica Blanco Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                             Polera Manga Corta Básica Blanco Nicopoly S Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                            Polera Manga Corta Básica Celeste Nicopoly S Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund               Polera Manga Corta Básica Gris Grafito Nicopoly Grafito M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                         Polera Manga Corta Básica Gris Nicopoly Gris Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                              Polera Manga Corta Básica Negro Nicopoly L Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                                Polera Manga Corta Básica Negro Nicopoly Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                        Polera Manga Corta Básica Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                       Polera Manga Corta Básica Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund               Polera Manga Corta Cuello Tipo U Blanco Nicopoly Blanco L Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund               Polera Manga Corta Cuello Tipo U Blanco Nicopoly Blanco M Liso                                      nan regular_payment           bpp_refunded      2      23980.00
    refund              Polera Manga Corta Cuello Tipo U Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                   Polera Manga Corta Cuello Tipo U Café Nicopoly Café L Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                 Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                 Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro L Liso                                      nan regular_payment                    nan      1      11990.00
    refund                 Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro M Liso                                      nan regular_payment           bpp_refunded      2      23980.00
    refund                 Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro S Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                 Polera Manga Larga Cuello Bote Burdeo Nicopoly Burdeo L Liso                                      nan regular_payment           bpp_refunded      3      13268.00
    refund                Polera Manga Larga Cuello Bote Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                  Polera Manga Larga Cuello Camisero Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      2      19980.00
    refund                            Polera Manga Larga Cuello Camisero Khaki Nicopoly                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                             Polera Manga Larga Cuello Camisero Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2      43140.00
    refund                             Polera Manga Larga Cuello Camisero Rojo Nicopoly                                      nan regular_payment             reconciled      1      21990.00
    refund              Polera Manga Larga Cuello Redondo Blanca  - Blanco - S/m - Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                    Polera Manga Larga Cuello Redondo Blanca  Blanco M/l Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                           Polera Manga Larga Cuello Redondo Grafito S/m Liso                                      nan regular_payment           bpp_refunded      1      16880.00
    refund                             Polera Manga Larga Cuello Redondo Khaki S/m Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                 Polera Rayas Cuello Bote Blanco Nicopoly - Blanco - L - Liso                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                       Polera Rayas Cuello Bote Blanco Nicopoly Blanco M Liso                                      nan regular_payment           bpp_refunded      2      26980.00
    refund                              Polera Rayas Cuello Bote Blanco Nicopoly S Liso                                      nan regular_payment             reconciled      1      23990.00
    refund                     Polera Rayas Manga Larga Grafito Nicopoly Grafito M Liso                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                       Polera Recta Manga Corta Blanco Nicopoly Blanco M Liso                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                            Polera Sin Manga Detalle Terciopelo Negro Lisa Xl                                      nan regular_payment           bpp_refunded      1      15390.00
    refund                       Polera Sin Manga Detalle Terciopelo Negro Negro Lisa L                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                     Polera Sin Mangas Leopardo Café Nicopoly                                      nan regular_payment           bpp_refunded      3      38970.00
    refund                                     Polera Sin Mangas Leopardo Café Nicopoly                                      nan regular_payment                    nan      2      26230.00
    refund                        Polera Sin Mangas Tipo Crochet Blanco Nicopoly M Liso                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                   Polera Sin Mangas Tipo Crochet Negro Nicopoly Negro S Liso                                      nan regular_payment                    nan      1      17992.00
    refund                       Polera Tejida Fantasia Blanco Nicopoly Blanco Rayado L                                      nan regular_payment           bpp_refunded      2      25980.00
    refund                         Polera Tejida Fantasia Negro Nicopoly Negro M Rayado                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                           Polera Transparante De Encaje Negro Negro M Encaje                                      nan regular_payment             reconciled      1      17480.00
    refund                          Polera Transparante De Encaje Negro Negro Xl Encaje                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                       Polera Transparente De Encaje Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                  Ropa - Ropa Mujer - Blusas - Blusas Manga Larga Café Liso L                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                 Ropa - Ropa Mujer - Blusas - Blusas Manga Larga Café Liso Xl                                      nan regular_payment           bpp_refunded      6     136740.00
    refund                                 Short Animal Print Café Nicopoly Café Lisa M                                      nan regular_payment           bpp_refunded      4      20157.00
    refund                                 Short Animal Print Café Nicopoly Café Lisa M                                      nan regular_payment             reconciled      2      37981.00
    refund                                 Short Animal Print Café Nicopoly Café Lisa S                                      nan regular_payment           bpp_refunded      1      18190.00
    refund                                      Short Básico Formal Azul Acero Nicopoly                                      nan regular_payment           bpp_refunded      3      47470.00
    refund                                           Short Básico Formal Camel Nicopoly                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                                            Short Básico Formal Gris Nicopoly                                      nan regular_payment           bpp_refunded      2      31574.00
    refund                                           Short Básico Formal Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      35980.00
    refund                                   Short Básico Tiro Alto Azul Acero Nicopoly                                      nan regular_payment           bpp_refunded      5      83414.00
    refund                                   Short Básico Tiro Alto Azul Acero Nicopoly                                      nan regular_payment             reconciled      1      20780.00
    refund                                        Short Básico Tiro Alto Beige Nicopoly                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                                       Short Básico Tiro Alto Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      5      96900.00
    refund                                        Short Básico Tiro Alto Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                                        Short Básico Tiro Alto Negro Nicopoly                                      nan regular_payment             reconciled      1      24990.00
    refund                                         Short Básico Tiro Alto Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3      65970.00
    refund                  Short Con Botones Delanteros  Blanco Nicopoly Blanco Lisa M                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                  Short Con Botones Delanteros  Blanco Nicopoly Blanco Lisa S                                      nan regular_payment           bpp_refunded      1      18840.00
    refund                       Short Con Botones Delanteros Gris Nicopoly Gris Lisa S                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                          Short Con Botones Delanteros Negro Nicopoly Lisa Xl                                      nan regular_payment                    nan      1      28990.00
    refund                     Short Con Botones Delanteros Negro Nicopoly Negro Lisa M                                      nan regular_payment           bpp_refunded      2      39380.00
    refund                     Short Con Botones Delanteros Negro Nicopoly Negro Lisa S                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                    Short Con Botones Delanteros Negro Nicopoly Negro Lisa Xl                                      nan regular_payment           bpp_refunded      4      90960.00
    refund                     Short Con Botones Delanteros Negro Nicopoly S Lisa Negro                                      nan regular_payment             reconciled      1      22990.00
    refund                                         Short Holgado Azul Grisáceo Nicopoly                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                                                 Short Holgado Beige Nicopoly                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                                                 Short Holgado Crema Nicopoly                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                                           Short Holgado Verde Musgo Nicopoly                                      nan regular_payment           bpp_refunded      2      27980.00
    refund                                  Sobrecamisa Cotelé Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      3      91220.00
    refund                                  Sobrecamisa Cotelé Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                                             Sobrecamisa Cotelé Café Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                             Sobrecamisa Cotelé Café Nicopoly                                      nan regular_payment            compensated      1      30990.00
    refund                                             Sobrecamisa Cotelé Café Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                                             Sobrecamisa Cotelé Gris Nicopoly                                      nan regular_payment           bpp_refunded      3      66070.00
    refund                                             Sobrecamisa Cotelé Gris Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                                     Sobrecamisa Cotelé Verde Oscuro Nicopoly                                      nan regular_payment            bpp_covered      1      23990.00
    refund                                     Sobrecamisa Cotelé Verde Oscuro Nicopoly                                      nan regular_payment           bpp_refunded      3      88970.00
    refund                                     Sobrecamisa Cotelé Verde Oscuro Nicopoly                                      nan regular_payment            compensated      1      29240.00
    refund                                     Sobrecamisa Cotelé Verde Oscuro Nicopoly                                      nan regular_payment             reconciled      1      30990.00
    refund                                     Sobrecamisa Larga Escocés Verde Nicopoly                                      nan regular_payment           bpp_refunded      2     239960.00
    refund                                Sobrecamisa Tipo Pana Broches Blanco Nicopoly                                      nan regular_payment           bpp_refunded      4      90820.00
    refund                                Sobrecamisa Tipo Pana Broches Blanco Nicopoly                                      nan regular_payment            compensated      1      22990.00
    refund                                 Sobrecamisa Tipo Pana Broches Taupe Nicopoly                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                                  Sweater Acanalado Cuello Alto Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      36990.00
    refund                                 Sweater Acanalado Cuello Alto Khaki Nicopoly                                      nan regular_payment           bpp_refunded      2      57980.00
    refund                Sweater Acanalado Cuello Bote Celeste Nicopoly Celeste Liso L                                      nan regular_payment                    nan      1      19990.00
    refund                Sweater Acanalado Cuello Bote Celeste Nicopoly Celeste Liso M                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                Sweater Acanalado Cuello Bote Celeste Nicopoly Celeste Liso S                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                Sweater Acanalado Cuello Bote Celeste Nicopoly Celeste Liso S                                      nan regular_payment                    nan      1      23990.00
    refund                      Sweater Acanalado Cuello Bote Lila Nicopoly Lila Liso L                                      nan regular_payment           bpp_refunded      2      35180.00
    refund                      Sweater Acanalado Cuello Bote Lila Nicopoly Lila Liso L                                      nan regular_payment                    nan      1      19990.00
    refund                      Sweater Acanalado Cuello Bote Lila Nicopoly Lila Liso M                                      nan regular_payment           bpp_refunded      3      66970.00
    refund                      Sweater Acanalado Cuello Bote Lila Nicopoly Lila Liso S                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                    Sweater Acanalado Cuello Bote Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                    Sweater Acanalado Cuello Bote Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                    Sweater Acanalado Cuello Bote Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                      Sweater Acanalado Cuello Bote Rojo Nicopoly Rojo Liso M                                      nan regular_payment           bpp_refunded      3      53970.00
    refund                      Sweater Acanalado Cuello Bote Rojo Nicopoly Rojo Liso M                                      nan regular_payment             reconciled      1       9000.00
    refund                                       Sweater Beatle Acanalado Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                    Sweater Beatle Acanalado Mostaza Nicopoly                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                      Sweater Beatle Acanalado Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                  Sweater Básico Cuello Beatle Acero Nicopoly                                      nan regular_payment           bpp_refunded      5     120950.00
    refund                                Sweater Básico Cuello Beatle Magenta Nicopoly                                      nan regular_payment           bpp_refunded      2      45980.00
    refund                                  Sweater Básico Cuello Beatle Negro Nicopoly                                      nan regular_payment           bpp_refunded     10     217250.00
    refund                                   Sweater Básico Cuello Beatle Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2      45980.00
    refund                                   Sweater Básico Cuello Beatle Rojo Nicopoly                                      nan regular_payment             reconciled      3      74970.00
    refund                               Sweater Básico Cuello Redondo Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      37880.00
    refund                               Sweater Básico Cuello Redondo Celeste Nicopoly                                      nan regular_payment             reconciled      1      26990.00
    refund                               Sweater Básico Cuello Redondo Magenta Nicopoly                                      nan regular_payment           bpp_refunded      2      47230.00
    refund                               Sweater Básico Cuello Redondo Magenta Nicopoly                                      nan regular_payment                    nan      1      21990.00
    refund                                 Sweater Básico Cuello Redondo Negro Nicopoly                                      nan regular_payment           bpp_refunded      6     138840.00
    refund                                 Sweater Básico Cuello Redondo Negro Nicopoly                                      nan regular_payment                    nan      1      26990.00
    refund                                 Sweater Básico Cuello Redondo Negro Nicopoly                                      nan regular_payment             reconciled      1      26990.00
    refund                                  Sweater Básico Cuello Redondo Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                                  Sweater Básico Cuello Redondo Rojo Nicopoly                                      nan regular_payment                    nan      1      21990.00
    refund                        Sweater Básico Perlas Celeste Nicopoly Celeste Liso L                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                        Sweater Básico Perlas Celeste Nicopoly Celeste Liso S                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                          Sweater Básico Perlas Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment           bpp_refunded      2      31176.00
    refund                          Sweater Básico Perlas Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment             reconciled      1      12804.00
    refund                          Sweater Básico Perlas Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                              Sweater Básico Perlas Gris Nicopoly Gris Liso L                                      nan regular_payment           bpp_refunded      2      43980.00
    refund                              Sweater Básico Perlas Gris Nicopoly Gris Liso M                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                              Sweater Básico Perlas Gris Nicopoly Gris Liso M                                      nan regular_payment             reconciled      1      21990.00
    refund                              Sweater Básico Perlas Rojo Nicopoly Rojo Liso L                                      nan regular_payment             reconciled      1      21990.00
    refund                              Sweater Básico Perlas Rojo Nicopoly Rojo Liso M                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                              Sweater Básico Perlas Rojo Nicopoly Rojo Liso S                                      nan regular_payment           bpp_refunded      1      21342.00
    refund                       Sweater Canalé Cuello Tortuga Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      3      71970.00
    refund                       Sweater Canalé Cuello Tortuga Blanco Invierno Nicopoly                                      nan regular_payment                    nan      1      19990.00
    refund                                 Sweater Canalé Cuello Tortuga Camel Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                 Sweater Canalé Cuello Tortuga Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                 Sweater Canalé Cuello Tortuga Negro Nicopoly                                      nan regular_payment            compensated      1      19990.00
    refund                                 Sweater Canalé Cuello Tortuga Negro Nicopoly                                      nan regular_payment             reconciled      2      43980.00
    refund                                  Sweater Canalé Cuello Tortuga Rojo Nicopoly                                      nan regular_payment             reconciled      1      22490.00
    refund                                          Sweater Color Block Fucsia Nicopoly                                      nan regular_payment           bpp_refunded      3      64020.00
    refund                                            Sweater Color Block Gris Nicopoly                                      nan regular_payment            compensated      1      21740.00
    refund                    Sweater Con Patrón Trenzado Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                      Sweater Con Patrón Trenzado Mocca Nicopoly Mocca Liso S                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                        Sweater Con Patrón Trenzado Rojo Nicopoly Rojo Liso M                                      nan regular_payment           bpp_refunded      1      33990.00
    refund                                         Sweater Crop Acanalado Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                         Sweater Crop Acanalado Gris Nicopoly                                      nan regular_payment             reconciled      1      19990.00
    refund                             Sweater Crop Cuello Tortuga Azul Índigo Nicopoly                                      nan regular_payment             reconciled      1      22490.00
    refund                         Sweater Cuello Alto Rombos Azul Nicopoly Azul Liso M                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                                Sweater Cuello Beatle Strass Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                                Sweater Cuello Beatle Strass Celeste Nicopoly                                      nan regular_payment                    nan      1      22990.00
    refund                                Sweater Cuello Beatle Strass Celeste Nicopoly                                      nan regular_payment             reconciled      3      75970.00
    refund                                   Sweater Cuello Beatle Strass Gris Nicopoly                                      nan regular_payment             reconciled      1      25490.00
    refund                                  Sweater Cuello Beatle Strass Negro Nicopoly                                      nan regular_payment                    nan      1      22990.00
    refund                                  Sweater Cuello Beatle Strass Negro Nicopoly                                      nan regular_payment             reconciled      1      22990.00
    refund                                  Sweater Cuello Beatle Strass Óxido Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                  Sweater Cuello Beatle Strass Óxido Nicopoly                                      nan regular_payment             reconciled      1      16093.00
    refund                                      Sweater Cuello Bote Azul Acero Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                                         Sweater Cuello Bote Magenta Nicopoly                                      nan regular_payment           bpp_refunded      2      42980.00
    refund                                            Sweater Cuello Bote Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                             Sweater Cuello Camisero Cadenetas Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                                           Sweater Cuello Polo Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      59960.00
    refund                                           Sweater Cuello Polo Negro Nicopoly                                      nan regular_payment            compensated      1      25990.00
    refund                                     Sweater Cuello V Acanalado Gris Nicopoly                                      nan regular_payment           bpp_refunded      2      29980.00
    refund                                    Sweater Cuello V Acanalado Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                 Sweater Detalle Punto Calado Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      16990.00
    refund                                     Sweater Diseño Cadenetas Burdeo Nicopoly                                      nan regular_payment                    nan      1      17990.00
    refund                                      Sweater Diseño Cadenetas Khaki Nicopoly                                      nan regular_payment           bpp_refunded      2      47980.00
    refund                                      Sweater Diseño Cadenetas Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      43770.00
    refund                                         Sweater Diseño Flores Negro Nicopoly                                      nan regular_payment           bpp_refunded      4     107960.00
    refund                                         Sweater Diseño Flores Negro Nicopoly                                      nan regular_payment            compensated      5     136912.00
    refund                                         Sweater Diseño Flores Negro Nicopoly                                      nan regular_payment             reconciled      3      83170.00
    refund                               Sweater Diseño Rombos Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      1      22490.00
    refund                               Sweater Diseño Rombos Blanco Invierno Nicopoly                                      nan regular_payment            compensated      1      22490.00
    refund                               Sweater Diseño Rombos Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                                       Sweater Diseño Rombos Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                       Sweater Diseño Rombos Celeste Nicopoly                                      nan regular_payment                    nan      1      23990.00
    refund                                       Sweater Diseño Rombos Magenta Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                                         Sweater Diseño Rombos Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      47980.00
    refund                                          Sweater Diseño Rombos Rojo Nicopoly                                      nan regular_payment             reconciled      2      23990.00
    refund                             Sweater Diseño Trenzado Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      1      20240.00
    refund                                       Sweater Diseño Trenzado Camel Nicopoly                                      nan regular_payment           bpp_refunded      3      61532.00
    refund                                       Sweater Diseño Trenzado Camel Nicopoly                                      nan regular_payment            compensated      1      20240.00
    refund                                       Sweater Diseño Trenzado Negro Nicopoly                                      nan regular_payment           bpp_refunded      5      84200.00
    refund                                     Sweater Diseños Espigas Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                        Sweater Diseños Espigas Gris Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                                       Sweater Diseños Espigas Negro Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                                       Sweater Diseños Espigas Óxido Nicopoly                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                         Sweater Escote Asimétrico Café Nicopoly Café Liso Xl                                      nan regular_payment           bpp_refunded      1      17999.00
    refund                         Sweater Escote Asimétrico Café Nicopoly Café Liso Xl                                      nan regular_payment            compensated      1       4991.00
    refund                        Sweater Escote Asimétrico Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                        Sweater Escote Asimétrico Verde Nicopoly Verde Liso L                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                        Sweater Escote Asimétrico Verde Nicopoly Verde Liso M                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                                      Sweater Escote Profundo Blanco Nicopoly                                      nan regular_payment             reconciled      1      21580.00
    refund                                       Sweater Escote Profundo Camel Nicopoly                                      nan regular_payment            bpp_covered      1      19490.00
    refund                                       Sweater Escote Profundo Camel Nicopoly                                      nan regular_payment           bpp_refunded      1      20272.00
    refund                                       Sweater Escote Profundo Camel Nicopoly                                      nan regular_payment                    nan      1      17990.00
    refund                                        Sweater Escote Profundo Gris Nicopoly                                      nan regular_payment           bpp_refunded      2      37980.00
    refund                                                Sweater Gilet Blanco Nicopoly                                      nan regular_payment           bpp_refunded      2      49980.00
    refund                                                  Sweater Gilet Negronicopoly                                      nan regular_payment           bpp_refunded      2      49980.00
    refund                                                  Sweater Gilet Negronicopoly                                      nan regular_payment                    nan      1      24990.00
    refund                                                  Sweater Gilet Negronicopoly                                      nan regular_payment             reconciled      1      24990.00
    refund                  Sweater Jaspeado Cuello Redondo Khaki Nicopoly Khaki Liso S                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                Sweater Jaspeado Cuello Redondo Morado Nicopoly Morado Liso M                                      nan regular_payment             reconciled      1      25990.00
    refund                                Sweater Manga Raglán Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      6      76684.00
    refund                                Sweater Manga Raglán Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      14252.00
    refund                                           Sweater Manga Raglán Gris Nicopoly                                      nan regular_payment           bpp_refunded      5     104232.00
    refund                                Sweater Mangas Detalles Perlas Camel Nicopoly                                      nan regular_payment           bpp_refunded      2      38480.00
    refund                              Sweater Mangas Detalles Perlas Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      34480.00
    refund                                 Sweater Mangas Detalles Perlas Lila Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                Sweater Mangas Detalles Perlas Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                Sweater Mangas Detalles Perlas Óxido Nicopoly                                      nan regular_payment           bpp_refunded      2      35980.00
    refund                             Sweater Peludo Recogido Lateral Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      12210.00
    refund                                Sweater Peludo Recogido Lateral Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                Sweater Peludo Recogido Lateral Gris Nicopoly                                      nan regular_payment             reconciled      1      18780.00
    refund                                Sweater Peludo Recogido Lateral Lila Nicopoly                                      nan regular_payment           bpp_refunded      1      12210.00
    refund                                Sweater Peludo Recogido Lateral Rosa Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                                Sweater Punto Fantasía Lurex Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      18990.00
    refund                                   Sweater Punto Fantasía Lurex Lila Nicopoly                                      nan regular_payment             reconciled      1      24480.00
    refund                                   Sweater Punto Fantasía Lurex Rosa Nicopoly                                      nan regular_payment           bpp_refunded      3      56100.00
    refund                                   Sweater Punto Fino Cadenetas Gris Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                                        Sweater Punto Trenzado Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                       Sweater Rayas Blanco Invierno Nicopoly                                      nan regular_payment           bpp_refunded      6     119540.00
    refund                                       Sweater Rayas Blanco Invierno Nicopoly                                      nan regular_payment            compensated      1      21990.00
    refund                                       Sweater Rayas Blanco Invierno Nicopoly                                      nan regular_payment             reconciled      1      21990.00
    refund                                                 Sweater Rayas Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      53570.00
    refund                                                 Sweater Rayas Negro Nicopoly                                      nan regular_payment             reconciled      3      65960.00
    refund                            Sweater Tipo Hilo Manga Princesa Mostaza Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                     Sweater Trenzado Cuello Alto Camel Nicopoly Camel Liso L                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                     Sweater Trenzado Cuello Alto Camel Nicopoly Camel Liso S                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                       Sweater Trenzado Cuello Alto Gris Nicopoly Gris Liso M                                      nan regular_payment             reconciled      1      25990.00
    refund                                        Tapado Básico Bolsillos Café Nicopoly                                      nan regular_payment           bpp_refunded      1      19192.00
    refund                                        Tapado Básico Bolsillos Café Nicopoly                                      nan regular_payment             reconciled      3      79970.00
    refund                                     Tapado Básico Bolsillos Celeste Nicopoly                                      nan regular_payment           bpp_refunded      1      23990.00
    refund                                     Tapado Básico Bolsillos Magenta Nicopoly                                      nan regular_payment           bpp_refunded      5     131950.00
    refund                                     Tapado Básico Bolsillos Magenta Nicopoly                                      nan regular_payment                    nan      1      23990.00
    refund                                     Tapado Básico Bolsillos Magenta Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                                        Tapado Básico Bolsillos Negronicopoly                                      nan regular_payment           bpp_refunded      5      64321.00
    refund                                        Tapado Básico Bolsillos Negronicopoly                                      nan regular_payment             reconciled      3      59707.00
    refund                                        Tapado Básico Bolsillos Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      39990.00
    refund                                        Tapado Básico Bolsillos Rojo Nicopoly                                      nan regular_payment             reconciled      1      23990.00
    refund                       Tapado Tejido Tipo Crochet Café Nicopoly Cafe Liso S/m                                      nan regular_payment           bpp_refunded      6      68535.00
    refund                       Tapado Tejido Tipo Crochet Café Nicopoly Cafe Liso S/m                                      nan regular_payment             reconciled      1      19449.00
    refund                     Tapado Tejido Tipo Crochet Negro Nicopoly Negro Liso M/l                                      nan regular_payment           bpp_refunded      1      36990.00
    refund                     Tapado Tejido Tipo Crochet Negro Nicopoly Negro Liso M/l                                      nan regular_payment             reconciled      1      21990.00
    refund                     Tapado Tejido Tipo Crochet Negro Nicopoly Negro Liso S/m                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                 Top Acanalado Hombros Caídos Blanco Nicopoly                                      nan regular_payment           bpp_refunded      3      49133.00
    refund                                 Top Acanalado Hombros Caídos Blanco Nicopoly                                      nan regular_payment             reconciled      1      11280.00
    refund                                  Top Acanalado Hombros Caídos Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                                  Top Acanalado Hombros Caídos Negro Nicopoly                                      nan regular_payment             reconciled      2      43920.00
    refund                                 Top Básico Leopardo Tipo Satín Café Nicopoly                                      nan regular_payment             reconciled      1      19480.00
    refund                                 Top Básico Leopardo Tipo Satín Gris Nicopoly                                      nan regular_payment           bpp_refunded      2      25980.00
    refund                                        Top Básico Tipo Satín Blanco Nicopoly                                      nan regular_payment           bpp_refunded      4      47960.00
    refund                                        Top Básico Tipo Satín Blanco Nicopoly                                      nan regular_payment             reconciled      2      30420.00
    refund                                       Top Básico Tipo Satín Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      23980.00
    refund                                         Top Básico Tipo Satín Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      35970.00
    refund                        Top Encaje Escote V Negro Nicopoly - Negro - L - Liso                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro L Liso                                      nan regular_payment           bpp_refunded      1      20790.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro M Liso                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro M Liso                                      nan regular_payment             reconciled      1      19990.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro S Liso                                      nan regular_payment           bpp_refunded      1      20790.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro S Liso                                      nan regular_payment             reconciled      1      19990.00
    refund                                      Top Pabilo Print Leopardo Café Nicopoly                                      nan regular_payment           bpp_refunded      5      75950.00
    refund                                      Top Pabilo Print Leopardo Café Nicopoly                                      nan regular_payment             reconciled      1      15990.00
    refund                                           Top Print Paisley Mostaza Nicopoly                                      nan regular_payment           bpp_refunded      1       6990.00
    refund                                                Top Print Snake Azul Nicopoly                                      nan regular_payment           bpp_refunded      4      49950.00
    refund                                                Top Print Snake Café Nicopoly                                      nan regular_payment           bpp_refunded      1      12990.00
    refund                                               Top Print Snake Verde Nicopoly                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                       Top Sin Mangas Acanalado Blanco Nicopoly Blanco Liso L                                      nan regular_payment           bpp_refunded      1       7990.00
    refund                              Top Sin Mangas Acanalado Blanco Nicopoly Liso L                                      nan regular_payment           bpp_refunded      2      19980.00
    refund                     Top Sin Mangas Acanalado Celeste Nicopoly Celeste Liso S                                      nan regular_payment           bpp_refunded      1       7990.00
    refund                     Top Sin Mangas Acanalado Gris Claro Nicopoly Gris Liso S                                      nan regular_payment           bpp_refunded      1       7990.00
    refund                         Top Sin Mangas Acanalado Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      1       7990.00
    refund                         Top Sin Mangas Acanalado Negro Nicopoly Negro M Liso                                      nan regular_payment           bpp_refunded      1       9990.00
    refund                         Top Sin Mangas Acanalado Oliva Nicopoly Oliva Liso L                                      nan regular_payment           bpp_refunded      1       7990.00
    refund                         Top Sin Mangas Acanalado Oliva Nicopoly Oliva Liso S                                      nan regular_payment           bpp_refunded      1       7990.00
    refund                      Top Tipo Lino Estampado Cebra Café Nicopoly Café Lisa M                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                      Top Tipo Lino Estampado Cebra Café Nicopoly Café Lisa S                                      nan regular_payment           bpp_refunded      1      11990.00
    refund                     Top Tipo Lino Estampado Cebra Café Nicopoly Café Lisa Xl                                      nan regular_payment           bpp_refunded      3      38970.00
    refund                                                Trench Hebilla Khaki Nicopoly                                      nan regular_payment           bpp_refunded     12     595702.00
    refund                                                Trench Hebilla Khaki Nicopoly                                      nan regular_payment                    nan      1      53990.00
    refund                                                Trench Hebilla Khaki Nicopoly                                      nan regular_payment             reconciled      4     199960.00
    refund                                                Trench Hebilla Oliva Nicopoly                                      nan regular_payment           bpp_refunded      9     253814.00
    refund                                                Trench Hebilla Oliva Nicopoly                                      nan regular_payment            compensated      1      40490.00
    refund                                                Trench Hebilla Oliva Nicopoly                                      nan regular_payment                    nan      1      43190.00
    refund                                                Trench Hebilla Oliva Nicopoly                                      nan regular_payment             reconciled      8     293906.00
    refund                                           Trench Lazo Hebilla Khaki Nicopoly                                      nan regular_payment           bpp_refunded      7     258430.00
    refund                                           Trench Lazo Hebilla Khaki Nicopoly                                      nan regular_payment             reconciled      4     128328.00
    refund                                           Trench Lazo Hebilla Negro Nicopoly                                      nan regular_payment           bpp_refunded     12     450983.00
    refund                                           Trench Lazo Hebilla Negro Nicopoly                                      nan regular_payment             reconciled      7     232201.00
    refund                                       Trench Lazo Tipo Gamuza Beige Nicopoly                                      nan regular_payment             reconciled      1      59990.00
    refund                                        Trench Lazo Tipo Gamuza Gris Nicopoly                                      nan regular_payment             reconciled      1      41990.00
    refund                                  Trench Príncipe De Gales Lazo Gris Nicopoly                                      nan regular_payment           bpp_refunded      6     161940.00
    refund                                  Trench Príncipe De Gales Lazo Gris Nicopoly                                      nan regular_payment             reconciled      3      80970.00
    refund                                             Trench Tipo Gamuza Café Nicopoly                                      nan regular_payment            bpp_covered      1      35990.00
    refund                                             Trench Tipo Gamuza Café Nicopoly                                      nan regular_payment           bpp_refunded     11     569890.00
    refund                                             Trench Tipo Gamuza Café Nicopoly                                      nan regular_payment            compensated      1      59990.00
    refund                                             Trench Tipo Gamuza Café Nicopoly                                      nan regular_payment                    nan      1      59990.00
    refund                                             Trench Tipo Gamuza Café Nicopoly                                      nan regular_payment             reconciled     10     512900.00
    refund                                            Trench Tipo Gamuza Negro Nicopoly                                      nan regular_payment           bpp_refunded      3     129512.00
    refund                                            Trench Tipo Gamuza Negro Nicopoly                                      nan regular_payment             reconciled      4     215960.00
    refund                                            Trench Tipo Gamuza Oliva Nicopoly                                      nan regular_payment           bpp_refunded      1      59990.00
    refund                                            Trench Tipo Gamuza Oliva Nicopoly                                      nan regular_payment                    nan      1      59990.00
    refund                               Vestido Acanalado Blanco Con Cinturón Blanco L                                      nan regular_payment             reconciled      1      35990.00
    refund               Vestido Acanalado Blanco Con Cinturón Nicopoly Blanco Liso M/l                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                                Vestido Acanalado Con Botones Fucsia Nicopoly                                      nan regular_payment           bpp_refunded      2      40524.00
    refund                                Vestido Acanalado Con Botones Fucsia Nicopoly                                      nan regular_payment             reconciled      1       1046.00
    refund                                 Vestido Acanalado Cuello Alto Beige Nicopoly                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                                 Vestido Acanalado Cuello Alto Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      72970.00
    refund                                 Vestido Acanalado Cuello Alto Negro Nicopoly                                      nan regular_payment            compensated      1      21980.00
    refund                                  Vestido Acanalado Cuello Alto Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      36990.00
    refund                                 Vestido Acanalado Cuello Alto Verde Nicopoly                                      nan regular_payment           bpp_refunded      1      17990.00
    refund                 Vestido Acanalado Negro Con Cinturón Nicopoly Negro Liso M/l                                      nan regular_payment           bpp_refunded      3      60456.00
    refund                            Vestido Acanalado Off The Shoulder Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      39780.00
    refund                            Vestido Acanalado Off The Shoulder Negro Nicopoly                                      nan regular_payment             reconciled      1      18990.00
    refund                         Vestido Ajustado Cut Out Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      2      64980.00
    refund                         Vestido Ajustado Cut Out Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      2      64980.00
    refund                         Vestido Ajustado Cut Out Negro Nicopoly Negro Liso S                                      nan regular_payment             reconciled      2      59980.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso L                                      nan regular_payment           bpp_refunded      3      80970.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso L                                      nan regular_payment             reconciled      1      22990.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso M                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso M                                      nan regular_payment             reconciled      2      45980.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso S                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                      Vestido Animal Print Tipo Satín Nicopoly Marrón Liso Xl                                      nan regular_payment           bpp_refunded      1      27590.00
    refund                      Vestido Animal Print Tipo Satín Nicopoly Xl Liso Marrón                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                          Vestido Asimétrico Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      47980.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment           bpp_refunded      5     136550.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment             reconciled      1      35990.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment             reconciled      1      28790.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso S                                      nan regular_payment           bpp_refunded      1      24990.00
    refund                     Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso Xl                                      nan regular_payment             reconciled      4      92462.00
    refund                     Vestido Asimétrico Floral Fucsia Nicopoly Xl Liso Fucsia                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso L                                      nan regular_payment           bpp_refunded      2      62980.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso L                                      nan regular_payment             reconciled      1      35990.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso M                                      nan regular_payment           bpp_refunded     10     188234.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso M                                      nan regular_payment             reconciled      4      84570.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso S                                      nan regular_payment           bpp_refunded      8     207720.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso S                                      nan regular_payment             reconciled      1      24990.00
    refund                       Vestido Asimétrico Floral Verde Nicopoly Verde Liso Xl                                      nan regular_payment           bpp_refunded      5     135760.00
    refund                       Vestido Asimétrico Floral Verde Nicopoly Verde Liso Xl                                      nan regular_payment             reconciled      3      65770.00
    refund                       Vestido Asimétrico Floral Verde Nicopoly Xl Liso Verde                                      nan regular_payment           bpp_refunded      1      35990.00
    refund                       Vestido Asimétrico Floral Verde Nicopoly Xl Liso Verde                                      nan regular_payment             reconciled      1      35990.00
    refund                               Vestido Broderie Blanco Nicopoly Blanco Liso M                                      nan regular_payment           bpp_refunded      1      43990.00
    refund                       Vestido Camisero Cebra Café Nicopoly - Café - Lisa - S                                      nan regular_payment           bpp_refunded      3       3381.00
    refund                       Vestido Camisero Cebra Café Nicopoly - Café - Lisa - S                                      nan regular_payment             reconciled      1      25863.00
    refund                             Vestido Camisero Cebra Café Nicopoly Café Lisa L                                      nan regular_payment             reconciled      1      20390.00
    refund                             Vestido Camisero Cebra Café Nicopoly Café Lisa M                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                             Vestido Camisero Cebra Café Nicopoly Café Lisa M                                      nan regular_payment             reconciled      1      23790.00
    refund                            Vestido Camisero Cebra Café Nicopoly Café Lisa Xl                                      nan regular_payment            compensated      1      20000.00
    refund                            Vestido Camisero Cebra Café Nicopoly Café Lisa Xl                                      nan regular_payment             reconciled      1      23790.00
    refund                            Vestido Camisero Cebra Café Nicopoly Xl Café Lisa                                      nan regular_payment           bpp_refunded      2      53980.00
    refund                               Vestido Camisero Cinturón Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      4     163625.00
    refund                               Vestido Camisero Cinturón Azul Marino Nicopoly                                      nan regular_payment             reconciled      2      64325.00
    refund                                         Vestido Camisero Tipo Denim Nicopoly                                      nan regular_payment           bpp_refunded      1      28990.00
    refund                                         Vestido Camisero Tipo Denim Nicopoly                                      nan regular_payment             reconciled      2      57980.00
    refund            Vestido Cintura Elasticada Flores Naranja Nicopoly Naranjo Liso L                                      nan regular_payment           bpp_refunded      4     105060.00
    refund            Vestido Cintura Elasticada Flores Naranja Nicopoly Naranjo Liso L                                      nan regular_payment             reconciled      1      27990.00
    refund            Vestido Cintura Elasticada Flores Naranja Nicopoly Naranjo Liso M                                      nan regular_payment           bpp_refunded      2      56980.00
    refund            Vestido Cintura Elasticada Flores Naranja Nicopoly Naranjo Liso M                                      nan regular_payment             reconciled      1      28990.00
    refund                                   Vestido Con Faldón Plisado Fucsia Nicopoly                                      nan regular_payment           bpp_refunded      2      45980.00
    refund                                   Vestido Con Faldón Plisado Fucsia Nicopoly                                      nan regular_payment             reconciled      1      20990.00
    refund                                      Vestido Corte Imperio Amarillo Nicopoly                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                      Vestido Corte Imperio Amarillo Nicopoly                                      nan regular_payment            compensated      1      20180.00
    refund                                          Vestido Corte Imperio Azul Nicopoly                                      nan regular_payment           bpp_refunded      1      21990.00
    refund                                          Vestido Corte Imperio Azul Nicopoly                                      nan regular_payment             reconciled      1      24990.00
    refund                               Vestido Corto Aberturas Mangas Blanco Nicopoly                                      nan regular_payment           bpp_refunded      2      36980.00
    refund                              Vestido Corto Aberturas Mangas Celeste Nicopoly                                      nan regular_payment           bpp_refunded      9     160690.00
    refund                              Vestido Corto Aberturas Mangas Celeste Nicopoly                                      nan regular_payment             reconciled      2      37480.00
    refund                                Vestido Corto Aberturas Mangas Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      63000.00
    refund                                Vestido Corto Aberturas Mangas Negro Nicopoly                                      nan regular_payment             reconciled      1      20480.00
    refund                                  Vestido Corto Cuello Halter Blanco Nicopoly                                      nan regular_payment           bpp_refunded      1      14990.00
    refund                                 Vestido Corto Cuello Halter Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      35080.00
    refund                                   Vestido Corto Cuello Halter Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      35470.00
    refund                                  Vestido Corto Cuello Halter Rosado Nicopoly                                      nan regular_payment           bpp_refunded      2      35470.00
    refund                                  Vestido Corto Cuello Halter Rosado Nicopoly                                      nan regular_payment             reconciled      2      39470.00
    refund Vestido Corto Floral Con Vuelos Cruzados Blanco Nicopoly - Blanco - Liso - M                                      nan regular_payment           bpp_refunded      1      33990.00
    refund       Vestido Corto Floral Con Vuelos Cruzados Blanco Nicopoly Blanco Liso L                                      nan regular_payment             reconciled      1      25990.00
    refund        Vestido Corto Floral Con Vuelos Cruzados Fucsia Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      2      48980.00
    refund        Vestido Corto Floral Con Vuelos Cruzados Fucsia Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      2      53180.00
    refund        Vestido Corto Floral Con Vuelos Cruzados Fucsia Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      1      25990.00
    refund        Vestido Corto Floral Con Vuelos Cruzados Fucsia Nicopoly Negro Liso S                                      nan regular_payment             reconciled      2      51980.00
    refund       Vestido Corto Floral Con Vuelos Cruzados Rosado Nicopoly Rosado Liso M                                      nan regular_payment           bpp_refunded      1      25990.00
    refund       Vestido Corto Floral Con Vuelos Cruzados Rosado Nicopoly Rosado Liso M                                      nan regular_payment             reconciled      1      23990.00
    refund       Vestido Corto Floral Con Vuelos Cruzados Rosado Nicopoly Rosado Liso S                                      nan regular_payment           bpp_refunded      1      25990.00
    refund      Vestido Corto Floral Con Vuelos Cruzados Rosado Nicopoly Rosado Liso Xl                                      nan regular_payment             reconciled      1      23990.00
    refund                                      Vestido Corto Sin Mangas Negro Nicopoly                                      nan regular_payment           bpp_refunded      4     131960.00
    refund                                      Vestido Corto Sin Mangas Negro Nicopoly                                      nan regular_payment            compensated      1      39990.00
    refund                                      Vestido Corto Sin Mangas Negro Nicopoly                                      nan regular_payment             reconciled      3      95172.00
    refund                                       Vestido Corto Sin Mangas Rojo Nicopoly                                      nan regular_payment           bpp_refunded      4     143162.00
    refund                                         Vestido Corto Tulipán Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      44900.00
    refund                                         Vestido Corto Tulipán Negro Nicopoly                                      nan regular_payment             reconciled      1      22990.00
    refund                                     Vestido Cuello Alto Azul Marino Nicopoly                                      nan regular_payment           bpp_refunded      4     154460.00
    refund                                     Vestido Cuello Alto Azul Marino Nicopoly                                      nan regular_payment             reconciled      1      37990.00
    refund                                          Vestido Cuello Alto Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      7     274430.00
    refund                                           Vestido Cuello Alto Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      58980.00
    refund                                           Vestido Cuello Alto Negro Nicopoly                                      nan regular_payment         not_reconciled      1      31990.00
    refund                                           Vestido Cuello Alto Negro Nicopoly                                      nan regular_payment             reconciled      4     145960.00
    refund                                          Vestido Cuello Mock Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      1      31022.00
    refund                                          Vestido Cuello Mock Burdeo Nicopoly                                      nan regular_payment            compensated      1       2968.00
    refund                                           Vestido Cuello Mock Negro Nicopoly                                      nan regular_payment             reconciled      1      33990.00
    refund                                            Vestido Cuello Mock Negronicopoly                                      nan regular_payment           bpp_refunded      4     143710.00
    refund                                     Vestido De Punto Trenzado Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      21824.00
    refund                                      Vestido De Punto Trenzado Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      13990.00
    refund                            Vestido Encaje Sirena Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      2     126980.00
    refund                            Vestido Encaje Sirena Negro Nicopoly Negro Liso L                                      nan regular_payment             reconciled      1      67990.00
    refund                            Vestido Encaje Sirena Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      1      59990.00
    refund                   Vestido Escote Cruzado Flores Negras Nicopoly Negro Liso M                                      nan regular_payment             reconciled      1      18190.00
    refund                Vestido Escote Cruzado Flores Rojas Nicoply - Rojo - Liso - M                                      nan regular_payment             reconciled      2      19990.00
    refund                      Vestido Escote Cruzado Flores Rojas Nicoply Rojo Liso M                                      nan regular_payment           bpp_refunded      1      18190.00
    refund                     Vestido Escote Cruzado Flores Verde Nicoply L Liso Verde                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                     Vestido Escote Cruzado Flores Verde Nicoply Verde Liso S                                      nan regular_payment             reconciled      2      38180.00
    refund                    Vestido Escote Cuadrado Negro Nicopoly - Negro - Liso - L                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                          Vestido Escote Cuadrado Negro Nicopoly L Liso Negro                                      nan regular_payment           bpp_refunded      1      27990.00
    refund                          Vestido Escote Cuadrado Negro Nicopoly Negro Liso L                                      nan regular_payment             reconciled      1      25094.00
    refund                          Vestido Escote Cuadrado Negro Nicopoly Negro Liso M                                      nan regular_payment             reconciled      1      25190.00
    refund                                   Vestido Escote Semi Corazón Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                                   Vestido Escote V Profundo Celeste Nicopoly                                      nan regular_payment           bpp_refunded      2      43980.00
    refund                Vestido Estampado Minimalista Naranja Nicopoly Naranjo Liso L                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                Vestido Estampado Minimalista Naranja Nicopoly Naranjo Liso M                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                Vestido Estampado Minimalista Naranja Nicopoly Naranjo Liso S                                      nan regular_payment           bpp_refunded      1      15990.00
    refund                                  Vestido Faldón Con Volantes Fucsia Nicopoly                                      nan regular_payment           bpp_refunded      1      20990.00
    refund                                           Vestido Floral Nudo Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      19790.00
    refund                      Vestido Floral Volantes Celeste Nicopoly Celeste Liso L                                      nan regular_payment           bpp_refunded      4     119960.00
    refund                      Vestido Floral Volantes Celeste Nicopoly Celeste Liso L                                      nan regular_payment             reconciled      1      29990.00
    refund                      Vestido Floral Volantes Celeste Nicopoly Celeste Liso M                                      nan regular_payment           bpp_refunded      2      58580.00
    refund                      Vestido Floral Volantes Celeste Nicopoly Celeste Liso M                                      nan regular_payment             reconciled      3      95970.00
    refund                      Vestido Floral Volantes Celeste Nicopoly M Liso Celeste                                      nan regular_payment           bpp_refunded      1      36990.00
    refund                      Vestido Floral Volantes Celeste Nicopoly S Liso Celeste                                      nan regular_payment           bpp_refunded      1      36990.00
    refund  Vestido Floreado Botones Delanteros Azul Marino Nicopoly Azul Marino Liso M                                      nan regular_payment           bpp_refunded      3      83970.00
    refund  Vestido Floreado Botones Delanteros Azul Marino Nicopoly Azul Marino Liso M                                      nan regular_payment             reconciled      1      29361.00
    refund  Vestido Floreado Botones Delanteros Azul Marino Nicopoly Azul Marino Liso S                                      nan regular_payment           bpp_refunded      1      23990.00
    refund            Vestido Floreado Botones Delanteros Fucsia Nicopoly L Liso Fucsia                                      nan regular_payment           bpp_refunded      1      31990.00
    refund           Vestido Floreado Botones Delanteros Fucsia Nicopoly Xl Liso Fucsia                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                           Vestido Flores Fucsia Nicopoly - Fucsia - Liso - M                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                          Vestido Flores Fucsia Nicopoly - Fucsia - Liso - Xl                                      nan regular_payment                    nan      1      29990.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment           bpp_refunded      4      75960.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment             reconciled      1      24480.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment           bpp_refunded      6     104528.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment             reconciled      1      25480.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso S                                      nan regular_payment           bpp_refunded      1      24690.00
    refund                                Vestido Flores Fucsia Nicopoly Fucsia Liso Xl                                      nan regular_payment           bpp_refunded      4      71960.00
    refund                                Vestido Flores Fucsia Nicopoly Fucsia Liso Xl                                      nan regular_payment             reconciled      1      18990.00
    refund                             Vestido Flores Pabilo Ajustable Celeste Nicopoly                                      nan regular_payment                    nan      1      16990.00
    refund                             Vestido Flores Pabilo Ajustable Celeste Nicopoly                                      nan regular_payment             reconciled      1      20490.00
    refund                                         Vestido Halter Cadena Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      51990.00
    refund                                   Vestido Holgado Con Brillos Khaki Nicopoly                                      nan regular_payment             reconciled      1      21990.00
    refund                            Vestido Holgado Con Mangas Caladas Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      59970.00
    refund      Vestido Largo Con Aberturas Laterales Negro Nicopoly - Negro - Liso - L                                      nan regular_payment           bpp_refunded      1      29990.00
    refund                  Vestido Largo Con Aberturas Laterales Negro Nicopoly Liso L                                      nan regular_payment           bpp_refunded      1      29990.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly M Liso Negro                                      nan regular_payment           bpp_refunded      2      71970.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly M Liso Negro                                      nan regular_payment             reconciled      1      23990.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      2      38980.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      2      44980.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso M                                      nan regular_payment             reconciled      2      53980.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      3      59970.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso S                                      nan regular_payment             reconciled      1      20990.00
    refund                                      Vestido Largo Cuello Mock Azul Nicopoly                                      nan regular_payment           bpp_refunded      4     181460.00
    refund                                      Vestido Largo Cuello Mock Azul Nicopoly                                      nan regular_payment             reconciled      3     109970.00
    refund                                    Vestido Largo Cuello Mock Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      4     153960.00
    refund                                    Vestido Largo Cuello Mock Burdeo Nicopoly                                      nan regular_payment             reconciled      2      76480.00
    refund                     Vestido Largo Escote Drapeado Azul Nicopoly Xl Azul Liso                                      nan regular_payment           bpp_refunded      1      46990.00
    refund                  Vestido Largo Escote Drapeado Morado Nicopoly Morado Liso L                                      nan regular_payment           bpp_refunded      1      45990.00
    refund                                         Vestido Largo Fiesta Burdeo Nicopoly                                      nan regular_payment           bpp_refunded      3     146332.00
    refund                                         Vestido Largo Fiesta Burdeo Nicopoly                                      nan regular_payment             reconciled      5     283950.00
    refund                                         Vestido Largo Fiesta Burdeo Nicopoly                                      nan regular_payment   refund_account_money      1      43390.00
    refund                                          Vestido Largo Fiesta Negro Nicopoly                                      nan regular_payment           bpp_refunded      6     137370.00
    refund                                          Vestido Largo Fiesta Negro Nicopoly                                      nan regular_payment             reconciled      7     327830.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso L                                      nan regular_payment           bpp_refunded      3     106970.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso L                                      nan regular_payment             reconciled      1      36990.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso M                                      nan regular_payment           bpp_refunded      6     203791.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso M                                      nan regular_payment             reconciled      1      15480.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso S                                      nan regular_payment             reconciled      5     106570.00
    refund                            Vestido Largo Floreado Lila Nicopoly Lila Liso Xl                                      nan regular_payment           bpp_refunded      8     192580.00
    refund                            Vestido Largo Floreado Lila Nicopoly Lila Liso Xl                                      nan regular_payment             reconciled      4     140960.00
    refund                   Vestido Largo Floreado Rosado Nicopoly - Rosado - Liso - S                                      nan regular_payment           bpp_refunded      1      56990.00
    refund                         Vestido Largo Floreado Rosado Nicopoly M Liso Rosado                                      nan regular_payment           bpp_refunded      1      48990.00
    refund                         Vestido Largo Floreado Rosado Nicopoly Rosado Liso L                                      nan regular_payment           bpp_refunded      1      34190.00
    refund                         Vestido Largo Floreado Rosado Nicopoly Rosado Liso M                                      nan regular_payment           bpp_refunded      1      36990.00
    refund                         Vestido Largo Floreado Rosado Nicopoly Rosado Liso S                                      nan regular_payment           bpp_refunded      3      69980.00
    refund                        Vestido Largo Floreado Rosado Nicopoly Rosado Liso Xl                                      nan regular_payment           bpp_refunded      2      71880.00
    refund                        Vestido Largo Floreado Rosado Nicopoly Rosado Liso Xl                                      nan regular_payment             reconciled      1      39890.00
    refund                  Vestido Largo Tirantes Cruzados Negro Nicopoly L Lisa Negro                                      nan regular_payment           bpp_refunded      1      61990.00
    refund                        Vestido Largo Tirantes Cruzados Negro Nicopoly Lisa L                                      nan regular_payment           bpp_refunded      1      61990.00
    refund                  Vestido Largo Tirantes Cruzados Negro Nicopoly Negro Lisa L                                      nan regular_payment           bpp_refunded      1      30990.00
    refund                  Vestido Largo Tirantes Cruzados Negro Nicopoly Negro Lisa L                                      nan regular_payment             reconciled      1      49990.00
    refund                  Vestido Largo Tirantes Cruzados Negro Nicopoly Negro Lisa M                                      nan regular_payment           bpp_refunded      6     237950.00
    refund                                         Vestido Midi Acanalado Café Nicopoly                                      nan regular_payment           bpp_refunded      1      19990.00
    refund                                        Vestido Midi Acanalado Negro Nicopoly                                      nan regular_payment           bpp_refunded      3      59970.00
    refund                                         Vestido Midi Acanalado Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2      39980.00
    refund                                   Vestido Midi Acanalado Tajo Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      23270.00
    refund                                   Vestido Midi Acanalado Tajo Negro Nicopoly                                      nan regular_payment             reconciled      2      52980.00
    refund                                 Vestido Midi Escote Drapeado Blanco Nicopoly                                      nan regular_payment             reconciled      1      15990.00
    refund                                  Vestido Midi Escote Drapeado Negro Nicopoly                                      nan regular_payment           bpp_refunded      1      25990.00
    refund                                   Vestido Pabilo Con Volantes Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      47980.00
    refund                                   Vestido Pabilo Con Volantes Negro Nicopoly                                      nan regular_payment                    nan      1      23990.00
    refund                                   Vestido Pliegues En Cintura Negro Nicopoly                                      nan regular_payment            bpp_covered      1      22990.00
    refund                                   Vestido Pliegues En Cintura Negro Nicopoly                                      nan regular_payment           bpp_refunded      5     114950.00
    refund                                   Vestido Pliegues En Cintura Negro Nicopoly                                      nan regular_payment             reconciled      1      22990.00
    refund                                    Vestido Pliegues En Cintura Rojo Nicopoly                                      nan regular_payment           bpp_refunded      3      77970.00
    refund                                    Vestido Pliegues En Cintura Rojo Nicopoly                                      nan regular_payment             reconciled      1      22990.00
    refund                                     Vestido Pliegues En Cintura Rojonicopoly                                      nan regular_payment           bpp_refunded      1      34490.00
    refund                                 Vestido Plisado Asimétrico Azul Rey Nicopoly                                      nan regular_payment           bpp_refunded      3     103970.00
    refund                                 Vestido Plisado Asimétrico Azul Rey Nicopoly                                      nan regular_payment             reconciled      2      63980.00
    refund                                     Vestido Plisado Asimétrico Rojo Nicopoly                                      nan regular_payment           bpp_refunded      8     271920.00
    refund                                     Vestido Plisado Asimétrico Rojo Nicopoly                                      nan regular_payment             reconciled      5     164750.00
    refund                                 Vestido Safari Cuello Camisero Café Nicopoly                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                                 Vestido Safari Cuello Camisero Café Nicopoly                                      nan regular_payment             reconciled      1      32990.00
    refund                   Vestido Satinado Escote Fruncido Lila Nicopoly Lila Liso M                                      nan regular_payment           bpp_refunded      1      27190.00
    refund                   Vestido Satinado Escote Fruncido Lila Nicopoly Lila Liso M                                      nan regular_payment             reconciled      1      25990.00
    refund                   Vestido Satinado Escote Fruncido Lila Nicopoly Lila Liso S                                      nan regular_payment             reconciled      1      25990.00
    refund                   Vestido Satinado Escote Fruncido Lila Nicopoly S Lila Liso                                      nan regular_payment           bpp_refunded      1      33990.00
    refund                                 Vestido Strapless Y Escote V Blanco Nicopoly                                      nan regular_payment           bpp_refunded      8     210920.00
    refund                                 Vestido Strapless Y Escote V Blanco Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                                  Vestido Strapless Y Escote V Negro Nicopoly                                      nan regular_payment           bpp_refunded      6     181940.00
    refund                                  Vestido Strapless Y Escote V Negro Nicopoly                                      nan regular_payment             reconciled      4     101360.00
    refund                                   Vestido Strapless Y Escote V Rojo Nicopoly                                      nan regular_payment           bpp_refunded     10     257360.00
    refund                                   Vestido Strapless Y Escote V Rojo Nicopoly                                      nan regular_payment             reconciled      3      77970.00
    refund                                          Vestido Sweater Midi Camel Nicopoly                                      nan regular_payment           bpp_refunded      2      59980.00
    refund                                          Vestido Sweater Midi Negro Nicopoly                                      nan regular_payment           bpp_refunded      8     237520.00
    refund                                           Vestido Sweater Midi Rojo Nicopoly                                      nan regular_payment           bpp_refunded      6     133660.00
    refund                                           Vestido Sweater Midi Rojo Nicopoly                                      nan regular_payment                    nan      1      28990.00
    refund                                           Vestido Sweater Midi Rojo Nicopoly                                      nan regular_payment             reconciled      3      77120.00
    refund                                           Vestido Tipo Blazer Negro Nicopoly                                      nan regular_payment           bpp_refunded      6     179440.00
    refund                                           Vestido Tipo Blazer Negro Nicopoly                                      nan regular_payment            compensated      2      56480.00
    refund                                           Vestido Tipo Blazer Negro Nicopoly                                      nan regular_payment             reconciled      1      25990.00
    refund                                            Vestido Tipo Blazer Rojo Nicopoly                                      nan regular_payment           bpp_refunded      1      37990.00
    refund                                            Vestido Tipo Blazer Rojo Nicopoly                                      nan regular_payment            compensated      1      27990.00
    refund                                            Vestido Tipo Blazer Rojo Nicopoly                                      nan regular_payment             reconciled      4     143440.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print L                                      nan regular_payment           bpp_refunded      2      33480.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print M                                      nan regular_payment           bpp_refunded      2      33980.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print M                                      nan regular_payment             reconciled      1      20284.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print S                                      nan regular_payment           bpp_refunded      1      16990.00
    refund             Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print Xl                                      nan regular_payment           bpp_refunded      3      50970.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly S Café Animal Print                                      nan regular_payment                    nan      1      19990.00
    refund                                  Vestido Tipo Camisero Leopard Café Nicopoly                                      nan regular_payment           bpp_refunded     11     268440.00
    refund                                  Vestido Tipo Camisero Leopard Café Nicopoly                                      nan regular_payment                    nan      1      25990.00
    refund                                  Vestido Tipo Camisero Leopard Café Nicopoly                                      nan regular_payment             reconciled      2      42480.00
    refund                      Vestido Tipo Satín Floreado Negro Nicopoly Negro Liso L                                      nan regular_payment           bpp_refunded      1      22990.00
    refund                      Vestido Tipo Satín Floreado Negro Nicopoly Negro Liso M                                      nan regular_payment           bpp_refunded      5     120950.00
    refund                      Vestido Tipo Satín Floreado Negro Nicopoly Negro Liso M                                      nan regular_payment             reconciled      1      24990.00
    refund                      Vestido Tipo Satín Floreado Negro Nicopoly Negro Liso S                                      nan regular_payment           bpp_refunded      3      67671.00
    refund              Vestido Tipo Satín Floreado Rosado Nicopoly - Rosado - Liso - M                                      nan regular_payment           bpp_refunded      1      26990.00
    refund              Vestido Tipo Satín Floreado Rosado Nicopoly - Rosado - Liso - S                                      nan regular_payment           bpp_refunded      1      26990.00
    refund                           Vestido Tipo Satín Floreado Rosado Nicopoly Liso L                                      nan regular_payment           bpp_refunded      1      31990.00
    refund                    Vestido Tipo Satín Floreado Rosado Nicopoly Rosado Liso L                                      nan regular_payment             reconciled      1      21990.00
    refund                    Vestido Tipo Satín Floreado Rosado Nicopoly Rosado Liso M                                      nan regular_payment             reconciled      1      24990.00
    refund                    Vestido Tipo Satín Print Flor Abstracta Celeste  Nicopoly                                      nan regular_payment           bpp_refunded      2      41980.00
    refund                                       Vestido Tubo Con Strass Negro Nicopoly                                      nan regular_payment           bpp_refunded      2      50048.00
    refund                                        Vestido Tubo Con Strass Rojo Nicopoly                                      nan regular_payment           bpp_refunded      2      44970.00
    refund                                        Vestido Tubo Con Strass Rojo Nicopoly                                      nan regular_payment             reconciled      1      21390.00
    refund                         Vestido Tul Floreado Celeste Nicopoly Celeste Liso M                                      nan regular_payment           bpp_refunded      1      43390.00
    refund                         Vestido Tul Floreado Celeste Nicopoly Celeste Liso S                                      nan regular_payment             reconciled      1      37990.00
    refund                        Vestido Tul Floreado Celeste Nicopoly Celeste Liso Xl                                      nan regular_payment             reconciled      2      77382.00
    refund                           Vestido Tul Floreado Fucsia Nicopoly Fucsia Liso S                                      nan regular_payment             reconciled      1      37190.00
    refund                                  Vestido Tul Floreado Fucsia Nicopoly Liso L                                      nan regular_payment           bpp_refunded      1      61990.00
    refund                                                       bonificaciones_flex_fc                                      nan  money_transfer                    nan    546     394876.00
    refund                                                         marketplace_shipment                                      nan regular_payment            bpp_covered      1      10532.00
    refund                                                         marketplace_shipment                                      nan regular_payment           bpp_refunded     70     263732.14
    refund                                                         marketplace_shipment                                      nan regular_payment               by_admin      3       7083.79
    refund                                                         marketplace_shipment                                      nan regular_payment               refunded      1       1208.00
```

## FASE 2: Trazabilidad Archivo Fuente -> Ledger (Muestra)

```
                  Archivo Fuente  ID Original  Monto Original                ClasificaciÃ³n Actual                                            Ledger ID      Estado
1 enero 2025 - 1 julio 2025.xlsx 113610989447         39990.0    Ajuste por Compra Protegida (BPP)  POS_113610989447_1 enero 2025 - 1 julio 2025.xlsx_1 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116910735964         23280.0       Ajuste por Cambio de Dirección  POS_116910735964_1 enero 2025 - 1 julio 2025.xlsx_2 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116836571904         47990.0           Ajuste por Arrepentimiento  POS_116836571904_1 enero 2025 - 1 julio 2025.xlsx_3 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116217584583         37990.0            Ajuste por Talla/Garantía  POS_116217584583_1 enero 2025 - 1 julio 2025.xlsx_4 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114321245153         55990.0            Ajuste por Talla/Garantía  POS_114321245153_1 enero 2025 - 1 julio 2025.xlsx_5 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116502809934         33990.0            Ajuste por Talla/Garantía  POS_116502809934_1 enero 2025 - 1 julio 2025.xlsx_6 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116052568980         41990.0            Ajuste por Talla/Garantía  POS_116052568980_1 enero 2025 - 1 julio 2025.xlsx_7 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115670860507         47990.0            Ajuste por Talla/Garantía  POS_115670860507_1 enero 2025 - 1 julio 2025.xlsx_8 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116885181836         47990.0           Ajuste por Arrepentimiento  POS_116885181836_1 enero 2025 - 1 julio 2025.xlsx_9 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116885428608         32990.0           Ajuste por Arrepentimiento POS_116885428608_1 enero 2025 - 1 julio 2025.xlsx_10 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116392547167         25990.0           Ajuste por Arrepentimiento POS_116392547167_1 enero 2025 - 1 julio 2025.xlsx_11 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116392535125         35990.0           Ajuste por Arrepentimiento POS_116392535125_1 enero 2025 - 1 julio 2025.xlsx_12 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116650180676         47990.0            Ajuste por Talla/Garantía POS_116650180676_1 enero 2025 - 1 julio 2025.xlsx_13 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116101546293         29990.0            Ajuste por Talla/Garantía POS_116101546293_1 enero 2025 - 1 julio 2025.xlsx_14 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116262006035         29990.0           Ajuste por Arrepentimiento POS_116262006035_1 enero 2025 - 1 julio 2025.xlsx_15 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116185574144         48990.0            Ajuste por Talla/Garantía POS_116185574144_1 enero 2025 - 1 julio 2025.xlsx_16 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113645388025         34990.0            Ajuste por Talla/Garantía POS_113645388025_1 enero 2025 - 1 julio 2025.xlsx_17 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116133595749         47990.0            Ajuste por Talla/Garantía POS_116133595749_1 enero 2025 - 1 julio 2025.xlsx_20 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114887979409         41990.0            Ajuste por Talla/Garantía POS_114887979409_1 enero 2025 - 1 julio 2025.xlsx_21 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116136319017         19990.0           Ajuste por Arrepentimiento POS_116136319017_1 enero 2025 - 1 julio 2025.xlsx_22 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114959941945         63990.0            Ajuste por Talla/Garantía POS_114959941945_1 enero 2025 - 1 julio 2025.xlsx_23 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116251180593         10990.0           Ajuste por Arrepentimiento POS_116251180593_1 enero 2025 - 1 julio 2025.xlsx_24 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115632579414         39990.0            Ajuste por Talla/Garantía POS_115632579414_1 enero 2025 - 1 julio 2025.xlsx_25 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114328872544         34990.0            Ajuste por Talla/Garantía POS_114328872544_1 enero 2025 - 1 julio 2025.xlsx_26 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115971205237         29990.0            Ajuste por Talla/Garantía POS_115971205237_1 enero 2025 - 1 julio 2025.xlsx_27 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116718212720         23990.0        Ajuste por Retraso en Entrega POS_116718212720_1 enero 2025 - 1 julio 2025.xlsx_28 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116628402608         47990.0 Ajuste por Diferencia de Publicación POS_116628402608_1 enero 2025 - 1 julio 2025.xlsx_29 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115856659941         52990.0 Ajuste por Diferencia de Publicación POS_115856659941_1 enero 2025 - 1 julio 2025.xlsx_30 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116156595237         19990.0        Ajuste por Retraso en Entrega POS_116156595237_1 enero 2025 - 1 julio 2025.xlsx_31 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116392378072         47990.0            Ajuste por Talla/Garantía POS_116392378072_1 enero 2025 - 1 julio 2025.xlsx_32 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114247010441         59990.0           Ajuste por Arrepentimiento POS_114247010441_1 enero 2025 - 1 julio 2025.xlsx_33 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115732185813         21990.0            Ajuste por Talla/Garantía POS_115732185813_1 enero 2025 - 1 julio 2025.xlsx_34 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116220805882         21990.0            Ajuste por Talla/Garantía POS_116220805882_1 enero 2025 - 1 julio 2025.xlsx_35 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116220898746          6990.0            Ajuste por Talla/Garantía POS_116220898746_1 enero 2025 - 1 julio 2025.xlsx_36 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116620228826         19990.0           Ajuste por Arrepentimiento POS_116620228826_1 enero 2025 - 1 julio 2025.xlsx_37 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116620108096         12990.0           Ajuste por Arrepentimiento POS_116620108096_1 enero 2025 - 1 julio 2025.xlsx_38 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116128317857         47990.0          Ajuste por Falla en Entrega POS_116128317857_1 enero 2025 - 1 julio 2025.xlsx_39 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116128369235         35990.0          Ajuste por Falla en Entrega POS_116128369235_1 enero 2025 - 1 julio 2025.xlsx_40 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113389029040         24990.0            Ajuste por Talla/Garantía POS_113389029040_1 enero 2025 - 1 julio 2025.xlsx_41 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116451558216         34990.0            Ajuste por Talla/Garantía POS_116451558216_1 enero 2025 - 1 julio 2025.xlsx_42 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116089725383          4490.0        Ajuste por Retraso en Entrega POS_116089725383_1 enero 2025 - 1 julio 2025.xlsx_43 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116581214354         13990.0        Ajuste por Retraso en Entrega POS_116581214354_1 enero 2025 - 1 julio 2025.xlsx_44 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116545497794         38990.0            Ajuste por Talla/Garantía POS_116545497794_1 enero 2025 - 1 julio 2025.xlsx_45 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114432812728         35990.0            Ajuste por Talla/Garantía POS_114432812728_1 enero 2025 - 1 julio 2025.xlsx_46 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113927719230         39990.0           Ajuste por Arrepentimiento POS_113927719230_1 enero 2025 - 1 julio 2025.xlsx_47 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116557041890         19990.0        Ajuste por Retraso en Entrega POS_116557041890_1 enero 2025 - 1 julio 2025.xlsx_48 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 112657666145         45990.0            Ajuste por Talla/Garantía POS_112657666145_1 enero 2025 - 1 julio 2025.xlsx_49 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115732141685         14990.0           Ajuste por Arrepentimiento POS_115732141685_1 enero 2025 - 1 julio 2025.xlsx_50 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115770034995         47990.0           Ajuste por Arrepentimiento POS_115770034995_1 enero 2025 - 1 julio 2025.xlsx_51 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113823873178         35990.0 Ajuste por Diferencia de Publicación POS_113823873178_1 enero 2025 - 1 julio 2025.xlsx_52 CLASIFICADO
```

## FASE 3: IdentificaciÃ³n de Registros

- **Registros Clasificados**: 11218
- **Registros Excluidos/Duplicados (Deduplicados en carga)**: 696
- **Registros HuÃ©rfanos**: 0
- **Registros Sin ClasificaciÃ³n**: 0

## FASE 4: Resultados y Delta

- **Total Devoluciones Fuente (Suma absoluta)**: $322,417,750.93
- **Total Devoluciones Ledger (Suma absoluta)**: $322,417,750.93
- **Delta**: $0.00

## CONCLUSIÃ“N DE AUDITORÃ A
Delta = 0