# DIRECTIVA DE AUDITORÍA DE TRAZABILIDAD DE DEVOLUCIONES

## FASE 1: Extracción desde Archivos Fuente

### Agrupación por Motivo y Flujo
```
      flow                                                                    reason_id                            reason_detail  operation_type operation_status  count  total_amount
chargeback                                                                           10                                      nan regular_payment     charged_back      1      19430.00
chargeback                                                                          104                                      nan regular_payment     charged_back      2      63440.00
chargeback                                                                         4837                    INVALID_AUTHORIZATION regular_payment     charged_back      1      35490.00
chargeback                                                                         4837                                      nan regular_payment     charged_back      1      19990.00
chargeback                                                                         4860                     CREDIT_NOT_PROCESSED regular_payment         refunded      1          0.00
chargeback                                                                         4860                                      nan regular_payment         refunded      1          0.00
     claim                                                                      PDD9502                          repentant_buyer regular_payment         refunded      1          0.00
     claim                                                                      PDD9536           not_expected_quality_different regular_payment         refunded      1          0.00
     claim                                                                      PDD9570        item_not_useful_fashion_different regular_payment         approved      1          0.00
     claim                                                                      PDD9829                        bought_by_mistake regular_payment         refunded      1          0.00
     claim                                                                      PDD9925 item_not_useful_fashion_different_change regular_payment         approved      6          0.00
     claim                                                                      PDD9925 item_not_useful_fashion_different_change regular_payment         refunded     90          0.00
     claim                                                                      PDD9925 item_not_useful_fashion_different_change regular_payment         rejected      2          0.00
     claim                                                                      PDD9926   different_color_or_size_fashion_change regular_payment         approved      2          0.00
     claim                                                                      PDD9926   different_color_or_size_fashion_change regular_payment         refunded     35          0.00
     claim                                                                      PDD9931              different_item_other_change regular_payment         refunded      1          0.00
     claim                                                                      PDD9939                          repentant_buyer regular_payment         approved     90          0.00
     claim                                                                      PDD9939                          repentant_buyer regular_payment        cancelled      2          0.00
     claim                                                                      PDD9939                          repentant_buyer regular_payment     in_mediation      8          0.00
     claim                                                                      PDD9939                          repentant_buyer regular_payment         refunded    550          0.00
     claim                                                                      PDD9939                          repentant_buyer regular_payment         rejected      6          0.00
     claim                                                                      PDD9941                  different_color_or_size regular_payment         approved      1          0.00
     claim                                                                      PDD9941                  different_color_or_size regular_payment         rejected      3          0.00
     claim                                                                      PDD9942                     different_item_other regular_payment         approved      5          0.00
     claim                                                                      PDD9942                     different_item_other regular_payment         refunded     12          0.00
     claim                                                                      PDD9944                 different_than_published regular_payment         approved      4          0.00
     claim                                                                      PDD9944                 different_than_published regular_payment     in_mediation      3          0.00
     claim                                                                      PDD9944                 different_than_published regular_payment         refunded     40          0.00
     claim                                                                      PDD9944                 different_than_published regular_payment         rejected      1          0.00
     claim                                                                      PDD9952                      missing_accessories regular_payment         approved      1          0.00
     claim                                                                      PDD9952                      missing_accessories regular_payment         refunded      2          0.00
     claim                                                                      PDD9955                             missing_item regular_payment         approved      3          0.00
     claim                                                                      PDD9955                             missing_item regular_payment         refunded      4          0.00
     claim                                                                      PDD9958                                empty_box regular_payment         approved      1          0.00
     claim                                                                      PDD9958                                empty_box regular_payment         refunded      2          0.00
     claim                                                                      PDD9960                          missing_invoice regular_payment         approved      2          0.00
     claim                                                                      PDD9960                          missing_invoice regular_payment         refunded      2          0.00
     claim                                                                      PDD9962             not_match_size_guide_fashion regular_payment         approved     12          0.00
     claim                                                                      PDD9962             not_match_size_guide_fashion regular_payment         refunded     77          0.00
     claim                                                                      PDD9962             not_match_size_guide_fashion regular_payment         rejected      4          0.00
     claim                                                                      PDD9963          different_color_or_size_fashion regular_payment         approved     33          0.00
     claim                                                                      PDD9963          different_color_or_size_fashion regular_payment     in_mediation      2          0.00
     claim                                                                      PDD9963          different_color_or_size_fashion regular_payment         refunded    149          0.00
     claim                                                                      PDD9963          different_color_or_size_fashion regular_payment         rejected      6          0.00
     claim                                                                      PDD9965                      broken_item_fashion regular_payment         approved     26          0.00
     claim                                                                      PDD9965                      broken_item_fashion regular_payment     in_mediation      2          0.00
     claim                                                                      PDD9965                      broken_item_fashion regular_payment         refunded     75          0.00
     claim                                                                      PDD9965                      broken_item_fashion regular_payment         rejected      1          0.00
     claim                                                                      PDD9966      damaged_package_broken_item_fashion regular_payment         refunded      1          0.00
     claim                                                                      PDD9976             bigger_than_expected_fashion regular_payment         approved    255          0.00
     claim                                                                      PDD9976             bigger_than_expected_fashion regular_payment        cancelled     10          0.00
     claim                                                                      PDD9976             bigger_than_expected_fashion regular_payment     in_mediation      1          0.00
     claim                                                                      PDD9976             bigger_than_expected_fashion regular_payment         refunded   1607          0.00
     claim                                                                      PDD9976             bigger_than_expected_fashion regular_payment         rejected     52          0.00
     claim                                                                      PDD9977            smaller_than_expected_fashion regular_payment         approved    305          0.00
     claim                                                                      PDD9977            smaller_than_expected_fashion regular_payment        cancelled      5          0.00
     claim                                                                      PDD9977            smaller_than_expected_fashion regular_payment     in_mediation      1          0.00
     claim                                                                      PDD9977            smaller_than_expected_fashion regular_payment         refunded   1377          0.00
     claim                                                                      PDD9977            smaller_than_expected_fashion regular_payment         rejected     17          0.00
     claim                                                                      PDD9978       dont_want_it_another_cause_fashion regular_payment         approved     89          0.00
     claim                                                                      PDD9978       dont_want_it_another_cause_fashion regular_payment         refunded    415          0.00
     claim                                                                      PDD9978       dont_want_it_another_cause_fashion regular_payment         rejected     14          0.00
     claim                                                                      PNR9501              undelivered_repentant_buyer regular_payment         approved      4          0.00
     claim                                                                      PNR9501              undelivered_repentant_buyer regular_payment         refunded    276          0.00
     claim                                                                      PNR9501              undelivered_repentant_buyer regular_payment         rejected      2          0.00
     claim                                                                      PNR9502                    respondent_unanswered regular_payment        cancelled      1          0.00
     claim                                                                      PNR9502                    respondent_unanswered regular_payment         refunded      4          0.00
     claim                                                                      PNR9502                    respondent_unanswered regular_payment         rejected      1          0.00
     claim                                                                      PNR9503                             out_of_stock regular_payment         refunded      5          0.00
     claim                                                                      PNR9504           estimated_delivery_out_of_time regular_payment         refunded     55          0.00
     claim                                                                      PNR9505                  change_receiver_address regular_payment         refunded     20          0.00
     claim                                                                      PNR9506                            buy_out_of_ml regular_payment         refunded      1          0.00
     claim                                                                      PNR9507                    unauthorized_purchase regular_payment         approved      3          0.00
     claim                                                                      PNR9507                    unauthorized_purchase regular_payment         refunded      9          0.00
     claim                                                                      PNR9507                    unauthorized_purchase regular_payment         rejected      2          0.00
     claim                                                                      PNR9508                        undelivered_other regular_payment         refunded     93          0.00
     claim                                                                      PNR9508                        undelivered_other regular_payment         rejected      2          0.00
     claim                                                                      PNR9509              undelivered_repentant_buyer regular_payment        cancelled      3          0.00
     claim                                                                      PNR9509              undelivered_repentant_buyer regular_payment         refunded    123          0.00
     claim                                                                      PNR9509              undelivered_repentant_buyer regular_payment         rejected      4          0.00
     claim                                                                      PNR9510           estimated_delivery_out_of_time regular_payment         refunded     25          0.00
     claim                                                                      PNR9510           estimated_delivery_out_of_time regular_payment         rejected      1          0.00
     claim                                                                      PNR9511                  change_receiver_address regular_payment         refunded      6          0.00
     claim                                                                      PNR9512                    unauthorized_purchase regular_payment         refunded      6          0.00
     claim                                                                      PNR9512                    unauthorized_purchase regular_payment         rejected      3          0.00
     claim                                                                      PNR9513                        undelivered_other regular_payment         refunded     47          0.00
     claim                                                                      PNR9513                        undelivered_other regular_payment         rejected      1          0.00
     claim                                                                      PNR9521                delivery_date_was_not_met regular_payment         approved     11          0.00
     claim                                                                      PNR9521                delivery_date_was_not_met regular_payment         refunded      2          0.00
     claim                                                                      PNR9560        delivered_but_not_receive_package regular_payment         approved      8          0.00
     claim                                                                      PNR9560        delivered_but_not_receive_package regular_payment         refunded      3          0.00
     claim                                                                      PNR9567        delivered_but_not_receive_package regular_payment         approved      9          0.00
     claim                                                                      PNR9567        delivered_but_not_receive_package regular_payment         refunded     10          0.00
    refund                                     Abrigo 4 Botones Azul Eléctrico Nicopoly                                      nan regular_payment         refunded      8     519920.00
    refund                                             Abrigo 4 Botones Morado Nicopoly                                      nan regular_payment         refunded     14     851860.00
    refund                                              Abrigo 4 Botones Negro Nicopoly                                      nan regular_payment         refunded      6     359940.00
    refund                                               Abrigo 4 Botones Rojo Nicopoly                                      nan regular_payment         refunded     10     607900.00
    refund                                              Abrigo 4 Botones Óxido Nicopoly                                      nan regular_payment         refunded      2     135980.00
    refund                                               Abrigo Bouclé Grafito Nicopoly                                      nan regular_payment         refunded     17     725842.00
    refund                                                 Abrigo Bouclé Khaki Nicopoly                                      nan regular_payment         refunded     16     712840.00
    refund                                                 Abrigo Bouclé Negro Nicopoly                                      nan regular_payment         refunded     24    1035270.00
    refund                                       Abrigo Básico 2 Botones Negro Nicopoly                                      nan regular_payment         refunded     20    1057800.00
    refund                              Abrigo Cierre Lateral Café Nicopoly Café M Liso                                      nan regular_payment         refunded      1      71990.00
    refund                              Abrigo Cierre Lateral Café Nicopoly Café S Liso                                      nan regular_payment         refunded      1      79990.00
    refund                            Abrigo Cierre Lateral Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      2     131780.00
    refund                            Abrigo Cierre Lateral Oliva Nicopoly Oliva L Liso                                      nan regular_payment         refunded      1      79990.00
    refund                            Abrigo Cierre Lateral Oliva Nicopoly Oliva M Liso                                      nan regular_payment         refunded      2      99980.00
    refund                           Abrigo Cierre Lateral Oliva Nicopoly Oliva Xl Liso                                      nan regular_payment         refunded      2     127980.00
    refund                       Abrigo Cinturón Y Solapa Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment         refunded      1      94990.00
    refund                     Abrigo Con Solapa Y Cinturón Beige Nicopoly Beige M Liso                                      nan regular_payment         refunded      1     136990.00
    refund                                                  Abrigo Corto Beige Nicopoly                                      nan regular_payment         refunded     15     451270.00
    refund                                                  Abrigo Corto Khaki Nicopoly                                      nan regular_payment         refunded     19     641975.00
    refund                                                  Abrigo Corto Negro Nicopoly                                      nan regular_payment         refunded     14     377198.00
    refund                                                  Abrigo Cotelé Café Nicopoly                                      nan regular_payment         refunded      3     107970.00
    refund                                               Abrigo Cotelé Celeste Nicopoly                                      nan regular_payment         refunded      3     111970.00
    refund                                              Abrigo Cuadrillé Negro Nicopoly                                      nan regular_payment         refunded     14     640620.00
    refund                     Abrigo Cuello Pelo Sintético Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      79990.00
    refund                                      Abrigo Forro Tipo Piel Grafito Nicopoly                                      nan regular_payment         refunded     13     716097.00
    refund                                      Abrigo Gorro Desmontable Beige Nicopoly                                      nan regular_payment         refunded      4     191960.00
    refund                                       Abrigo Gorro Desmontable Café Nicopoly                                      nan regular_payment         refunded      5     285950.00
    refund                      Abrigo Hombros Caídos Blanco Invierno Invierno Nicopoly                                      nan regular_payment         refunded     12     465898.00
    refund                                          Abrigo Hombros Caídos Gris Nicopoly                                      nan regular_payment         refunded     10     311916.00
    refund                                          Abrigo Hombros Caídos Moca Nicopoly                                      nan regular_payment         refunded     27     792890.00
    refund                                         Abrigo Hombros Caídos Negro Nicopoly                                      nan regular_payment         refunded     25     703346.00
    refund                                      Abrigo Interior Corderito Café Nicopoly                                      nan regular_payment         refunded     19    1000613.00
    refund                                             Abrigo Largo Lazo Camel Nicopoly                                      nan regular_payment         refunded      6     328690.00
    refund                                           Abrigo Largo Lazo Celeste Nicopoly                                      nan regular_payment         refunded      6     357440.00
    refund                                             Abrigo Largo Lazo Negro Nicopoly                                      nan regular_payment         refunded      6     411190.00
    refund                                              Abrigo Largo Lazo Rojo Nicopoly                                      nan regular_payment         refunded      6     400190.00
    refund                                               Abrigo Largo Lazo Uva Nicopoly                                      nan regular_payment         refunded      3     176220.00
    refund                                 Abrigo Oversize Pied De Poule Khaki Nicopoly                                      nan regular_payment         refunded      3      66480.00
    refund                                  Abrigo Oversize Pied De Poule Rojo Nicopoly                                      nan regular_payment         refunded      4     144960.00
    refund                                        Abrigo Patrón Espiga Grafito Nicopoly                                      nan regular_payment         refunded     14     671370.00
    refund                                          Abrigo Pied De Poule Negro Nicopoly                                      nan regular_payment         refunded     14     588260.00
    refund                                       Abrigo Solapa Redonda Celeste Nicopoly                                      nan regular_payment         refunded      4     220460.00
    refund                                          Abrigo Solapa Redonda Negronicopoly                                      nan regular_payment         refunded     12     713584.00
    refund                                          Abrigo Solapa Redonda Rojo Nicopoly                                      nan regular_payment         refunded      9     519910.00
    refund                                           Abrigo Solapa Redonda Uva Nicopoly                                      nan regular_payment         refunded      8     358940.00
    refund                                    Abrigo Solapa Redonda Verde Lima Nicopoly                                      nan regular_payment         refunded      4     223960.00
    refund         Abrigo Solapa Redonda Verde Petróleo Nicopoly Verde Petróleo Xl Liso                                      nan regular_payment         refunded      1      71990.00
    refund                         Abrigo Solapa Y Cinturón Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      2     161980.00
    refund                         Abrigo Solapa Y Cinturón Negro Nicopoly Negro S Liso                                      nan regular_payment         refunded      1      76990.00
    refund                        Abrigo Solapa Y Cinturón Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      1      76990.00
    refund                           Abrigo Solapa Y Cinturón Rojo Nicopoly Rojo L Liso                                      nan regular_payment         refunded      1      76990.00
    refund                           Abrigo Solapa Y Cinturón Rojo Nicopoly Rojo S Liso                                      nan regular_payment         refunded      1      76990.00
    refund                          Abrigo Solapa Y Cinturón Rojo Nicopoly Rojo Xl Liso                                      nan regular_payment         refunded      1      50990.00
    refund                                     Abrigo Tipo Paño 2 Botones Gris Nicopoly                                      nan regular_payment         refunded      4     239960.00
    refund                                     Abrigo Tipo Paño 2 Botones Negronicopoly                                      nan regular_payment         refunded     14     821860.00
    refund                                    Abrigo Tipo Paño 2 Botones Óxido Nicopoly                                      nan regular_payment         refunded      2      55990.00
    refund                                  Blazer 4 Botones Decorativos Negro Nicopoly                                      nan regular_payment         refunded     16     491532.00
    refund                                   Blazer 4 Botones Decorativos Rojo Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                Blazer 6 Botones Grafito - Grafito - M - Liso                                      nan regular_payment         refunded      1      27990.00
    refund                                      Blazer 6 Botones Grafito Grafito L Liso                                      nan regular_payment         refunded      1      27990.00
    refund                                      Blazer 6 Botones Grafito Grafito M Liso                                      nan regular_payment         refunded      1      27990.00
    refund                                      Blazer 6 Botones Grafito L Liso Grafito                                      nan regular_payment         refunded      1      27990.00
    refund                               Blazer 6 Botones Marrón Nicopoly Marrón L Liso                                      nan regular_payment         refunded      3      80050.00
    refund                                 Blazer 6 Botones Marrón Nicopoly Marrón Liso                                      nan regular_payment         refunded      2      67180.00
    refund                               Blazer 6 Botones Marrón Nicopoly Marrón M Liso                                      nan regular_payment         refunded      1      32990.00
    refund                                                Blazer 6 Botones Negro L Liso                                      nan regular_payment         refunded      1      33590.00
    refund                                                Blazer 6 Botones Negro M Liso                                      nan regular_payment         refunded      2      67180.00
    refund                                          Blazer 6 Botones Negro Negro L Liso                                      nan regular_payment         refunded      5     195950.00
    refund                                          Blazer 6 Botones Negro Negro M Liso                                      nan regular_payment         refunded      1      27990.00
    refund                                          Blazer 6 Botones Negro Negro S Liso                                      nan regular_payment         refunded      3     111970.00
    refund                                         Blazer 6 Botones Negro Negro Xl Liso                                      nan regular_payment         refunded      6     139960.00
    refund                                               Blazer 6 Botones Negro Xl Liso                                      nan regular_payment         refunded      1      55990.00
    refund                                            Blazer 6 Botones Rojo L Rojo Liso                                      nan regular_payment         refunded      2      65980.00
    refund                                                 Blazer 6 Botones Rojo M Liso                                      nan regular_payment         refunded      1      24070.00
    refund                                            Blazer 6 Botones Rojo Rojo L Liso                                      nan regular_payment         refunded      5      68100.00
    refund                                            Blazer 6 Botones Rojo Rojo M Liso                                      nan regular_payment         refunded      3     116970.00
    refund                                            Blazer 6 Botones Rojo Rojo S Liso                                      nan regular_payment         refunded      1      27990.00
    refund                                           Blazer 6 Botones Rojo Rojo Xl Liso                                      nan regular_payment         refunded      3     139970.00
    refund                                                 Blazer 6 Botones Rojo S Liso                                      nan regular_payment         refunded      1      33590.00
    refund                                                Blazer 6 Botones Rojo Xl Liso                                      nan regular_payment         refunded      1      33590.00
    refund                                           Blazer 6 Botones Rojo Xl Rojo Liso                                      nan regular_payment         refunded      1      32990.00
    refund                             Blazer Bolsillos Con Solapas Azul Medio Nicopoly                                      nan regular_payment         refunded      1      52990.00
    refund                                  Blazer Bolsillos Con Solapas Khaki Nicopoly                                      nan regular_payment         refunded      3      71730.00
    refund                                     Blazer Bolsillos Y Botón  Negro Nicopoly                                      nan regular_payment         refunded      6     215940.00
    refund                                    Blazer Bolsillos Y Botón Celeste Nicopoly                                      nan regular_payment         refunded      5     127460.00
    refund                                       Blazer Bolsillos Y Botón Rojo Nicopoly                                      nan regular_payment         refunded      3      94770.00
    refund                                    Blazer Botones Decorativos Crema Nicopoly                                      nan regular_payment         refunded     10     281305.00
    refund                              Blazer Básico De Tope Azul Nicopoly Azul L Lisa                                      nan regular_payment         refunded      4     107970.00
    refund                              Blazer Básico De Tope Azul Nicopoly Azul S Lisa                                      nan regular_payment         refunded      1      26990.00
    refund                             Blazer Básico De Tope Azul Nicopoly Azul Xl Lisa                                      nan regular_payment         refunded      1      29990.00
    refund                                   Blazer Básico De Tope Azul Nicopoly M Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                              Blazer Básico De Tope Azul Nicopoly S Azul Lisa                                      nan regular_payment         refunded      2      71980.00
    refund                                   Blazer Básico De Tope Azul Nicopoly S Lisa                                      nan regular_payment         refunded      1      31490.00
    refund                             Blazer Básico De Tope Azul Nicopoly Xl Azul Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                                  Blazer Básico De Tope Azul Nicopoly Xl Lisa                                      nan regular_payment         refunded      1      31490.00
    refund                            Blazer Básico De Tope Azul Nicopoly Xxl Azul Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                          Blazer Básico De Tope Blanco Nicopoly Blanco L Lisa                                      nan regular_payment         refunded      8     227185.00
    refund                         Blazer Básico De Tope Blanco Nicopoly Blanco Xl Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                        Blazer Básico De Tope Blanco Nicopoly Blanco Xxl Lisa                                      nan regular_payment         refunded      3      89970.00
    refund                          Blazer Básico De Tope Blanco Nicopoly L Lisa Blanco                                      nan regular_payment         refunded      2      71980.00
    refund                                 Blazer Básico De Tope Blanco Nicopoly M Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                                Blazer Básico De Tope Blanco Nicopoly Xl Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                              Blazer Básico De Tope Café Nicopoly Café M Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                              Blazer Básico De Tope Café Nicopoly Café S Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                             Blazer Básico De Tope Café Nicopoly Café Xl Lisa                                      nan regular_payment         refunded      8     305920.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris L Lisa                                      nan regular_payment         refunded     10     359900.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris M Lisa                                      nan regular_payment         refunded      8     220430.00
    refund                              Blazer Básico De Tope Gris Nicopoly Gris S Lisa                                      nan regular_payment         refunded      3      86970.00
    refund                             Blazer Básico De Tope Gris Nicopoly Gris Xl Lisa                                      nan regular_payment         refunded      6     196440.00
    refund                            Blazer Básico De Tope Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment         refunded      8     161150.00
    refund                              Blazer Básico De Tope Gris Nicopoly L Gris Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                                   Blazer Básico De Tope Gris Nicopoly L Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                      Blazer Básico De Tope Khaki Nicopoly - Khaki - S - Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                     Blazer Básico De Tope Khaki Nicopoly - Khaki - Xl - Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                            Blazer Básico De Tope Khaki Nicopoly Khaki L Lisa                                      nan regular_payment         refunded      2      61480.00
    refund                            Blazer Básico De Tope Khaki Nicopoly Khaki M Lisa                                      nan regular_payment         refunded      2      61480.00
    refund                            Blazer Básico De Tope Khaki Nicopoly Khaki S Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                           Blazer Básico De Tope Khaki Nicopoly Khaki Xl Lisa                                      nan regular_payment         refunded      7      88088.00
    refund                                 Blazer Básico De Tope Morado Nicopoly L Lisa                                      nan regular_payment         refunded      1      31490.00
    refund                          Blazer Básico De Tope Morado Nicopoly L Lisa Morado                                      nan regular_payment         refunded      1      35990.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado L Lisa                                      nan regular_payment         refunded      4     143960.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado M Lisa                                      nan regular_payment         refunded      9     248140.00
    refund                          Blazer Básico De Tope Morado Nicopoly Morado S Lisa                                      nan regular_payment         refunded      2      89980.00
    refund                         Blazer Básico De Tope Morado Nicopoly Morado Xl Lisa                                      nan regular_payment         refunded      3      91470.00
    refund                         Blazer Básico De Tope Morado Nicopoly Xl Lisa Morado                                      nan regular_payment         refunded      1      35990.00
    refund                      Blazer Básico De Tope Negro Nicopoly - Negro - L - Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                                  Blazer Básico De Tope Negro Nicopoly L Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                            Blazer Básico De Tope Negro Nicopoly M Lisa Negro                                      nan regular_payment         refunded      2      71980.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro L Lisa                                      nan regular_payment         refunded      4     143960.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro M Lisa                                      nan regular_payment         refunded      4     121460.00
    refund                            Blazer Básico De Tope Negro Nicopoly Negro S Lisa                                      nan regular_payment         refunded      4     149960.00
    refund                           Blazer Básico De Tope Negro Nicopoly Negro Xl Lisa                                      nan regular_payment         refunded      6     188940.00
    refund                          Blazer Básico De Tope Negro Nicopoly Negro Xxl Lisa                                      nan regular_payment         refunded      2      58480.00
    refund                                Blazer Básico De Tope Negro Nicopoly Xxl Lisa                                      nan regular_payment         refunded      2      80980.00
    refund                        Blazer Básico De Tope Rojo Nicopoly - Rojo - M - Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                              Blazer Básico De Tope Rojo Nicopoly Rojo L Lisa                                      nan regular_payment         refunded      1      36990.00
    refund                              Blazer Básico De Tope Rojo Nicopoly Rojo M Lisa                                      nan regular_payment         refunded      2      59980.00
    refund                              Blazer Básico De Tope Rojo Nicopoly Rojo S Lisa                                      nan regular_payment         refunded      2      61480.00
    refund                             Blazer Básico De Tope Rojo Nicopoly Rojo Xl Lisa                                      nan regular_payment         refunded      6     202440.00
    refund                   Blazer Básico De Tope Rosado Nicopoly - Rosado - Xl - Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                                 Blazer Básico De Tope Rosado Nicopoly L Lisa                                      nan regular_payment         refunded      3     107970.00
    refund                          Blazer Básico De Tope Rosado Nicopoly Rosado M Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                          Blazer Básico De Tope Rosado Nicopoly Rosado S Lisa                                      nan regular_payment         refunded      2      89980.00
    refund                         Blazer Básico De Tope Rosado Nicopoly Rosado Xl Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                        Blazer Básico De Tope Rosado Nicopoly Rosado Xxl Lisa                                      nan regular_payment         refunded      2      65980.00
    refund                                Blazer Básico De Tope Rosado Nicopoly Xl Lisa                                      nan regular_payment         refunded      5      80216.00
    refund                         Blazer Básico De Tope Rosado Nicopoly Xl Lisa Rosado                                      nan regular_payment         refunded      1      35990.00
    refund                               Blazer Básico De Tope Rosado Nicopoly Xxl Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                            Blazer Básico De Tope Verde Nicopoly Verde L Lisa                                      nan regular_payment         refunded      3     134970.00
    refund                            Blazer Básico De Tope Verde Nicopoly Verde M Lisa                                      nan regular_payment         refunded      6     260940.00
    refund                            Blazer Básico De Tope Verde Nicopoly Verde S Lisa                                      nan regular_payment         refunded      1      44990.00
    refund                           Blazer Básico De Tope Verde Nicopoly Verde Xl Lisa                                      nan regular_payment         refunded      4     107970.00
    refund                            Blazer Básico De Tope Óxido Nicopoly Óxido M Lisa                                      nan regular_payment         refunded      1      35990.00
    refund                           Blazer Básico De Tope Óxido Nicopoly Óxido Xl Lisa                                      nan regular_payment         refunded      2      89980.00
    refund                                            Blazer Con Solapa Blanco Nicopoly                                      nan regular_payment         refunded      2      51480.00
    refund                                             Blazer Con Solapa Khaki Nicopoly                                      nan regular_payment         refunded      3      81470.00
    refund                                             Blazer Con Solapa Negro Nicopoly                                      nan regular_payment         refunded     13     359071.00
    refund                                                   Blazer Corto Rosa Nicopoly                                      nan regular_payment         refunded      1      39990.00
    refund                                                Blazer Cotelé Burdeo Nicopoly                                      nan regular_payment         refunded     19     611340.00
    refund                                       Blazer Cruzado Ecocuero Negro Nicopoly                                      nan regular_payment         refunded     15     450560.00
    refund                           Blazer Cruzado Pied De Poule Blanco/negro Nicopoly                                      nan regular_payment         refunded      1      39990.00
    refund                          Blazer Cruzado Sin Mangas Gris Nicopoly Gris M Liso                                      nan regular_payment         refunded      3      34990.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco L Lisa                                      nan regular_payment         refunded      3     114970.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco M Lisa                                      nan regular_payment         refunded      5     189950.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly Blanco S Lisa                                      nan regular_payment         refunded      3     109970.00
    refund                         Blazer Cuello Cruzado Blanco Nicopoly Blanco Xl Lisa                                      nan regular_payment         refunded      7     254930.00
    refund                        Blazer Cuello Cruzado Blanco Nicopoly Blanco Xxl Lisa                                      nan regular_payment         refunded      6     224940.00
    refund                                 Blazer Cuello Cruzado Blanco Nicopoly L Lisa                                      nan regular_payment         refunded      2      74980.00
    refund                                 Blazer Cuello Cruzado Blanco Nicopoly M Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                                 Blazer Cuello Cruzado Blanco Nicopoly S Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                          Blazer Cuello Cruzado Blanco Nicopoly S Lisa Blanco                                      nan regular_payment         refunded      1      31992.00
    refund                                Blazer Cuello Cruzado Blanco Nicopoly Xl Lisa                                      nan regular_payment         refunded      1      34990.00
    refund                  Blazer Cuello Cruzado Celeste Nicopoly - Celeste - L - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                  Blazer Cuello Cruzado Celeste Nicopoly - Celeste - S - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                 Blazer Cuello Cruzado Celeste Nicopoly - Celeste - Xl - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste L Lisa                                      nan regular_payment         refunded      4     139960.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste M Lisa                                      nan regular_payment         refunded      3     134970.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly Celeste S Lisa                                      nan regular_payment         refunded      2      34990.00
    refund                       Blazer Cuello Cruzado Celeste Nicopoly Celeste Xl Lisa                                      nan regular_payment         refunded      9     249930.00
    refund                      Blazer Cuello Cruzado Celeste Nicopoly Celeste Xxl Lisa                                      nan regular_payment         refunded      3     119970.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly L Lisa Celeste                                      nan regular_payment         refunded      1      39990.00
    refund                        Blazer Cuello Cruzado Celeste Nicopoly M Lisa Celeste                                      nan regular_payment         refunded      1      39990.00
    refund                                Blazer Cuello Cruzado Celeste Nicopoly S Lisa                                      nan regular_payment         refunded      1      34990.00
    refund                              Blazer Cuello Cruzado Celeste Nicopoly Xxl Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                       Blazer Cuello Cruzado Gris Nicopoly - Gris - Xl - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly Gris L Lisa                                      nan regular_payment         refunded      2      69980.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly Gris M Lisa                                      nan regular_payment         refunded      1      34990.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly Gris S Lisa                                      nan regular_payment         refunded      2      69980.00
    refund                             Blazer Cuello Cruzado Gris Nicopoly Gris Xl Lisa                                      nan regular_payment         refunded      1      34990.00
    refund                            Blazer Cuello Cruzado Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment         approved      1       5248.50
    refund                            Blazer Cuello Cruzado Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment         refunded      3     104970.00
    refund                              Blazer Cuello Cruzado Gris Nicopoly L Gris Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                      Blazer Cuello Cruzado Khaki Nicopoly - Khaki - M - Lisa                                      nan regular_payment         refunded      2      79980.00
    refund                            Blazer Cuello Cruzado Khaki Nicopoly Khaki L Lisa                                      nan regular_payment         refunded      2      79980.00
    refund                            Blazer Cuello Cruzado Khaki Nicopoly Khaki M Lisa                                      nan regular_payment         refunded      1      34990.00
    refund                           Blazer Cuello Cruzado Khaki Nicopoly Khaki Xl Lisa                                      nan regular_payment         refunded      7     168278.00
    refund                           Blazer Cuello Cruzado Khaki Nicopoly Xl Lisa Khaki                                      nan regular_payment         refunded      1      39990.00
    refund                                 Blazer Cuello Cruzado Morado Nicopoly M Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                          Blazer Cuello Cruzado Morado Nicopoly Morado L Lisa                                      nan regular_payment         refunded      4     134970.00
    refund                          Blazer Cuello Cruzado Morado Nicopoly Morado M Lisa                                      nan regular_payment         refunded      4     174960.00
    refund                          Blazer Cuello Cruzado Morado Nicopoly Morado S Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                         Blazer Cuello Cruzado Morado Nicopoly Morado Xl Lisa                                      nan regular_payment         refunded      3     119970.00
    refund                      Blazer Cuello Cruzado Negro Nicopoly - Negro - M - Lisa                                      nan regular_payment         refunded      2      79980.00
    refund                      Blazer Cuello Cruzado Negro Nicopoly - Negro - S - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                   Blazer Cuello Cruzado Negro Nicopoly Blanco,negro Xxl Lisa                                      nan regular_payment         refunded      2      99980.00
    refund                                  Blazer Cuello Cruzado Negro Nicopoly L Lisa                                      nan regular_payment         refunded      2      84980.00
    refund                                  Blazer Cuello Cruzado Negro Nicopoly M Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro L Lisa                                      nan regular_payment         refunded     10     364910.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro M Lisa                                      nan regular_payment         refunded      5     169950.00
    refund                            Blazer Cuello Cruzado Negro Nicopoly Negro S Lisa                                      nan regular_payment         refunded     10     294920.00
    refund                           Blazer Cuello Cruzado Negro Nicopoly Negro Xl Lisa                                      nan regular_payment         refunded      8     324920.00
    refund                                   Blazer Cuello Cruzado Rojo Nicopoly M Lisa                                      nan regular_payment         refunded      1      34990.00
    refund                              Blazer Cuello Cruzado Rojo Nicopoly Rojo L Lisa                                      nan regular_payment         refunded      3     149970.00
    refund                              Blazer Cuello Cruzado Rojo Nicopoly Rojo M Lisa                                      nan regular_payment         refunded      1      29990.00
    refund                             Blazer Cuello Cruzado Rojo Nicopoly Rojo Xl Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                            Blazer Cuello Cruzado Verde Nicopoly Verde M Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                            Blazer Cuello Cruzado Verde Nicopoly Verde S Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                           Blazer Cuello Cruzado Verde Nicopoly Verde Xl Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                                 Blazer Cuello Cruzado Verde Nicopoly Xl Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                                             Blazer Cuello Mao Khaki Nicopoly                                      nan regular_payment         refunded      8     294920.00
    refund                                            Blazer Cuello Mao Morado Nicopoly                                      nan regular_payment         refunded     13     504873.00
    refund                                             Blazer Cuello Mao Negro Nicopoly                                      nan regular_payment         refunded     10     371900.00
    refund                                              Blazer Cuello Mao Rojo Nicopoly                                      nan regular_payment         refunded     10     356400.00
    refund                                      Blazer Cuello Mao Verde Oscuro Nicopoly                                      nan regular_payment         refunded     11     409890.00
    refund                   Blazer Cuello Redondo Sin Solapa Gris Nicopoly Gris S Liso                                      nan regular_payment         refunded      1      43990.00
    refund                                     Blazer Cuello Sin Solapa Blanco Nicopoly                                      nan regular_payment         refunded      9     272910.00
    refund              Blazer Cuello Sin Solapa Celeste Nicopoly - Celeste - Xl - Liso                                      nan regular_payment         refunded      1      34990.00
    refund                     Blazer Cuello Sin Solapa Celeste Nicopoly Celeste L Liso                                      nan regular_payment         refunded      1      34990.00
    refund                    Blazer Cuello Sin Solapa Celeste Nicopoly Celeste Xl Liso                                      nan regular_payment         refunded      2      55980.00
    refund                             Blazer Cuello Sin Solapa Celeste Nicopoly L Liso                                      nan regular_payment         refunded      1      34990.00
    refund                               Blazer Cuello Sin Solapa Celeste Nicopoly Liso                                      nan regular_payment         refunded      4      40020.00
    refund                             Blazer Cuello Sin Solapa Celeste Nicopoly M Liso                                      nan regular_payment         refunded      1      34990.00
    refund                     Blazer Cuello Sin Solapa Celeste Nicopoly M Liso Celeste                                      nan regular_payment         refunded      1      34990.00
    refund                     Blazer Cuello Sin Solapa Celeste Nicopoly S Liso Celeste                                      nan regular_payment         refunded      1      34990.00
    refund                                      Blazer Cuello Sin Solapa Negro Nicopoly                                      nan regular_payment         refunded     18     538820.00
    refund                                       Blazer Cuello Sin Solapa Rojo Nicopoly                                      nan regular_payment         refunded      8     194430.00
    refund                       Blazer Cuello Sin Solapa Rosado Nicopoly Rosado L Liso                                      nan regular_payment         refunded      1      27990.00
    refund                       Blazer Cuello Sin Solapa Rosado Nicopoly Rosado M Liso                                      nan regular_payment         refunded      4      90960.00
    refund                       Blazer Cuello Sin Solapa Rosado Nicopoly Rosado S Liso                                      nan regular_payment         refunded      1      27990.00
    refund                            Blazer De Tope Botones Decorativos Negro Nicopoly                                      nan regular_payment         refunded      2      89980.00
    refund                      Blazer De Tope Botones Decorativos Rojo Oscuro Nicopoly                                      nan regular_payment         refunded      3     125970.00
    refund                      Blazer De Tope Botones Decorativosverde Oscuro Nicopoly                                      nan regular_payment         refunded      3     134970.00
    refund                                      Blazer De Tope Manga 3/4 Beige Nicopoly                                      nan regular_payment         refunded      2      89980.00
    refund                                     Blazer De Tope Manga 3/4 Burdeo Nicopoly                                      nan regular_payment         refunded      9     449910.00
    refund                                      Blazer De Tope Manga 3/4 Negro Nicopoly                                      nan regular_payment         refunded      1      49990.00
    refund          Blazer De Tope Manga 3/4 Recogida Beige Nicopoly - Beige - L - Liso                                      nan regular_payment         refunded      1      39990.00
    refund          Blazer De Tope Manga 3/4 Recogida Beige Nicopoly - Beige - M - Liso                                      nan regular_payment         refunded      1      39990.00
    refund                Blazer De Tope Manga 3/4 Recogida Beige Nicopoly Beige L Liso                                      nan regular_payment         refunded      2      89980.00
    refund                Blazer De Tope Manga 3/4 Recogida Beige Nicopoly Beige M Liso                                      nan regular_payment         refunded      1      49990.00
    refund                Blazer De Tope Manga 3/4 Recogida Beige Nicopoly Beige S Liso                                      nan regular_payment         refunded      1      49990.00
    refund                      Blazer De Tope Manga 3/4 Recogida Beige Nicopoly M Liso                                      nan regular_payment         refunded      1      39990.00
    refund              Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment         refunded      2      73980.00
    refund              Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Burdeo S Liso                                      nan regular_payment         refunded      1      49990.00
    refund             Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment         refunded      1      49990.00
    refund                     Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly L Liso                                      nan regular_payment         refunded      2      89980.00
    refund                    Blazer De Tope Manga 3/4 Recogida Burdeo Nicopoly Xl Liso                                      nan regular_payment         refunded      3     124970.00
    refund            Blazer De Tope Manga 3/4 Recogida Celeste Nicopoly Celeste S Liso                                      nan regular_payment         refunded      1      49990.00
    refund                  Blazer De Tope Manga 3/4 Recogida Rojo Nicopoly Rojo L Liso                                      nan regular_payment         refunded      1      39990.00
    refund                  Blazer De Tope Manga 3/4 Recogida Rojo Nicopoly Rojo M Liso                                      nan regular_payment         refunded      3     109970.00
    refund                 Blazer De Tope Manga 3/4 Recogida Rojo Nicopoly Rojo Xl Liso                                      nan regular_payment         refunded      1      49990.00
    refund                                       Blazer De Tope Manga 3/4 Rojo Nicopoly                                      nan regular_payment         refunded      1      49990.00
    refund                                                Blazer Escocés Negro Nicopoly                                      nan regular_payment         refunded      4      82470.00
    refund                                             Blazer Floreado Celeste Nicopoly                                      nan regular_payment         refunded      8     263920.00
    refund                                               Blazer Floreado Negro Nicopoly                                      nan regular_payment         refunded     16     552730.00
    refund                                      Blazer Largo 4 Botones Celeste Nicopoly                                      nan regular_payment         refunded      5     143634.00
    refund                                        Blazer Largo 4 Botones Khaki Nicopoly                                      nan regular_payment         refunded     12     370286.00
    refund                                        Blazer Largo 4 Botones Negro Nicopoly                                      nan regular_payment         refunded      6     137350.00
    refund                  Blazer Largo 4 Botones Rosado Nicopoly - Rosado - Xl - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                                Blazer Largo 4 Botones Rosado Nicopoly L Lisa                                      nan regular_payment         refunded      3     129970.00
    refund                                Blazer Largo 4 Botones Rosado Nicopoly M Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                         Blazer Largo 4 Botones Rosado Nicopoly Rosado M Lisa                                      nan regular_payment         refunded      1      29990.00
    refund                         Blazer Largo 4 Botones Rosado Nicopoly Rosado S Lisa                                      nan regular_payment         refunded      2      69980.00
    refund                        Blazer Largo 4 Botones Rosado Nicopoly Rosado Xl Lisa                                      nan regular_payment         refunded      6     121466.00
    refund                       Blazer Largo 4 Botones Rosado Nicopoly Rosado Xxl Lisa                                      nan regular_payment         refunded      3     109970.00
    refund                               Blazer Largo 4 Botones Rosado Nicopoly Xl Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                       Blazer Largo 4 Botones Rosado Nicopoly Xxl Lisa Rosado                                      nan regular_payment         refunded      2      79980.00
    refund                                               Blazer Largo Amarillo Nicopoly                                      nan regular_payment         refunded     10     339910.00
    refund                                   Blazer Largo Cuello Cruzado Khaki Nicopoly                                      nan regular_payment         refunded     14     769840.00
    refund                                  Blazer Largo Cuello Cruzado Morado Nicopoly                                      nan regular_payment         refunded      6     269940.00
    refund                                   Blazer Largo Cuello Cruzado Negro Nicopoly                                      nan regular_payment         refunded      8     399920.00
    refund                             Blazer Largo Cuello Cruzado Rojo Oscuro Nicopoly                                      nan regular_payment         refunded      7     309930.00
    refund                                          Blazer Largo De Tope Negro Nicopoly                                      nan regular_payment         refunded     10     253822.00
    refund                                           Blazer Largo De Tope Rojo Nicopoly                                      nan regular_payment         refunded     13     479880.00
    refund                                   Blazer Largo Manga Drapeada Negro Nicopoly                                      nan regular_payment         refunded      1      39990.00
    refund                                              Blazer Largo Terracota Nicopoly                                      nan regular_payment         refunded      2      64980.00
    refund                                         Blazer Lazo Delantero Negro Nicopoly                                      nan regular_payment         refunded     12     404880.00
    refund                                          Blazer Lazo Delantero Rojo Nicopoly                                      nan regular_payment         refunded      8     354900.00
    refund            Blazer Manga 3/4 Ajustada Con Pliegues Blanco - Blanco - L - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Blanco Blanco L Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Blanco M Lisa                                      nan regular_payment         refunded      2      99980.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Blanco S Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                      Blazer Manga 3/4 Ajustada Con Pliegues Celeste Nicopoly                                      nan regular_payment         refunded      3     139970.00
    refund            Blazer Manga 3/4 Ajustada Con Pliegues Marrón - Marrón - M - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Marrón M Lisa Marrón                                      nan regular_payment         refunded      1      39990.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Marrón Marrón S Lisa                                      nan regular_payment         refunded      3     134970.00
    refund                 Blazer Manga 3/4 Ajustada Con Pliegues Marrón Xl Lisa Marrón                                      nan regular_payment         refunded      1      39990.00
    refund              Blazer Manga 3/4 Ajustada Con Pliegues Negro - Negro - L - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund              Blazer Manga 3/4 Ajustada Con Pliegues Negro - Negro - M - Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                    Blazer Manga 3/4 Ajustada Con Pliegues Negro L Lisa Negro                                      nan regular_payment         refunded      1      39990.00
    refund                          Blazer Manga 3/4 Ajustada Con Pliegues Negro M Lisa                                      nan regular_payment         refunded      3     129970.00
    refund                    Blazer Manga 3/4 Ajustada Con Pliegues Negro Negro L Lisa                                      nan regular_payment         refunded      2      69980.00
    refund                    Blazer Manga 3/4 Ajustada Con Pliegues Negro Negro M Lisa                                      nan regular_payment         refunded      2      79980.00
    refund                   Blazer Manga 3/4 Ajustada Con Pliegues Negro Negro Xl Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                        Blazer Manga 3/4 Ajustada Con Pliegues Negro Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                         Blazer Manga 3/4 Ajustada Con Pliegues Negro Xl Lisa                                      nan regular_payment         refunded      2      84980.00
    refund                        Blazer Manga 3/4 Ajustada Con Pliegues Negro Xxl Lisa                                      nan regular_payment         refunded      2      79980.00
    refund                  Blazer Manga 3/4 Ajustada Con Pliegues Negro Xxl Lisa Negro                                      nan regular_payment         refunded      1      39990.00
    refund                       Blazer Manga 3/4 Ajustada Con Pliegues Rosado Nicopoly                                      nan regular_payment         refunded      7     319930.00
    refund                                Blazer Manga Detalle Drapeado Blanco Nicopoly                                      nan regular_payment         refunded      4     124560.00
    refund                               Blazer Manga Detalle Drapeado Celeste Nicopoly                                      nan regular_payment         refunded      7     180530.00
    refund                                 Blazer Manga Detalle Drapeado Negro Nicopoly                                      nan regular_payment         refunded      2      64580.00
    refund                              Blazer Manga Drapeada Gris Nicopoly Gris S Lisa                                      nan regular_payment         refunded      1      49990.00
    refund                            Blazer Manga Drapeada Gris Nicopoly Gris Xxl Lisa                                      nan regular_payment         refunded      1      39990.00
    refund                                  Blazer Manga Drapeada Gris Nicopoly Xl Lisa                                      nan regular_payment         refunded      1      34990.00
    refund                                    Blazer Mangas 3/4 Solapa Púrpura Nicopoly                                      nan regular_payment         refunded     18     554420.00
    refund                                    Blazer Mangas Drapeadas 3/4 Gris Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                        Blazer Oversize Tipo Gamuza Café Nicopoly Café L Liso                                      nan regular_payment         refunded      5     125798.00
    refund                        Blazer Oversize Tipo Gamuza Café Nicopoly Café S Liso                                      nan regular_payment         refunded      2     111980.00
    refund                                        Blazer Patrón Espiga Grafito Nicopoly                                      nan regular_payment         refunded      5     193960.00
    refund                                     Blazer Patrón Espiga Gris Claro Nicopoly                                      nan regular_payment         refunded     18     710030.00
    refund                                           Blazer Pied De Poule Café Nicopoly                                      nan regular_payment         refunded     33    1176031.00
    refund                                              Blazer Pinceladas Azul Nicopoly                                      nan regular_payment         refunded      6     221940.00
    refund                   Blazer Sastrero Dos Botones Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment         refunded      3      69990.00
    refund                                  Blazer Sin Mangas Bolsillos Blanco Nicopoly                                      nan regular_payment         refunded      1      27590.00
    refund                                 Blazer Sin Mangas Bolsillos Burdeos Nicopoly                                      nan regular_payment         refunded      2      55180.00
    refund                                 Blazer Sin Mangas Bolsillos Celeste Nicopoly                                      nan regular_payment         refunded      1      29990.00
    refund                      Blazer Sin Mangas Bolsillos Marrón Nicopoly Café L Liso                                      nan regular_payment         refunded      1      27590.00
    refund                        Blazer Sin Mangas Bolsillos Marrón Nicopoly Café Liso                                      nan regular_payment         refunded      2      55180.00
    refund                      Blazer Sin Mangas Bolsillos Marrón Nicopoly Café S Liso                                      nan regular_payment         refunded      2      64580.00
    refund                                   Blazer Sin Mangas Bolsillos Negro Nicopoly                                      nan regular_payment         refunded      7     267504.00
    refund                      Blazer Sin Mangas Bolsillos Rosa Nicopoly Rosado L Liso                                      nan regular_payment         refunded      1      45990.00
    refund                      Blazer Sin Mangas Bolsillos Rosa Nicopoly Rosado M Liso                                      nan regular_payment         refunded      2      43520.00
    refund                     Blazer Sin Mangas Bolsillos Rosa Nicopoly Rosado Xl Liso                                      nan regular_payment         refunded      2      55180.00
    refund                                     Blazer Sin Mangas Botón Burdeos Nicopoly                                      nan regular_payment         refunded      4     116960.00
    refund                                      Blazer Sin Mangas Botón Lúcuma Nicopoly                                      nan regular_payment         refunded      3      82970.00
    refund                                      Blazer Solapa Manga 3/4 Rosado Nicopoly                                      nan regular_payment         refunded      4     105560.00
    refund                                          Blazer Un Botón Azul Acero Nicopoly                                      nan regular_payment         refunded     12     444880.00
    refund                                               Blazer Un Botón Khaki Nicopoly                                      nan regular_payment         refunded     10     354900.00
    refund                                               Blazer Un Botón Negro Nicopoly                                      nan regular_payment         refunded     12     459880.00
    refund                                                Blazer Un Botón Rojo Nicopoly                                      nan regular_payment         refunded     10     374900.00
    refund                                          Blusa Bolsillos Cargo Café Nicopoly                                      nan regular_payment         refunded      2      57980.00
    refund                                         Blusa Bolsillos Cargo Khaki Nicopoly                                      nan regular_payment         refunded      1      27990.00
    refund                                Blusa Bolsillos Tipo Satín Palo Rosa Nicopoly                                      nan regular_payment         refunded      1      10490.00
    refund                                     Blusa Botonera Invisible Blanco Nicopoly                                      nan regular_payment         refunded      5      91794.00
    refund                               Blusa Botonera Invisible Básica Khaki Nicopoly                                      nan regular_payment         refunded      1      19490.00
    refund                                    Blusa Botonera Invisible Celeste Nicopoly                                      nan regular_payment         refunded     12     250680.00
    refund                                    Blusa Botonera Invisible Durazno Nicopoly                                      nan regular_payment         refunded      2      50133.00
    refund                                 Blusa Broderie Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      16990.00
    refund                                 Blusa Broderie Blanco Nicopoly Blanco Liso M                                      nan regular_payment         refunded      1      16990.00
    refund                                 Blusa Broderie Blanco Nicopoly Blanco Liso S                                      nan regular_payment         refunded      1      21224.00
    refund                                     Blusa Básica Escote En V Blanco Nicopoly                                      nan regular_payment         refunded      5      93950.00
    refund                                    Blusa Básica Escote En V Celeste Nicopoly                                      nan regular_payment         refunded      1      14990.00
    refund                                      Blusa Básica Escote En V Negro Nicopoly                                      nan regular_payment         refunded      2      29980.00
    refund                      Blusa Básica Escote En V Rosado Nicopoly Rosado Liso Xl                                      nan regular_payment         refunded      2      36980.00
    refund                      Blusa Básica Escote En V Rosado Nicopoly Xl Liso Rosado                                      nan regular_payment         refunded      1      17990.00
    refund                                                   Blusa Cebra Beige Nicopoly                                      nan regular_payment         refunded      3      81370.00
    refund                                  Blusa Con Lazo Desmontable Celeste Nicopoly                                      nan regular_payment         refunded      2      49980.00
    refund                                    Blusa Con Lazo Desmontable Negro Nicopoly                                      nan regular_payment         refunded      8     189924.00
    refund                                     Blusa Con Lazo Desmontable Rojo Nicopoly                                      nan regular_payment         refunded      6     148542.00
    refund                          Blusa Corbatín Y Vuelos Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      21990.00
    refund                          Blusa Corbatín Y Vuelos Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      27990.00
    refund          Blusa Corbatín Y Vuelos Verde Azulado Nicopoly Verde Azulado Liso S                                      nan regular_payment         refunded      2      52980.00
    refund                                     Blusa Cuello Mao Botones Blanco Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                    Blusa Cuello Mao Botones Celeste Nicopoly                                      nan regular_payment         refunded      6     108340.00
    refund                                      Blusa Cuello Mao Botones Negro Nicopoly                                      nan regular_payment         refunded      4      74560.00
    refund                                       Blusa Cuello Mao Floral Negro Nicopoly                                      nan regular_payment         refunded      4      71960.00
    refund                   Blusa Cuello Mao Manga Globo Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      29990.00
    refund                                    Blusa Cuello Mao Tipo Satín Gris Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                    Blusa Cuello Mao Tipo Satín Rojo Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                            Blusa Cuello Mao Tipo Satín Verde Oscuro Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                      Blusa Cuello Tipo Corbata Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      18990.00
    refund                    Blusa Cuello Tipo Corbata Celeste Nicopoly L Liso Celeste                                      nan regular_payment         refunded      1      23090.00
    refund                        Blusa Cuello Tipo Corbata Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      23090.00
    refund                       Blusa Cuello Tipo Corbata Negro Nicopoly Negro Liso Xl                                      nan regular_payment         refunded      1      25990.00
    refund                                     Blusa Cuello V Tipo Gasa Blanco Nicopoly                                      nan regular_payment         refunded      4      69960.00
    refund                                    Blusa Cuello V Tipo Gasa Celeste Nicopoly                                      nan regular_payment         refunded      5      89950.00
    refund                                       Blusa Drapeada Manga Larga Azul Lisa L                                      nan regular_payment         refunded      1      27990.00
    refund                                       Blusa Drapeada Manga Larga Azul Lisa M                                      nan regular_payment         refunded      1      27990.00
    refund                        Blusa Drapeada Manga Larga Blanco - Blanco - Liso - S                                      nan regular_payment         refunded      1      21990.00
    refund                                      Blusa Drapeada Manga Larga Negro Lisa L                                      nan regular_payment         refunded      1      27990.00
    refund                                      Blusa Drapeada Manga Larga Negro Lisa S                                      nan regular_payment         refunded      1      27990.00
    refund                                Blusa Drapeada Manga Larga Negro Negro Lisa L                                      nan regular_payment         refunded      1      28990.00
    refund                                Blusa Drapeada Manga Larga Negro Negro Lisa M                                      nan regular_payment         refunded      1      22990.00
    refund                                Blusa Drapeada Manga Larga Negro Negro Lisa S                                      nan regular_payment         refunded      2      48980.00
    refund                              Blusa Efecto Cruzado Tipo Satín Blanco Nicopoly                                      nan regular_payment         refunded      1      12490.00
    refund                               Blusa Efecto Cruzado Tipo Satín Negro Nicopoly                                      nan regular_payment         refunded      3      41970.00
    refund         Blusa Encaje Detalle Lentejuelas Blanco Nicopoly - Blanco - Liso - M                                      nan regular_payment         refunded      1      23990.00
    refund                                         Blusa Encaje Hombros Blanco Nicopoly                                      nan regular_payment         refunded     10     184190.00
    refund                                         Blusa Encaje Hombros Fucsia Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                          Blusa Encaje Hombros Negro Nicopoly                                      nan regular_payment         refunded      9     158110.00
    refund                                    Blusa Escote V Sin Mangas Blanco Nicopoly                                      nan regular_payment         refunded      2      32780.00
    refund                                   Blusa Escote V Sin Mangas Celeste Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                     Blusa Escote V Sin Mangas Negro Nicopoly                                      nan regular_payment         refunded      1      16790.00
    refund                                      Blusa Escote V Sin Mangas Rojo Nicopoly                                      nan regular_payment         refunded      3      53364.00
    refund                                                 Blusa Leopard Negro Nicopoly                                      nan regular_payment         refunded      1      19980.00
    refund                                                 Blusa Leopardo Café Nicopoly                                      nan regular_payment         refunded      1      26990.00
    refund                     Blusa Manga Larga Con Corbatín Café Nicopoly Café Liso L                                      nan regular_payment         refunded      1      29990.00
    refund                                           Blusa Mangas Vuelos Negro Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                      Blusa Nudo Delantero Encaje Negro Nicopoly Negro Lisa L                                      nan regular_payment         refunded      4      65960.00
    refund                      Blusa Nudo Delantero Encaje Negro Nicopoly Negro Lisa M                                      nan regular_payment         refunded      1      15990.00
    refund                                      Blusa Print Abstracto Azul Rey Nicopoly                                      nan regular_payment         refunded      4      83960.00
    refund                               Blusa Print Serpiente Morado Nicopoly Liso M/l                                      nan regular_payment         refunded      1      22180.00
    refund                        Blusa Print Serpiente Morado Nicopoly Morado Liso M/l                                      nan regular_payment         refunded      1      23990.00
    refund                        Blusa Print Serpiente Morado Nicopoly Morado Liso S/m                                      nan regular_payment         refunded      1      14390.00
    refund                                  Blusa Puntos Blancos Nicopoly Blanco Liso M                                      nan regular_payment         refunded      1      17990.00
    refund                              Blusa Puntos Negros Nicopoly - Negro - Liso - L                                      nan regular_payment         refunded      1      17990.00
    refund                                Blusa Rayada Lazo Desmontable Blanco Nicopoly                                      nan regular_payment         refunded      1      29990.00
    refund                   Blusa Rayas Lazo Desmontable Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      29990.00
    refund                     Blusa Rayas Lazo Desmontable Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      29990.00
    refund                                               Blusa Sin Mangas Lila Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund        Blusa Sin Mangas Negra Con Flores Blancas Nicopoly - Negro - Lisa - L                                      nan regular_payment         refunded      1      16990.00
    refund              Blusa Sin Mangas Negra Con Flores Blancas Nicopoly Negro Lisa L                                      nan regular_payment         refunded      1      16990.00
    refund              Blusa Sin Mangas Negra Con Flores Blancas Nicopoly Negro Lisa M                                      nan regular_payment         refunded      1      10190.00
    refund                                              Blusa Tipo Gasa Rosado Nicopoly                                      nan regular_payment         refunded      3      54970.00
    refund                     Blusa Transparencia Nudo Cebra Café Nicopoly Café Liso M                                      nan regular_payment         refunded      2      28980.00
    refund             Blusa Transparente Manga Globo Negro Nicopoly - Negro - Liso - L                                      nan regular_payment         refunded      1      19990.00
    refund                                         Blusa Vuelos Hombros Fucsia Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                       Blusa Vuelos Manga Larga Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      2      57980.00
    refund                       Blusa Vuelos Manga Larga Blanco Nicopoly Blanco Liso M                                      nan regular_payment         refunded      1      28990.00
    refund                       Blusa Vuelos Manga Larga Burdeo Nicopoly Burdeo Lisa L                                      nan regular_payment         refunded      2      47180.00
    refund                       Blusa Vuelos Manga Larga Burdeo Nicopoly Burdeo Lisa M                                      nan regular_payment         refunded      1      28990.00
    refund                           Blusa Vuelos Manga Larga Café Nicopoly Café Lisa L                                      nan regular_payment         refunded      2      57980.00
    refund                           Blusa Vuelos Manga Larga Café Nicopoly Café Lisa M                                      nan regular_payment         refunded      1      28990.00
    refund                           Blusa Vuelos Manga Larga Café Nicopoly Café Lisa S                                      nan regular_payment         refunded      1      28990.00
    refund                                 Body Acanalado Manga Larga Amarillo Nicopoly                                      nan regular_payment         approved      1       9990.00
    refund                                 Body Acanalado Manga Larga Amarillo Nicopoly                                      nan regular_payment         refunded      2      21980.00
    refund                                     Body Acanalado Manga Larga Rojo Nicopoly                                      nan regular_payment         refunded      1      10990.00
    refund                                           Body Escote Encaje Blanco Nicopoly                                      nan regular_payment         refunded      3      44970.00
    refund                                             Body Escote Encaje Rojo Nicopoly                                      nan regular_payment         refunded      5      72950.00
    refund                                        Body Escote V Acanalado Café Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                                     Body Escote V Acanalado Mostaza Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                           Body Escote Volantes Blanco Nicopoly Blanco Liso S                                      nan regular_payment         refunded      1      14990.00
    refund                                    Body Escote Volantes Café Nicopoly Liso L                                      nan regular_payment         refunded      1      21990.00
    refund                             Body Escote Volantes Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      14990.00
    refund                             Body Escote Volantes Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      1      14990.00
    refund                                       Body Halter Tipo Satín Blanco Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                                        Body Halter Tipo Satín Negro Nicopoly                                      nan regular_payment         refunded      1      14990.00
    refund                                  Body Texturizado Acanalado Celeste Nicopoly                                      nan regular_payment         refunded      1       9990.00
    refund                                     Body Texturizado Acanalado Gris Nicopoly                                      nan regular_payment         refunded      1       9990.00
    refund                                   Body Texturizado Acanalado Rosado Nicopoly                                      nan regular_payment         refunded      2      20980.00
    refund                                                Bomber Ecocuero Moca Nicopoly                                      nan regular_payment         refunded      2      65980.00
    refund                                               Bomber Ecocuero Negro Nicopoly                                      nan regular_payment         refunded     11     374650.00
    refund                         Bomber Tipo Gamuza Blanco Invierno Invierno Nicopoly                                      nan regular_payment         refunded     13     372380.00
    refund                                            Bomber Tipo Gamuza Camel Nicopoly                                      nan regular_payment         refunded     11     280826.00
    refund                                            Bomber Tipo Gamuza Oliva Nicopoly                                      nan regular_payment         refunded      9     292212.00
    refund                                           Bomber Tipo Lanilla Negro Nicopoly                                      nan regular_payment         refunded     27     799752.00
    refund                                    Bufanda Cuadrillé Grande Celeste Nicopoly                                      nan regular_payment         refunded      2      25470.00
    refund                                       Bufanda Cuadrillé Grande Moca Nicopoly                                      nan regular_payment         refunded      1       9990.00
    refund                    Bufanda Cuadrillé Grande Moca Nicopoly Color Café Talla U                                      nan regular_payment         refunded      1      13684.00
    refund                                      Bufanda Cuadrillé Pequeña Moca Nicopoly                                      nan regular_payment         refunded      1       9590.00
    refund                                   Bufanda Gruesa Azul Acero Nicopoly Talla U                                      nan regular_payment         refunded      1       5990.00
    refund                                              Bufanda Gruesa Grafito Nicopoly                                      nan regular_payment         refunded      1       7990.00
    refund                                                 Bufanda Gruesa Moca Nicopoly                                      nan regular_payment         refunded      4      41254.00
    refund                                                Bufanda Gruesa Negro Nicopoly                                      nan regular_payment         refunded      1       7490.00
    refund                                               Bufanda Gruesa Rosado Nicopoly                                      nan regular_payment         refunded      1       7990.00
    refund                                                Bufanda Suave Fucsia Nicopoly                                      nan regular_payment         refunded      1       5390.00
    refund                                               Bufanda Suave Grafito Nicopoly                                      nan regular_payment         refunded      1       6990.00
    refund                                          Bufanda Suave Gris Nicopoly Talla U                                      nan regular_payment         refunded      1       5990.00
    refund                                                  Bufanda Suave Moca Nicopoly                                      nan regular_payment         refunded      1       6740.00
    refund                                           Bufanda Suave Moca Nicopoly Café U                                      nan regular_payment         refunded      1       5990.00
    refund                                                 Bufanda Suave Negro Nicopoly                                      nan regular_payment         refunded      4      36400.00
    refund                                          Bufanda Suave Rosado Claro Nicopoly                                      nan regular_payment         refunded      1       6990.00
    refund                                   Calza Cierres Decorativos Grafito Nicopoly                                      nan regular_payment         refunded      1      26240.00
    refund                                     Calza Cierres Decorativos Negro Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                   Calza Cuadrillé Pie De Poule Café Nicopoly                                      nan regular_payment         refunded      3      68970.00
    refund                       Calza Elasticada Skinny Tipo Encerada Burdeos Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                          Calza Elasticada Skinny Tipo Encerada Café Nicopoly                                      nan regular_payment         refunded      2      51980.00
    refund                         Calza Elasticada Skinny Tipo Encerada Negro Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                                                 Calza Leopardo Café Nicopoly                                      nan regular_payment         refunded     12     249880.00
    refund                                       Calza Lisa Con Cierre Burdeos Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                                          Calza Lisa Con Cierre Café Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                                    Calza Skinny Tipo Encerada Negro Nicopoly                                      nan regular_payment         refunded     15     339850.00
    refund                            Calza Skinny Vichy Con Cierre Azul/negro Nicopoly                                      nan regular_payment         refunded      2      35580.00
    refund                          Calza Skinny Vichy Con Cierre Blanco/negro Nicopoly                                      nan regular_payment         refunded     14     317112.00
    refund                                  Calza Skinny Vichy Con Cierre Rojo Nicopoly                                      nan regular_payment         refunded      2      32980.00
    refund                                            Calza Tipo Gamuza Burdeo Nicopoly                                      nan regular_payment         refunded      4      71960.00
    refund                                             Calza Tipo Gamuza Camel Nicopoly                                      nan regular_payment         refunded      9     188910.00
    refund                                             Calza Tipo Gamuza Negro Nicopoly                                      nan regular_payment         refunded     11     235500.00
    refund                                Calza Vichy Con Cierre Burdeos/negro Nicopoly                                      nan regular_payment         refunded      4      79960.00
    refund                        Camisa Botonera Espalda Blanco Nicopoly Blanco Lisa M                                      nan regular_payment         refunded      1      17990.00
    refund                          Camisa Botonera Espalda Khaki Nicopoly Khaki Lisa L                                      nan regular_payment         refunded      2      41980.00
    refund                          Camisa Botonera Espalda Khaki Nicopoly Khaki Lisa M                                      nan regular_payment         refunded      2      35980.00
    refund                          Camisa Botonera Espalda Khaki Nicopoly Khaki Lisa S                                      nan regular_payment         refunded      1      17990.00
    refund                                        Camisa Básica Algodón Blanco Nicopoly                                      nan regular_payment         refunded      2      24990.00
    refund                                         Camisa Básica Algodón Negro Nicopoly                                      nan regular_payment         refunded      1      22990.00
    refund                                                 Camisa Básica Negro Nicopoly                                      nan regular_payment         refunded      3      62970.00
    refund                                                  Camisa Básica Rojo Nicopoly                                      nan regular_payment         refunded      3      63358.00
    refund                          Camisa Básica Tipo Lino Beige Nicopoly Óxido Lisa M                                      nan regular_payment         refunded      1      18990.00
    refund                  Camisa Básica Tipo Lino Blanco Nicopoly - Blanco - Lisa - M                                      nan regular_payment         refunded      1      21990.00
    refund                               Camisa Básica Tipo Lino Blanco Nicopoly Lisa S                                      nan regular_payment         refunded      1      53980.00
    refund                      Camisa Básica Tipo Lino Celeste Nicopoly Celeste Lisa L                                      nan regular_payment         refunded      1      16190.00
    refund                              Camisa Básica Tipo Lino Celeste Nicopoly Lisa M                                      nan regular_payment         refunded      1      18890.00
    refund                          Camisa Básica Tipo Lino Verde Oliva Nicopoly Lisa M                                      nan regular_payment         refunded      1      26990.00
    refund                    Camisa Básica Tipo Lino Verde Oliva Nicopoly Oliva Lisa L                                      nan regular_payment         refunded      2      31980.00
    refund                                      Camisa Básica Tipo Satín Negro Nicopoly                                      nan regular_payment         refunded      2      47980.00
    refund                                       Camisa Básica Tipo Satín Rojo Nicopoly                                      nan regular_payment         refunded      1      27990.00
    refund                                     Camisa Básica Tipo Satín Rosado Nicopoly                                      nan regular_payment         refunded      1      27990.00
    refund                                        Camisa Manga Ajustable Negro Nicopoly                                      nan regular_payment         refunded      1      24740.00
    refund                                       Camisa Pliegues Cintura Negro Nicopoly                                      nan regular_payment         refunded      4      91960.00
    refund                                        Camisa Pliegues Cintura Rojo Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                      Camisa Rayas Café Nicopoly Café Liso Xl                                      nan regular_payment         refunded      1      27190.00
    refund                                                Camisa Rayas Celeste Nicopoly                                      nan regular_payment         refunded      8     203320.00
    refund                                                  Camisa Rayas Negro Nicopoly                                      nan regular_payment         refunded      5     116950.00
    refund                   Camisa Satinada Transparente Blanco Nicopoly Blanco Liso M                                      nan regular_payment         refunded      3      54970.00
    refund                            Camisa Satinada Transparente Gris Nicopoly Gris L                                      nan regular_payment         refunded      1      13990.00
    refund                            Camisa Satinada Transparente Gris Nicopoly M Gris                                      nan regular_payment         refunded      1      18990.00
    refund          Camisa Sin Mangas Tipo Lino Azul Marino Nicopoly Azul Marino Liso L                                      nan regular_payment         refunded      1      14990.00
    refund                                      Chaleco Cuello V Oversize Rosa Nicopoly                                      nan regular_payment         refunded      2      24920.00
    refund                                          Chaleco Pied De Poule Café Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                               Chaqueta Barn Jacket Café Nicopoly Café L Liso                                      nan regular_payment         refunded      1      51990.00
    refund                             Chaqueta Barn Jacket Oliva Nicopoly Oliva S Liso                                      nan regular_payment         refunded      1      51990.00
    refund                                                 Chaqueta Biker Café Nicopoly                                      nan regular_payment         refunded      7     271430.00
    refund                                  Chaqueta Biker Ecocuero Corta Café Nicopoly                                      nan regular_payment         refunded      2      59980.00
    refund                                  Chaqueta Biker Ecocuero Corta Gris Nicopoly                                      nan regular_payment         refunded      4     122760.00
    refund                                Chaqueta Biker Ecocuero Corta Negro  Nicopoly                                      nan regular_payment         refunded     12     523860.00
    refund                                        Chaqueta Biker Ecocuero Gris Nicopoly                                      nan regular_payment         refunded      2      82980.00
    refund                                                Chaqueta Biker Negro Nicopoly                                      nan regular_payment         refunded     25     987380.00
    refund                             Chaqueta Bomber Broches Blanco Invierno Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                                       Chaqueta Bomber Broches Camel Nicopoly                                      nan regular_payment         refunded      4     103960.00
    refund                            Chaqueta Bouclé Blanco Invierno Invierno Nicopoly                                      nan regular_payment         refunded      8     267670.00
    refund                                                Chaqueta Bouclé Gris Nicopoly                                      nan regular_payment         refunded     18     638520.00
    refund                                                Chaqueta Bouclé Moca Nicopoly                                      nan regular_payment         refunded      7     227130.00
    refund                                               Chaqueta Bouclé Negro Nicopoly                                      nan regular_payment         refunded      9     265806.00
    refund                                    Chaqueta Corta Impermeable Khaki Nicopoly                                      nan regular_payment         refunded      6     159035.00
    refund                                    Chaqueta Corta Impermeable Negro Nicopoly                                      nan regular_payment         approved      1      45990.00
    refund                                    Chaqueta Corta Impermeable Negro Nicopoly                                      nan regular_payment         refunded     22     855280.00
    refund                                    Chaqueta Corta Impermeable Oliva Nicopoly                                      nan regular_payment         refunded     13     481612.00
    refund                          Chaqueta Corta Tipo Gamuza Blanco Invierno Nicopoly                                      nan regular_payment         refunded      5     146952.00
    refund                         Chaqueta Corta Tipo Gamuza Café Nicopoly Café L Liso                                      nan regular_payment         refunded      1      51990.00
    refund                                    Chaqueta Corta Tipo Gamuza Camel Nicopoly                                      nan regular_payment         refunded     18     573824.00
    refund                                    Chaqueta Corta Tipo Gamuza Oliva Nicopoly                                      nan regular_payment         refunded     10     277789.00
    refund                              Chaqueta Cuello Camisero Ecocuero Café Nicopoly                                      nan regular_payment         refunded      3     103970.00
    refund                             Chaqueta Cuello Camisero Ecocuero Negro Nicopoly                                      nan regular_payment         refunded     11     370890.00
    refund                             Chaqueta Cuello Camisero Ecocuero Oliva Nicopoly                                      nan regular_payment         refunded      1      34990.00
    refund                                            Chaqueta Cuello Mao Café Nicopoly                                      nan regular_payment         refunded     10     344400.00
    refund                                  Chaqueta Cuello Mao Ecocuero Khaki Nicopoly                                      nan regular_payment         refunded      2      55980.00
    refund                                   Chaqueta Cuello Mao Ecocuero Lila Nicopoly                                      nan regular_payment         refunded      1      34990.00
    refund                            Chaqueta Cuello Mao Ecocuero Rosa Chicle Nicopoly                                      nan regular_payment         refunded      1      27990.00
    refund                                           Chaqueta Cuello Mao Negro Nicopoly                                      nan regular_payment         refunded     10     393402.00
    refund           Chaqueta Ecocuero Acolchado Cuello Mao Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      34790.00
    refund                                        Chaqueta Ecocuero Lazo Camel Nicopoly                                      nan regular_payment         refunded     14     408708.00
    refund                                        Chaqueta Ecocuero Lazo Negro Nicopoly                                      nan regular_payment         refunded     12     569682.00
    refund                                   Chaqueta Ecocuero Tipo Biker Café Nicopoly                                      nan regular_payment         refunded     10     373058.00
    refund                                  Chaqueta Ecocuero Tipo Biker Negro Nicopoly                                      nan regular_payment         refunded      1      41990.00
    refund                                    Chaqueta Ecocuero/tipo Piel Café Nicopoly                                      nan regular_payment         refunded     13     480160.00
    refund                           Chaqueta Larga Impermeable Mostaza Oscuro Nicopoly                                      nan regular_payment         refunded     54    2204572.00
    refund                                    Chaqueta Larga Impermeable Negro Nicopoly                                      nan regular_payment         refunded     24    1101760.00
    refund                              Chaqueta Larga Impermeable Oliva Claro Nicopoly                                      nan regular_payment         refunded     25    1003442.00
    refund                                             Chaqueta Leñadora Beige Nicopoly                                      nan regular_payment         refunded      7     211970.00
    refund                                             Chaqueta Leñadora Camel Nicopoly                                      nan regular_payment         refunded      1      30990.00
    refund                                          Chaqueta Mao Ecocuero Café Nicopoly                                      nan regular_payment         refunded      3      67980.00
    refund                                         Chaqueta Mao Ecocuero Negro Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                       Chaqueta Mitad Chiporro/parka Blanco Invierno Nicopoly                                      nan regular_payment         refunded      7     175930.00
    refund                                 Chaqueta Mitad Chiporro/parka Khaki Nicopoly                                      nan regular_payment         refunded     26     548614.00
    refund                                 Chaqueta Mitad Chiporro/parka Negro Nicopoly                                      nan regular_payment         refunded     12     362880.00
    refund                                  Chaqueta Mitad Chiporro/parka Rojo Nicopoly                                      nan regular_payment         refunded      6     142450.00
    refund                              Chaqueta Puffer Cotelé Blanco Invierno Nicopoly                                      nan regular_payment         refunded      9     242310.00
    refund                                        Chaqueta Puffer Cotelé Camel Nicopoly                                      nan regular_payment         refunded      9     251490.00
    refund                                 Chaqueta Quilt Tipo Camisera Fucsia Nicopoly                                      nan regular_payment         refunded     10     209900.00
    refund                                 Chaqueta Quilt Tipo Camisera Marrón Nicopoly                                      nan regular_payment         refunded      5     129950.00
    refund                                  Chaqueta Quilt Tipo Camisera Negro Nicopoly                                      nan regular_payment         refunded     15     297360.00
    refund                                  Chaqueta Quilt Tipo Camisera Oliva Nicopoly                                      nan regular_payment         refunded      3      61161.00
    refund                                            Chaqueta Reversible Moca Nicopoly                                      nan regular_payment         refunded      4     158760.00
    refund                                           Chaqueta Reversible Negro Nicopoly                                      nan regular_payment         refunded     25     918812.00
    refund                                           Chaqueta Reversible Oliva Nicopoly                                      nan regular_payment         refunded      5     197702.00
    refund                              Chaqueta Tipo Barbour Café Nicopoly Café L Liso                                      nan regular_payment         refunded      1      55990.00
    refund                            Chaqueta Tipo Barbour Mocca Nicopoly Mocca L Liso                                      nan regular_payment         refunded      5     321950.00
    refund                                  Chaqueta Tipo Biker Ecocuero Khaki Nicopoly                                      nan regular_payment         refunded      2      87980.00
    refund                                                   Crop Encaje Negro Nicopoly                                      nan regular_payment         refunded      3      45960.00
    refund                                 Crop Top Espalda Elasticada Magenta Nicopoly                                      nan regular_payment         refunded      5      81950.00
    refund                  Crop Top Espalda Elasticada Mostaza Nicopoly Mostaza M Liso                                      nan regular_payment         refunded      1      14990.00
    refund                 Crop Top Espalda Elasticada Mostaza Nicopoly Mostaza Xl Liso                                      nan regular_payment         refunded      1      13990.00
    refund                                   Crop Top Espalda Elasticada Negro Nicopoly                                      nan regular_payment         refunded      5      76950.00
    refund                                   Crop Top Espalda Elasticada Verde Nicopoly                                      nan regular_payment         refunded      1      13990.00
    refund                                           Crop Top Jaspeado Celeste Nicopoly                                      nan regular_payment         refunded      2      19980.00
    refund                                            Crop Top Jaspeado Rosado Nicopoly                                      nan regular_payment         refunded      2      31980.00
    refund                                               Cuello Tipo Piel Gris Nicopoly                                      nan regular_payment         refunded      2      10980.00
    refund                                    Cárdigan Botones Acanalado Negro Nicopoly                                      nan regular_payment         refunded      1      16990.00
    refund                               Cárdigan Básico Azul  Nicopoly Azul Tejido M/l                                      nan regular_payment         refunded      1      21990.00
    refund                               Cárdigan Básico Azul  Nicopoly Azul Tejido S/m                                      nan regular_payment         refunded      1      15990.00
    refund                                    Cárdigan Básico Azul  Nicopoly Tejido S/m                                      nan regular_payment         refunded      1      17990.00
    refund                                       Cárdigan Básico Botones Negro Nicopoly                                      nan regular_payment         refunded      6     133840.00
    refund                           Cárdigan Básico Morado  Nicopoly Morado Tejido M/l                                      nan regular_payment         refunded      1      21990.00
    refund                           Cárdigan Básico Morado  Nicopoly Morado Tejido S/m                                      nan regular_payment         refunded      2      47970.00
    refund                                      Cárdigan Corto Botones Mostaza Nicopoly                                      nan regular_payment         refunded      1      16990.00
    refund                                          Cárdigan Crop Flores Negro Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                Cárdigan Crop Perlas Blanco Invierno Nicopoly                                      nan regular_payment         refunded      4      47982.00
    refund                                          Cárdigan Crop Perlas Negro Nicopoly                                      nan regular_payment         refunded      2      46480.00
    refund                                           Cárdigan Crop Perlas Rojo Nicopoly                                      nan regular_payment         refunded      4      97460.00
    refund                Cárdigan Cuello V Con 3 Botones Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment         refunded      1      22490.00
    refund                                             Cárdigan Floreado Negro Nicopoly                                      nan regular_payment         refunded      3      65970.00
    refund                                            Cárdigan Flores 3d Negro Nicopoly                                      nan regular_payment         refunded      1      24990.00
    refund                       Cárdigan Manga Globo Ladrillo Nicopoly Ladrillo Liso S                                      nan regular_payment         refunded      1      34390.00
    refund                                  Cárdigan Multicolor Flores 3d Café Nicopoly                                      nan regular_payment         refunded      1      27990.00
    refund                                        Cárdigan Punto Fantasía Gris Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                     Cárdigan Punto Fantasía Magenta Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                  Cárdigan Punto Fino Cadenetas Café Nicopoly                                      nan regular_payment         refunded      2      31980.00
    refund                                  Cárdigan Punto Fino Cadenetas Gris Nicopoly                                      nan regular_payment         refunded      3      35574.00
    refund                                 Cárdigan Punto Fino Cadenetas Negro Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                               Cárdigan Rayado Negro Nicopoly                                      nan regular_payment         refunded      3      44380.00
    refund                                                 Cárdigan Rayas Rojo Nicopoly                                      nan regular_payment         refunded      1      20180.00
    refund              Cárdigan Tipo Crochet Botones Dorados Café Nicopoly Café Liso L                                      nan regular_payment         refunded      1      22990.00
    refund              Cárdigan Tipo Crochet Botones Dorados Café Nicopoly Café Liso M                                      nan regular_payment         refunded      1      31990.00
    refund        Cárdigan Tipo Crochet Botones Dorados Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      1      22990.00
    refund                   Cárdigan Tipo Crochet Hilo Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      1      17990.00
    refund                   Cárdigan Tipo Crochet Hilo Celeste Nicopoly Celeste Liso S                                      nan regular_payment         refunded      1      31990.00
    refund                       Cárdigan Tipo Crochet Hilo Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      21990.00
    refund                     Cárdigan Tipo Crochet Hilo Rosado Nicopoly Rosado Liso L                                      nan regular_payment         refunded      2      21990.00
    refund                                       Enterito Bustier Encaje Negro Nicopoly                                      nan regular_payment         refunded     10     279900.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly Morado Liso M                                      nan regular_payment         refunded      6     102770.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly Morado Liso S                                      nan regular_payment         refunded      3     105370.00
    refund                    Enterito Cinturón Ajustable Morado Nicopoly S Liso Morado                                      nan regular_payment         refunded      1      43990.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly M Liso Negro                                      nan regular_payment         refunded      1      43990.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      34990.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      2      70380.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      2      56380.00
    refund                      Enterito Cinturón Ajustable Negro Nicopoly S Liso Negro                                      nan regular_payment         refunded      1      43990.00
    refund         Enterito Cinturón Ajustable Verde Oscuro Nicopoly - Verde - Liso - L                                      nan regular_payment         refunded      1      43990.00
    refund         Enterito Cinturón Ajustable Verde Oscuro Nicopoly - Verde - Liso - M                                      nan regular_payment         refunded      1      43990.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly L Liso Verde                                      nan regular_payment         refunded      2      87980.00
    refund                     Enterito Cinturón Ajustable Verde Oscuro Nicopoly Liso L                                      nan regular_payment         refunded      1      43990.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly M Liso Verde                                      nan regular_payment         refunded      1      43990.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly S Liso Verde                                      nan regular_payment         refunded      3     131970.00
    refund               Enterito Cinturón Ajustable Verde Oscuro Nicopoly Verde Liso S                                      nan regular_payment         refunded      1      35190.00
    refund                                          Enterito Con Encaje Blanco Nicopoly                                      nan regular_payment         refunded      1      28990.00
    refund                                           Enterito Con Encaje Negro Nicopoly                                      nan regular_payment         refunded      3      92970.00
    refund                                    Enterito Con Solapa Y Lazo Negro Nicopoly                                      nan regular_payment         refunded      1      16990.00
    refund                                     Enterito Corto Flores Lazo Lila Nicopoly                                      nan regular_payment         refunded      6     133340.00
    refund                                  Enterito Corto Flores Lazo Naranjo Nicopoly                                      nan regular_payment         refunded      1      20990.00
    refund                                    Enterito Cruzado 2 Botones Negro Nicopoly                                      nan regular_payment         refunded      5     194950.00
    refund                                     Enterito Cruzado 2 Botones Rojo Nicopoly                                      nan regular_payment         refunded      3     109970.00
    refund                                           Enterito Cuello Mock Azul Nicopoly                                      nan regular_payment         refunded     11     449190.00
    refund                                         Enterito Cuello Mock Burdeo Nicopoly                                      nan regular_payment         refunded     11     358022.00
    refund                                  Enterito Cut Out Escote Azul Acero Nicopoly                                      nan regular_payment         refunded      9     358410.00
    refund                                       Enterito Cut Out Escote Cobre Nicopoly                                      nan regular_payment         refunded     10     373802.00
    refund                                 Enterito Cut Out Escote Rojo Oscuro Nicopoly                                      nan regular_payment         refunded      9     340910.00
    refund                            Enterito Detalles Dorados Hombros Burdeo Nicopoly                                      nan regular_payment         refunded      4      87960.00
    refund                             Enterito Detalles Dorados Hombros Negro Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund                                  Enterito Efecto Dos Piezas Celeste Nicopoly                                      nan regular_payment         refunded     13     445480.00
    refund               Enterito Efecto Dos Piezas Morado Nicopoly - Morado - Liso - L                                      nan regular_payment         refunded      1      45990.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly M Liso Morado                                      nan regular_payment         refunded      1      45990.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso L                                      nan regular_payment         refunded      6     181340.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso M                                      nan regular_payment         refunded      3      99570.00
    refund                     Enterito Efecto Dos Piezas Morado Nicopoly Morado Liso S                                      nan regular_payment         refunded      2      72780.00
    refund                                    Enterito Efecto Dos Piezas Negro Nicopoly                                      nan regular_payment         refunded     14     427443.00
    refund                                     Enterito Efecto Dos Piezas Rojo Nicopoly                                      nan regular_payment         refunded      1      22490.00
    refund                                      Enterito Escote Cruzado Blanco Nicopoly                                      nan regular_payment         refunded      5     172954.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment         refunded      3      91472.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment         refunded      4     124466.00
    refund                        Enterito Escote Cruzado Burdeo Nicopoly Burdeo Liso S                                      nan regular_payment         refunded      5     159452.00
    refund                                       Enterito Escote Cruzado Negro Nicopoly                                      nan regular_payment         refunded     10     306610.00
    refund                                      Enterito Escote V Y Lazo Negro Nicopoly                                      nan regular_payment         refunded      2      54980.00
    refund                            Enterito Halter Con Cinturón Lazo Burdeo Nicopoly                                      nan regular_payment         refunded     16     639850.00
    refund                             Enterito Halter Con Cinturón Lazo Negro Nicopoly                                      nan regular_payment         refunded      6     258140.00
    refund                    Enterito Halter Con Cinturón Lazo Verde Petróleo Nicopoly                                      nan regular_payment         refunded      7     293930.00
    refund                                 Enterito Lazo Y Hebilla Verde Oliva Nicopoly                                      nan regular_payment         refunded     16     387090.00
    refund                            Falda Asimétrica Animal Print Cafe Animal Print S                                      nan regular_payment         refunded      1      13990.00
    refund                                 Falda Denim Tajo Frontal Azul Medio Nicopoly                                      nan regular_payment         refunded      4      72680.00
    refund                                       Falda Denim Tajo Frontal Azul Nicopoly                                      nan regular_payment         refunded      2      35980.00
    refund                               Falda Larga Animal Print Marrón Animal Print L                                      nan regular_payment         refunded      1      21990.00
    refund                               Falda Larga Animal Print Marrón Animal Print M                                      nan regular_payment         refunded      5     109950.00
    refund                               Falda Larga Animal Print Marrón Animal Print S                                      nan regular_payment         refunded      6     155940.00
    refund                             Falda Midi Ecocuero Negro Nicopoly Negro Liso Xl                                      nan regular_payment         refunded      1      23990.00
    refund                    Falda Midi Negra Con Flores Blancas Nicopoly Negro Lisa M                                      nan regular_payment         refunded      1      20980.00
    refund                    Falda Midi Negra Con Flores Blancas Nicopoly Negro Lisa S                                      nan regular_payment         refunded      1      14990.00
    refund                    Falda Satín Encaje En Ruedo Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment         refunded      1      25990.00
    refund                    Falda Satín Encaje En Ruedo Burdeo Nicopoly Burdeo Liso S                                      nan regular_payment         refunded      1      20790.00
    refund                                Falda Short Tipo Gamuza Oliva Nicopoly Liso S                                      nan regular_payment         refunded      1      24990.00
    refund                          Falda Short Tipo Gamuza Oliva Nicopoly Oliva Liso M                                      nan regular_payment         refunded      1      14990.00
    refund                            Gilet 4 Botones Beige Nicopoly - Beige - Lisa - L                                      nan regular_payment         refunded      1      19990.00
    refund                                        Gilet 4 Botones Beige Nicopoly Lisa S                                      nan regular_payment         refunded      2      51980.00
    refund                          Gilet 4 Botones Blanco Nicopoly - Blanco - M - Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                                       Gilet 4 Botones Blanco Nicopoly S Lisa                                      nan regular_payment         refunded      2      45980.00
    refund                        Gilet 4 Botones Celeste Nicopoly - Celeste - L - Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                             Gilet 4 Botones Celeste Nicopoly Celeste Xl Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                                      Gilet 4 Botones Celeste Nicopoly L Lisa                                      nan regular_payment         refunded      1      25990.00
    refund                              Gilet 4 Botones Celeste Nicopoly M Lisa Celeste                                      nan regular_payment         refunded      1      19990.00
    refund                                    Gilet 4 Botones Gris Nicopoly Gris L Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                                    Gilet 4 Botones Gris Nicopoly Gris M Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                                   Gilet 4 Botones Gris Nicopoly Gris Xl Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                                    Gilet 4 Botones Gris Nicopoly L Gris Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                                 Gilet 4 Botones Lila Nicopoly Violeta Lisa M                                      nan regular_payment         refunded      4      85960.00
    refund                                Gilet 4 Botones Lila Nicopoly Violeta Lisa Xl                                      nan regular_payment         refunded      1      25990.00
    refund                                Gilet 4 Botones Morado Nicopoly Morado S Lisa                                      nan regular_payment         refunded      1      26990.00
    refund                            Gilet 4 Botones Negro Nicopoly - Negro - Lisa - L                                      nan regular_payment         refunded      4      79960.00
    refund                            Gilet 4 Botones Negro Nicopoly - Negro - Lisa - M                                      nan regular_payment         refunded      1      19990.00
    refund                            Gilet 4 Botones Negro Nicopoly - Negro - Lisa - S                                      nan regular_payment         refunded      3      59970.00
    refund                                        Gilet 4 Botones Negro Nicopoly Lisa S                                      nan regular_payment         refunded      3      46780.00
    refund                                       Gilet 4 Botones Negro Nicopoly Lisa Xl                                      nan regular_payment         refunded      2      46780.00
    refund                                  Gilet 4 Botones Negro Nicopoly Negro L Lisa                                      nan regular_payment         refunded      1      20990.00
    refund                                  Gilet 4 Botones Negro Nicopoly Negro Lisa M                                      nan regular_payment         refunded      1      10000.00
    refund                                 Gilet 4 Botones Negro Nicopoly Negro Lisa Xl                                      nan regular_payment         refunded      1      25990.00
    refund                                 Gilet 4 Botones Negro Nicopoly Negro Xl Lisa                                      nan regular_payment         refunded      1      26990.00
    refund                                 Gilet 4 Botones Negro Nicopoly Xl Lisa Negro                                      nan regular_payment         refunded      2      39980.00
    refund                                  Gilet 4 Botones Rosa Nicopoly M Lisa Rosado                                      nan regular_payment         refunded      1      19990.00
    refund                                  Gilet 4 Botones Rosa Nicopoly Rosado M Lisa                                      nan regular_payment         refunded      3      60770.00
    refund                                  Gilet 4 Botones Rosa Nicopoly Rosado S Lisa                                      nan regular_payment         refunded      2      51980.00
    refund                                 Gilet 4 Botones Rosa Nicopoly Xl Lisa Rosado                                      nan regular_payment         refunded      2      39980.00
    refund                            Gilet 4 Botones Verde Nicopoly - Verde - Lisa - M                                      nan regular_payment         refunded      2      39980.00
    refund                                       Gilet 4 Botones Verde Nicopoly Lisa Xl                                      nan regular_payment         refunded      1      25990.00
    refund                                  Gilet 4 Botones Verde Nicopoly Verde Lisa M                                      nan regular_payment         refunded      1      25990.00
    refund                                 Gilet 4 Botones Verde Nicopoly Verde Xl Lisa                                      nan regular_payment         refunded      1      26990.00
    refund                                        Gilet Básico 4 Botones Khaki Nicopoly                                      nan regular_payment         refunded      5     181930.00
    refund                                       Gilet Básico 4 Botones Morado Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                                        Gilet Básico 4 Botones Negro Nicopoly                                      nan regular_payment         refunded      5     171530.00
    refund                                  Gilet Básico 4 Botones Rojo Oscuro Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                                 Gilet Básico 4 Botones Verde Oscuro Nicopoly                                      nan regular_payment         refunded      3      77970.00
    refund                             Gilet Básico Ajustable Azul Nicopoly Azul L Liso                                      nan regular_payment         refunded      1      29990.00
    refund                   Gilet Básico Ajustable Burdeo Nicopoly - Burdeo - L - Liso                                      nan regular_payment         refunded      1      22990.00
    refund                   Gilet Básico Ajustable Burdeo Nicopoly - Burdeo - S - Liso                                      nan regular_payment         refunded      1      22990.00
    refund                         Gilet Básico Ajustable Burdeo Nicopoly Burdeo L Liso                                      nan regular_payment         refunded      1      28990.00
    refund                         Gilet Básico Ajustable Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment         refunded      1      28990.00
    refund                                Gilet Básico Ajustable Burdeo Nicopoly L Liso                                      nan regular_payment         refunded      1      23190.00
    refund                               Gilet Básico Ajustable Burdeo Nicopoly Xl Liso                                      nan regular_payment         refunded      1      23190.00
    refund                       Gilet Básico Ajustable Celeste Nicopoly Celeste M Liso                                      nan regular_payment         refunded      3      87970.00
    refund                               Gilet Básico Ajustable Celeste Nicopoly L Liso                                      nan regular_payment         refunded      1      23190.00
    refund                     Gilet Básico Ajustable Negro Nicopoly - Negro - S - Liso                                      nan regular_payment         refunded      1      22990.00
    refund                    Gilet Básico Ajustable Negro Nicopoly - Negro - Xl - Liso                                      nan regular_payment         refunded      1      22990.00
    refund                           Gilet Básico Ajustable Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      29990.00
    refund                           Gilet Básico Ajustable Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      3      69660.00
    refund                           Gilet Básico Ajustable Negro Nicopoly Negro S Liso                                      nan regular_payment         refunded      2      57980.00
    refund                          Gilet Básico Ajustable Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      4     104360.00
    refund                       Gilet Básico Ajustable Rojo Nicopoly - Rojo - M - Liso                                      nan regular_payment         refunded      1      22990.00
    refund                       Gilet Básico Ajustable Rojo Nicopoly - Rojo - S - Liso                                      nan regular_payment         refunded      1      22990.00
    refund                                  Gilet Básico Ajustable Rojo Nicopoly L Liso                                      nan regular_payment         refunded      1      23190.00
    refund                                  Gilet Básico Ajustable Rojo Nicopoly M Liso                                      nan regular_payment         refunded      1      28990.00
    refund                             Gilet Básico Ajustable Rojo Nicopoly Rojo M Liso                                      nan regular_payment         refunded      2      45980.00
    refund                                  Gilet Básico Ajustable Rojo Nicopoly S Liso                                      nan regular_payment         refunded      1      28990.00
    refund                                          Gilet Básico Blanco Nicopoly L Liso                                      nan regular_payment         refunded      1      23190.00
    refund                                          Gilet Básico Blanco Nicopoly M Liso                                      nan regular_payment         refunded      1      22990.00
    refund                                         Gilet Básico Blanco Nicopoly Xl Liso                                      nan regular_payment         refunded      1      23190.00
    refund                          Gilet Básico Celeste Nicopoly - Celeste - Xl - Lisa                                      nan regular_payment         refunded      1      22990.00
    refund                                 Gilet Básico Celeste Nicopoly M Lisa Celeste                                      nan regular_payment         refunded      2      45980.00
    refund                                 Gilet Básico Gris Nicopoly - Gris - L - Lisa                                      nan regular_payment         refunded      1      22990.00
    refund                                Gilet Básico Gris Nicopoly - Gris - Xl - Lisa                                      nan regular_payment         refunded      1      22990.00
    refund                                      Gilet Básico Gris Nicopoly Gris Xl Lisa                                      nan regular_payment         refunded      1      22990.00
    refund                                            Gilet Básico Gris Nicopoly S Lisa                                      nan regular_payment         refunded      1      28990.00
    refund                                      Gilet Básico Gris Nicopoly Xl Gris Lisa                                      nan regular_payment         refunded      1      22990.00
    refund                              Gilet Básico Hilo Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      2      53980.00
    refund                              Gilet Básico Hilo Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      1      21990.00
    refund                              Gilet Básico Hilo Blanco Nicopoly L Liso Blanco                                      nan regular_payment         refunded      1      21990.00
    refund                                     Gilet Básico Hilo Blanco Nicopoly M Liso                                      nan regular_payment         refunded      2      57580.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - L - Liso                                      nan regular_payment         refunded      6      38046.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - M - Liso                                      nan regular_payment         refunded      1      13990.00
    refund                        Gilet Básico Hilo Burdeo Nicopoly - Burdeo - S - Liso                                      nan regular_payment         refunded      2      41990.00
    refund                              Gilet Básico Hilo Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment         refunded      1      21924.00
    refund                              Gilet Básico Hilo Burdeo Nicopoly Burdeo S Liso                                      nan regular_payment         refunded      1      21990.00
    refund                                     Gilet Básico Hilo Burdeo Nicopoly M Liso                                      nan regular_payment         refunded      2      57580.00
    refund                            Gilet Básico Hilo Café Nicopoly - Cafe - L - Liso                                      nan regular_payment         refunded      1      21990.00
    refund                          Gilet Básico Hilo Negro Nicopoly - Negro - L - Liso                                      nan regular_payment         refunded      2      43980.00
    refund                                Gilet Básico Hilo Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      2      43980.00
    refund                                Gilet Básico Hilo Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      1      21990.00
    refund                                          Gilet Básico Rosado Nicopoly M Liso                                      nan regular_payment         refunded      1      20290.00
    refund                                   Gilet Básico Rosado Nicopoly Rosado S Liso                                      nan regular_payment         refunded      1      28990.00
    refund                                  Gilet Básico Rosado Nicopoly Xl Liso Rosado                                      nan regular_payment         refunded      1      22990.00
    refund                              Gilet Con Drapeado Lateral Blanco Blanco M Lisa                                      nan regular_payment         refunded      1      18890.00
    refund                              Gilet Con Drapeado Lateral Blanco Blanco S Lisa                                      nan regular_payment         refunded      3      72870.00
    refund                          Gilet Con Drapeado Lateral Negro - Negro - L - Liso                                      nan regular_payment         refunded      1      26990.00
    refund                                Gilet Con Drapeado Lateral Negro Negro L Liso                                      nan regular_payment         refunded      4      77760.00
    refund                                Gilet Con Drapeado Lateral Negro Negro S Liso                                      nan regular_payment         refunded      1      19990.00
    refund                                  Gilet Con Drapeado Lateral Rojo Rojo S Liso                                      nan regular_payment         refunded      1      19990.00
    refund                    Gilet Crop Con Solapa Blanco Nicopoly - Blanco - L - Liso                                      nan regular_payment         refunded      4      31060.00
    refund                            Gilet Crop Con Solapa Caqui Nicopoly Khaki M Liso                                      nan regular_payment         refunded      1      19790.00
    refund                            Gilet Crop Con Solapa Caqui Nicopoly Khaki S Liso                                      nan regular_payment         refunded      1      16990.00
    refund                                  Gilet Espalda Ajustable Azul Acero Nicopoly                                      nan regular_payment         refunded      1      28990.00
    refund                                       Gilet Espalda Ajustable Beige Nicopoly                                      nan regular_payment         refunded      7     289900.00
    refund                                      Gilet Espalda Ajustable Burdeo Nicopoly                                      nan regular_payment         approved      1      28990.00
    refund                                      Gilet Espalda Ajustable Burdeo Nicopoly                                      nan regular_payment         refunded      2      57980.00
    refund                                       Gilet Espalda Ajustable Negro Nicopoly                                      nan regular_payment         refunded      8     260910.00
    refund                                        Gilet Espalda Ajustable Rojo Nicopoly                                      nan regular_payment         refunded      3      86970.00
    refund               Gilet Halter Espalda Descubierta Blanco Nicopoly Blanco M Lisa                                      nan regular_payment         refunded      2      44980.00
    refund               Gilet Halter Espalda Descubierta Blanco Nicopoly Blanco S Lisa                                      nan regular_payment         refunded      2      41830.00
    refund              Gilet Halter Espalda Descubierta Blanco Nicopoly Blanco Xl Lisa                                      nan regular_payment         refunded      1      21990.00
    refund                 Gilet Halter Espalda Descubierta Negro Nicopoly Negro L Lisa                                      nan regular_payment         refunded      1      21990.00
    refund                Gilet Halter Espalda Descubierta Negro Nicopoly Negro Xl Lisa                                      nan regular_payment         refunded      2      40830.00
    refund                      Gilet Halter Espalda Descubierta Negro Nicopoly Xl Lisa                                      nan regular_payment         refunded      1      23190.00
    refund                           Gilet Largo Con Botones Blanco - Blanco - M - Liso                                      nan regular_payment         refunded      1      29990.00
    refund                                 Gilet Largo Con Botones Blanco Blanco M Liso                                      nan regular_payment         refunded      7      88298.00
    refund                                 Gilet Largo Con Botones Blanco Blanco S Liso                                      nan regular_payment         refunded      1      29990.00
    refund                                        Gilet Largo Con Botones Blanco S Liso                                      nan regular_payment         refunded      1      29990.00
    refund                                Gilet Largo Con Botones Burdeo Burdeos L Liso                                      nan regular_payment         refunded      1      20990.00
    refund                                Gilet Largo Con Botones Burdeo Burdeos M Liso                                      nan regular_payment         refunded      1      29990.00
    refund                                     Gilet Largo Con Botones Café Cafe M Liso                                      nan regular_payment         refunded      1      21990.00
    refund                                     Gilet Largo Con Botones Café Cafe S Liso                                      nan regular_payment         refunded      1      29990.00
    refund                                   Gilet Largo Con Botones Negro Negro M Liso                                      nan regular_payment         refunded      1      29990.00
    refund                          Gilet Largo Con Botones Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      1      20990.00
    refund                         Gilet Largo Con Botones Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      2      20990.00
    refund                                         Gilet Largo Con Botones Negro S Liso                                      nan regular_payment         refunded      2      47980.00
    refund                                         Gilet Lazo Ajustable Blanco Nicopoly                                      nan regular_payment         refunded      1      29990.00
    refund                             Gilet Lazo Ajustable Café Nicopoly Marrón S Lisa                                      nan regular_payment         refunded      1      28990.00
    refund                              Gilet Lazo Ajustable Café Nicopoly Mocca S Liso                                      nan regular_payment         refunded      1      29990.00
    refund                        Gilet Leopard Café Nicopoly - Cafe - Animal Print - L                                      nan regular_payment         refunded      2      39980.00
    refund                        Gilet Leopard Café Nicopoly - Cafe - Animal Print - M                                      nan regular_payment         refunded      3      59970.00
    refund                              Gilet Leopard Café Nicopoly Cafe Animal Print L                                      nan regular_payment         refunded      1      19990.00
    refund                              Gilet Leopard Café Nicopoly Cafe Animal Print M                                      nan regular_payment         refunded      2      39980.00
    refund                                             Gilet Mezcla Lino Beige Nicopoly                                      nan regular_payment         refunded      7     128430.00
    refund                                            Gilet Mezcla Lino Blanco Nicopoly                                      nan regular_payment         refunded      6     119340.00
    refund                            Gilet Mezcla Lino Celeste Nicopoly Celeste M Liso                                      nan regular_payment         refunded      2      33980.00
    refund                            Gilet Mezcla Lino Celeste Nicopoly Celeste S Liso                                      nan regular_payment         refunded      2      36980.00
    refund                         Gilet Negro Rayas Diplomáticas Nicopoly Negro S Liso                                      nan regular_payment         refunded      1      31990.00
    refund                 Gilet Rayas Diplomáticas Blanco Nicopoly - Blanco - M - Liso                                      nan regular_payment         refunded      1      26990.00
    refund                       Gilet Rayas Diplomáticas Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      1      22390.00
    refund                       Gilet Rayas Diplomáticas Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      2      47980.00
    refund                       Gilet Rayas Diplomáticas Blanco Nicopoly Blanco S Liso                                      nan regular_payment         refunded      1      23990.00
    refund                      Gilet Rayas Diplomáticas Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment         refunded      1      23990.00
    refund                     Gilet Rayas Diplomáticas Celeste Nicopoly Celeste M Liso                                      nan regular_payment         refunded      1      23990.00
    refund                     Gilet Rayas Diplomáticas Gris Nicopoly - Gris - M - Liso                                      nan regular_payment         refunded      1      31990.00
    refund                           Gilet Rayas Diplomáticas Gris Nicopoly Gris L Liso                                      nan regular_payment         refunded      2      46380.00
    refund                           Gilet Rayas Diplomáticas Gris Nicopoly Gris S Liso                                      nan regular_payment         refunded      3      68770.00
    refund                                Gilet Rayas Diplomáticas Gris Nicopoly M Liso                                      nan regular_payment         refunded      1      31990.00
    refund                   Gilet Sastre Entallado Blanco Nicopoly - Blanco - L - Liso                                      nan regular_payment         refunded      1      25990.00
    refund                   Gilet Sastre Entallado Blanco Nicopoly - Blanco - M - Liso                                      nan regular_payment         refunded      1      25990.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      5     133454.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      5     124350.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly Blanco S Liso                                      nan regular_payment         refunded      5     136950.00
    refund                         Gilet Sastre Entallado Blanco Nicopoly S Liso Blanco                                      nan regular_payment         refunded      2      51980.00
    refund                         Gilet Sastre Entallado Burdeo Nicopoly Burdeo S Liso                                      nan regular_payment         refunded      1      26390.00
    refund                                 Gilet Sastre Entallado Negro Nicopoly L Liso                                      nan regular_payment         refunded      1      26390.00
    refund                           Gilet Sastre Entallado Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      32990.00
    refund                                            Gilet Tejido Hilo Blanco Nicopoly                                      nan regular_payment         refunded      6     185540.00
    refund                                            Gilet Tejido Hilo Burdeo Nicopoly                                      nan regular_payment         refunded      2      63980.00
    refund                                             Gilet Tejido Hilo Negro Nicopoly                                      nan regular_payment         refunded      5     159950.00
    refund                      Gilet Tipo Crepé Animal Print Café Nicopoly Café L Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                     Gilet Tipo Crepé Animal Print Café Nicopoly Café Xl Lisa                                      nan regular_payment         refunded      2      35980.00
    refund                      Gilet Tipo Crepé Animal Print Café Nicopoly L Café Lisa                                      nan regular_payment         refunded      1      24990.00
    refund                           Gilet Tipo Crepé Animal Print Café Nicopoly L Lisa                                      nan regular_payment         refunded      1      19990.00
    refund                                 Gilet Tipo Crepé Khaki Nicopoly Khaki L Liso                                      nan regular_payment         refunded      1      19990.00
    refund                                       Gilet Tipo Crepé Khaki Nicopoly L Liso                                      nan regular_payment         refunded      1      18990.00
    refund                                       Gilet Tipo Crepé Negro Nicopoly M Liso                                      nan regular_payment         refunded      1      16790.00
    refund                                 Gilet Tipo Crepé Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      19990.00
    refund                                Gilet Tipo Crepé Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      1      19990.00
    refund                     Jeans Básico Pierna Acampanada - Azul Marino - Liso - 40                                      nan regular_payment         refunded      1      32990.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 36                                      nan regular_payment         refunded      1      29990.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 38                                      nan regular_payment         refunded      1      29990.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 40                                      nan regular_payment         refunded      4     147560.00
    refund                           Jeans Básico Pierna Acampanada Azul Marino Liso 42                                      nan regular_payment         refunded      2      59980.00
    refund                          Jeans Básico Pierna Ancha - Azul Marino - Liso - 42                                      nan regular_payment         refunded      1      33990.00
    refund                                Jeans Básico Pierna Ancha Azul Marino Liso 36                                      nan regular_payment         refunded      2      39980.00
    refund                                Jeans Básico Pierna Ancha Azul Marino Liso 38                                      nan regular_payment         refunded      2      53980.00
    refund                                Jeans Básico Pierna Ancha Azul Marino Liso 40                                      nan regular_payment         refunded      3      88970.00
    refund                                      Jeans Básico Recto Azul Marino Nicopoly                                      nan regular_payment         refunded     14     324913.00
    refund                                            Jeans Básico Recto Negro Nicopoly                                      nan regular_payment         refunded     12     314880.00
    refund                                 Jeans Corte Barrel Azul Nicopoly Azul Liso M                                      nan regular_payment         refunded      1      44990.00
    refund                                  Jeans Corte Recto Café Nicopoly Café Liso L                                      nan regular_payment         refunded      1      39990.00
    refund                                  Jeans Corte Recto Café Nicopoly Café Liso S                                      nan regular_payment         refunded      2      63980.00
    refund                                Jeans Corte Recto Khaki Nicopoly Khaki Liso L                                      nan regular_payment         refunded      1      27990.00
    refund                                             Jeans Flare Azul Marino Nicopoly                                      nan regular_payment         refunded      6      73579.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly 36 Azul Liso                                      nan regular_payment         refunded      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly 38 Azul Liso                                      nan regular_payment         refunded      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly 42 Azul Liso                                      nan regular_payment         refunded      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 34                                      nan regular_payment         refunded      1      32990.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 36                                      nan regular_payment         refunded      5     155950.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 38                                      nan regular_payment         refunded      8     250120.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 40                                      nan regular_payment         refunded      3     107970.00
    refund                             Jeans Pierna Wide Leg Azul Nicopoly Azul Liso 42                                      nan regular_payment         refunded      4     133160.00
    refund                                  Jeans Pierna Wide Leg Azul Nicopoly Liso 36                                      nan regular_payment         refunded      1      32990.00
    refund                                  Jeans Pierna Wide Leg Azul Nicopoly Liso 38                                      nan regular_payment         refunded      2      65980.00
    refund                                  Jeans Pierna Wide Leg Azul Nicopoly Liso 40                                      nan regular_payment         refunded      3     116970.00
    refund                                                  Jeans Recto Rosado Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund                            Jeans Rectos Tiro Alto Café Nicopoly Café Liso 34                                      nan regular_payment         refunded      1      29990.00
    refund                            Jeans Rectos Tiro Alto Café Nicopoly Café Liso 38                                      nan regular_payment         refunded      3     125970.00
    refund                            Jeans Rectos Tiro Alto Café Nicopoly Café Liso 42                                      nan regular_payment         refunded      1      33990.00
    refund                         Jeans Wide Leg Blancos Nicopoly - Blanco - Liso - 42                                      nan regular_payment         refunded      1      32990.00
    refund                               Jeans Wide Leg Blancos Nicopoly 42 Liso Blanco                                      nan regular_payment         refunded      1      32990.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 38                                      nan regular_payment         refunded      1      25190.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 40                                      nan regular_payment         refunded      5     155950.00
    refund                               Jeans Wide Leg Blancos Nicopoly Blanco Liso 42                                      nan regular_payment         refunded      4     125960.00
    refund                                      Jeans Wide Leg Blancos Nicopoly Liso 38                                      nan regular_payment         refunded      1      41990.00
    refund                              Kimono Negro Detalles Flecos Nicopoly Negro M/l                                      nan regular_payment         refunded      1      29990.00
    refund                             Legging Ecocuero Cierre Lateral Burdeos Nicopoly                                      nan regular_payment         refunded      2      39980.00
    refund                                 Legging Tiro Alto Aberturas Burdeos Nicopoly                                      nan regular_payment         refunded      1      16990.00
    refund                              Maxi Vestido Corte Imperio Floral Azul Nicopoly                                      nan regular_payment         refunded      4     143960.00
    refund                                   Maxi Vestido Tajo Y Costuras Café Nicopoly                                      nan regular_payment         refunded      1      16990.00
    refund                                   Maxi Vestido Tajo Y Costuras Gris Nicopoly                                      nan regular_payment         refunded      1      13990.00
    refund                                            Mini Falda Leopardo Café Nicopoly                                      nan regular_payment         refunded      9     147394.00
    refund                                       Minifalda Ecocuero Tajo Negro Nicopoly                                      nan regular_payment         refunded      3      60970.00
    refund                          Pantalón Básico Blanco Nicopoly - Blanco - Liso - L                                      nan regular_payment         refunded      1      27990.00
    refund                          Pantalón Básico Blanco Nicopoly - Blanco - Liso - S                                      nan regular_payment         refunded      1      27990.00
    refund                         Pantalón Básico Blanco Nicopoly - Blanco - Liso - Xl                                      nan regular_payment         refunded      1      27990.00
    refund                                Pantalón Básico Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      2      59480.00
    refund                                Pantalón Básico Blanco Nicopoly Blanco Liso M                                      nan regular_payment         refunded      1      34990.00
    refund                                       Pantalón Básico Blanco Nicopoly Liso M                                      nan regular_payment         refunded      1      34990.00
    refund                                    Pantalón Básico Café Nicopoly Café Liso M                                      nan regular_payment         refunded      2      75980.00
    refund                                    Pantalón Básico Café Nicopoly Café Liso S                                      nan regular_payment         refunded      1      37990.00
    refund                                   Pantalón Básico Café Nicopoly Café Liso Xl                                      nan regular_payment         refunded      1      37990.00
    refund                        Pantalón Básico Celeste Nicopoly - Celeste - Liso - S                                      nan regular_payment         refunded      2      55980.00
    refund                              Pantalón Básico Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      1      34990.00
    refund                                      Pantalón Básico Celeste Nicopoly Liso M                                      nan regular_payment         refunded      1      34990.00
    refund                                    Pantalón Básico Gris Nicopoly Gris Liso L                                      nan regular_payment         refunded      1      24490.00
    refund                                    Pantalón Básico Gris Nicopoly Gris Liso M                                      nan regular_payment         refunded      1      24490.00
    refund                                    Pantalón Básico Gris Nicopoly L Gris Liso                                      nan regular_payment         refunded      1      27990.00
    refund                                         Pantalón Básico Gris Nicopoly Liso L                                      nan regular_payment         refunded      1      34990.00
    refund                                         Pantalón Básico Gris Nicopoly Liso M                                      nan regular_payment         refunded      1      34990.00
    refund                                    Pantalón Básico Gris Nicopoly M Gris Liso                                      nan regular_payment         refunded      1      27990.00
    refund                            Pantalón Básico Khaki Nicopoly - Khaki - Liso - M                                      nan regular_payment         refunded      2      27990.00
    refund                                  Pantalón Básico Khaki Nicopoly Khaki Liso S                                      nan regular_payment         refunded      1      34990.00
    refund                                        Pantalón Básico Khaki Nicopoly Liso M                                      nan regular_payment         refunded      2      62980.00
    refund                                Pantalón Básico Morado Nicopoly Morado Liso L                                      nan regular_payment         refunded      2      72980.00
    refund                                Pantalón Básico Morado Nicopoly Morado Liso M                                      nan regular_payment         refunded      2      58980.00
    refund                                Pantalón Básico Morado Nicopoly Morado Liso S                                      nan regular_payment         refunded      2      72980.00
    refund                               Pantalón Básico Morado Nicopoly Morado Liso Xl                                      nan regular_payment         refunded      1      34990.00
    refund                                        Pantalón Básico Negro Nicopoly Liso L                                      nan regular_payment         refunded      2      55980.00
    refund                                        Pantalón Básico Negro Nicopoly Liso M                                      nan regular_payment         refunded      1      27990.00
    refund                                        Pantalón Básico Negro Nicopoly Liso S                                      nan regular_payment         refunded      2      34990.00
    refund                                       Pantalón Básico Negro Nicopoly Liso Xl                                      nan regular_payment         refunded      2      69980.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      3     107970.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      2      69980.00
    refund                                  Pantalón Básico Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      1      34990.00
    refund                                 Pantalón Básico Negro Nicopoly Negro Liso Xl                                      nan regular_payment         refunded      2      69980.00
    refund                                  Pantalón Básico Pierna Ancha Beige Nicopoly                                      nan regular_payment         refunded      4     113910.00
    refund                       Pantalón Básico Pierna Ancha Gris Nicopoly Gris Liso L                                      nan regular_payment         refunded      1      26990.00
    refund                       Pantalón Básico Pierna Ancha Gris Nicopoly Gris Liso M                                      nan regular_payment         refunded      1      28990.00
    refund                            Pantalón Básico Pierna Ancha Gris Nicopoly Liso S                                      nan regular_payment         refunded      1      35990.00
    refund                                  Pantalón Básico Pierna Ancha Khaki Nicopoly                                      nan regular_payment         refunded      5     152450.00
    refund                   Pantalón Básico Pierna Ancha Marrón Nicopoly Marrón Lisa S                                      nan regular_payment         refunded      1      35990.00
    refund                                  Pantalón Básico Pierna Ancha Negro Nicopoly                                      nan regular_payment         refunded     11     338193.00
    refund                              Pantalón Básico Rojo Nicopoly - Rojo - Liso - L                                      nan regular_payment         refunded      1      27990.00
    refund                              Pantalón Básico Rojo Nicopoly - Rojo - Liso - M                                      nan regular_payment         refunded      1      27990.00
    refund                                         Pantalón Básico Rojo Nicopoly Liso M                                      nan regular_payment         refunded      1      34990.00
    refund                                    Pantalón Básico Rojo Nicopoly Rojo Liso L                                      nan regular_payment         refunded      3      70970.00
    refund                           Pantalón Básico Rosa Nicopoly - Rosado - Liso - Xl                                      nan regular_payment         refunded      1      27990.00
    refund                                  Pantalón Básico Rosa Nicopoly Rosado Liso L                                      nan regular_payment         refunded      1      34990.00
    refund                                  Pantalón Básico Rosa Nicopoly Rosado Liso M                                      nan regular_payment         refunded      4     132960.00
    refund                                  Pantalón Básico Rosa Nicopoly Rosado Liso S                                      nan regular_payment         refunded      1      34990.00
    refund                                 Pantalón Básico Rosa Nicopoly Rosado Liso Xl                                      nan regular_payment         refunded      1      34990.00
    refund                                  Pantalón Básico Verde Nicopoly Verde Liso L                                      nan regular_payment         refunded      3     104970.00
    refund                                  Pantalón Básico Verde Nicopoly Verde Liso M                                      nan regular_payment         refunded      1      34990.00
    refund                                 Pantalón Básico Verde Nicopoly Verde Liso Xl                                      nan regular_payment         refunded      2      55980.00
    refund                                              Pantalón Carrot Blanco Nicopoly                                      nan regular_payment         refunded      1      29990.00
    refund                                               Pantalón Carrot Khaki Nicopoly                                      nan regular_payment         refunded      2      60880.00
    refund                                               Pantalón Carrot Negro Nicopoly                                      nan regular_payment         refunded      5     178450.00
    refund                    Pantalón Con Costuras Frontales Recto Azul Acero Nicopoly                                      nan regular_payment         refunded      6     121950.00
    refund                       Pantalón Con Costuras Frontales Recto Burdeos Nicopoly                                      nan regular_payment         refunded      9     201860.00
    refund                        Pantalón Con Costuras Frontales Recto Lúcuma Nicopoly                                      nan regular_payment         refunded      6     127950.00
    refund                                    Pantalón Con Pinzas Recto Blanco Nicopoly                                      nan regular_payment         approved      1      37990.00
    refund                                    Pantalón Con Pinzas Recto Blanco Nicopoly                                      nan regular_payment         refunded      5     147950.00
    refund                                   Pantalón Con Pinzas Recto Celeste Nicopoly                                      nan regular_payment         refunded     13     375670.00
    refund                                     Pantalón Con Pinzas Recto Negro Nicopoly                                      nan regular_payment         refunded      3      49470.00
    refund                                    Pantalón Con Pinzas Recto Rosado Nicopoly                                      nan regular_payment         refunded      5     140950.00
    refund                            Pantalón Costuras Frontales Recto Lúcuma Nicopoly                                      nan regular_payment         refunded      4      81800.00
    refund                              Pantalón Costuras Frontales Recto Rosa Nicopoly                                      nan regular_payment         refunded      7     179930.00
    refund         Pantalón De Pierna Recta Raya Diplomática Blanco - Blanco - Liso - L                                      nan regular_payment         refunded      2      61180.00
    refund         Pantalón De Pierna Recta Raya Diplomática Blanco - Blanco - Liso - M                                      nan regular_payment         refunded      1      35990.00
    refund               Pantalón De Pierna Recta Raya Diplomática Blanco Blanco Liso S                                      nan regular_payment         refunded      1      37990.00
    refund      Pantalón De Pierna Recta Raya Diplomática Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment         refunded      2      75980.00
    refund             Pantalón De Pierna Recta Raya Diplomática Celeste Celeste Liso L                                      nan regular_payment         refunded      1      26990.00
    refund             Pantalón De Pierna Recta Raya Diplomática Gris - Gris - Liso - M                                      nan regular_payment         refunded      1      35990.00
    refund             Pantalón De Pierna Recta Raya Diplomática Gris - Gris - Liso - S                                      nan regular_payment         refunded      1      25190.00
    refund                   Pantalón De Pierna Recta Raya Diplomática Gris Gris Liso M                                      nan regular_payment         refunded      2      61180.00
    refund                   Pantalón De Pierna Recta Raya Diplomática Gris Gris Liso S                                      nan regular_payment         refunded      2      63180.00
    refund                        Pantalón De Pierna Recta Raya Diplomática Gris Liso L                                      nan regular_payment         refunded      1      35990.00
    refund                        Pantalón De Pierna Recta Raya Diplomática Gris Liso M                                      nan regular_payment         refunded      1      35990.00
    refund        Pantalón De Pierna Recta Raya Diplomática Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      37990.00
    refund        Pantalón De Pierna Recta Raya Diplomática Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      37990.00
    refund       Pantalón De Pierna Recta Raya Diplomática Negro Nicopoly Negro Liso Xl                                      nan regular_payment         refunded      1      37990.00
    refund                                Pantalón Dos Botones Blanco Invierno Nicopoly                                      nan regular_payment         refunded      1      21590.00
    refund                                        Pantalón Dos Botones Celeste Nicopoly                                      nan regular_payment         refunded      2      49980.00
    refund                     Pantalón Dos Botones Rosado Nicopoly - Rosado - Liso - M                                      nan regular_payment         refunded      1      25190.00
    refund                       Pantalón Dos Botones Verde Oliva Nicopoly Oliva Liso M                                      nan regular_payment         refunded      2      55980.00
    refund   Pantalón Entallado Costuras Delanteras Blanco Nicopoly - Blanco - Liso - S                                      nan regular_payment         refunded      1      25990.00
    refund         Pantalón Entallado Costuras Delanteras Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      19790.00
    refund             Pantalón Entallado Costuras Delanteras Café Nicopoly Café Liso L                                      nan regular_payment         refunded      2      45980.00
    refund             Pantalón Entallado Costuras Delanteras Café Nicopoly Café Liso S                                      nan regular_payment         refunded      1      22990.00
    refund       Pantalón Entallado Costuras Delanteras Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      1      25990.00
    refund             Pantalón Entallado Costuras Delanteras Gris Nicopoly Gris Liso L                                      nan regular_payment         refunded      1      22990.00
    refund             Pantalón Entallado Costuras Delanteras Gris Nicopoly Gris Liso M                                      nan regular_payment         refunded      2      42780.00
    refund                          Pantalón Estampado Cebra Café Nicopoly Café Liso Xl                                      nan regular_payment         refunded      3      55970.00
    refund           Pantalón Estilo Japonés Pierna Ancha Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment         refunded      1      35990.00
    refund           Pantalón Estilo Japonés Pierna Ancha Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment         refunded      1      35990.00
    refund          Pantalón Estilo Japonés Pierna Ancha Burdeo Nicopoly Burdeo Liso Xl                                      nan regular_payment         refunded      1      35990.00
    refund               Pantalón Estilo Japonés Pierna Ancha Café Nicopoly Café Liso L                                      nan regular_payment         refunded      1      35990.00
    refund              Pantalón Estilo Japonés Pierna Ancha Café Nicopoly Café Liso Xl                                      nan regular_payment         refunded      1      44990.00
    refund             Pantalón Estilo Japonés Pierna Ancha Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      5      91532.00
    refund             Pantalón Estilo Japonés Pierna Ancha Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      1      35990.00
    refund            Pantalón Estilo Japonés Pierna Ancha Negro Nicopoly Negro Liso Xl                                      nan regular_payment         refunded      3     116970.00
    refund                                Pantalón Holgado Pretina Alta Blanco Nicopoly                                      nan regular_payment         refunded      4      83960.00
    refund                                       Pantalón Lazo De Hebilla Café Nicopoly                                      nan regular_payment         refunded      6     249940.00
    refund                                      Pantalón Lazo De Hebilla Khaki Nicopoly                                      nan regular_payment         refunded      3     133092.00
    refund                            Pantalón Leopardo Café Nicopoly - Café - Liso - L                                      nan regular_payment         refunded      1      25990.00
    refund                            Pantalón Leopardo Café Nicopoly - Café - Liso - M                                      nan regular_payment         refunded      3      77970.00
    refund                                  Pantalón Leopardo Café Nicopoly Café Liso L                                      nan regular_payment         refunded      1      18190.00
    refund                                  Pantalón Leopardo Café Nicopoly Café Liso M                                      nan regular_payment         refunded      1      25990.00
    refund                                 Pantalón Leopardo Café Nicopoly Café Liso Xl                                      nan regular_payment         refunded      1      19990.00
    refund                                          Pantalón Mezcla Lino Beige Nicopoly                                      nan regular_payment         refunded     11     264921.00
    refund                                         Pantalón Mezcla Lino Blanco Nicopoly                                      nan regular_payment         refunded      6     155940.00
    refund                         Pantalón Mezcla Lino Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      3      49419.00
    refund                         Pantalón Mezcla Lino Celeste Nicopoly Celeste Liso S                                      nan regular_payment         refunded      2      43980.00
    refund                                Pantalón Negro Flores Blancas Nicopoly Lisa L                                      nan regular_payment         refunded      2      49980.00
    refund                                Pantalón Negro Flores Blancas Nicopoly Lisa M                                      nan regular_payment         refunded      1      24990.00
    refund                          Pantalón Negro Flores Blancas Nicopoly Negro Lisa M                                      nan regular_payment         refunded      3      49970.00
    refund                          Pantalón Negro Flores Blancas Nicopoly Negro Lisa S                                      nan regular_payment         refunded      2      39980.00
    refund                                Pantalón Palazzo Lazo Frontal Blanco Nicopoly                                      nan regular_payment         refunded      1      37990.00
    refund                                         Pantalón Palazzo Tajos Café Nicopoly                                      nan regular_payment         refunded      2      53980.00
    refund                                      Pantalón Palazzo Tajos Magenta Nicopoly                                      nan regular_payment         refunded     15     429460.00
    refund                       Pantalón Palazzo Tajos Mostaza Nicopoly M Liso Mostaza                                      nan regular_payment         refunded      1      36990.00
    refund                       Pantalón Palazzo Tajos Mostaza Nicopoly Mostaza Liso L                                      nan regular_payment         refunded      1      28990.00
    refund                      Pantalón Palazzo Tajos Mostaza Nicopoly Mostaza Liso Xl                                      nan regular_payment         refunded      1      26990.00
    refund                                        Pantalón Palazzo Tajos Negro Nicopoly                                      nan regular_payment         refunded     16     439870.00
    refund                                        Pantalón Palazzo Tajos Verde Nicopoly                                      nan regular_payment         refunded     10     233110.00
    refund                                        Pantalón Pierna Ancha Blanco Nicopoly                                      nan regular_payment         refunded      1      26490.00
    refund                                       Pantalón Pierna Ancha Celeste Nicopoly                                      nan regular_payment         refunded      4     103460.00
    refund                             Pantalón Pierna Ancha Con Pasador Khaki Nicopoly                                      nan regular_payment         refunded      3      87470.00
    refund                            Pantalón Pierna Ancha Con Pasador Morado Nicopoly                                      nan regular_payment         refunded      7     189284.00
    refund                             Pantalón Pierna Ancha Con Pasador Negro Nicopoly                                      nan regular_payment         refunded      6     195940.00
    refund                       Pantalón Pierna Ancha Con Pasador Rojo Oscuro Nicopoly                                      nan regular_payment         refunded      3      97970.00
    refund                                         Pantalón Pierna Ancha Khaki Nicopoly                                      nan regular_payment         refunded      2      59980.00
    refund                                         Pantalón Pierna Ancha Negro Nicopoly                                      nan regular_payment         refunded      1      16490.00
    refund                                          Pantalón Pierna Ancha Rojo Nicopoly                                      nan regular_payment         refunded      3      76970.00
    refund                                           Pantalón Pierna Ancha Rojonicopoly                                      nan regular_payment         refunded      2      46480.00
    refund                                       Pantalón Pinzas Recto Burdeos Nicopoly                                      nan regular_payment         refunded      7     163930.00
    refund                                          Pantalón Pinzas Recto Gris Nicopoly                                      nan regular_payment         refunded      3      68950.00
    refund                                         Pantalón Pinzas Recto Óxido Nicopoly                                      nan regular_payment         refunded      4      68950.00
    refund                                    Pantalón Pinzas Tiro Alto Blanco Nicopoly                                      nan regular_payment         refunded      4      97960.00
    refund                                   Pantalón Pinzas Tiro Alto Celeste Nicopoly                                      nan regular_payment         refunded      3      68970.00
    refund                                     Pantalón Pinzas Tiro Alto Khaki Nicopoly                                      nan regular_payment         refunded      1      19190.00
    refund                                     Pantalón Pinzas Tiro Alto Negro Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                      Pantalón Pinzas Tiro Alto Rojo Nicopoly                                      nan regular_payment         refunded      1      24990.00
    refund                                Pantalón Pretina Ancha Azul Grisáceo Nicopoly                                      nan regular_payment         refunded      1      20990.00
    refund                                  Pantalón Pretina Ancha Verde Musgo Nicopoly                                      nan regular_payment         refunded      4      83960.00
    refund                                      Pantalón Recto Botones Burdeos Nicopoly                                      nan regular_payment         refunded      2      42100.00
    refund                           Pantalón Recto Con Pinza Azul Nicopoly Azul Liso L                                      nan regular_payment         refunded      1      75980.00
    refund                        Pantalón Recto Con Pinza Oliva Nicopoly Oliva Liso Xl                                      nan regular_payment         refunded      1      37990.00
    refund                                Pantalón Recto Con Pinzas Azul Acero Nicopoly                                      nan regular_payment         refunded      9     284710.00
    refund                                     Pantalón Recto Con Pinzas Beige Nicopoly                                      nan regular_payment         refunded      3      86370.00
    refund                                    Pantalón Recto Con Pinzas Burdeo Nicopoly                                      nan regular_payment         refunded     12     395880.00
    refund                                     Pantalón Recto Con Pinzas Negro Nicopoly                                      nan regular_payment         refunded     12     397680.00
    refund                                      Pantalón Recto Con Pinzas Rojo Nicopoly                                      nan regular_payment         refunded      3     100970.00
    refund                             Pantalón Recto Costura Frontal  Celeste Nicopoly                                      nan regular_payment         refunded      2      37980.00
    refund                              Pantalón Recto Costura Frontal Burdeos Nicopoly                                      nan regular_payment         refunded      1      18990.00
    refund                                Pantalón Recto Costura Frontal Negro Nicopoly                                      nan regular_payment         refunded      7     129864.00
    refund                                    Pantalón Recto Rayas Azul Marino Nicopoly                                      nan regular_payment         refunded      2      59980.00
    refund                        Pantalón Sastrero Recto Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      2      63980.00
    refund                        Pantalón Sastrero Recto Burdeo Nicopoly Burdeo Liso M                                      nan regular_payment         refunded      1      31990.00
    refund                            Pantalón Sastrero Recto Café Nicopoly Café Liso M                                      nan regular_payment         refunded      1      31990.00
    refund             Pantalón Tipo Crepé Ajustable Khaki Nicopoly - Khaki - Lisa - Xl                                      nan regular_payment         refunded      1      23990.00
    refund                    Pantalón Tipo Crepé Ajustable Khaki Nicopoly Khaki Lisa M                                      nan regular_payment         refunded      1      17990.00
    refund                    Pantalón Tipo Crepé Ajustable Khaki Nicopoly Khaki Lisa S                                      nan regular_payment         refunded      1      17990.00
    refund                   Pantalón Tipo Crepé Ajustable Khaki Nicopoly Khaki Lisa Xl                                      nan regular_payment         refunded      1      19990.00
    refund                    Pantalón Tipo Crepé Ajustable Khaki Nicopoly L Lisa Khaki                                      nan regular_payment         refunded      1      23990.00
    refund                          Pantalón Tipo Crepé Ajustable Negro Nicopoly Lisa M                                      nan regular_payment         refunded      1      16790.00
    refund                                    Pantalón Tiro Alto Básico Blanco Nicopoly                                      nan regular_payment         refunded      5     106640.00
    refund                                   Pantalón Tiro Alto Básico Celeste Nicopoly                                      nan regular_payment         refunded      9     182460.00
    refund                                     Pantalón Tiro Alto Básico Khaki Nicopoly                                      nan regular_payment         refunded     18     369120.00
    refund                                     Pantalón Tiro Alto Básico Negro Nicopoly                                      nan regular_payment         refunded      8     260820.00
    refund                                      Pantalón Tiro Alto Básico Rojo Nicopoly                                      nan regular_payment         refunded     14     289310.00
    refund                                  Pantalón Tiro Alto Jaspeado Blanco Nicopoly                                      nan regular_payment         refunded      5      85950.00
    refund                                 Pantalón Tiro Alto Jaspeado Celeste Nicopoly                                      nan regular_payment         refunded      6     102440.00
    refund                                  Pantalón Tiro Alto Jaspeado Rosado Nicopoly                                      nan regular_payment         refunded      4      73914.00
    refund                            Pantalón Vestir Costuras Frontales Camel Nicopoly                                      nan regular_payment         refunded      3      56970.00
    refund                            Pantalón Vestir Costuras Frontales Negro Nicopoly                                      nan regular_payment         refunded      2      52780.00
    refund                                 Pantalón Vestir Recto Blanco Nicopoly Liso M                                      nan regular_payment         refunded      2      64780.00
    refund                                 Pantalón Vestir Recto Blanco Nicopoly Liso S                                      nan regular_payment         refunded      2      57580.00
    refund                         Pantalón Vestir Recto Blanco Nicopoly Xl Liso Blanco                                      nan regular_payment         refunded      1      23390.00
    refund                          Pantalón Vestir Recto Burdeo Nicopoly Burdeo Liso L                                      nan regular_payment         refunded      2      77980.00
    refund                        Pantalón Vestir Recto Café Nicopoly - Café - Liso - L                                      nan regular_payment         refunded      1      35990.00
    refund                        Pantalón Vestir Recto Café Nicopoly - Café - Liso - S                                      nan regular_payment         refunded      1      35990.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso L                                      nan regular_payment         refunded      5     188950.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso M                                      nan regular_payment         refunded      4     122360.00
    refund                              Pantalón Vestir Recto Café Nicopoly Café Liso S                                      nan regular_payment         refunded      3      71570.00
    refund                             Pantalón Vestir Recto Café Nicopoly Café Liso Xl                                      nan regular_payment         refunded      1      23390.00
    refund                      Pantalón Vestir Recto Khaki Nicopoly - Khaki - Liso - L                                      nan regular_payment         refunded      1      35990.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly Khaki Liso M                                      nan regular_payment         refunded      3      83970.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly Khaki Liso S                                      nan regular_payment         refunded      2      48380.00
    refund                           Pantalón Vestir Recto Khaki Nicopoly Khaki Liso Xl                                      nan regular_payment         refunded      1      23390.00
    refund                                  Pantalón Vestir Recto Khaki Nicopoly Liso M                                      nan regular_payment         refunded      2      61180.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly M Liso Khaki                                      nan regular_payment         refunded      1      35990.00
    refund                            Pantalón Vestir Recto Khaki Nicopoly S Liso Khaki                                      nan regular_payment         refunded      1      23390.00
    refund                            Pantalón Vestir Recto Mocca Nicopoly Mocca Liso L                                      nan regular_payment         refunded      1      38990.00
    refund                            Pantalón Vestir Recto Mocca Nicopoly Mocca Liso S                                      nan regular_payment         refunded      1      38990.00
    refund                    Parka Acolchada Bolsillos Grandes Celeste Pastel Nicopoly                                      nan regular_payment         refunded      1      35990.00
    refund                              Parka Acolchada Midi Con Gorro Celeste Nicopoly                                      nan regular_payment         refunded      8     228935.00
    refund                                Parka Acolchada Midi Con Gorro Negro Nicopoly                                      nan regular_payment         refunded      2      91980.00
    refund                                 Parka Corta Acolchada Azul Grisáceo Nicopoly                                      nan regular_payment         refunded      4     116960.00
    refund                               Parka Corta Acolchada Blanco Invierno Nicopoly                                      nan regular_payment         refunded      4     125960.00
    refund                                          Parka Corta Acolchada Café Nicopoly                                      nan regular_payment         refunded     21     481412.00
    refund                             Parka Corta Quilt Con Gorro Azul Marino Nicopoly                                      nan regular_payment         refunded      3      59970.00
    refund                                   Parka Corta Quilt Con Gorro Negro Nicopoly                                      nan regular_payment         refunded      1      28490.00
    refund                                    Parka Corta Quilt Con Gorro Rojo Nicopoly                                      nan regular_payment         refunded      2      50480.00
    refund                                   Parka Corta Quilt Con Gorro Óxido Nicopoly                                      nan regular_payment         refunded      4      46778.00
    refund                     Parka Corta Sin Mangas Tipo Ecocuero Azul Cielo Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                    Parka Corta Tipo Ecocuero  Khaki Nicopoly                                      nan regular_payment         refunded      2      69980.00
    refund                           Parka Corta Tipo Ecocuero Blanco Invierno Nicopoly                                      nan regular_payment         refunded      3     131970.00
    refund                             Parka Corta Tipo Ecocuero Gris Metálico Nicopoly                                      nan regular_payment         refunded      2      71980.00
    refund                                     Parka Corta Tipo Ecocuero Negro Nicopoly                                      nan regular_payment         refunded      4     133960.00
    refund                             Parka Corta Tipo Ecocuero Rosado Chicle Nicopoly                                      nan regular_payment         refunded      1      35990.00
    refund                           Parka Larga Acolchada Cuello Alto Celeste Nicopoly                                      nan regular_payment         refunded      1      41990.00
    refund                            Parka Larga Quilt Cintura Ajustable Gris Nicopoly                                      nan regular_payment         refunded     13     395970.00
    refund                           Parka Larga Quilt Cintura Ajustable Negro Nicopoly                                      nan regular_payment         refunded      8     301720.00
    refund                           Parka Larga Quilt Cintura Ajustable Oliva Nicopoly                                      nan regular_payment         refunded     10     299410.00
    refund                                Parka Midi Tipo Quilt Bolsillos Gris Nicopoly                                      nan regular_payment         refunded      9     241910.00
    refund                              Parka Midi Tipo Quilt Bolsillos Marrón Nicopoly                                      nan regular_payment         refunded      7     235610.00
    refund                               Parka Midi Tipo Quilt Bolsillos Negro Nicopoly                                      nan regular_payment         refunded      4     123960.00
    refund                                  Parka Quilt Broches Gris Brillante Nicopoly                                      nan regular_payment         refunded      5     146250.00
    refund                                 Parka Quilt Broches Negro Brillante Nicopoly                                      nan regular_payment         refunded      8     253820.00
    refund                             Parka Sin Mangas Cordón Blanco Invierno Nicopoly                                      nan regular_payment         refunded      9     342110.00
    refund                                        Parka Sin Mangas Cordón Café Nicopoly                                      nan regular_payment         refunded     10     376500.00
    refund                                       Parka Sin Mangas Cordón Negro Nicopoly                                      nan regular_payment         refunded     24     860631.00
    refund                                        Parka Sin Mangas Cordón Rojo Nicopoly                                      nan regular_payment         refunded      7     259930.00
    refund                          Parka Sin Mangas Imán Cuello Azul Grisáceo Nicopoly                                      nan regular_payment         refunded      3      49980.00
    refund                        Parka Sin Mangas Imán Cuello Blanco Invierno Nicopoly                                      nan regular_payment         refunded      6     147440.00
    refund                                   Parka Sin Mangas Imán Cuello Café Nicopoly                                      nan regular_payment         refunded      2      49980.00
    refund                                         Parka Sin Mangas Quilt Gris Nicopoly                                      nan regular_payment         refunded      2      51980.00
    refund                                       Parka Sin Mangas Quilt Marrón Nicopoly                                      nan regular_payment         refunded      1      38990.00
    refund                                        Parka Sin Mangas Quilt Oliva Nicopoly                                      nan regular_payment         refunded      1      38990.00
    refund                                             Peto Básico Azul Marino Nicopoly                                      nan regular_payment         refunded      1       4990.00
    refund                                      Peto Cuello Halter Azul Marino Nicopoly                                      nan regular_payment         refunded      1       4990.00
    refund                                             Peto Escote En V Rosado Nicopoly                                      nan regular_payment         refunded      1       8990.00
    refund                       Polera Blanca Detalle De Encaje Nicopoly Blanco M Liso                                      nan regular_payment         refunded      1      14990.00
    refund                       Polera Blanca Detalle De Encaje Nicopoly Blanco S Liso                                      nan regular_payment         refunded      4      60434.00
    refund        Polera Básica Cuello Redondo Azul Marino Nicopoly Azul Marino Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                   Polera Básica Cuello Redondo Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      1       9990.00
    refund Polera Básica Cuello Redondo Líneas Azul Marino Nicopoly Azul Marino Xl Liso                                      nan regular_payment         refunded      1       9690.00
    refund          Polera Básica Cuello Redondo Líneas Grafito Nicopoly Grafito M Liso                                      nan regular_payment         refunded      1      11990.00
    refund               Polera Básica Cuello Redondo Líneas Gris Claro Nicopoly M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                     Polera Básica Cuello Redondo Líneas Rojo Nicopoly M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                    Polera Básica Cuello Redondo Líneas Rojo Nicopoly Xl Liso                                      nan regular_payment         refunded      1      14184.00
    refund                        Polera Con Transparencias Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      18190.00
    refund                       Polera Con Transparencias Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      2      35980.00
    refund                                  Polera Cuello Alto Blanco Invierno Nicopoly                                      nan regular_payment         refunded      1       8240.00
    refund                                           Polera Cuello Alto Burdeo Nicopoly                                      nan regular_payment         refunded      2      21980.00
    refund                                             Polera Cuello Alto Café Nicopoly                                      nan regular_payment         refunded      1       8240.00
    refund                                          Polera Cuello Alto Grafito Nicopoly                                      nan regular_payment         refunded      2      15930.00
    refund                                             Polera Cuello Alto Gris Nicopoly                                      nan regular_payment         refunded      3      29770.00
    refund                               Polera Cuello Redondo Blanco Invierno Nicopoly                                      nan regular_payment         refunded      2      20980.00
    refund                                        Polera Cuello Redondo Burdeo Nicopoly                                      nan regular_payment         refunded      5      51200.00
    refund                                          Polera Cuello Redondo Café Nicopoly                                      nan regular_payment         refunded      4      43754.00
    refund                                       Polera Cuello Redondo Grafito Nicopoly                                      nan regular_payment         refunded      3      30570.00
    refund                                         Polera Cuello Redondo Negro Nicopoly                                      nan regular_payment         refunded      3      29770.00
    refund                     Polera Encaje Cuello Alto Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment         refunded      1      19990.00
    refund                     Polera Encaje Cuello Alto Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment         refunded      1      19990.00
    refund                        Polera Encaje Cuello Alto Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      13190.00
    refund                        Polera Encaje Cuello Alto Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      1      13190.00
    refund                       Polera Encaje Cuello Alto Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      2      41980.00
    refund                        Polera Encaje Escote Nudo Beige Nicopoly Beige Liso M                                      nan regular_payment         refunded      3      50770.00
    refund                        Polera Encaje Escote Nudo Beige Nicopoly Beige Liso S                                      nan regular_payment         refunded      1      22990.00
    refund                              Polera Encaje Escote Nudo Negro Nicopoly Liso M                                      nan regular_payment         refunded      1      22990.00
    refund                        Polera Encaje Escote Nudo Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      22990.00
    refund                        Polera Encaje Escote Nudo Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      13790.00
    refund                Polera Encaje Escote Nudo Rosado Nicopoly - Rosado - Liso - M                                      nan regular_payment         refunded      1      17990.00
    refund                      Polera Encaje Escote Nudo Rosado Nicopoly Rosado Liso M                                      nan regular_payment         refunded      3      59770.00
    refund                      Polera Encaje Manga Larga Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      23990.00
    refund                      Polera Encaje Manga Larga Blanco Nicopoly Blanco Liso S                                      nan regular_payment         refunded      1      23990.00
    refund                      Polera Encaje Manga Larga Burdeo Nicopoly Burdeo M Liso                                      nan regular_payment         refunded      1      15590.00
    refund                             Polera Encaje Manga Larga Burdeo Nicopoly M Liso                                      nan regular_payment         refunded      1      20790.00
    refund                              Polera Encaje Manga Larga Negro Nicopoly L Liso                                      nan regular_payment         refunded      1      20790.00
    refund                        Polera Encaje Manga Larga Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      2      25990.00
    refund                        Polera Encaje Manga Larga Negro Nicopoly Negro S Liso                                      nan regular_payment         refunded      1      25990.00
    refund            Polera Escote En V Básica Azul Marino Nicopoly Azul Marino L Liso                                      nan regular_payment         refunded      4      89910.00
    refund            Polera Escote En V Básica Azul Marino Nicopoly Azul Marino M Liso                                      nan regular_payment         refunded      4      39960.00
    refund                      Polera Escote En V Básica Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      5      42998.00
    refund                      Polera Escote En V Básica Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      2      29970.00
    refund                     Polera Escote En V Básica Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                             Polera Escote En V Básica Blanco Nicopoly L Liso                                      nan regular_payment         refunded      1      23980.00
    refund                      Polera Escote En V Básica Blanco Nicopoly L Liso Blanco                                      nan regular_payment         refunded      1       9990.00
    refund                      Polera Escote En V Básica Blanco Nicopoly M Liso Blanco                                      nan regular_payment         refunded      1       9990.00
    refund                            Polera Escote En V Básica Blanco Nicopoly Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                    Polera Escote En V Básica Café Nicopoly - Café - L - Liso                                      nan regular_payment         refunded      2      23070.00
    refund                          Polera Escote En V Básica Café Nicopoly Café M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                         Polera Escote En V Básica Café Nicopoly Café Xl Liso                                      nan regular_payment         refunded      3      29970.00
    refund                          Polera Escote En V Básica Café Nicopoly L Café Liso                                      nan regular_payment         refunded      1       9990.00
    refund                         Polera Escote En V Básica Café Nicopoly Xl Café Liso                                      nan regular_payment         refunded      1       9990.00
    refund                              Polera Escote En V Básica Café Nicopoly Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                    Polera Escote En V Básica Celeste Nicopoly Celeste L Liso                                      nan regular_payment         refunded      1      12980.00
    refund                    Polera Escote En V Básica Celeste Nicopoly Celeste M Liso                                      nan regular_payment         refunded      2      19980.00
    refund                   Polera Escote En V Básica Celeste Nicopoly Celeste Xl Liso                                      nan regular_payment         refunded      1      11990.00
    refund                            Polera Escote En V Básica Celeste Nicopoly M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                   Polera Escote En V Básica Gris Nicopoly - Gris - Xl - Liso                                      nan regular_payment         refunded      1       9990.00
    refund                          Polera Escote En V Básica Gris Nicopoly Gris S Liso                                      nan regular_payment         refunded      1       9990.00
    refund                              Polera Escote En V Básica Gris Nicopoly Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                        Polera Escote En V Básica Negro Nicopoly L Liso Negro                                      nan regular_payment         refunded      1       9990.00
    refund                        Polera Escote En V Básica Negro Nicopoly M Liso Negro                                      nan regular_payment         refunded      1       9990.00
    refund                        Polera Escote En V Básica Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      3      29970.00
    refund                        Polera Escote En V Básica Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      3      31824.00
    refund                       Polera Escote En V Básica Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                             Polera Escote En V Básica Negro Nicopoly Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                       Polera Escote En V Básica Negro Nicopoly Xl Liso Negro                                      nan regular_payment         refunded      1       9990.00
    refund                      Polera Escote En V Básica Rosado Nicopoly Rosado L Liso                                      nan regular_payment         refunded      1       9990.00
    refund                      Polera Escote En V Básica Rosado Nicopoly Rosado M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                                 Polera Halter Calada Bicolor Fucsia Nicopoly                                      nan regular_payment         refunded      1      17764.00
    refund                                         Polera Halter Calada Blanco Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                  Polera Hilo Cuello V Botones Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment         refunded      1      31990.00
    refund                       Polera Malla Cuello Alto Burdeo Nicopoly Burdeo L Liso                                      nan regular_payment         refunded      1      11990.00
    refund                   Polera Manga 3/4 Cuello Bote Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      1      12990.00
    refund                      Polera Manga Corta Básica Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      1       9990.00
    refund                      Polera Manga Corta Básica Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                      Polera Manga Corta Básica Blanco Nicopoly Blanco S Liso                                      nan regular_payment         refunded      2      21980.00
    refund                     Polera Manga Corta Básica Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                             Polera Manga Corta Básica Blanco Nicopoly M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                             Polera Manga Corta Básica Blanco Nicopoly S Liso                                      nan regular_payment         refunded      1      11990.00
    refund                            Polera Manga Corta Básica Celeste Nicopoly S Liso                                      nan regular_payment         refunded      1      11990.00
    refund               Polera Manga Corta Básica Gris Grafito Nicopoly Grafito M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                         Polera Manga Corta Básica Gris Nicopoly Gris Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                              Polera Manga Corta Básica Negro Nicopoly L Liso                                      nan regular_payment         refunded      1      11990.00
    refund                                Polera Manga Corta Básica Negro Nicopoly Liso                                      nan regular_payment         refunded      1      11990.00
    refund                        Polera Manga Corta Básica Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1       9990.00
    refund                       Polera Manga Corta Básica Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund               Polera Manga Corta Cuello Tipo U Blanco Nicopoly Blanco L Liso                                      nan regular_payment         refunded      1      11990.00
    refund               Polera Manga Corta Cuello Tipo U Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      2      23980.00
    refund              Polera Manga Corta Cuello Tipo U Blanco Nicopoly Blanco Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                   Polera Manga Corta Cuello Tipo U Café Nicopoly Café L Liso                                      nan regular_payment         refunded      1      11990.00
    refund                 Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      2      23980.00
    refund                 Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      2      23980.00
    refund                 Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro S Liso                                      nan regular_payment         refunded      1      11990.00
    refund                Polera Manga Corta Cuello Tipo U Negro Nicopoly Negro Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                 Polera Manga Larga Cuello Bote Burdeo Nicopoly Burdeo L Liso                                      nan regular_payment         refunded      3      13268.00
    refund                Polera Manga Larga Cuello Bote Burdeo Nicopoly Burdeo Xl Liso                                      nan regular_payment         refunded      1       9990.00
    refund                  Polera Manga Larga Cuello Camisero Blanco Invierno Nicopoly                                      nan regular_payment         refunded      2      19980.00
    refund                            Polera Manga Larga Cuello Camisero Khaki Nicopoly                                      nan regular_payment         refunded      1       9990.00
    refund                             Polera Manga Larga Cuello Camisero Rojo Nicopoly                                      nan regular_payment         refunded      3      65130.00
    refund              Polera Manga Larga Cuello Redondo Blanca  - Blanco - S/m - Liso                                      nan regular_payment         refunded      1       9990.00
    refund                    Polera Manga Larga Cuello Redondo Blanca  Blanco M/l Liso                                      nan regular_payment         refunded      1      11990.00
    refund                           Polera Manga Larga Cuello Redondo Grafito S/m Liso                                      nan regular_payment         refunded      1      16880.00
    refund                             Polera Manga Larga Cuello Redondo Khaki S/m Liso                                      nan regular_payment         refunded      1      11990.00
    refund                 Polera Rayas Cuello Bote Blanco Nicopoly - Blanco - L - Liso                                      nan regular_payment         refunded      1      15990.00
    refund                       Polera Rayas Cuello Bote Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      2      26980.00
    refund                              Polera Rayas Cuello Bote Blanco Nicopoly S Liso                                      nan regular_payment         refunded      1      23990.00
    refund                     Polera Rayas Manga Larga Grafito Nicopoly Grafito M Liso                                      nan regular_payment         refunded      1      13990.00
    refund                       Polera Recta Manga Corta Blanco Nicopoly Blanco M Liso                                      nan regular_payment         refunded      1      11990.00
    refund                            Polera Sin Manga Detalle Terciopelo Negro Lisa Xl                                      nan regular_payment         refunded      1      15390.00
    refund                       Polera Sin Manga Detalle Terciopelo Negro Negro Lisa L                                      nan regular_payment         refunded      1      14990.00
    refund                                     Polera Sin Mangas Leopardo Café Nicopoly                                      nan regular_payment         refunded      5      65200.00
    refund                        Polera Sin Mangas Tipo Crochet Blanco Nicopoly M Liso                                      nan regular_payment         refunded      1      23990.00
    refund                   Polera Sin Mangas Tipo Crochet Negro Nicopoly Negro S Liso                                      nan regular_payment         refunded      1      17992.00
    refund                       Polera Tejida Fantasia Blanco Nicopoly Blanco Rayado L                                      nan regular_payment         refunded      2      25980.00
    refund                         Polera Tejida Fantasia Negro Nicopoly Negro M Rayado                                      nan regular_payment         refunded      1      17990.00
    refund                           Polera Transparante De Encaje Negro Negro M Encaje                                      nan regular_payment         refunded      1      17480.00
    refund                          Polera Transparante De Encaje Negro Negro Xl Encaje                                      nan regular_payment         refunded      1      13990.00
    refund                       Polera Transparente De Encaje Blanco Invierno Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund                  Ropa - Ropa Mujer - Blusas - Blusas Manga Larga Café Liso L                                      nan regular_payment         refunded      1      24990.00
    refund                 Ropa - Ropa Mujer - Blusas - Blusas Manga Larga Café Liso Xl                                      nan regular_payment         refunded      6     136740.00
    refund                                 Short Animal Print Café Nicopoly Café Lisa M                                      nan regular_payment         refunded      6      58138.00
    refund                                 Short Animal Print Café Nicopoly Café Lisa S                                      nan regular_payment         refunded      1      18190.00
    refund                                      Short Básico Formal Azul Acero Nicopoly                                      nan regular_payment         refunded      3      47470.00
    refund                                           Short Básico Formal Camel Nicopoly                                      nan regular_payment         refunded      1      17990.00
    refund                                            Short Básico Formal Gris Nicopoly                                      nan regular_payment         refunded      2      31574.00
    refund                                           Short Básico Formal Negro Nicopoly                                      nan regular_payment         refunded      2      35980.00
    refund                                   Short Básico Tiro Alto Azul Acero Nicopoly                                      nan regular_payment         refunded      6     104194.00
    refund                                        Short Básico Tiro Alto Beige Nicopoly                                      nan regular_payment         refunded      1      18990.00
    refund                                       Short Básico Tiro Alto Burdeo Nicopoly                                      nan regular_payment         refunded      5      96900.00
    refund                                        Short Básico Tiro Alto Negro Nicopoly                                      nan regular_payment         refunded      2      49980.00
    refund                                         Short Básico Tiro Alto Rojo Nicopoly                                      nan regular_payment         refunded      3      65970.00
    refund                  Short Con Botones Delanteros  Blanco Nicopoly Blanco Lisa M                                      nan regular_payment         refunded      1      21990.00
    refund                  Short Con Botones Delanteros  Blanco Nicopoly Blanco Lisa S                                      nan regular_payment         refunded      1      18840.00
    refund                       Short Con Botones Delanteros Gris Nicopoly Gris Lisa S                                      nan regular_payment         refunded      1      19990.00
    refund                          Short Con Botones Delanteros Negro Nicopoly Lisa Xl                                      nan regular_payment         refunded      1      28990.00
    refund                     Short Con Botones Delanteros Negro Nicopoly Negro Lisa M                                      nan regular_payment         refunded      2      39380.00
    refund                     Short Con Botones Delanteros Negro Nicopoly Negro Lisa S                                      nan regular_payment         refunded      1      19990.00
    refund                    Short Con Botones Delanteros Negro Nicopoly Negro Lisa Xl                                      nan regular_payment         refunded      4      90960.00
    refund                     Short Con Botones Delanteros Negro Nicopoly S Lisa Negro                                      nan regular_payment         refunded      1      22990.00
    refund                                         Short Holgado Azul Grisáceo Nicopoly                                      nan regular_payment         refunded      1      13990.00
    refund                                                 Short Holgado Beige Nicopoly                                      nan regular_payment         refunded      1      13990.00
    refund                                                 Short Holgado Crema Nicopoly                                      nan regular_payment         refunded      1      13990.00
    refund                                           Short Holgado Verde Musgo Nicopoly                                      nan regular_payment         refunded      2      27980.00
    refund                                  Sobrecamisa Cotelé Blanco Invierno Nicopoly                                      nan regular_payment         refunded      4     115210.00
    refund                                             Sobrecamisa Cotelé Café Nicopoly                                      nan regular_payment         refunded      3      78970.00
    refund                                             Sobrecamisa Cotelé Gris Nicopoly                                      nan regular_payment         refunded      4      86060.00
    refund                                     Sobrecamisa Cotelé Verde Oscuro Nicopoly                                      nan regular_payment         refunded      6     173190.00
    refund                                     Sobrecamisa Larga Escocés Verde Nicopoly                                      nan regular_payment         refunded      2     239960.00
    refund                                Sobrecamisa Tipo Pana Broches Blanco Nicopoly                                      nan regular_payment         refunded      5     113810.00
    refund                                 Sobrecamisa Tipo Pana Broches Taupe Nicopoly                                      nan regular_payment         refunded      1      18990.00
    refund                                  Sweater Acanalado Cuello Alto Gris Nicopoly                                      nan regular_payment         refunded      1      36990.00
    refund                                 Sweater Acanalado Cuello Alto Khaki Nicopoly                                      nan regular_payment         refunded      2      57980.00
    refund                Sweater Acanalado Cuello Bote Celeste Nicopoly Celeste Liso L                                      nan regular_payment         refunded      1      19990.00
    refund                Sweater Acanalado Cuello Bote Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      1      23990.00
    refund                Sweater Acanalado Cuello Bote Celeste Nicopoly Celeste Liso S                                      nan regular_payment         refunded      2      43980.00
    refund                      Sweater Acanalado Cuello Bote Lila Nicopoly Lila Liso L                                      nan regular_payment         refunded      3      55170.00
    refund                      Sweater Acanalado Cuello Bote Lila Nicopoly Lila Liso M                                      nan regular_payment         refunded      3      66970.00
    refund                      Sweater Acanalado Cuello Bote Lila Nicopoly Lila Liso S                                      nan regular_payment         refunded      1      23990.00
    refund                    Sweater Acanalado Cuello Bote Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      18990.00
    refund                    Sweater Acanalado Cuello Bote Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      23990.00
    refund                    Sweater Acanalado Cuello Bote Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      2      39980.00
    refund                      Sweater Acanalado Cuello Bote Rojo Nicopoly Rojo Liso M                                      nan regular_payment         refunded      4      62970.00
    refund                                       Sweater Beatle Acanalado Gris Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                    Sweater Beatle Acanalado Mostaza Nicopoly                                      nan regular_payment         refunded      2      39980.00
    refund                                      Sweater Beatle Acanalado Negro Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                  Sweater Básico Cuello Beatle Acero Nicopoly                                      nan regular_payment         refunded      5     120950.00
    refund                                Sweater Básico Cuello Beatle Magenta Nicopoly                                      nan regular_payment         refunded      2      45980.00
    refund                                  Sweater Básico Cuello Beatle Negro Nicopoly                                      nan regular_payment         refunded     10     217250.00
    refund                                   Sweater Básico Cuello Beatle Rojo Nicopoly                                      nan regular_payment         refunded      5     120950.00
    refund                               Sweater Básico Cuello Redondo Celeste Nicopoly                                      nan regular_payment         refunded      3      64870.00
    refund                               Sweater Básico Cuello Redondo Magenta Nicopoly                                      nan regular_payment         refunded      3      69220.00
    refund                                 Sweater Básico Cuello Redondo Negro Nicopoly                                      nan regular_payment         refunded      8     192820.00
    refund                                  Sweater Básico Cuello Redondo Rojo Nicopoly                                      nan regular_payment         refunded      2      48980.00
    refund                        Sweater Básico Perlas Celeste Nicopoly Celeste Liso L                                      nan regular_payment         refunded      1      21990.00
    refund                        Sweater Básico Perlas Celeste Nicopoly Celeste Liso S                                      nan regular_payment         refunded      1      21990.00
    refund                          Sweater Básico Perlas Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment         refunded      3      43980.00
    refund                          Sweater Básico Perlas Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment         refunded      1      21990.00
    refund                              Sweater Básico Perlas Gris Nicopoly Gris Liso L                                      nan regular_payment         refunded      2      43980.00
    refund                              Sweater Básico Perlas Gris Nicopoly Gris Liso M                                      nan regular_payment         refunded      2      43980.00
    refund                              Sweater Básico Perlas Rojo Nicopoly Rojo Liso L                                      nan regular_payment         refunded      1      21990.00
    refund                              Sweater Básico Perlas Rojo Nicopoly Rojo Liso M                                      nan regular_payment         refunded      1      21990.00
    refund                              Sweater Básico Perlas Rojo Nicopoly Rojo Liso S                                      nan regular_payment         refunded      1      21342.00
    refund                       Sweater Canalé Cuello Tortuga Blanco Invierno Nicopoly                                      nan regular_payment         refunded      4      91960.00
    refund                                 Sweater Canalé Cuello Tortuga Camel Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund                                 Sweater Canalé Cuello Tortuga Negro Nicopoly                                      nan regular_payment         refunded      4      87960.00
    refund                                  Sweater Canalé Cuello Tortuga Rojo Nicopoly                                      nan regular_payment         refunded      1      22490.00
    refund                                          Sweater Color Block Fucsia Nicopoly                                      nan regular_payment         refunded      3      64020.00
    refund                                            Sweater Color Block Gris Nicopoly                                      nan regular_payment         refunded      1      21740.00
    refund                    Sweater Con Patrón Trenzado Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      26990.00
    refund                      Sweater Con Patrón Trenzado Mocca Nicopoly Mocca Liso S                                      nan regular_payment         refunded      1      28990.00
    refund                        Sweater Con Patrón Trenzado Rojo Nicopoly Rojo Liso M                                      nan regular_payment         refunded      1      33990.00
    refund                                         Sweater Crop Acanalado Gris Nicopoly                                      nan regular_payment         refunded      2      39980.00
    refund                             Sweater Crop Cuello Tortuga Azul Índigo Nicopoly                                      nan regular_payment         refunded      1      22490.00
    refund                         Sweater Cuello Alto Rombos Azul Nicopoly Azul Liso M                                      nan regular_payment         refunded      2      59980.00
    refund                                Sweater Cuello Beatle Strass Celeste Nicopoly                                      nan regular_payment         refunded      5     121950.00
    refund                                   Sweater Cuello Beatle Strass Gris Nicopoly                                      nan regular_payment         refunded      1      25490.00
    refund                                  Sweater Cuello Beatle Strass Negro Nicopoly                                      nan regular_payment         refunded      2      45980.00
    refund                                  Sweater Cuello Beatle Strass Óxido Nicopoly                                      nan regular_payment         refunded      2      36083.00
    refund                                      Sweater Cuello Bote Azul Acero Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                                         Sweater Cuello Bote Magenta Nicopoly                                      nan regular_payment         refunded      2      42980.00
    refund                                            Sweater Cuello Bote Rojo Nicopoly                                      nan regular_payment         refunded      1      18990.00
    refund                             Sweater Cuello Camisero Cadenetas Negro Nicopoly                                      nan regular_payment         refunded      1      16990.00
    refund                                           Sweater Cuello Polo Negro Nicopoly                                      nan regular_payment         refunded      4      85950.00
    refund                                     Sweater Cuello V Acanalado Gris Nicopoly                                      nan regular_payment         refunded      2      29980.00
    refund                                    Sweater Cuello V Acanalado Negro Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                 Sweater Detalle Punto Calado Blanco Nicopoly                                      nan regular_payment         refunded      1      16990.00
    refund                                     Sweater Diseño Cadenetas Burdeo Nicopoly                                      nan regular_payment         refunded      1      17990.00
    refund                                      Sweater Diseño Cadenetas Khaki Nicopoly                                      nan regular_payment         refunded      2      47980.00
    refund                                      Sweater Diseño Cadenetas Negro Nicopoly                                      nan regular_payment         refunded      3      43770.00
    refund                                         Sweater Diseño Flores Negro Nicopoly                                      nan regular_payment         refunded     12     328042.00
    refund                               Sweater Diseño Rombos Blanco Invierno Nicopoly                                      nan regular_payment         refunded      3      68970.00
    refund                                       Sweater Diseño Rombos Celeste Nicopoly                                      nan regular_payment         refunded      2      47980.00
    refund                                       Sweater Diseño Rombos Magenta Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                                         Sweater Diseño Rombos Negro Nicopoly                                      nan regular_payment         refunded      2      47980.00
    refund                                          Sweater Diseño Rombos Rojo Nicopoly                                      nan regular_payment         refunded      2      23990.00
    refund                             Sweater Diseño Trenzado Blanco Invierno Nicopoly                                      nan regular_payment         refunded      1      20240.00
    refund                                       Sweater Diseño Trenzado Camel Nicopoly                                      nan regular_payment         refunded      4      81772.00
    refund                                       Sweater Diseño Trenzado Negro Nicopoly                                      nan regular_payment         refunded      5      84200.00
    refund                                     Sweater Diseños Espigas Celeste Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                                        Sweater Diseños Espigas Gris Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                                       Sweater Diseños Espigas Negro Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                                       Sweater Diseños Espigas Óxido Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                         Sweater Escote Asimétrico Café Nicopoly Café Liso Xl                                      nan regular_payment         refunded      2      23741.00
    refund                        Sweater Escote Asimétrico Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      23990.00
    refund                        Sweater Escote Asimétrico Verde Nicopoly Verde Liso L                                      nan regular_payment         refunded      1      23990.00
    refund                        Sweater Escote Asimétrico Verde Nicopoly Verde Liso M                                      nan regular_payment         refunded      1      29990.00
    refund                                      Sweater Escote Profundo Blanco Nicopoly                                      nan regular_payment         refunded      1      21580.00
    refund                                       Sweater Escote Profundo Camel Nicopoly                                      nan regular_payment         refunded      3      57752.00
    refund                                        Sweater Escote Profundo Gris Nicopoly                                      nan regular_payment         refunded      2      37980.00
    refund                                                Sweater Gilet Blanco Nicopoly                                      nan regular_payment         refunded      2      49980.00
    refund                                                  Sweater Gilet Negronicopoly                                      nan regular_payment         refunded      4      99960.00
    refund                  Sweater Jaspeado Cuello Redondo Khaki Nicopoly Khaki Liso S                                      nan regular_payment         refunded      1      21990.00
    refund                Sweater Jaspeado Cuello Redondo Morado Nicopoly Morado Liso M                                      nan regular_payment         refunded      1      25990.00
    refund                                Sweater Manga Raglán Blanco Invierno Nicopoly                                      nan regular_payment         refunded      7      90936.00
    refund                                           Sweater Manga Raglán Gris Nicopoly                                      nan regular_payment         refunded      5     104232.00
    refund                                Sweater Mangas Detalles Perlas Camel Nicopoly                                      nan regular_payment         refunded      2      38480.00
    refund                              Sweater Mangas Detalles Perlas Celeste Nicopoly                                      nan regular_payment         refunded      2      34480.00
    refund                                 Sweater Mangas Detalles Perlas Lila Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund                                Sweater Mangas Detalles Perlas Negro Nicopoly                                      nan regular_payment         refunded      2      39980.00
    refund                                Sweater Mangas Detalles Perlas Óxido Nicopoly                                      nan regular_payment         refunded      2      35980.00
    refund                             Sweater Peludo Recogido Lateral Celeste Nicopoly                                      nan regular_payment         refunded      1      12210.00
    refund                                Sweater Peludo Recogido Lateral Gris Nicopoly                                      nan regular_payment         refunded      2      44770.00
    refund                                Sweater Peludo Recogido Lateral Lila Nicopoly                                      nan regular_payment         refunded      1      12210.00
    refund                                Sweater Peludo Recogido Lateral Rosa Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                                Sweater Punto Fantasía Lurex Celeste Nicopoly                                      nan regular_payment         refunded      1      18990.00
    refund                                   Sweater Punto Fantasía Lurex Lila Nicopoly                                      nan regular_payment         refunded      1      24480.00
    refund                                   Sweater Punto Fantasía Lurex Rosa Nicopoly                                      nan regular_payment         refunded      3      56100.00
    refund                                   Sweater Punto Fino Cadenetas Gris Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                                        Sweater Punto Trenzado Negro Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                       Sweater Rayas Blanco Invierno Nicopoly                                      nan regular_payment         refunded      8     163520.00
    refund                                                 Sweater Rayas Negro Nicopoly                                      nan regular_payment         refunded      6     119530.00
    refund                            Sweater Tipo Hilo Manga Princesa Mostaza Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund                     Sweater Trenzado Cuello Alto Camel Nicopoly Camel Liso L                                      nan regular_payment         refunded      1      27990.00
    refund                     Sweater Trenzado Cuello Alto Camel Nicopoly Camel Liso S                                      nan regular_payment         refunded      1      27990.00
    refund                       Sweater Trenzado Cuello Alto Gris Nicopoly Gris Liso M                                      nan regular_payment         refunded      1      25990.00
    refund                                        Tapado Básico Bolsillos Café Nicopoly                                      nan regular_payment         refunded      4     103960.00
    refund                                     Tapado Básico Bolsillos Celeste Nicopoly                                      nan regular_payment         refunded      1      23990.00
    refund                                     Tapado Básico Bolsillos Magenta Nicopoly                                      nan regular_payment         refunded      7     179930.00
    refund                                        Tapado Básico Bolsillos Negronicopoly                                      nan regular_payment         refunded      8     124028.00
    refund                                        Tapado Básico Bolsillos Rojo Nicopoly                                      nan regular_payment         refunded      2      63980.00
    refund                       Tapado Tejido Tipo Crochet Café Nicopoly Cafe Liso S/m                                      nan regular_payment         refunded      7      87984.00
    refund                     Tapado Tejido Tipo Crochet Negro Nicopoly Negro Liso M/l                                      nan regular_payment         refunded      2      58980.00
    refund                     Tapado Tejido Tipo Crochet Negro Nicopoly Negro Liso S/m                                      nan regular_payment         refunded      1      21990.00
    refund                                 Top Acanalado Hombros Caídos Blanco Nicopoly                                      nan regular_payment         refunded      4      60413.00
    refund                                  Top Acanalado Hombros Caídos Negro Nicopoly                                      nan regular_payment         refunded      3      61910.00
    refund                                 Top Básico Leopardo Tipo Satín Café Nicopoly                                      nan regular_payment         refunded      1      19480.00
    refund                                 Top Básico Leopardo Tipo Satín Gris Nicopoly                                      nan regular_payment         refunded      2      25980.00
    refund                                        Top Básico Tipo Satín Blanco Nicopoly                                      nan regular_payment         refunded      6      78380.00
    refund                                       Top Básico Tipo Satín Celeste Nicopoly                                      nan regular_payment         refunded      2      23980.00
    refund                                         Top Básico Tipo Satín Negro Nicopoly                                      nan regular_payment         refunded      3      35970.00
    refund                        Top Encaje Escote V Negro Nicopoly - Negro - L - Liso                                      nan regular_payment         refunded      1      25990.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro L Liso                                      nan regular_payment         refunded      1      20790.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      2      39980.00
    refund                              Top Encaje Escote V Negro Nicopoly Negro S Liso                                      nan regular_payment         refunded      2      40780.00
    refund                                      Top Pabilo Print Leopardo Café Nicopoly                                      nan regular_payment         refunded      6      91940.00
    refund                                           Top Print Paisley Mostaza Nicopoly                                      nan regular_payment         refunded      1       6990.00
    refund                                                Top Print Snake Azul Nicopoly                                      nan regular_payment         refunded      4      49950.00
    refund                                                Top Print Snake Café Nicopoly                                      nan regular_payment         refunded      1      12990.00
    refund                                               Top Print Snake Verde Nicopoly                                      nan regular_payment         refunded      1       9990.00
    refund                       Top Sin Mangas Acanalado Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1       7990.00
    refund                              Top Sin Mangas Acanalado Blanco Nicopoly Liso L                                      nan regular_payment         refunded      2      19980.00
    refund                     Top Sin Mangas Acanalado Celeste Nicopoly Celeste Liso S                                      nan regular_payment         refunded      1       7990.00
    refund                     Top Sin Mangas Acanalado Gris Claro Nicopoly Gris Liso S                                      nan regular_payment         refunded      1       7990.00
    refund                         Top Sin Mangas Acanalado Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      1       7990.00
    refund                         Top Sin Mangas Acanalado Negro Nicopoly Negro M Liso                                      nan regular_payment         refunded      1       9990.00
    refund                         Top Sin Mangas Acanalado Oliva Nicopoly Oliva Liso L                                      nan regular_payment         refunded      1       7990.00
    refund                         Top Sin Mangas Acanalado Oliva Nicopoly Oliva Liso S                                      nan regular_payment         refunded      1       7990.00
    refund                      Top Tipo Lino Estampado Cebra Café Nicopoly Café Lisa M                                      nan regular_payment         refunded      1      11990.00
    refund                      Top Tipo Lino Estampado Cebra Café Nicopoly Café Lisa S                                      nan regular_payment         refunded      1      11990.00
    refund                     Top Tipo Lino Estampado Cebra Café Nicopoly Café Lisa Xl                                      nan regular_payment         refunded      3      38970.00
    refund                                                Trench Hebilla Khaki Nicopoly                                      nan regular_payment         refunded     17     849652.00
    refund                                                Trench Hebilla Oliva Nicopoly                                      nan regular_payment         refunded     19     630018.00
    refund                                           Trench Lazo Hebilla Khaki Nicopoly                                      nan regular_payment         refunded     11     386758.00
    refund                                           Trench Lazo Hebilla Negro Nicopoly                                      nan regular_payment         refunded     19     683184.00
    refund                                       Trench Lazo Tipo Gamuza Beige Nicopoly                                      nan regular_payment         refunded      1      59990.00
    refund                                        Trench Lazo Tipo Gamuza Gris Nicopoly                                      nan regular_payment         refunded      1      41990.00
    refund                                  Trench Príncipe De Gales Lazo Gris Nicopoly                                      nan regular_payment         refunded      9     242910.00
    refund                                             Trench Tipo Gamuza Café Nicopoly                                      nan regular_payment         refunded     24    1238760.00
    refund                                            Trench Tipo Gamuza Negro Nicopoly                                      nan regular_payment         refunded      7     346732.00
    refund                                            Trench Tipo Gamuza Oliva Nicopoly                                      nan regular_payment         refunded      2     119980.00
    refund                               Vestido Acanalado Blanco Con Cinturón Blanco L                                      nan regular_payment         refunded      1      35990.00
    refund               Vestido Acanalado Blanco Con Cinturón Nicopoly Blanco Liso M/l                                      nan regular_payment         refunded      1      35990.00
    refund                                Vestido Acanalado Con Botones Fucsia Nicopoly                                      nan regular_payment         refunded      3      41570.00
    refund                                 Vestido Acanalado Cuello Alto Beige Nicopoly                                      nan regular_payment         refunded      1      17990.00
    refund                                 Vestido Acanalado Cuello Alto Negro Nicopoly                                      nan regular_payment         refunded      4      94950.00
    refund                                  Vestido Acanalado Cuello Alto Rojo Nicopoly                                      nan regular_payment         refunded      1      36990.00
    refund                                 Vestido Acanalado Cuello Alto Verde Nicopoly                                      nan regular_payment         refunded      1      17990.00
    refund                 Vestido Acanalado Negro Con Cinturón Nicopoly Negro Liso M/l                                      nan regular_payment         refunded      3      75570.00
    refund                            Vestido Acanalado Off The Shoulder Negro Nicopoly                                      nan regular_payment         refunded      3      58770.00
    refund                         Vestido Ajustado Cut Out Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      2      64980.00
    refund                         Vestido Ajustado Cut Out Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      4     124960.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso L                                      nan regular_payment         refunded      4     103960.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso M                                      nan regular_payment         refunded      3      68970.00
    refund                       Vestido Animal Print Tipo Satín Nicopoly Marrón Liso S                                      nan regular_payment         refunded      1      22990.00
    refund                      Vestido Animal Print Tipo Satín Nicopoly Marrón Liso Xl                                      nan regular_payment         refunded      1      27590.00
    refund                      Vestido Animal Print Tipo Satín Nicopoly Xl Liso Marrón                                      nan regular_payment         refunded      1      31990.00
    refund                                          Vestido Asimétrico Celeste Nicopoly                                      nan regular_payment         refunded      2      47980.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment         refunded      6     172540.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment         refunded      2      53780.00
    refund                      Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso S                                      nan regular_payment         refunded      1      24990.00
    refund                     Vestido Asimétrico Floral Fucsia Nicopoly Fucsia Liso Xl                                      nan regular_payment         refunded      4      92462.00
    refund                     Vestido Asimétrico Floral Fucsia Nicopoly Xl Liso Fucsia                                      nan regular_payment         refunded      1      35990.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso L                                      nan regular_payment         refunded      3      98970.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso M                                      nan regular_payment         refunded     14     272804.00
    refund                        Vestido Asimétrico Floral Verde Nicopoly Verde Liso S                                      nan regular_payment         refunded      9     232710.00
    refund                       Vestido Asimétrico Floral Verde Nicopoly Verde Liso Xl                                      nan regular_payment         refunded      8     201530.00
    refund                       Vestido Asimétrico Floral Verde Nicopoly Xl Liso Verde                                      nan regular_payment         refunded      2      71980.00
    refund                               Vestido Broderie Blanco Nicopoly Blanco Liso M                                      nan regular_payment         refunded      1      43990.00
    refund                       Vestido Camisero Cebra Café Nicopoly - Café - Lisa - S                                      nan regular_payment         refunded      4      29244.00
    refund                             Vestido Camisero Cebra Café Nicopoly Café Lisa L                                      nan regular_payment         refunded      1      20390.00
    refund                             Vestido Camisero Cebra Café Nicopoly Café Lisa M                                      nan regular_payment         refunded      2      50780.00
    refund                            Vestido Camisero Cebra Café Nicopoly Café Lisa Xl                                      nan regular_payment         refunded      2      43790.00
    refund                            Vestido Camisero Cebra Café Nicopoly Xl Café Lisa                                      nan regular_payment         refunded      2      53980.00
    refund                               Vestido Camisero Cinturón Azul Marino Nicopoly                                      nan regular_payment         refunded      6     227950.00
    refund                                         Vestido Camisero Tipo Denim Nicopoly                                      nan regular_payment         refunded      3      86970.00
    refund            Vestido Cintura Elasticada Flores Naranja Nicopoly Naranjo Liso L                                      nan regular_payment         refunded      5     133050.00
    refund            Vestido Cintura Elasticada Flores Naranja Nicopoly Naranjo Liso M                                      nan regular_payment         refunded      3      85970.00
    refund                                   Vestido Con Faldón Plisado Fucsia Nicopoly                                      nan regular_payment         refunded      3      66970.00
    refund                                      Vestido Corte Imperio Amarillo Nicopoly                                      nan regular_payment         refunded      2      35170.00
    refund                                          Vestido Corte Imperio Azul Nicopoly                                      nan regular_payment         refunded      2      46980.00
    refund                               Vestido Corto Aberturas Mangas Blanco Nicopoly                                      nan regular_payment         refunded      2      36980.00
    refund                              Vestido Corto Aberturas Mangas Celeste Nicopoly                                      nan regular_payment         refunded     11     200170.00
    refund                                Vestido Corto Aberturas Mangas Negro Nicopoly                                      nan regular_payment         refunded      4      83480.00
    refund                                  Vestido Corto Cuello Halter Blanco Nicopoly                                      nan regular_payment         refunded      1      14990.00
    refund                                 Vestido Corto Cuello Halter Celeste Nicopoly                                      nan regular_payment         refunded      2      35080.00
    refund                                   Vestido Corto Cuello Halter Negro Nicopoly                                      nan regular_payment         refunded      2      35470.00
    refund                                  Vestido Corto Cuello Halter Rosado Nicopoly                                      nan regular_payment         refunded      4      74940.00
    refund Vestido Corto Floral Con Vuelos Cruzados Blanco Nicopoly - Blanco - Liso - M                                      nan regular_payment         refunded      1      33990.00
    refund       Vestido Corto Floral Con Vuelos Cruzados Blanco Nicopoly Blanco Liso L                                      nan regular_payment         refunded      1      25990.00
    refund        Vestido Corto Floral Con Vuelos Cruzados Fucsia Nicopoly Negro Liso L                                      nan regular_payment         refunded      2      48980.00
    refund        Vestido Corto Floral Con Vuelos Cruzados Fucsia Nicopoly Negro Liso M                                      nan regular_payment         refunded      2      53180.00
    refund        Vestido Corto Floral Con Vuelos Cruzados Fucsia Nicopoly Negro Liso S                                      nan regular_payment         refunded      3      77970.00
    refund       Vestido Corto Floral Con Vuelos Cruzados Rosado Nicopoly Rosado Liso M                                      nan regular_payment         refunded      2      49980.00
    refund       Vestido Corto Floral Con Vuelos Cruzados Rosado Nicopoly Rosado Liso S                                      nan regular_payment         refunded      1      25990.00
    refund      Vestido Corto Floral Con Vuelos Cruzados Rosado Nicopoly Rosado Liso Xl                                      nan regular_payment         refunded      1      23990.00
    refund                                      Vestido Corto Sin Mangas Negro Nicopoly                                      nan regular_payment         refunded      8     267122.00
    refund                                       Vestido Corto Sin Mangas Rojo Nicopoly                                      nan regular_payment         refunded      4     143162.00
    refund                                         Vestido Corto Tulipán Negro Nicopoly                                      nan regular_payment         refunded      3      67890.00
    refund                                     Vestido Cuello Alto Azul Marino Nicopoly                                      nan regular_payment         refunded      5     192450.00
    refund                                          Vestido Cuello Alto Burdeo Nicopoly                                      nan regular_payment         refunded      7     281930.00
    refund                                           Vestido Cuello Alto Negro Nicopoly                                      nan regular_payment         refunded      7     241930.00
    refund                                          Vestido Cuello Mock Burdeo Nicopoly                                      nan regular_payment         refunded      2      33990.00
    refund                                           Vestido Cuello Mock Negro Nicopoly                                      nan regular_payment         refunded      1      33990.00
    refund                                            Vestido Cuello Mock Negronicopoly                                      nan regular_payment         refunded      4     143710.00
    refund                                     Vestido De Punto Trenzado Negro Nicopoly                                      nan regular_payment         refunded      1      21824.00
    refund                                      Vestido De Punto Trenzado Rojo Nicopoly                                      nan regular_payment         refunded      1      13990.00
    refund                            Vestido Encaje Sirena Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      3     194970.00
    refund                            Vestido Encaje Sirena Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      1      59990.00
    refund                   Vestido Escote Cruzado Flores Negras Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      18190.00
    refund                Vestido Escote Cruzado Flores Rojas Nicoply - Rojo - Liso - M                                      nan regular_payment         refunded      2      19990.00
    refund                      Vestido Escote Cruzado Flores Rojas Nicoply Rojo Liso M                                      nan regular_payment         refunded      1      18190.00
    refund                     Vestido Escote Cruzado Flores Verde Nicoply L Liso Verde                                      nan regular_payment         refunded      1      19990.00
    refund                     Vestido Escote Cruzado Flores Verde Nicoply Verde Liso S                                      nan regular_payment         refunded      2      38180.00
    refund                    Vestido Escote Cuadrado Negro Nicopoly - Negro - Liso - L                                      nan regular_payment         refunded      1      27990.00
    refund                          Vestido Escote Cuadrado Negro Nicopoly L Liso Negro                                      nan regular_payment         refunded      1      27990.00
    refund                          Vestido Escote Cuadrado Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      25094.00
    refund                          Vestido Escote Cuadrado Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      1      25190.00
    refund                                   Vestido Escote Semi Corazón Negro Nicopoly                                      nan regular_payment         refunded      1      22990.00
    refund                                   Vestido Escote V Profundo Celeste Nicopoly                                      nan regular_payment         refunded      2      43980.00
    refund                Vestido Estampado Minimalista Naranja Nicopoly Naranjo Liso L                                      nan regular_payment         refunded      1      15990.00
    refund                Vestido Estampado Minimalista Naranja Nicopoly Naranjo Liso M                                      nan regular_payment         refunded      1      15990.00
    refund                Vestido Estampado Minimalista Naranja Nicopoly Naranjo Liso S                                      nan regular_payment         refunded      1      15990.00
    refund                                  Vestido Faldón Con Volantes Fucsia Nicopoly                                      nan regular_payment         refunded      1      20990.00
    refund                                           Vestido Floral Nudo Negro Nicopoly                                      nan regular_payment         refunded      1      19790.00
    refund                      Vestido Floral Volantes Celeste Nicopoly Celeste Liso L                                      nan regular_payment         refunded      5     149950.00
    refund                      Vestido Floral Volantes Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      5     154550.00
    refund                      Vestido Floral Volantes Celeste Nicopoly M Liso Celeste                                      nan regular_payment         refunded      1      36990.00
    refund                      Vestido Floral Volantes Celeste Nicopoly S Liso Celeste                                      nan regular_payment         refunded      1      36990.00
    refund  Vestido Floreado Botones Delanteros Azul Marino Nicopoly Azul Marino Liso M                                      nan regular_payment         refunded      4     113331.00
    refund  Vestido Floreado Botones Delanteros Azul Marino Nicopoly Azul Marino Liso S                                      nan regular_payment         refunded      1      23990.00
    refund            Vestido Floreado Botones Delanteros Fucsia Nicopoly L Liso Fucsia                                      nan regular_payment         refunded      1      31990.00
    refund           Vestido Floreado Botones Delanteros Fucsia Nicopoly Xl Liso Fucsia                                      nan regular_payment         refunded      1      31990.00
    refund                           Vestido Flores Fucsia Nicopoly - Fucsia - Liso - M                                      nan regular_payment         refunded      1      29990.00
    refund                          Vestido Flores Fucsia Nicopoly - Fucsia - Liso - Xl                                      nan regular_payment         refunded      1      29990.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso L                                      nan regular_payment         refunded      5     100440.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso M                                      nan regular_payment         refunded      7     130008.00
    refund                                 Vestido Flores Fucsia Nicopoly Fucsia Liso S                                      nan regular_payment         refunded      1      24690.00
    refund                                Vestido Flores Fucsia Nicopoly Fucsia Liso Xl                                      nan regular_payment         refunded      5      90950.00
    refund                             Vestido Flores Pabilo Ajustable Celeste Nicopoly                                      nan regular_payment         refunded      2      37480.00
    refund                                         Vestido Halter Cadena Negro Nicopoly                                      nan regular_payment         refunded      1      51990.00
    refund                                   Vestido Holgado Con Brillos Khaki Nicopoly                                      nan regular_payment         refunded      1      21990.00
    refund                            Vestido Holgado Con Mangas Caladas Negro Nicopoly                                      nan regular_payment         refunded      3      59970.00
    refund      Vestido Largo Con Aberturas Laterales Negro Nicopoly - Negro - Liso - L                                      nan regular_payment         refunded      1      29990.00
    refund                  Vestido Largo Con Aberturas Laterales Negro Nicopoly Liso L                                      nan regular_payment         refunded      1      29990.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly M Liso Negro                                      nan regular_payment         refunded      3      95960.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      2      38980.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      4      98960.00
    refund            Vestido Largo Con Aberturas Laterales Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      4      80960.00
    refund                                      Vestido Largo Cuello Mock Azul Nicopoly                                      nan regular_payment         refunded      7     291430.00
    refund                                    Vestido Largo Cuello Mock Burdeo Nicopoly                                      nan regular_payment         refunded      6     230440.00
    refund                     Vestido Largo Escote Drapeado Azul Nicopoly Xl Azul Liso                                      nan regular_payment         refunded      1      46990.00
    refund                  Vestido Largo Escote Drapeado Morado Nicopoly Morado Liso L                                      nan regular_payment         refunded      1      45990.00
    refund                                         Vestido Largo Fiesta Burdeo Nicopoly                                      nan regular_payment         refunded      9     473672.00
    refund                                          Vestido Largo Fiesta Negro Nicopoly                                      nan regular_payment         refunded     13     475200.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso L                                      nan regular_payment         refunded      4     143960.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso M                                      nan regular_payment         refunded      7     219271.00
    refund                             Vestido Largo Floreado Lila Nicopoly Lila Liso S                                      nan regular_payment         refunded      5     106570.00
    refund                            Vestido Largo Floreado Lila Nicopoly Lila Liso Xl                                      nan regular_payment         refunded     12     333540.00
    refund                   Vestido Largo Floreado Rosado Nicopoly - Rosado - Liso - S                                      nan regular_payment         refunded      1      56990.00
    refund                         Vestido Largo Floreado Rosado Nicopoly M Liso Rosado                                      nan regular_payment         refunded      1      48990.00
    refund                         Vestido Largo Floreado Rosado Nicopoly Rosado Liso L                                      nan regular_payment         refunded      1      34190.00
    refund                         Vestido Largo Floreado Rosado Nicopoly Rosado Liso M                                      nan regular_payment         refunded      1      36990.00
    refund                         Vestido Largo Floreado Rosado Nicopoly Rosado Liso S                                      nan regular_payment         refunded      3      69980.00
    refund                        Vestido Largo Floreado Rosado Nicopoly Rosado Liso Xl                                      nan regular_payment         refunded      3     116770.00
    refund                  Vestido Largo Tirantes Cruzados Negro Nicopoly L Lisa Negro                                      nan regular_payment         refunded      1      61990.00
    refund                        Vestido Largo Tirantes Cruzados Negro Nicopoly Lisa L                                      nan regular_payment         refunded      1      61990.00
    refund                  Vestido Largo Tirantes Cruzados Negro Nicopoly Negro Lisa L                                      nan regular_payment         refunded      2      80980.00
    refund                  Vestido Largo Tirantes Cruzados Negro Nicopoly Negro Lisa M                                      nan regular_payment         refunded      6     237950.00
    refund                                         Vestido Midi Acanalado Café Nicopoly                                      nan regular_payment         refunded      1      19990.00
    refund                                        Vestido Midi Acanalado Negro Nicopoly                                      nan regular_payment         refunded      3      59970.00
    refund                                         Vestido Midi Acanalado Rojo Nicopoly                                      nan regular_payment         refunded      2      39980.00
    refund                                   Vestido Midi Acanalado Tajo Negro Nicopoly                                      nan regular_payment         refunded      3      76970.00
    refund                                 Vestido Midi Escote Drapeado Blanco Nicopoly                                      nan regular_payment         refunded      1      15990.00
    refund                                  Vestido Midi Escote Drapeado Negro Nicopoly                                      nan regular_payment         refunded      1      25990.00
    refund                                   Vestido Pabilo Con Volantes Negro Nicopoly                                      nan regular_payment         refunded      3      71970.00
    refund                                   Vestido Pliegues En Cintura Negro Nicopoly                                      nan regular_payment         refunded      7     160930.00
    refund                                    Vestido Pliegues En Cintura Rojo Nicopoly                                      nan regular_payment         refunded      4     100960.00
    refund                                     Vestido Pliegues En Cintura Rojonicopoly                                      nan regular_payment         refunded      1      34490.00
    refund                                 Vestido Plisado Asimétrico Azul Rey Nicopoly                                      nan regular_payment         refunded      5     167950.00
    refund                                     Vestido Plisado Asimétrico Rojo Nicopoly                                      nan regular_payment         refunded     13     436670.00
    refund                                 Vestido Safari Cuello Camisero Café Nicopoly                                      nan regular_payment         refunded      3      92970.00
    refund                   Vestido Satinado Escote Fruncido Lila Nicopoly Lila Liso M                                      nan regular_payment         refunded      2      53180.00
    refund                   Vestido Satinado Escote Fruncido Lila Nicopoly Lila Liso S                                      nan regular_payment         refunded      1      25990.00
    refund                   Vestido Satinado Escote Fruncido Lila Nicopoly S Lila Liso                                      nan regular_payment         refunded      1      33990.00
    refund                                 Vestido Strapless Y Escote V Blanco Nicopoly                                      nan regular_payment         refunded      9     236910.00
    refund                                  Vestido Strapless Y Escote V Negro Nicopoly                                      nan regular_payment         refunded     10     283300.00
    refund                                   Vestido Strapless Y Escote V Rojo Nicopoly                                      nan regular_payment         refunded     13     335330.00
    refund                                          Vestido Sweater Midi Camel Nicopoly                                      nan regular_payment         refunded      2      59980.00
    refund                                          Vestido Sweater Midi Negro Nicopoly                                      nan regular_payment         refunded      8     237520.00
    refund                                           Vestido Sweater Midi Rojo Nicopoly                                      nan regular_payment         refunded     10     239770.00
    refund                                           Vestido Tipo Blazer Negro Nicopoly                                      nan regular_payment         refunded      9     261910.00
    refund                                            Vestido Tipo Blazer Rojo Nicopoly                                      nan regular_payment         refunded      6     209420.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print L                                      nan regular_payment         refunded      2      33480.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print M                                      nan regular_payment         refunded      3      53924.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print S                                      nan regular_payment         refunded      1      16990.00
    refund             Vestido Tipo Camisero Animal Print Nicopoly Café Animal Print Xl                                      nan regular_payment         refunded      3      50970.00
    refund              Vestido Tipo Camisero Animal Print Nicopoly S Café Animal Print                                      nan regular_payment         refunded      1      19990.00
    refund                                  Vestido Tipo Camisero Leopard Café Nicopoly                                      nan regular_payment         refunded     14     336910.00
    refund                      Vestido Tipo Satín Floreado Negro Nicopoly Negro Liso L                                      nan regular_payment         refunded      1      22990.00
    refund                      Vestido Tipo Satín Floreado Negro Nicopoly Negro Liso M                                      nan regular_payment         refunded      6     145940.00
    refund                      Vestido Tipo Satín Floreado Negro Nicopoly Negro Liso S                                      nan regular_payment         refunded      3      69970.00
    refund              Vestido Tipo Satín Floreado Rosado Nicopoly - Rosado - Liso - M                                      nan regular_payment         refunded      1      26990.00
    refund              Vestido Tipo Satín Floreado Rosado Nicopoly - Rosado - Liso - S                                      nan regular_payment         refunded      1      26990.00
    refund                           Vestido Tipo Satín Floreado Rosado Nicopoly Liso L                                      nan regular_payment         refunded      1      31990.00
    refund                    Vestido Tipo Satín Floreado Rosado Nicopoly Rosado Liso L                                      nan regular_payment         refunded      1      21990.00
    refund                    Vestido Tipo Satín Floreado Rosado Nicopoly Rosado Liso M                                      nan regular_payment         refunded      1      24990.00
    refund                    Vestido Tipo Satín Print Flor Abstracta Celeste  Nicopoly                                      nan regular_payment         refunded      2      41980.00
    refund                                       Vestido Tubo Con Strass Negro Nicopoly                                      nan regular_payment         refunded      2      50048.00
    refund                                        Vestido Tubo Con Strass Rojo Nicopoly                                      nan regular_payment         refunded      3      66360.00
    refund                         Vestido Tul Floreado Celeste Nicopoly Celeste Liso M                                      nan regular_payment         refunded      1      43390.00
    refund                         Vestido Tul Floreado Celeste Nicopoly Celeste Liso S                                      nan regular_payment         refunded      1      37990.00
    refund                        Vestido Tul Floreado Celeste Nicopoly Celeste Liso Xl                                      nan regular_payment         refunded      2      77382.00
    refund                           Vestido Tul Floreado Fucsia Nicopoly Fucsia Liso S                                      nan regular_payment         refunded      1      37190.00
    refund                                  Vestido Tul Floreado Fucsia Nicopoly Liso L                                      nan regular_payment         refunded      1      61990.00
    refund                                                       bonificaciones_flex_fc                                      nan  money_transfer         refunded    546     394876.00
    refund                                                         marketplace_shipment                                      nan regular_payment         refunded     75     282555.93
```

## FASE 2: Trazabilidad Archivo Fuente -> Ledger (Muestra)

```
                  Archivo Fuente  ID Original  Monto Original                 Clasificación Actual                                            Ledger ID      Estado
1 enero 2025 - 1 julio 2025.xlsx 113610989447             0.0    Ajuste por Compra Protegida (BPP)  POS_113610989447_1 enero 2025 - 1 julio 2025.xlsx_1 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116910735964             0.0       Ajuste por Cambio de Dirección  POS_116910735964_1 enero 2025 - 1 julio 2025.xlsx_2 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116836571904             0.0           Ajuste por Arrepentimiento  POS_116836571904_1 enero 2025 - 1 julio 2025.xlsx_3 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116217584583             0.0            Ajuste por Talla/Garantía  POS_116217584583_1 enero 2025 - 1 julio 2025.xlsx_4 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114321245153             0.0            Ajuste por Talla/Garantía  POS_114321245153_1 enero 2025 - 1 julio 2025.xlsx_5 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116502809934             0.0            Ajuste por Talla/Garantía  POS_116502809934_1 enero 2025 - 1 julio 2025.xlsx_6 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116052568980             0.0            Ajuste por Talla/Garantía  POS_116052568980_1 enero 2025 - 1 julio 2025.xlsx_7 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115670860507             0.0            Ajuste por Talla/Garantía  POS_115670860507_1 enero 2025 - 1 julio 2025.xlsx_8 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116885181836             0.0           Ajuste por Arrepentimiento  POS_116885181836_1 enero 2025 - 1 julio 2025.xlsx_9 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116885428608             0.0           Ajuste por Arrepentimiento POS_116885428608_1 enero 2025 - 1 julio 2025.xlsx_10 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116392547167             0.0           Ajuste por Arrepentimiento POS_116392547167_1 enero 2025 - 1 julio 2025.xlsx_11 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116392535125             0.0           Ajuste por Arrepentimiento POS_116392535125_1 enero 2025 - 1 julio 2025.xlsx_12 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116650180676             0.0            Ajuste por Talla/Garantía POS_116650180676_1 enero 2025 - 1 julio 2025.xlsx_13 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116101546293             0.0            Ajuste por Talla/Garantía POS_116101546293_1 enero 2025 - 1 julio 2025.xlsx_14 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116262006035             0.0           Ajuste por Arrepentimiento POS_116262006035_1 enero 2025 - 1 julio 2025.xlsx_15 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116185574144             0.0            Ajuste por Talla/Garantía POS_116185574144_1 enero 2025 - 1 julio 2025.xlsx_16 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113645388025             0.0            Ajuste por Talla/Garantía POS_113645388025_1 enero 2025 - 1 julio 2025.xlsx_17 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113645388025             0.0            Ajuste por Talla/Garantía POS_113645388025_1 enero 2025 - 1 julio 2025.xlsx_17 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113645388025             0.0            Ajuste por Talla/Garantía POS_113645388025_1 enero 2025 - 1 julio 2025.xlsx_17 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116133595749             0.0            Ajuste por Talla/Garantía POS_116133595749_1 enero 2025 - 1 julio 2025.xlsx_20 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114887979409             0.0            Ajuste por Talla/Garantía POS_114887979409_1 enero 2025 - 1 julio 2025.xlsx_21 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116136319017             0.0           Ajuste por Arrepentimiento POS_116136319017_1 enero 2025 - 1 julio 2025.xlsx_22 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114959941945             0.0            Ajuste por Talla/Garantía POS_114959941945_1 enero 2025 - 1 julio 2025.xlsx_23 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116251180593             0.0           Ajuste por Arrepentimiento POS_116251180593_1 enero 2025 - 1 julio 2025.xlsx_24 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115632579414             0.0            Ajuste por Talla/Garantía POS_115632579414_1 enero 2025 - 1 julio 2025.xlsx_25 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114328872544             0.0            Ajuste por Talla/Garantía POS_114328872544_1 enero 2025 - 1 julio 2025.xlsx_26 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115971205237             0.0            Ajuste por Talla/Garantía POS_115971205237_1 enero 2025 - 1 julio 2025.xlsx_27 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116718212720             0.0        Ajuste por Retraso en Entrega POS_116718212720_1 enero 2025 - 1 julio 2025.xlsx_28 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116628402608             0.0 Ajuste por Diferencia de Publicación POS_116628402608_1 enero 2025 - 1 julio 2025.xlsx_29 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115856659941             0.0 Ajuste por Diferencia de Publicación POS_115856659941_1 enero 2025 - 1 julio 2025.xlsx_30 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116156595237             0.0        Ajuste por Retraso en Entrega POS_116156595237_1 enero 2025 - 1 julio 2025.xlsx_31 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116392378072             0.0            Ajuste por Talla/Garantía POS_116392378072_1 enero 2025 - 1 julio 2025.xlsx_32 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114247010441             0.0           Ajuste por Arrepentimiento POS_114247010441_1 enero 2025 - 1 julio 2025.xlsx_33 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115732185813             0.0            Ajuste por Talla/Garantía POS_115732185813_1 enero 2025 - 1 julio 2025.xlsx_34 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116220805882             0.0            Ajuste por Talla/Garantía POS_116220805882_1 enero 2025 - 1 julio 2025.xlsx_35 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116220898746             0.0            Ajuste por Talla/Garantía POS_116220898746_1 enero 2025 - 1 julio 2025.xlsx_36 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116620228826             0.0           Ajuste por Arrepentimiento POS_116620228826_1 enero 2025 - 1 julio 2025.xlsx_37 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116620108096             0.0           Ajuste por Arrepentimiento POS_116620108096_1 enero 2025 - 1 julio 2025.xlsx_38 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116128317857             0.0          Ajuste por Falla en Entrega POS_116128317857_1 enero 2025 - 1 julio 2025.xlsx_39 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116128369235             0.0          Ajuste por Falla en Entrega POS_116128369235_1 enero 2025 - 1 julio 2025.xlsx_40 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113389029040             0.0            Ajuste por Talla/Garantía POS_113389029040_1 enero 2025 - 1 julio 2025.xlsx_41 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116451558216             0.0            Ajuste por Talla/Garantía POS_116451558216_1 enero 2025 - 1 julio 2025.xlsx_42 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116089725383             0.0        Ajuste por Retraso en Entrega POS_116089725383_1 enero 2025 - 1 julio 2025.xlsx_43 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116581214354             0.0        Ajuste por Retraso en Entrega POS_116581214354_1 enero 2025 - 1 julio 2025.xlsx_44 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116545497794             0.0            Ajuste por Talla/Garantía POS_116545497794_1 enero 2025 - 1 julio 2025.xlsx_45 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 114432812728             0.0            Ajuste por Talla/Garantía POS_114432812728_1 enero 2025 - 1 julio 2025.xlsx_46 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 113927719230             0.0           Ajuste por Arrepentimiento POS_113927719230_1 enero 2025 - 1 julio 2025.xlsx_47 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 116557041890             0.0        Ajuste por Retraso en Entrega POS_116557041890_1 enero 2025 - 1 julio 2025.xlsx_48 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 112657666145             0.0            Ajuste por Talla/Garantía POS_112657666145_1 enero 2025 - 1 julio 2025.xlsx_49 CLASIFICADO
1 enero 2025 - 1 julio 2025.xlsx 115732141685             0.0           Ajuste por Arrepentimiento POS_115732141685_1 enero 2025 - 1 julio 2025.xlsx_50 CLASIFICADO
```

## FASE 3: Identificación de Registros

- **Registros Clasificados**: 11914
- **Registros Excluidos/Duplicados (Deduplicados en carga)**: 0
- **Registros Huérfanos**: 0
- **Registros Sin Clasificación**: 0

## FASE 4: Resultados y Delta

- **Total Devoluciones Fuente (Suma absoluta)**: $155,518,101.43
- **Total Devoluciones Ledger (Suma absoluta)**: $338,221,581.93
- **Delta**: $-182,703,480.50

## CONCLUSIÓN DE AUDITORÍA
Discrepancia detectada: $-182,703,480.50